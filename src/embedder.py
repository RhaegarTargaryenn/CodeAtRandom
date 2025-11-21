"""
Embedder Module
Handles text embedding generation using sentence-transformers.
Uses all-MiniLM-L6-v2 model for efficient and quality embeddings.
"""

import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Union
import torch


class Embedder:
    """
    Embedder class for generating text embeddings.
    Uses sentence-transformers/all-MiniLM-L6-v2 model.
    Automatically detects and uses GPU if available.
    """
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the embedder with specified model.
        
        Args:
            model_name (str): Name of the sentence-transformers model
        """
        self.model_name = model_name
        self.model = None
        self.device = None
        self.load_model()
    
    def load_model(self) -> None:
        """
        Load the sentence-transformers model.
        Automatically uses GPU if available, otherwise CPU.
        """
        # Check if GPU is available
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"Loading model: {self.model_name}")
        print(f"Using device: {self.device}")
        
        # Load the model
        self.model = SentenceTransformer(self.model_name, device=self.device)
        
        print(f"Model loaded successfully on {self.device}")
    
    def embed_text(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text string.
        
        Args:
            text (str): Input text to embed
            
        Returns:
            np.ndarray: Embedding vector as numpy array
        """
        if not text or not isinstance(text, str):
            raise ValueError("Input text must be a non-empty string")
        
        # Lowercase the text as per requirements
        text = text.lower()
        
        # Generate embedding
        embedding = self.model.encode(text, convert_to_numpy=True)
        
        return embedding
    
    def embed_documents(self, texts: List[str], batch_size: int = 32, show_progress: bool = True) -> np.ndarray:
        """
        Generate embeddings for multiple documents.
        Uses batching for efficiency.
        
        Args:
            texts (List[str]): List of text documents to embed
            batch_size (int): Batch size for processing
            show_progress (bool): Whether to show progress bar
            
        Returns:
            np.ndarray: Array of embeddings, shape (num_docs, embedding_dim)
        """
        if not texts or not isinstance(texts, list):
            raise ValueError("Input must be a non-empty list of strings")
        
        # Lowercase all texts
        texts = [text.lower() for text in texts]
        
        # Generate embeddings with batching
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True
        )
        
        return embeddings
    
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of embeddings produced by this model.
        
        Returns:
            int: Embedding dimension
        """
        return self.model.get_sentence_embedding_dimension()
    
    def normalize_embeddings(self, embeddings: np.ndarray) -> np.ndarray:
        """
        Normalize embeddings to unit length (L2 normalization).
        Useful for cosine similarity and FAISS IndexFlatIP.
        
        Args:
            embeddings (np.ndarray): Input embeddings
            
        Returns:
            np.ndarray: Normalized embeddings
        """
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        # Avoid division by zero
        norms = np.where(norms == 0, 1, norms)
        return embeddings / norms


# Example usage and testing
if __name__ == "__main__":
    # Test the embedder
    embedder = Embedder()
    
    # Test single text embedding
    sample_text = "This is a test document about machine learning and AI."
    embedding = embedder.embed_text(sample_text)
    print(f"\nSingle text embedding shape: {embedding.shape}")
    print(f"Embedding dimension: {embedder.get_embedding_dimension()}")
    
    # Test multiple documents
    sample_texts = [
        "Machine learning is a subset of artificial intelligence.",
        "Deep learning uses neural networks with multiple layers.",
        "Natural language processing helps computers understand text."
    ]
    embeddings = embedder.embed_documents(sample_texts, show_progress=False)
    print(f"\nMultiple documents embedding shape: {embeddings.shape}")
    
    # Test normalization
    normalized = embedder.normalize_embeddings(embeddings)
    print(f"Normalized embeddings shape: {normalized.shape}")
    print(f"Sample normalized embedding norm: {np.linalg.norm(normalized[0]):.4f}")
