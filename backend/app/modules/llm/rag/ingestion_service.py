"""
Ingestion service for RAG pipeline.
Orchestrates document loading, splitting, embedding generation, and storing.
"""

from typing import List
from langchain_core.documents import Document
from app.modules.llm.rag.document_loader import load_document, load_documents_from_directory
from app.modules.llm.rag.text_splitter import split_documents
from app.modules.llm.rag.embedding_generator import EmbeddingGenerator
from app.modules.llm.rag.vector_store import get_vector_store


_embedding_generator = EmbeddingGenerator()


def ingest_document(file_path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """
    Loads, splits, generates embeddings for, and prepares a single document for further processing.

    Args:
        file_path: Path to the document file.
        chunk_size: Size of document chunks.
        chunk_overlap: Overlap between document chunks.

    Returns:
        A list of Document objects (chunks) with embeddings in metadata.
    """
    documents = load_document(file_path)
    chunks = split_documents(documents, chunk_size, chunk_overlap)
    
    texts = [chunk.page_content for chunk in chunks]
    embeddings = _embedding_generator.generate_embeddings(texts)
    
    for chunk, embedding in zip(chunks, embeddings):
        chunk.metadata['embedding'] = embedding
    
    return chunks


def ingest_documents_from_directory(directory_path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """
    Loads, splits, generates embeddings for, and prepares multiple documents from a directory for further processing.

    Args:
        directory_path: Path to the directory containing documents.
        chunk_size: Size of document chunks.
        chunk_overlap: Overlap between document chunks.

    Returns:
        A list of Document objects (chunks) from all ingested documents with embeddings in metadata.
    """
    documents = load_documents_from_directory(directory_path)
    all_chunks = []
    for doc in documents:
        chunks = split_documents([doc], chunk_size, chunk_overlap)
        all_chunks.extend(chunks)
    
    texts = [chunk.page_content for chunk in all_chunks]
    embeddings = _embedding_generator.generate_embeddings(texts)
    
    for chunk, embedding in zip(all_chunks, embeddings):
        chunk.metadata['embedding'] = embedding
    
    return all_chunks


async def ingest_and_store_document(file_path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """
    Loads, splits, generates embeddings for, and stores a single document in the vector store.

    Args:
        file_path: Path to the document file.
        chunk_size: Size of document chunks.
        chunk_overlap: Overlap between document chunks.

    Returns:
        A list of Document objects (chunks) that were stored.
    """
    chunks = ingest_document(file_path, chunk_size, chunk_overlap)
    
    vector_store = get_vector_store()
    
    docs_to_store = []
    for i, chunk in enumerate(chunks):
        doc_id = f"{file_path}_{i}"
        docs_to_store.append({
            'id': doc_id,
            'embedding': chunk.metadata['embedding'],
            'document': chunk.page_content,
            'metadata': {k: v for k, v in chunk.metadata.items() if k != 'embedding'}
        })
    
    vector_store.add_documents(docs_to_store)
    
    return chunks


async def ingest_and_store_documents_from_directory(directory_path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """
    Loads, splits, generates embeddings for, and stores multiple documents from a directory in the vector store.

    Args:
        directory_path: Path to the directory containing documents.
        chunk_size: Size of document chunks.
        chunk_overlap: Overlap between document chunks.

    Returns:
        A list of Document objects (chunks) that were stored.
    """
    chunks = ingest_documents_from_directory(directory_path, chunk_size, chunk_overlap)
    
    vector_store = get_vector_store()
    
    docs_to_store = []
    for i, chunk in enumerate(chunks):
        source = chunk.metadata.get('source', 'unknown')
        doc_id = f"{source}_{i}"
        docs_to_store.append({
            'id': doc_id,
            'embedding': chunk.metadata['embedding'],
            'document': chunk.page_content,
            'metadata': {k: v for k, v in chunk.metadata.items() if k != 'embedding'}
        })
    
    vector_store.add_documents(docs_to_store)
    
    return chunks
