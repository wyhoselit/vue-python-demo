import chromadb
from chromadb.config import Settings
from typing import Optional


class VectorStore:
    def __init__(self, persist_directory: str = "./chroma_db", collection_name: str = "rag_documents"):
        """
        Initializes the ChromaDB client and collection.

        Args:
            persist_directory: Directory where ChromaDB will persist data.
            collection_name: Name of the collection to use/create.
        """
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_documents(self, documents: list[dict]):
        """
        Adds documents with embeddings to the vector store.

        Args:
            documents: List of dicts with keys: 'id', 'embedding', 'document', 'metadata'
        """
        ids = [doc['id'] for doc in documents]
        embeddings = [doc['embedding'] for doc in documents]
        texts = [doc['document'] for doc in documents]
        metadatas = [doc['metadata'] for doc in documents]
        
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )

    def query(self, query_embedding: list[float], n_results: int = 5) -> dict:
        """
        Performs similarity search against the vector store.

        Args:
            query_embedding: The embedding vector to search for.
            n_results: Number of results to return.

        Returns:
            Dictionary with keys: 'ids', 'documents', 'metadatas', 'distances'
        """
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

    def get_collection_info(self) -> dict:
        """
        Returns information about the collection.
        """
        return {
            "name": self.collection.name,
            "count": self.collection.count()
        }


_vector_store: Optional[VectorStore] = None


def get_vector_store(persist_directory: str = "./chroma_db", collection_name: str = "rag_documents") -> VectorStore:
    """
    Returns a singleton instance of the VectorStore.
    """
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore(persist_directory, collection_name)
    return _vector_store