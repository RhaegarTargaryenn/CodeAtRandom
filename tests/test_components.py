"""
Unit Tests for Document Search Engine Components
Tests the core functionality of embedder and cache manager.
"""

import unittest
import numpy as np
import sys
import os
from pathlib import Path
import tempfile
import shutil

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.embedder import Embedder
from src.cache_manager import CacheManager


class TestEmbedder(unittest.TestCase):
    """Test cases for the Embedder class"""
    
    @classmethod
    def setUpClass(cls):
        """Set up embedder instance once for all tests"""
        print("\n" + "="*60)
        print("TESTING: Embedder")
        print("="*60)
        cls.embedder = Embedder()
    
    def test_model_loaded(self):
        """Test that model is loaded successfully"""
        self.assertIsNotNone(self.embedder.model)
        print("✓ Model loaded successfully")
    
    def test_embedding_dimension(self):
        """Test that embedding dimension is correct"""
        dim = self.embedder.get_embedding_dimension()
        self.assertEqual(dim, 384, "Expected 384-dimensional embeddings")
        print(f"✓ Embedding dimension: {dim}")
    
    def test_embed_single_text(self):
        """Test embedding a single text"""
        text = "This is a test document about machine learning."
        embedding = self.embedder.embed_text(text)
        
        self.assertIsInstance(embedding, np.ndarray)
        self.assertEqual(embedding.shape[0], 384)
        print(f"✓ Single text embedding shape: {embedding.shape}")
    
    def test_embed_multiple_texts(self):
        """Test embedding multiple texts"""
        texts = [
            "Machine learning is a subset of AI.",
            "Deep learning uses neural networks.",
            "NLP helps computers understand text."
        ]
        
        embeddings = self.embedder.embed_documents(texts, show_progress=False)
        
        self.assertIsInstance(embeddings, np.ndarray)
        self.assertEqual(embeddings.shape, (3, 384))
        print(f"✓ Multiple texts embedding shape: {embeddings.shape}")
    
    def test_lowercase_normalization(self):
        """Test that text is lowercased"""
        text1 = "MACHINE LEARNING"
        text2 = "machine learning"
        
        emb1 = self.embedder.embed_text(text1)
        emb2 = self.embedder.embed_text(text2)
        
        # Should be identical due to lowercasing
        np.testing.assert_array_equal(emb1, emb2)
        print("✓ Lowercase normalization works")
    
    def test_normalize_embeddings(self):
        """Test embedding normalization"""
        embeddings = np.random.rand(5, 384).astype(np.float32)
        normalized = self.embedder.normalize_embeddings(embeddings)
        
        # Check that norms are approximately 1
        norms = np.linalg.norm(normalized, axis=1)
        np.testing.assert_array_almost_equal(norms, np.ones(5), decimal=5)
        print("✓ Embedding normalization works")
    
    def test_empty_text_handling(self):
        """Test handling of empty text"""
        with self.assertRaises(ValueError):
            self.embedder.embed_text("")
        print("✓ Empty text handling works")


