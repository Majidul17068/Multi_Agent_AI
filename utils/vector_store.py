import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from typing import List, Dict, Optional
import os

class VectorStore:
    def __init__(self, persist_directory: str = "data/chroma_db"):
        """
        Initialize the vector store with ChromaDB
        
        Args:
            persist_directory (str): Directory to persist the database
        """
        # Create persist directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Initialize the embedding function
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Create or get the collection
        self.collection = self.client.get_or_create_collection(
            name="documents",
            embedding_function=self.embedding_function
        )

    def add_documents(self, documents: List[str], metadatas: Optional[List[Dict]] = None, ids: Optional[List[str]] = None):
        """
        Add documents to the vector store
        
        Args:
            documents (List[str]): List of documents to add
            metadatas (Optional[List[Dict]]): List of metadata for each document
            ids (Optional[List[str]]): List of unique IDs for each document
        """
        if metadatas is None:
            metadatas = [{"source": f"document_{i}"} for i in range(len(documents))]
        
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]
        
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def search(self, query: str, n_results: int = 5) -> Dict:
        """
        Search for similar documents
        
        Args:
            query (str): Query text
            n_results (int): Number of results to return
            
        Returns:
            Dict: Dictionary containing results
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results

    def get_document(self, doc_id: str) -> Optional[Dict]:
        """
        Get a specific document by ID
        
        Args:
            doc_id (str): Document ID
            
        Returns:
            Optional[Dict]: Document data if found
        """
        try:
            result = self.collection.get(ids=[doc_id])
            return result
        except Exception:
            return None

    def delete_document(self, doc_id: str):
        """
        Delete a document by ID
        
        Args:
            doc_id (str): Document ID to delete
        """
        self.collection.delete(ids=[doc_id])

    def update_document(self, doc_id: str, document: str, metadata: Optional[Dict] = None):
        """
        Update a document
        
        Args:
            doc_id (str): Document ID to update
            document (str): New document content
            metadata (Optional[Dict]): New metadata
        """
        if metadata is None:
            metadata = {"source": f"document_{doc_id}"}
        
        self.collection.update(
            ids=[doc_id],
            documents=[document],
            metadatas=[metadata]
        )

    def get_all_documents(self) -> Dict:
        """
        Get all documents in the collection
        
        Returns:
            Dict: All documents and their metadata
        """
        return self.collection.get()

# Initialize the vector store
vector_store = VectorStore() 