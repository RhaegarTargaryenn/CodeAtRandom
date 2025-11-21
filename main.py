"""
Main Module
Entry point for the Document Search Engine application.
Initializes the search engine and starts the FastAPI server.
"""

import os
import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.search_engine import SearchEngine
from src.utils import create_sample_documents, validate_directory
import src.api as api_module
import uvicorn


def initialize_search_engine(
    data_dir: str = "data",
    cache_db_path: str = "cache/embeddings_cache.db",
    use_faiss: bool = True,
    force_regenerate: bool = False
) -> SearchEngine:
    """
    Initialize the search engine with documents and embeddings.
    
    Args:
        data_dir (str): Directory containing text documents
        cache_db_path (str): Path to cache database
        use_faiss (bool): Whether to use FAISS for search
        force_regenerate (bool): Force regeneration of embeddings
        
    Returns:
        SearchEngine: Initialized search engine instance
    """
    print("="*60)
    print("INITIALIZING DOCUMENT SEARCH ENGINE")
    print("="*60)
    
    # Validate data directory
    is_valid, message = validate_directory(data_dir)
    
    if not is_valid:
        print(f"\n⚠️  {message}")
        print(f"\nCreating sample documents in {data_dir}...")
        create_sample_documents(data_dir, num_docs=20)
        print("✓ Sample documents created")
    else:
        print(f"✓ {message}")
    
    # Initialize search engine
    print("\n" + "-"*60)
    engine = SearchEngine(
        data_dir=data_dir,
        cache_db_path=cache_db_path,
        use_faiss=use_faiss
    )
    
    # Load documents
    print("\n" + "-"*60)
    num_docs = engine.load_documents()
    
    if num_docs == 0:
        print("\n❌ No documents loaded. Cannot continue.")
        sys.exit(1)
    
    print(f"✓ Loaded {num_docs} documents")
    
    # Generate embeddings
    print("\n" + "-"*60)
    engine.generate_embeddings(force_regenerate=force_regenerate)
    print("✓ Embeddings generated")
    
    # Build vector index
    print("\n" + "-"*60)
    engine.build_vector_index()
    print("✓ Vector index built")
    
    # Show statistics
    print("\n" + "="*60)
    print("SEARCH ENGINE STATISTICS")
    print("="*60)
    stats = engine.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*60)
    print("✓ SEARCH ENGINE READY")
    print("="*60)
    
    return engine


def start_api_server(
    engine: SearchEngine,
    host: str = "0.0.0.0",
    port: int = 8000,
    reload: bool = False
):
    """
    Start the FastAPI server.
    
    Args:
        engine (SearchEngine): Initialized search engine
        host (str): Host to bind to
        port (int): Port to bind to
        reload (bool): Enable auto-reload (development mode)
    """
    # Set the search engine in the API module
    api_module.set_search_engine(engine)
    
    print("\n" + "="*60)
    print("STARTING API SERVER")
    print("="*60)
    print(f"  Host: {host}")
    print(f"  Port: {port}")
    print(f"  API Documentation: http://localhost:{port}/docs")
    print(f"  Interactive API: http://localhost:{port}/redoc")
    print("="*60)
    print("\n🚀 Server starting...\n")
    
    # Start server
    uvicorn.run(
        api_module.app,
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )


def main():
    """
    Main function with CLI argument parsing.
    """
    parser = argparse.ArgumentParser(
        description="Document Search Engine - Embedding-based semantic search"
    )
    
    parser.add_argument(
        "--data-dir",
        type=str,
        default="data",
        help="Directory containing text documents (default: data)"
    )
    
    parser.add_argument(
        "--cache-db",
        type=str,
        default="cache/embeddings_cache.db",
        help="Path to cache database (default: cache/embeddings_cache.db)"
    )
    
    parser.add_argument(
        "--no-faiss",
        action="store_true",
        help="Use cosine similarity instead of FAISS"
    )
    
    parser.add_argument(
        "--force-regenerate",
        action="store_true",
        help="Force regeneration of all embeddings (ignore cache)"
    )
    
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="API server host (default: 0.0.0.0)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="API server port (default: 8000)"
    )
    
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload (development mode)"
    )
    
    parser.add_argument(
        "--create-samples",
        type=int,
        metavar="N",
        help="Create N sample documents and exit"
    )
    
    args = parser.parse_args()
    
    # Handle create-samples command
    if args.create_samples:
        print(f"Creating {args.create_samples} sample documents...")
        create_sample_documents(args.data_dir, num_docs=args.create_samples)
        print(f"✓ Created {args.create_samples} documents in {args.data_dir}")
        return
    
    # Initialize search engine
    try:
        engine = initialize_search_engine(
            data_dir=args.data_dir,
            cache_db_path=args.cache_db,
            use_faiss=not args.no_faiss,
            force_regenerate=args.force_regenerate
        )
    except Exception as e:
        print(f"\n❌ Failed to initialize search engine: {e}")
        sys.exit(1)
    
    # Start API server
    try:
        start_api_server(
            engine=engine,
            host=args.host,
            port=args.port,
            reload=args.reload
        )
    except KeyboardInterrupt:
        print("\n\n⏹️  Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
