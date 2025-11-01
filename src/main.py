"""
FastAPI application for AI Market Analyst.

MODERN VERSION - Uses LangChain 1.0 create_agent with messages-based invocation
Migrated from deprecated AgentExecutor to modern agent API
"""
import time
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from config import Config
from schemas.models import QueryRequest, QueryResponse
from agent import agent
from services.document_processor import DocumentProcessor
from services.vector_store import VectorStoreManager


# Initialize FastAPI app
app = FastAPI(
    title="AI Market Analyst API",
    description="Multi-functional AI agent for market research analysis",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
document_processor = DocumentProcessor()
vector_store_manager = VectorStoreManager()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AI Market Analyst API",
        "version": "1.0.0",
        "langchain_version": "1.0.3",
        "endpoints": {
            "query": "/api/query",
            "upload": "/api/upload",
            "health": "/api/health"
        }
    }


@app.post("/api/query", response_model=QueryResponse)
async def query_agent(request: QueryRequest):
    """
    Query the AI Market Analyst agent.
    
    The agent will automatically route to the appropriate tool:
    - Q&A Tool: For factual questions
    - Insights Tool: For summaries and analysis
    - Extract Tool: For structured data extraction
    
    Note: Uses modern LangChain 1.0 messages-based invocation pattern.
    """
    start_time = time.time()
    
    # Generate session ID (note: current implementation doesn't use it for memory)
    # For proper session-based memory, would need to implement custom memory management
    session_id = request.session_id or f"session_{int(time.time())}"
    
    try:
        # Invoke agent with modern LangChain 1.0 pattern (messages-based)
        # Input format: {"messages": [{"role": "user", "content": "..."}]}
        result = agent.invoke({
            "messages": [{"role": "user", "content": request.query}]
        })
        
        # Extract answer from result
        # Modern create_agent returns {"messages": [...]} where last message is the response
        messages = result.get("messages", [])
        
        if not messages:
            raise ValueError("No messages in agent response")
        
        # Get the last message (agent's response)
        last_message = messages[-1]
        
        # Handle different content formats (string, list, etc.)
        if hasattr(last_message, 'content'):
            content = last_message.content
            # If content is a list, extract text from list items
            if isinstance(content, list):
                # Handle list of strings or other objects
                text_parts = []
                for item in content:
                    if isinstance(item, str):
                        text_parts.append(item)
                    elif hasattr(item, 'text'):
                        text_parts.append(item.text)
                    elif hasattr(item, 'content'):
                        text_parts.append(str(item.content))
                    else:
                        text_parts.append(str(item))
                answer = '\n'.join(text_parts) if text_parts else str(content)
            else:
                answer = str(content)
        else:
            answer = str(last_message)
        
        # Final safety check - ensure answer is always a non-empty string
        if not answer or not isinstance(answer, str):
            # Fallback: convert entire message to string
            answer = str(last_message)
        
        # Detect which tool was used by examining messages
        tool_used = None
        for msg in messages:
            # Tool call messages have tool_calls attribute
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                tool_used = msg.tool_calls[0].get('name', 'unknown_tool')
                break
            # Or check if it's a tool message
            elif hasattr(msg, 'type') and msg.type == 'tool':
                tool_used = getattr(msg, 'name', 'unknown_tool')
                break
        
        # Calculate execution time
        execution_time = int((time.time() - start_time) * 1000)
        
        return QueryResponse(
            answer=answer,
            tool_used=tool_used or "direct_response",
            session_id=session_id,
            execution_time_ms=execution_time
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Agent execution failed: {str(e)}"
        )


@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process a new market research document.
    
    Supports: .txt and .pdf files
    
    This will:
    1. Extract text from document (TXT or PDF)
    2. Process the document into chunks
    3. Generate embeddings
    4. Store in Pinecone vector database
    """
    try:
        # Read file content
        content = await file.read()
        
        # Extract text based on file type
        filename_lower = file.filename.lower()
        
        if filename_lower.endswith('.pdf'):
            # Handle PDF files
            try:
                from pypdf import PdfReader
                from io import BytesIO
                
                pdf_file = BytesIO(content)
                pdf_reader = PdfReader(pdf_file)
                
                # Extract text from all pages
                text_parts = []
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    page_text = page.extract_text()
                    if page_text.strip():
                        text_parts.append(page_text)
                
                text = "\n\n".join(text_parts)
                
                if not text.strip():
                    raise HTTPException(
                        status_code=400,
                        detail="PDF appears to be empty or contains only images. Please upload a PDF with extractable text."
                    )
                    
            except Exception as pdf_error:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to process PDF: {str(pdf_error)}. Ensure the PDF is not password-protected or corrupted."
                )
                
        elif filename_lower.endswith('.txt'):
            # Handle text files
            try:
                text = content.decode('utf-8')
            except UnicodeDecodeError:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid text file encoding. Please ensure the file is UTF-8 encoded."
                )
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format. Please upload a .txt or .pdf file."
            )
        
        # Process document
        documents = document_processor.process_document(
            text=text,
            source=file.filename
        )
        
        # Ingest into vector store
        result = vector_store_manager.ingest_documents(documents)
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["error"])
        
        return {
            "message": "Document processed successfully",
            "filename": file.filename,
            "file_type": "PDF" if filename_lower.endswith('.pdf') else "TXT",
            "chunks_created": len(documents),
            "namespace": Config.PINECONE_NAMESPACE,
            "status": "success"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )


@app.get("/api/health")
async def health_check():
    """
    System health check and statistics.
    """
    try:
        # Get vector store stats
        stats = vector_store_manager.get_stats()
        
        return {
            "status": "healthy",
            "configuration": {
                "gemini_model": Config.GEMINI_MODEL,
                "embedding_model": Config.EMBEDDING_MODEL,
                "pinecone_index": Config.PINECONE_INDEX_NAME,
                "namespace": Config.PINECONE_NAMESPACE,
                "langchain_version": "1.0.3"
            },
            "vector_store": stats
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


if __name__ == "__main__":
    import sys
    from pathlib import Path
    
    # Add src directory to Python path
    src_dir = Path(__file__).parent
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))
    
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False
    )

