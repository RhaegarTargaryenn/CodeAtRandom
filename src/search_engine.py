"""
Search Engine Module
Implements the main search engine with document loading, embedding generation,
caching, and vector search using both FAISS and cosine similarity.
"""

import numpy as np
from typing import List, Dict, Optional, Tuple
import os
from pathlib import Path

# Import our modules
from src.embedder import Embedder
from src.cache_manager import CacheManager
from src.utils import load_text_files, extract_keywords, compute_overlap, get_text_preview

# FAISS for vector search
try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    print("Warning: FAISS not available. Will use cosine similarity instead.")


class SearchEngine:
    """
    Main search engine class that handles document loading,
    embedding generation with caching, and vector-based search.
    """
    
    def __init__(
        self, 
        data_dir: str = "data",
        cache_db_path: str = "cache/embeddings_cache.db",
        use_faiss: bool = True
    ):
        """
        Initialize the search engine.
        
        Args:
            data_dir (str): Directory containing text documents
            cache_db_path (str): Path to cache database
            use_faiss (bool): Whether to use FAISS (if available) or cosine similarity
        """
        self.data_dir = data_dir
        self.use_faiss = use_faiss and FAISS_AVAILABLE
        
        # Initialize components
        print("Initializing Embedder...")
        self.embedder = Embedder()
        
        print("Initializing Cache Manager...")
        self.cache_manager = CacheManager(cache_db_path)
        
        # Storage for documents and embeddings
        self.documents: List[Dict] = []
        self.embeddings: Optional[np.ndarray] = None
        self.doc_id_to_idx: Dict[str, int] = {}
        
        # FAISS index
        self.faiss_index = None
        
        print("Search Engine initialized")
    
    def load_documents(self) -> int:
        """
        Load all documents from data directory.
        Processes text and prepares for embedding.
        
        Returns:
            int: Number of documents loaded
        """
        print(f"\nLoading documents from {self.data_dir}...")
        
        # Load text files
        self.documents = load_text_files(self.data_dir)
        
        if len(self.documents) == 0:
            print(f"Warning: No documents found in {self.data_dir}")
            print("You can create sample documents using utils.create_sample_documents()")
            return 0
        
        # Create doc_id to index mapping
        self.doc_id_to_idx = {
            doc["doc_id"]: idx for idx, doc in enumerate(self.documents)
        }
        
        print(f"Loaded {len(self.documents)} documents")
        return len(self.documents)
    
    def generate_embeddings(self, force_regenerate: bool = False) -> None:
        """
        Generate embeddings for all documents.
        Uses cache when possible to avoid recomputation.
        
        Args:
            force_regenerate (bool): Force regeneration even if cached
        """
        if len(self.documents) == 0:
            raise ValueError("No documents loaded. Call load_documents() first.")
        
        print("\nGenerating embeddings...")
        
        embeddings_list = []
        cache_hits = 0
        cache_misses = 0
        
        embedding_dim = self.embedder.get_embedding_dimension()
        
        for idx, doc in enumerate(self.documents):
            doc_id = doc["doc_id"]
            content = doc["content"]
            
            # Check cache
            if not force_regenerate:
                cached_embedding = self.cache_manager.check_cache(doc_id, content, embedding_dim)
                
                if cached_embedding is not None:
                    embeddings_list.append(cached_embedding)
                    cache_hits += 1
                    
                    if (idx + 1) % 50 == 0:
                        print(f"Processed {idx + 1}/{len(self.documents)} documents (cached)")
                    continue
            
            # Generate new embedding
            embedding = self.embedder.embed_text(content)
            embeddings_list.append(embedding)
            
            # Save to cache
            self.cache_manager.save_embedding(doc_id, content, embedding)
            cache_misses += 1
            
            if (idx + 1) % 50 == 0:
                print(f"Processed {idx + 1}/{len(self.documents)} documents (generated)")
        
        # Convert to numpy array
        self.embeddings = np.array(embeddings_list)
        
        print(f"\nEmbedding generation complete:")
        print(f"  - Total documents: {len(self.documents)}")
        print(f"  - Cache hits: {cache_hits}")
        print(f"  - Cache misses (newly generated): {cache_misses}")
        print(f"  - Embeddings shape: {self.embeddings.shape}")
    
    def build_vector_index(self) -> None:
        """
        Build vector search index.
        Uses FAISS if available, otherwise prepares for cosine similarity.
        """
        if self.embeddings is None:
            raise ValueError("No embeddings available. Call generate_embeddings() first.")
        
        print("\nBuilding vector search index...")
        
        if self.use_faiss:
            self._build_faiss_index()
        else:
            self._prepare_cosine_similarity()
        
        print("Vector index built successfully")
    
    def _build_faiss_index(self) -> None:
        """
        Build FAISS index for fast similarity search.
        Uses IndexFlatIP (Inner Product) with normalized embeddings.
        """
        print("Using FAISS IndexFlatIP...")
        
        # Normalize embeddings for cosine similarity with inner product
        embeddings_normalized = self.embedder.normalize_embeddings(self.embeddings)
        
        # Create FAISS index
        dimension = embeddings_normalized.shape[1]
        self.faiss_index = faiss.IndexFlatIP(dimension)
        
        # Add embeddings to index
        self.faiss_index.add(embeddings_normalized.astype('float32'))
        
        print(f"FAISS index created with {self.faiss_index.ntotal} vectors")
    
    def _prepare_cosine_similarity(self) -> None:
        """
        Prepare embeddings for cosine similarity search.
        Normalizes embeddings for efficient computation.
        """
        print("Using cosine similarity...")
        
        # Normalize embeddings
        self.embeddings = self.embedder.normalize_embeddings(self.embeddings)
        
        print("Embeddings normalized for cosine similarity")
    
    def search(
        self, 
        query: str, 
        top_k: int = 5,
        return_scores: bool = True
    ) -> List[Dict]:
        """
        Search for documents similar to query.
        
        Args:
            query (str): Search query text
            top_k (int): Number of top results to return
            return_scores (bool): Whether to include similarity scores
            
        Returns:
            List[Dict]: List of search results with metadata
        """
        if self.embeddings is None:
            raise ValueError("Search index not built. Call build_vector_index() first.")
        
        # Generate query embedding
        query_embedding = self.embedder.embed_text(query)
        query_embedding = self.embedder.normalize_embeddings(
            query_embedding.reshape(1, -1)
        )[0]
        
        # Perform search
        if self.use_faiss:
            scores, indices = self._search_faiss(query_embedding, top_k)
        else:
            scores, indices = self._search_cosine(query_embedding, top_k)
        
        # Build results with explanations
        results = []
        query_keywords = extract_keywords(query)
        
        for rank, (idx, score) in enumerate(zip(indices, scores)):
            doc = self.documents[idx]
            doc_keywords = extract_keywords(doc["content"])
            
            # Compute overlap explanation
            overlap_info = compute_overlap(query_keywords, doc_keywords)
            
            result = {
                "rank": rank + 1,
                "doc_id": doc["doc_id"],
                "filename": doc["filename"],
                "score": float(score),
                "preview": get_text_preview(doc["content"], 150),
                "doc_length": doc["cleaned_length"],
                "keywords_overlap": overlap_info["overlapping_keywords"],
                "overlap_count": overlap_info["overlap_count"],
                "overlap_ratio": overlap_info["overlap_ratio"],
                "explanation": self._generate_explanation(score, overlap_info, doc)
            }
            
            results.append(result)
        
        return results
    
    def _search_faiss(
        self, 
        query_embedding: np.ndarray, 
        top_k: int
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Search using FAISS index.
        
        Args:
            query_embedding (np.ndarray): Query embedding vector
            top_k (int): Number of results
            
        Returns:
            Tuple[np.ndarray, np.ndarray]: (scores, indices)
        """
        # Reshape for FAISS
        query_vector = query_embedding.reshape(1, -1).astype('float32')
        
        # Search
        scores, indices = self.faiss_index.search(query_vector, top_k)
        
        return scores[0], indices[0]
    
    def _search_cosine(
        self, 
        query_embedding: np.ndarray, 
        top_k: int
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Search using cosine similarity (dot product of normalized vectors).
        
        Args:
            query_embedding (np.ndarray): Query embedding vector
            top_k (int): Number of results
            
        Returns:
            Tuple[np.ndarray, np.ndarray]: (scores, indices)
        """
        # Compute similarity scores (dot product)
        scores = np.dot(self.embeddings, query_embedding)
        
        # Get top-k indices
        top_indices = np.argsort(scores)[::-1][:top_k]
        top_scores = scores[top_indices]
        
        return top_scores, top_indices
    
    def _generate_explanation(
        self, 
        score: float, 
        overlap_info: Dict, 
        doc: Dict
    ) -> str:
        """
        Generate human-readable explanation for why document was matched.
        
        Args:
            score (float): Similarity score
            overlap_info (Dict): Keyword overlap information
            doc (Dict): Document metadata
            
        Returns:
            str: Explanation text
        """
        explanation_parts = []
        
        # Similarity score explanation
        if score > 0.7:
            explanation_parts.append(f"High semantic similarity (score: {score:.3f})")
        elif score > 0.5:
            explanation_parts.append(f"Moderate semantic similarity (score: {score:.3f})")
        else:
            explanation_parts.append(f"Low semantic similarity (score: {score:.3f})")
        
        # Keyword overlap explanation
        overlap_count = overlap_info["overlap_count"]
        overlap_ratio = overlap_info["overlap_ratio"]
        
        if overlap_count > 0:
            keywords_str = ", ".join(overlap_info["overlapping_keywords"][:5])
            explanation_parts.append(
                f"{overlap_count} matching keywords ({overlap_ratio:.1%}): {keywords_str}"
            )
        else:
            explanation_parts.append("No exact keyword matches (semantic match only)")
        
        # Document length context
        doc_length = doc["cleaned_length"]
        if doc_length < 100:
            explanation_parts.append("short document")
        elif doc_length > 500:
            explanation_parts.append("long document")
        
        return " | ".join(explanation_parts)
    
    def get_stats(self) -> Dict:
        """
        Get search engine statistics.
        
        Returns:
            Dict: Statistics about the search engine
        """
        stats = {
            "total_documents": len(self.documents),
            "embeddings_generated": self.embeddings is not None,
            "embedding_dimension": self.embedder.get_embedding_dimension(),
            "search_method": "FAISS" if self.use_faiss else "Cosine Similarity",
            "cache_stats": self.cache_manager.get_cache_stats()
        }
        
        if self.embeddings is not None:
            stats["embeddings_shape"] = self.embeddings.shape
        
        return stats


# Example usage and testing
if __name__ == "__main__":
    # Initialize search engine
    engine = SearchEngine(data_dir="data", use_faiss=True)
    
    # Load documents
    num_docs = engine.load_documents()
    
    if num_docs > 0:
        # Generate embeddings
        engine.generate_embeddings()
        
        # Build index
        engine.build_vector_index()
        
        # Test search
        results = engine.search("machine learning algorithms", top_k=3)
        
        print("\nSearch Results:")
        for result in results:
            print(f"\n{result['rank']}. {result['filename']} (score: {result['score']:.3f})")
            print(f"   {result['preview']}")
            print(f"   {result['explanation']}")
        
        # Show stats
        print("\n" + "="*60)
        stats = engine.get_stats()
        print("Search Engine Stats:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
