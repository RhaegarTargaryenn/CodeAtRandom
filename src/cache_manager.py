"""
Cache Manager Module
Handles caching of document embeddings using SQLite database.
Implements hash-based cache invalidation to avoid recomputing embeddings.
"""

import sqlite3
import hashlib
import json
import numpy as np
from typing import Optional, Dict, List, Tuple
from datetime import datetime
import os


class CacheManager:
    """
    Manages caching of document embeddings using SQLite.
    Uses document hash to detect changes and invalidate cache.
    """
    
    def __init__(self, cache_db_path: str = "cache/embeddings_cache.db"):
        """
        Initialize the cache manager.
        
        Args:
            cache_db_path (str): Path to SQLite database file
        """
        self.cache_db_path = cache_db_path
        
        # Create cache directory if it doesn't exist
        os.makedirs(os.path.dirname(cache_db_path), exist_ok=True)
        
        # Initialize database
        self._init_database()
        
        print(f"Cache manager initialized with database: {cache_db_path}")
    
    def _init_database(self) -> None:
        """
        Initialize SQLite database with required schema.
        Creates table if it doesn't exist.
        """
        conn = sqlite3.connect(self.cache_db_path)
        cursor = conn.cursor()
        
        # Create embeddings cache table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS embeddings_cache (
                doc_id TEXT PRIMARY KEY,
                embedding BLOB NOT NULL,
                hash TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
        
        print("Database schema initialized")
    
    def compute_hash(self, text: str) -> str:
        """
        Compute SHA256 hash of text content.
        Used to detect if document has changed.
        
        Args:
            text (str): Text content to hash
            
        Returns:
            str: SHA256 hash as hexadecimal string
        """
        return hashlib.sha256(text.encode('utf-8')).hexdigest()
    
    def save_embedding(self, doc_id: str, text: str, embedding: np.ndarray) -> None:
        """
        Save or update embedding in cache.
        
        Args:
            doc_id (str): Unique document identifier
            text (str): Document text content
            embedding (np.ndarray): Embedding vector
        """
        # Compute hash
        text_hash = self.compute_hash(text)
        
        # Convert embedding to bytes for storage
        embedding_bytes = embedding.tobytes()
        
        # Current timestamp
        timestamp = datetime.now().isoformat()
        
        conn = sqlite3.connect(self.cache_db_path)
        cursor = conn.cursor()
        
        # Insert or replace
        cursor.execute("""
            INSERT OR REPLACE INTO embeddings_cache (doc_id, embedding, hash, updated_at)
            VALUES (?, ?, ?, ?)
        """, (doc_id, embedding_bytes, text_hash, timestamp))
        
        conn.commit()
        conn.close()
    
    def check_cache(self, doc_id: str, text: str, embedding_dim: int) -> Optional[np.ndarray]:
        """
        Check if valid cached embedding exists for document.
        Returns embedding if hash matches, None otherwise.
        
        Args:
            doc_id (str): Unique document identifier
            text (str): Current document text content
            embedding_dim (int): Expected embedding dimension
            
        Returns:
            Optional[np.ndarray]: Cached embedding if valid, None otherwise
        """
        # Compute current hash
        current_hash = self.compute_hash(text)
        
        conn = sqlite3.connect(self.cache_db_path)
        cursor = conn.cursor()
        
        # Query cache
        cursor.execute("""
            SELECT embedding, hash FROM embeddings_cache WHERE doc_id = ?
        """, (doc_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        # If no cache entry exists
        if result is None:
            return None
        
        embedding_bytes, cached_hash = result
        
        # If hash doesn't match, cache is invalid
        if cached_hash != current_hash:
            return None
        
        # Convert bytes back to numpy array
        embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
        
        # Reshape if needed (flatten embeddings are stored as 1D)
        if len(embedding) != embedding_dim:
            return None
        
        return embedding
    
    def get_all_cached_embeddings(self) -> Dict[str, Dict]:
        """
        Retrieve all cached embeddings.
        
        Returns:
            Dict[str, Dict]: Dictionary mapping doc_id to cache info
        """
        conn = sqlite3.connect(self.cache_db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT doc_id, hash, updated_at FROM embeddings_cache
        """)
        
        results = cursor.fetchall()
        conn.close()
        
        cache_info = {}
        for doc_id, hash_val, updated_at in results:
            cache_info[doc_id] = {
                "hash": hash_val,
                "updated_at": updated_at
            }
        
        return cache_info
    
    def delete_cache_entry(self, doc_id: str) -> None:
        """
        Delete a specific cache entry.
        
        Args:
            doc_id (str): Document identifier to delete
        """
        conn = sqlite3.connect(self.cache_db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM embeddings_cache WHERE doc_id = ?", (doc_id,))
        
        conn.commit()
        conn.close()
    
    def clear_cache(self) -> None:
        """
        Clear all cached embeddings.
        """
        conn = sqlite3.connect(self.cache_db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM embeddings_cache")
        
        conn.commit()
        conn.close()
        
        print("Cache cleared")
    
    def get_cache_stats(self) -> Dict[str, int]:
        """
        Get statistics about the cache.
        
        Returns:
            Dict[str, int]: Cache statistics
        """
        conn = sqlite3.connect(self.cache_db_path)
        cursor = conn.cursor()
        
        # Count total entries
        cursor.execute("SELECT COUNT(*) FROM embeddings_cache")
        total_entries = cursor.fetchone()[0]
        
        # Get database file size
        db_size = os.path.getsize(self.cache_db_path) if os.path.exists(self.cache_db_path) else 0
        
        conn.close()
        
        return {
            "total_cached_documents": total_entries,
            "database_size_bytes": db_size,
            "database_size_mb": round(db_size / (1024 * 1024), 2)
        }
    
    def load_cache(self) -> Dict[str, Tuple[np.ndarray, str]]:
        """
        Load all cached embeddings into memory.
        
        Returns:
            Dict[str, Tuple[np.ndarray, str]]: Map of doc_id to (embedding, hash)
        """
        conn = sqlite3.connect(self.cache_db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT doc_id, embedding, hash FROM embeddings_cache")
        results = cursor.fetchall()
        
        conn.close()
        
        cache_data = {}
        for doc_id, embedding_bytes, hash_val in results:
            embedding = np.frombuffer(embedding_bytes, dtype=np.float32)
            cache_data[doc_id] = (embedding, hash_val)
        
        return cache_data


# Example usage and testing
if __name__ == "__main__":
    # Test cache manager
    cache_mgr = CacheManager("cache/test_cache.db")
    
    # Test hash computation
    text1 = "This is a test document"
    hash1 = cache_mgr.compute_hash(text1)
    print(f"Hash: {hash1}")
    
    # Test saving embedding
    test_embedding = np.random.rand(384).astype(np.float32)
    cache_mgr.save_embedding("doc_001", text1, test_embedding)
    print("Embedding saved")
    
    # Test cache check (should return embedding)
    cached = cache_mgr.check_cache("doc_001", text1, 384)
    print(f"Cache hit: {cached is not None}")
    
    # Test cache check with modified text (should return None)
    text2 = "This is a modified document"
    cached = cache_mgr.check_cache("doc_001", text2, 384)
    print(f"Cache miss (modified text): {cached is None}")
    
    # Test cache stats
    stats = cache_mgr.get_cache_stats()
    print(f"Cache stats: {stats}")
