"""
Test Script - Verify Search Engine Components
Run this script to test individual components before starting the full server.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def test_embedder():
    """Test the Embedder component"""
    print("\n" + "="*60)
    print("TEST 1: Embedder")
    print("="*60)
    
    try:
        from src.embedder import Embedder
        
        embedder = Embedder()
        
        # Test single embedding
        text = "This is a test document about machine learning."
        embedding = embedder.embed_text(text)
        
        print(f"✓ Embedder loaded successfully")
        print(f"✓ Embedding dimension: {embedder.get_embedding_dimension()}")
        print(f"✓ Single text embedding shape: {embedding.shape}")
        
        # Test batch embedding
        texts = ["First document", "Second document", "Third document"]
        embeddings = embedder.embed_documents(texts, show_progress=False)
        print(f"✓ Batch embeddings shape: {embeddings.shape}")
        
        return True
    except Exception as e:
        print(f"❌ Embedder test failed: {e}")
        return False


def test_cache_manager():
    """Test the CacheManager component"""
    print("\n" + "="*60)
    print("TEST 2: Cache Manager")
    print("="*60)
    
    try:
        from src.cache_manager import CacheManager
        import numpy as np
        import os
        
        # Use test cache
        test_cache_path = "cache/test_cache.db"
        cache_mgr = CacheManager(test_cache_path)
        
        # Test hash computation
        text = "Test document content"
        hash_val = cache_mgr.compute_hash(text)
        print(f"✓ Hash computation works: {hash_val[:16]}...")
        
        # Test save/load
        test_embedding = np.random.rand(384).astype(np.float32)
        cache_mgr.save_embedding("test_doc", text, test_embedding)
        print(f"✓ Embedding saved to cache")
        
        # Test cache hit
        cached = cache_mgr.check_cache("test_doc", text, 384)
        if cached is not None:
            print(f"✓ Cache hit successful")
        
        # Test cache miss (modified text)
        cached = cache_mgr.check_cache("test_doc", "Modified text", 384)
        if cached is None:
            print(f"✓ Cache miss detected correctly")
        
        # Clean up test cache
        if os.path.exists(test_cache_path):
            os.remove(test_cache_path)
        
        return True
    except Exception as e:
        print(f"❌ Cache Manager test failed: {e}")
        return False


def test_utils():
    """Test utility functions"""
    print("\n" + "="*60)
    print("TEST 3: Utils")
    print("="*60)
    
    try:
        from src.utils import clean_text, extract_keywords, compute_overlap
        
        # Test text cleaning
        dirty = "<html>  Test   TEXT  </html>"
        clean = clean_text(dirty)
        print(f"✓ Text cleaning: '{dirty}' -> '{clean}'")
        
        # Test keyword extraction
        keywords = extract_keywords("Machine learning and deep learning")
        print(f"✓ Keyword extraction: {keywords}")
        
        # Test overlap
        overlap = compute_overlap(["machine", "learning"], ["machine", "neural", "learning"])
        print(f"✓ Overlap computation: {overlap['overlap_count']} keywords")
        
        return True
    except Exception as e:
        print(f"❌ Utils test failed: {e}")
        return False


def test_search_engine_basic():
    """Test basic SearchEngine initialization"""
    print("\n" + "="*60)
    print("TEST 4: Search Engine (Basic)")
    print("="*60)
    
    try:
        from src.search_engine import SearchEngine
        from src.utils import create_sample_documents
        import os
        
        # Create test data directory
        test_data_dir = "data/test"
        os.makedirs(test_data_dir, exist_ok=True)
        
        # Create sample documents
        create_sample_documents(test_data_dir, num_docs=5)
        print(f"✓ Created 5 test documents")
        
        # Initialize search engine
        engine = SearchEngine(
            data_dir=test_data_dir,
            cache_db_path="cache/test_search_cache.db",
            use_faiss=False  # Use cosine similarity for testing
        )
        print(f"✓ Search engine initialized")
        
        # Load documents
        num_docs = engine.load_documents()
        print(f"✓ Loaded {num_docs} documents")
        
        # Generate embeddings
        engine.generate_embeddings()
        print(f"✓ Generated embeddings")
        
        # Build index
        engine.build_vector_index()
        print(f"✓ Built vector index")
        
        # Test search
        results = engine.search("machine learning", top_k=3)
        print(f"✓ Search works! Found {len(results)} results")
        
        if len(results) > 0:
            print(f"\nTop result:")
            print(f"  - Document: {results[0]['filename']}")
            print(f"  - Score: {results[0]['score']:.3f}")
            print(f"  - Preview: {results[0]['preview'][:50]}...")
        
        return True
    except Exception as e:
        print(f"❌ Search Engine test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_api_models():
    """Test API Pydantic models"""
    print("\n" + "="*60)
    print("TEST 5: API Models")
    print("="*60)
    
    try:
        from src.api import SearchRequest, SearchResponse, SearchResult
        
        # Test request model
        request = SearchRequest(query="test query", top_k=5)
        print(f"✓ SearchRequest model works")
        
        # Test result model
        result = SearchResult(
            rank=1,
            doc_id="doc_001",
            filename="test.txt",
            score=0.85,
            preview="Test preview",
            doc_length=100,
            keywords_overlap=["test"],
            overlap_count=1,
            overlap_ratio=0.5,
            explanation="Test explanation"
        )
        print(f"✓ SearchResult model works")
        
        # Test response model
        response = SearchResponse(
            query="test",
            top_k=5,
            total_results=1,
            search_time_ms=10.5,
            results=[result]
        )
        print(f"✓ SearchResponse model works")
        
        return True
    except Exception as e:
        print(f"❌ API Models test failed: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "█"*60)
    print("RUNNING COMPONENT TESTS")
    print("█"*60)
    
    results = []
    
    # Run tests
    results.append(("Embedder", test_embedder()))
    results.append(("Cache Manager", test_cache_manager()))
    results.append(("Utils", test_utils()))
    results.append(("Search Engine", test_search_engine_basic()))
    results.append(("API Models", test_api_models()))
    
    # Summary
    print("\n" + "█"*60)
    print("TEST SUMMARY")
    print("█"*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print("\n" + "="*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("\n🎉 All tests passed! Your project is ready.")
        print("\nNext steps:")
        print("1. Prepare your data in the data/ directory")
        print("2. Run: python main.py")
        print("3. Open: http://localhost:8000/docs")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
