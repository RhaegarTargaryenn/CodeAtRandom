"""
Download 20 Newsgroups Dataset
Run this script to download real text data for the search engine.
"""

from sklearn.datasets import fetch_20newsgroups
import os
from pathlib import Path


def download_newsgroups_dataset(output_dir: str = "data", max_docs: int = 200):
    """
    Download and save 20 Newsgroups dataset.
    
    Args:
        output_dir (str): Directory to save text files
        max_docs (int): Maximum number of documents to download
    """
    print("Downloading 20 Newsgroups dataset...")
    print("This may take a minute on first run...")
    
    # Fetch dataset (train subset)
    dataset = fetch_20newsgroups(
        subset='train',
        remove=('headers', 'footers', 'quotes'),
        shuffle=True,
        random_state=42
    )
    
    print(f"Downloaded {len(dataset.data)} documents")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Save documents
    saved_count = 0
    for idx, (text, label) in enumerate(zip(dataset.data[:max_docs], dataset.target[:max_docs])):
        # Skip very short documents
        if len(text.strip()) < 50:
            continue
        
        filename = f"newsgroup_{idx:04d}_cat{label}.txt"
        filepath = os.path.join(output_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(text)
            saved_count += 1
        except Exception as e:
            print(f"Error saving {filename}: {e}")
    
    print(f"\n✓ Successfully saved {saved_count} documents to {output_dir}/")
    print(f"  Category labels: {set(dataset.target[:max_docs])}")
    print(f"  Categories: {len(set(dataset.target[:max_docs]))}")
    
    # Show some category names
    print("\nSample categories:")
    for i in range(min(5, len(dataset.target_names))):
        print(f"  {i}: {dataset.target_names[i]}")
    
    print(f"\nYou can now run: python main.py")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Download 20 Newsgroups dataset")
    parser.add_argument(
        "--output-dir",
        type=str,
        default="data",
        help="Output directory for text files"
    )
    parser.add_argument(
        "--max-docs",
        type=int,
        default=200,
        help="Maximum number of documents to download"
    )
    
    args = parser.parse_args()
    
    download_newsgroups_dataset(args.output_dir, args.max_docs)
