"""
Vector store management using Pinecone.
"""
import time
from typing import List
from pinecone import Pinecone as PineconeClient, ServerlessSpec
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import Pinecone as PineconeVectorStore
from langchain_core.documents import Document
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config


class VectorStoreManager:
    """Manages Pinecone vector store operations."""
    
    def __init__(self):
        # Initialize Pinecone client
        self.pc = PineconeClient(api_key=Config.PINECONE_API_KEY)
        self.index_name = Config.PINECONE_INDEX_NAME
        
        # Initialize HuggingFace embeddings (all-MiniLM-L12-v2)
        self.embeddings = HuggingFaceEmbeddings(
            model_name=Config.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}  # Normalize for cosine similarity
        )
        
        # Initialize or get index
        self._init_index()
        
        # Get index reference
        self.index = self.pc.Index(self.index_name)
        
        # Initialize vector store with newer API
        self.vector_store = PineconeVectorStore(
            index=self.index,
            embedding=self.embeddings,
            text_key="text",
            namespace=Config.PINECONE_NAMESPACE
        )
    
    def _init_index(self):
        """Initialize Pinecone index if it doesn't exist."""
        existing_indexes = [idx["name"] for idx in self.pc.list_indexes()]
        
        if self.index_name not in existing_indexes:
            print(f"Creating new Pinecone index: {self.index_name}")
            self.pc.create_index(
                name=self.index_name,
                dimension=Config.EMBEDDING_DIMENSION,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region=Config.PINECONE_ENVIRONMENT
                )
            )
            # Wait for index to be ready
            time.sleep(1)
    
    def ingest_documents(self, documents: List[Document]) -> dict:
        """
        Ingest documents into Pinecone.
        
        Args:
            documents: List of Document objects
            
        Returns:
            Dictionary with ingestion statistics
        """
        try:
            # Generate unique IDs
            ids = [f"chunk_{i}" for i in range(len(documents))]
            
            # Upsert to vector store
            self.vector_store.add_documents(
                documents=documents,
                ids=ids
            )
            
            return {
                "status": "success",
                "chunks_processed": len(documents),
                "namespace": Config.PINECONE_NAMESPACE
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def get_retriever(self, k: int = None, score_threshold: float = None):
        """
        Get retriever for RAG.
        
        Args:
            k: Number of documents to retrieve
            score_threshold: Minimum relevance score (None means no threshold filtering)
            
        Returns:
            Configured retriever
        """
        k = k or Config.RETRIEVAL_K
        
        # If score_threshold is explicitly None, use similarity search without threshold
        if score_threshold is None:
            return self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": k}
            )
        
        # Otherwise use the provided threshold (guaranteed to be not None here)
        return self.vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": k,
                "score_threshold": score_threshold
            }
        )
    
    def get_stats(self) -> dict:
        """Get index statistics."""
        try:
            stats = self.index.describe_index_stats()
            return {
                "total_vectors": stats.total_vector_count,
                "dimension": stats.dimension,
                "namespaces": dict(stats.namespaces)
            }
        except Exception as e:
            return {"error": str(e)}