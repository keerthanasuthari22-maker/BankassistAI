"""
Configuration management for Banking AI Agent
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Gemini Configuration (Free API)
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.0-flash"
    TEMPERATURE: float = 0.7
    
    # Backend Configuration
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    DEBUG: bool = False
    
    # Frontend Configuration
    FRONTEND_URL: str = "http://localhost:8501"
    
    # Data Paths
    DATA_DIR: Path = Path(__file__).parent / "data"
    VECTORSTORE_DIR: Path = Path(__file__).parent.parent / "vectorstore"
    LOGS_DIR: Path = Path(__file__).parent / "logs"
    
    # RAG Configuration
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 200
    EMBEDDING_DIMENSION: int = 768
    TOP_K_RETRIEVAL: int = 5
    
    # Agent Configuration
    MAX_ITERATIONS: int = 10
    TIMEOUT_SECONDS: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"
    
    def __init__(self, **data):
        super().__init__(**data)
        # Create necessary directories
        self.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        self.VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)


# Load settings
try:
    settings = Settings()
except Exception as e:
    print(f"⚠️  Warning: Could not load environment variables: {e}")
    print("Make sure .env file exists with OPENAI_API_KEY")
    raise
