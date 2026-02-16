"""
Banking AI Agent - FastAPI Backend
Main application entry point
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

from backend.config import settings
from backend.agent.rag import initialize_rag
from backend.agent.agent import FunctionCallingAgent
from backend.data_init import create_sample_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global variables
rag_system = None
agent = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown"""
    # Startup
    global rag_system, agent
    logger.info("🚀 Starting Banking AI Agent...")
    
    try:
        # Initialize sample data
        logger.info("Creating sample banking data...")
        create_sample_data()
        
        # Initialize RAG system
        logger.info("Initializing RAG system with vector embeddings...")
        rag_system = initialize_rag(settings)
        
        # Initialize Agent
        logger.info("Initializing function calling agent...")
        agent = FunctionCallingAgent(rag_system, settings)
        
        logger.info("✅ Banking AI Agent ready!")
    except Exception as e:
        logger.error(f"❌ Startup error: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Banking AI Agent...")


# Create FastAPI app
app = FastAPI(
    title="Banking AI Agent API",
    description="AI-powered banking customer service with function calling",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class ChatRequest(BaseModel):
    """Chat request model"""
    message: str
    conversation_id: str = "default"


class ChatResponse(BaseModel):
    """Chat response model"""
    response: str
    iterations: int
    tool_calls: list
    success: bool


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    rag_ready: bool
    agent_ready: bool


# Routes
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "rag_ready": rag_system is not None,
        "agent_ready": agent is not None
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a customer query through the banking AI agent
    
    Args:
        request: ChatRequest containing customer message
    
    Returns:
        ChatResponse with agent's response and metadata
    """
    if agent is None or rag_system is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    try:
        logger.info(f"Processing message: {request.message[:100]}...")
        
        result = agent.process_message(request.message)
        
        return ChatResponse(
            response=result["response"],
            iterations=result["iterations"],
            tool_calls=result["tool_calls"],
            success=result["success"]
        )
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reset")
async def reset_conversation():
    """Reset conversation history"""
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    agent.reset_conversation()
    return {"message": "Conversation reset successfully"}


@app.get("/info")
async def get_info():
    """Get agent information"""
    return {
        "name": "Banking AI Agent",
        "version": "1.0.0",
        "capabilities": [
            "Account information retrieval",
            "Transaction history lookup",
            "Branch location finder",
            "Loan eligibility check",
            "Query escalation to human agents",
            "Context-aware responses using RAG"
        ],
        "model": settings.GEMINI_MODEL,
        "rag_enabled": rag_system is not None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        log_level="info"
    )
