"""
Document loader module for RAG pipeline.
Supports loading various document types (PDF, TXT).
"""

import os
from pathlib import Path
from typing import List, Union
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document


def load_document(file_path: Union[str, Path]) -> List[Document]:
    """
    Load a document based on its file extension.
    
    Args:
        file_path: Path to the document file
        
    Returns:
        List of Document objects
        
    Raises:
        ValueError: If file type is not supported
    """
    file_path = Path(file_path)
    extension = file_path.suffix.lower()
    
    if extension == '.pdf':
        loader = PyPDFLoader(str(file_path))
        return loader.load()
    elif extension == '.txt':
        loader = TextLoader(str(file_path), encoding='utf-8')
        return loader.load()
    else:
        raise ValueError(f"Unsupported file type: {extension}")


def load_documents_from_directory(directory_path: Union[str, Path]) -> List[Document]:
    """
    Load all supported documents from a directory.
    
    Args:
        directory_path: Path to the directory containing documents
        
    Returns:
        List of Document objects from all supported files
    """
    directory_path = Path(directory_path)
    documents = []
    
    for file_path in directory_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in ['.pdf', '.txt']:
            try:
                docs = load_document(file_path)
                documents.extend(docs)
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
                
    return documents