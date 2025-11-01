"""
Configuration management for the AI Market Analyst application.
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration."""
    
    # API Keys
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    
    # Pinecone Configuration
    PINECONE_ENVIRONMENT: str = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "market-analyst-index")
    PINECONE_NAMESPACE: str = "innovate_inc"
    
    # Model Configuration
    GEMINI_MODEL: str = "gemini-2.5-flash"  # Free tier model
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L12-v2"
    EMBEDDING_DIMENSION: int = 384
    
    # Chunking Configuration
    CHUNK_SIZE: int = 400
    CHUNK_OVERLAP: int = 80
    
    # Retrieval Configuration
    RETRIEVAL_K: int = 4
    RELEVANCE_THRESHOLD: float = 0.7
    
    # Application Settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate(cls) -> None:
        """Validate required configuration."""
        required_keys = [
            ("GOOGLE_API_KEY", cls.GOOGLE_API_KEY),
            ("PINECONE_API_KEY", cls.PINECONE_API_KEY),
        ]
        
        missing = [key for key, value in required_keys if not value]
        if missing:
            # Defer hard failure to runtime; warn during startup
            print(
                f"[Config] Warning: Missing environment variables: {', '.join(missing)}. "
                "Some features (LLM, embeddings, vector store) will fail until these are set."
            )


# Optional strict validation: set STRICT_CONFIG=1 to enforce at startup
if os.getenv("STRICT_CONFIG", "0") == "1":
    Config.validate()