"""
Text splitter module for RAG pipeline.
Splits documents into smaller chunks for embedding.
"""

from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def split_documents(documents: List[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """
    Splits a list of documents into smaller, overlapping chunks.

    Args:
        documents: A list of Document objects.
        chunk_size: The maximum size of each chunk.
        chunk_overlap: The number of characters to overlap between chunks.

    Returns:
        A list of Document objects, where each document is a chunk.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)