class TestCacheManager(unittest.TestCase):
    """Test cases for the CacheManager class"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test cache directory"""
        print("\n" + "="*60)
        print("TESTING: Cache Manager")
        print("="*60)
        cls.test_cache_dir = tempfile.mkdtemp()
        cls.test_cache_path = os.path.join(cls.test_cache_dir, "test_cache.db")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test cache directory"""
        if os.path.exists(cls.test_cache_dir):
            shutil.rmtree(cls.test_cache_dir)
    
    def setUp(self):
        """Create fresh cache manager for each test"""
        self.cache_mgr = CacheManager(self.test_cache_path)
    
    def test_database_initialized(self):
        """Test that database is initialized"""
        self.assertTrue(os.path.exists(self.test_cache_path))
        print(f"✓ Database initialized at {self.test_cache_path}")
    
    def test_compute_hash(self):
        """Test hash computation"""
        text1 = "This is a test"
        text2 = "This is a test"
        text3 = "This is different"
        
        hash1 = self.cache_mgr.compute_hash(text1)
        hash2 = self.cache_mgr.compute_hash(text2)
        hash3 = self.cache_mgr.compute_hash(text3)
        
        # Same text should have same hash
        self.assertEqual(hash1, hash2)
        # Different text should have different hash
        self.assertNotEqual(hash1, hash3)
        
        # Hash should be 64 characters (SHA256 hex)
        self.assertEqual(len(hash1), 64)
        print(f"✓ Hash computation works: {hash1[:16]}...")
    
    def test_save_and_retrieve_embedding(self):
        """Test saving and retrieving an embedding"""
        doc_id = "test_doc_001"
        text = "This is a test document for caching."
        embedding = np.random.rand(384).astype(np.float32)
        
        # Save embedding
        self.cache_mgr.save_embedding(doc_id, text, embedding)
        print("✓ Embedding saved to cache")
        
        # Retrieve embedding
        cached = self.cache_mgr.check_cache(doc_id, text, 384)
        
        self.assertIsNotNone(cached)
        np.testing.assert_array_almost_equal(embedding, cached, decimal=6)
        print("✓ Embedding retrieved from cache")
    
    def test_cache_invalidation(self):
        """Test that cache is invalidated when text changes"""
        doc_id = "test_doc_002"
        text1 = "Original text"
        text2 = "Modified text"
        embedding = np.random.rand(384).astype(np.float32)
        
        # Save with original text
        self.cache_mgr.save_embedding(doc_id, text1, embedding)
        
        # Try to retrieve with modified text
        cached = self.cache_mgr.check_cache(doc_id, text2, 384)
        
        # Should return None because hash doesn't match
        self.assertIsNone(cached)
        print("✓ Cache invalidation on text change works")
    
    def test_cache_hit(self):
        """Test cache hit scenario"""
        doc_id = "test_doc_003"
        text = "Cache hit test"
        embedding = np.random.rand(384).astype(np.float32)
        
        # Save embedding
        self.cache_mgr.save_embedding(doc_id, text, embedding)
        
        # Retrieve with same text
        cached = self.cache_mgr.check_cache(doc_id, text, 384)
        
        self.assertIsNotNone(cached)
        print("✓ Cache hit works correctly")
    
    def test_cache_miss(self):
        """Test cache miss scenario"""
        doc_id = "nonexistent_doc"
        text = "This doc doesn't exist"
        
        cached = self.cache_mgr.check_cache(doc_id, text, 384)
        
        self.assertIsNone(cached)
        print("✓ Cache miss works correctly")
    
    def test_cache_stats(self):
        """Test cache statistics"""
        # Add some entries
        for i in range(5):
            doc_id = f"doc_{i}"
            text = f"Document {i}"
            embedding = np.random.rand(384).astype(np.float32)
            self.cache_mgr.save_embedding(doc_id, text, embedding)
        
        stats = self.cache_mgr.get_cache_stats()
        
        self.assertEqual(stats['total_cached_documents'], 5)
        self.assertGreater(stats['database_size_bytes'], 0)
        print(f"✓ Cache stats: {stats}")
    
    def test_get_all_cached_embeddings(self):
        """Test retrieving all cache info"""
        # Add entries
        for i in range(3):
            doc_id = f"doc_{i}"
            text = f"Document {i}"
            embedding = np.random.rand(384).astype(np.float32)
            self.cache_mgr.save_embedding(doc_id, text, embedding)
        
        cache_info = self.cache_mgr.get_all_cached_embeddings()
        
        self.assertEqual(len(cache_info), 3)
        print(f"✓ Retrieved {len(cache_info)} cached entries")


def run_tests():
    """Run all tests with detailed output"""
    print("\n" + "█"*60)
    print("RUNNING UNIT TESTS")
    print("█"*60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestEmbedder))
    suite.addTests(loader.loadTestsFromTestCase(TestCacheManager))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "█"*60)
    print("TEST SUMMARY")
    print("█"*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED!")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
