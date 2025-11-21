"""
API Module
FastAPI application for the document search engine.
Provides REST endpoints for searching documents.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import time

# This will be imported from main
search_engine = None


# Request/Response models
class SearchRequest(BaseModel):
    """Search request model"""
    query: str = Field(..., description="Search query text", min_length=1)
    top_k: int = Field(5, description="Number of top results to return", ge=1, le=50)
    
    class Config:
        schema_extra = {
            "example": {
                "query": "machine learning algorithms",
                "top_k": 5
            }
        }


class SearchResult(BaseModel):
    """Single search result model"""
    rank: int = Field(..., description="Result ranking position")
    doc_id: str = Field(..., description="Document identifier")
    filename: str = Field(..., description="Document filename")
    score: float = Field(..., description="Similarity score")
    preview: str = Field(..., description="Document preview text")
    doc_length: int = Field(..., description="Document length in characters")
    keywords_overlap: List[str] = Field(..., description="Overlapping keywords with query")
    overlap_count: int = Field(..., description="Number of overlapping keywords")
    overlap_ratio: float = Field(..., description="Ratio of overlapping keywords")
    explanation: str = Field(..., description="Human-readable match explanation")


class SearchResponse(BaseModel):
    """Search response model"""
    query: str = Field(..., description="Original search query")
    top_k: int = Field(..., description="Number of results requested")
    total_results: int = Field(..., description="Number of results returned")
    search_time_ms: float = Field(..., description="Search execution time in milliseconds")
    results: List[SearchResult] = Field(..., description="List of search results")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str
    stats: Optional[Dict] = None


# Create FastAPI app
app = FastAPI(
    title="Document Search Engine API",
    description="Embedding-based search engine with caching for text documents",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def set_search_engine(engine):
    """
    Set the search engine instance.
    Called from main.py during initialization.
    
    Args:
        engine: SearchEngine instance
    """
    global search_engine
    search_engine = engine


@app.get("/", tags=["General"])
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Document Search Engine API",
        "version": "1.0.0",
        "description": "Embedding-based semantic search over text documents",
        "endpoints": {
            "health": "/health",
            "search": "/search",
            "stats": "/stats",
            "docs": "/docs"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check():
    """
    Health check endpoint.
    Returns the status of the search engine.
    """
    if search_engine is None:
        raise HTTPException(
            status_code=503, 
            detail="Search engine not initialized"
        )
    
    stats = search_engine.get_stats()
    
    return {
        "status": "healthy",
        "message": "Search engine is operational",
        "stats": stats
    }


@app.get("/stats", tags=["General"])
async def get_stats():
    """
    Get search engine statistics.
    Returns information about loaded documents, cache, etc.
    """
    if search_engine is None:
        raise HTTPException(
            status_code=503,
            detail="Search engine not initialized"
        )
    
    return search_engine.get_stats()


@app.post("/search", response_model=SearchResponse, tags=["Search"])
async def search_documents(request: SearchRequest):
    """
    Search for documents similar to the query.
    
    Uses semantic similarity (embeddings) to find relevant documents.
    Returns ranked results with similarity scores and explanations.
    
    Args:
        request (SearchRequest): Search request with query and top_k
        
    Returns:
        SearchResponse: Search results with metadata
    """
    if search_engine is None:
        raise HTTPException(
            status_code=503,
            detail="Search engine not initialized"
        )
    
    # Validate query
    if not request.query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty"
        )
    
    # Perform search with timing
    start_time = time.time()
    
    try:
        results = search_engine.search(
            query=request.query,
            top_k=request.top_k
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )
    
    search_time_ms = (time.time() - start_time) * 1000
    
    # Build response
    response = SearchResponse(
        query=request.query,
        top_k=request.top_k,
        total_results=len(results),
        search_time_ms=round(search_time_ms, 2),
        results=[SearchResult(**result) for result in results]
    )
    
    return response


@app.get("/search", response_model=SearchResponse, tags=["Search"])
async def search_documents_get(
    query: str = Query(..., description="Search query text", min_length=1),
    top_k: int = Query(5, description="Number of results", ge=1, le=50)
):
    """
    Search for documents (GET method).
    Alternative to POST /search for simple browser-based queries.
    
    Args:
        query (str): Search query text
        top_k (int): Number of top results to return
        
    Returns:
        SearchResponse: Search results with metadata
    """
    request = SearchRequest(query=query, top_k=top_k)
    return await search_documents(request)


@app.get("/documents", tags=["Documents"])
async def list_documents(
    limit: int = Query(100, description="Maximum number of documents to return", ge=1, le=1000),
    offset: int = Query(0, description="Offset for pagination", ge=0)
):
    """
    List all loaded documents with metadata.
    
    Args:
        limit (int): Maximum number of documents to return
        offset (int): Offset for pagination
        
    Returns:
        Dict: Document list with metadata
    """
    if search_engine is None:
        raise HTTPException(
            status_code=503,
            detail="Search engine not initialized"
        )
    
    documents = search_engine.documents[offset:offset + limit]
    
    # Return limited metadata (without full content)
    doc_list = [
        {
            "doc_id": doc["doc_id"],
            "filename": doc["filename"],
            "length": doc["cleaned_length"],
            "preview": doc["content"][:100] + "..." if len(doc["content"]) > 100 else doc["content"]
        }
        for doc in documents
    ]
    
    return {
        "total_documents": len(search_engine.documents),
        "offset": offset,
        "limit": limit,
        "returned": len(doc_list),
        "documents": doc_list
    }


@app.get("/document/{doc_id}", tags=["Documents"])
async def get_document(doc_id: str):
    """
    Get a specific document by ID.
    
    Args:
        doc_id (str): Document identifier
        
    Returns:
        Dict: Document with full content
    """
    if search_engine is None:
        raise HTTPException(
            status_code=503,
            detail="Search engine not initialized"
        )
    
    # Find document
    doc_idx = search_engine.doc_id_to_idx.get(doc_id)
    
    if doc_idx is None:
        raise HTTPException(
            status_code=404,
            detail=f"Document not found: {doc_id}"
        )
    
    doc = search_engine.documents[doc_idx]
    
    return {
        "doc_id": doc["doc_id"],
        "filename": doc["filename"],
        "filepath": doc["filepath"],
        "content": doc["content"],
        "raw_content": doc["raw_content"],
        "length": doc["cleaned_length"],
        "raw_length": doc["length"]
    }


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors"""
    return {
        "error": "Not Found",
        "message": "The requested resource was not found",
        "path": str(request.url)
    }


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle 500 errors"""
    return {
        "error": "Internal Server Error",
        "message": "An unexpected error occurred",
        "detail": str(exc)
    }


# Example usage
if __name__ == "__main__":
    import uvicorn
    
    print("Starting FastAPI server...")
    print("Note: Search engine must be initialized from main.py")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
