import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from langchain_core.documents import Document

from app.modules.llm.rag.document_loader import load_document, load_documents_from_directory
from app.modules.llm.rag.text_splitter import split_documents

# --- Test Document Loader ---

@pytest.fixture
def temp_dir(tmp_path):
    # Create dummy files for testing
    (tmp_path / "test.txt").write_text("This is a test document.")
    (tmp_path / "another.txt").write_text("Another test document for directory loading.")
    (tmp_path / "unsupported.csv").write_text("col1,col2\n1,2")
    # For PDF, create a minimal valid PDF file
    (tmp_path / "test.pdf").write_bytes(b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Count 0>>endobj\nxref\n0 3\n0000000000 65535 f\n0000000009 00000 n\n0000000052 00000 n\ntrailer<</Size 3/Root 1 0 R>>startxref\n104\n%%EOF")
    return tmp_path

@patch('app.modules.llm.rag.document_loader.PyPDFLoader')
def test_load_pdf_document(mock_pypdf_loader, temp_dir):
    mock_instance = mock_pypdf_loader.return_value
    mock_instance.load.return_value = [Document(page_content="PDF content")]
    
    docs = load_document(temp_dir / "test.pdf")
    assert len(docs) == 1
    assert docs[0].page_content == "PDF content"
    mock_pypdf_loader.assert_called_once_with(str(temp_dir / "test.pdf"))
    mock_instance.load.assert_called_once()

def test_load_txt_document(temp_dir):
    docs = load_document(temp_dir / "test.txt")
    assert len(docs) == 1
    assert docs[0].page_content == "This is a test document."
    assert docs[0].metadata['source'] == str(temp_dir / "test.txt")

def test_load_unsupported_document(temp_dir):
    with pytest.raises(ValueError, match="Unsupported file type"):
        load_document(temp_dir / "unsupported.csv")

@patch('langchain_community.document_loaders.PyPDFLoader')
def test_load_documents_from_directory(mock_pypdf_loader, temp_dir):
    # Test that directory loads txt files and skips unsupported
    docs = load_documents_from_directory(temp_dir)
    
    # Should load test.txt, another.txt (PDF is skipped due to error)
    assert len(docs) == 2
    contents = sorted([d.page_content for d in docs])
    assert "Another test document for directory loading." in contents
    assert "This is a test document." in contents
    
    # Ensure unsupported file is skipped
    assert not any("csv" in d.metadata.get('source', '') for d in docs)

# --- Test Text Splitter ---

@pytest.fixture
def sample_documents():
    return [
        Document(page_content="This is a very long sentence that needs to be split into multiple chunks."),
        Document(page_content="Another short document.")
    ]

def test_split_documents_basic(sample_documents):
    chunks = split_documents(sample_documents, chunk_size=20, chunk_overlap=5)
    assert len(chunks) == 8
    assert all(len(c.page_content) <= 20 for c in chunks)
    assert chunks[0].page_content == "This is a very long"
    assert chunks[1].page_content == "long sentence that"
    assert chunks[2].page_content == "that needs to be"

def test_split_documents_no_overlap():
    doc = Document(page_content="This is a long text for splitting.")
    chunks = split_documents([doc], chunk_size=10, chunk_overlap=0)
    assert len(chunks) == 5
    assert chunks[0].page_content == "This is a"
    assert chunks[1].page_content == "long text"
    assert chunks[2].page_content == "for"
    assert chunks[3].page_content == "splitting"
    assert chunks[4].page_content == "."

def test_split_documents_metadata_preserved():
    doc = Document(page_content="Content", metadata={"source": "test_file.txt", "page": 1})
    chunks = split_documents([doc], chunk_size=10, chunk_overlap=0)
    assert len(chunks) == 1
    assert chunks[0].metadata == {"source": "test_file.txt", "page": 1}

def test_split_documents_empty_input():
    chunks = split_documents([], chunk_size=10, chunk_overlap=0)
    assert len(chunks) == 0