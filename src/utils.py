"""
Utils Module
Contains utility functions for text preprocessing and document handling.
"""

import re
import os
from typing import List, Dict, Tuple
from pathlib import Path


def clean_text(text: str) -> str:
    """
    Clean and preprocess text.
    - Convert to lowercase
    - Remove HTML tags
    - Remove extra whitespace
    - Strip leading/trailing spaces
    
    Args:
        text (str): Raw text to clean
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove HTML tags
    text = remove_html_tags(text)
    
    # Remove extra whitespace (multiple spaces, tabs, newlines)
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def remove_html_tags(text: str) -> str:
    """
    Remove HTML tags from text.
    
    Args:
        text (str): Text potentially containing HTML
        
    Returns:
        str: Text with HTML tags removed
    """
    # Remove HTML tags
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def extract_keywords(text: str, min_length: int = 3) -> List[str]:
    """
    Extract keywords from text.
    Simple tokenization - splits by whitespace and punctuation.
    Filters out short words.
    
    Args:
        text (str): Input text
        min_length (int): Minimum word length to consider
        
    Returns:
        List[str]: List of keywords
    """
    # Split by non-alphanumeric characters
    words = re.findall(r'\b[a-z0-9]+\b', text.lower())
    
    # Filter by length
    keywords = [word for word in words if len(word) >= min_length]
    
    return keywords


def compute_overlap(query_keywords: List[str], doc_keywords: List[str]) -> Dict:
    """
    Compute overlap between query and document keywords.
    
    Args:
        query_keywords (List[str]): Keywords from query
        doc_keywords (List[str]): Keywords from document
        
    Returns:
        Dict: Overlap statistics
    """
    query_set = set(query_keywords)
    doc_set = set(doc_keywords)
    
    # Find intersection
    overlap = query_set.intersection(doc_set)
    
    # Compute ratio
    overlap_ratio = len(overlap) / len(query_set) if len(query_set) > 0 else 0.0
    
    return {
        "overlapping_keywords": sorted(list(overlap)),
        "overlap_count": len(overlap),
        "overlap_ratio": round(overlap_ratio, 3),
        "query_keyword_count": len(query_set),
        "doc_keyword_count": len(doc_set)
    }


def load_text_files(directory: str) -> List[Dict]:
    """
    Load all .txt files from a directory.
    
    Args:
        directory (str): Path to directory containing text files
        
    Returns:
        List[Dict]: List of documents with metadata
    """
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    documents = []
    
    # Find all .txt files
    txt_files = list(Path(directory).rglob("*.txt"))
    
    print(f"Found {len(txt_files)} text files in {directory}")
    
    for file_path in txt_files:
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Create document metadata
            doc = {
                "doc_id": file_path.stem,  # filename without extension
                "filepath": str(file_path),
                "filename": file_path.name,
                "raw_content": content,
                "content": clean_text(content),
                "length": len(content),
                "cleaned_length": len(clean_text(content))
            }
            
            documents.append(doc)
            
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue
    
    return documents


def get_text_preview(text: str, max_length: int = 150) -> str:
    """
    Get a preview of text (first N characters).
    
    Args:
        text (str): Full text
        max_length (int): Maximum preview length
        
    Returns:
        str: Preview text
    """
    if len(text) <= max_length:
        return text
    
    # Truncate and add ellipsis
    return text[:max_length] + "..."


def create_sample_documents(output_dir: str, num_docs: int = 10) -> None:
    """
    Create sample text documents for testing.
    Useful if you don't have a dataset yet.
    
    Args:
        output_dir (str): Directory to save sample documents
        num_docs (int): Number of sample documents to create
    """
    os.makedirs(output_dir, exist_ok=True)
    
    sample_texts = [
        "Machine learning is a subset of artificial intelligence that focuses on learning from data.",
        "Deep learning uses neural networks with multiple layers to learn hierarchical representations.",
        "Natural language processing enables computers to understand and generate human language.",
        "Computer vision allows machines to interpret and understand visual information from images.",
        "Reinforcement learning trains agents to make decisions through trial and error.",
        "Supervised learning uses labeled data to train predictive models.",
        "Unsupervised learning discovers patterns in data without labels.",
        "Transfer learning leverages pre-trained models for new tasks.",
        "Convolutional neural networks are specialized for processing grid-like data such as images.",
        "Recurrent neural networks are designed to handle sequential data like text and time series.",
        "Transformers have revolutionized natural language processing with attention mechanisms.",
        "Generative AI can create new content including text, images, and audio.",
        "Data preprocessing is crucial for building effective machine learning models.",
        "Feature engineering involves creating relevant features from raw data.",
        "Model evaluation metrics help assess the performance of machine learning algorithms.",
        "Overfitting occurs when a model learns noise in the training data.",
        "Regularization techniques help prevent overfitting in machine learning models.",
        "Cross-validation is used to assess model performance on unseen data.",
        "Ensemble methods combine multiple models to improve predictions.",
        "Hyperparameter tuning optimizes model configuration for better performance."
    ]
    
    for i in range(num_docs):
        filename = f"doc_{i+1:03d}.txt"
        filepath = os.path.join(output_dir, filename)
        
        # Use sample texts cyclically
        content = sample_texts[i % len(sample_texts)]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"Created {num_docs} sample documents in {output_dir}")


def validate_directory(directory: str) -> Tuple[bool, str]:
    """
    Validate if directory exists and contains text files.
    
    Args:
        directory (str): Path to directory
        
    Returns:
        Tuple[bool, str]: (is_valid, message)
    """
    if not os.path.exists(directory):
        return False, f"Directory does not exist: {directory}"
    
    if not os.path.isdir(directory):
        return False, f"Path is not a directory: {directory}"
    
    # Check for .txt files
    txt_files = list(Path(directory).rglob("*.txt"))
    
    if len(txt_files) == 0:
        return False, f"No .txt files found in directory: {directory}"
    
    return True, f"Directory valid with {len(txt_files)} text files"


# Example usage and testing
if __name__ == "__main__":
    # Test text cleaning
    dirty_text = "<html>  This   is   a   TEST  with   HTML   </html>"
    cleaned = clean_text(dirty_text)
    print(f"Cleaned text: {cleaned}")
    
    # Test keyword extraction
    text = "Machine learning and deep learning are subsets of artificial intelligence"
    keywords = extract_keywords(text)
    print(f"Keywords: {keywords}")
    
    # Test overlap computation
    query_kw = ["machine", "learning", "algorithms"]
    doc_kw = ["machine", "learning", "neural", "networks"]
    overlap = compute_overlap(query_kw, doc_kw)
    print(f"Overlap: {overlap}")
    
    # Test preview
    long_text = "This is a very long text that needs to be truncated for preview purposes."
    preview = get_text_preview(long_text, 30)
    print(f"Preview: {preview}")
