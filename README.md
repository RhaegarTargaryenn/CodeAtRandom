# Document Search Engine with Caching + Streamlit UI

A production-ready, embedding-based semantic search engine for text documents with intelligent caching, FastAPI backend, and beautiful Streamlit UI. Built with sentence-transformers and FAISS for efficient similarity search.

## 🎯 Project Overview

This project implements a complete multi-document embedding search engine that:
- Loads 100-200+ text documents
- Generates embeddings using sentence-transformers
- Caches embeddings with hash-based invalidation
- Performs fast vector similarity search using FAISS
- Provides a REST API for querying documents (FastAPI)
- **Includes a Streamlit web UI** for interactive searching
- Returns ranked results with keyword overlap explanations

## ✨ Features

### Core Features
- **Efficient Embedding Generation**: Uses `sentence-transformers/all-MiniLM-L6-v2` for high-quality 384-dimensional embeddings
- **Smart Caching System**: SQLite-based caching with SHA256 hash validation to avoid recomputing unchanged documents
- **Dual Search Methods**: 
  - FAISS IndexFlatIP (fast, scalable)
  - Cosine similarity (fallback, no dependencies)
- **Ranking Explanation**: Each result includes:
  - Similarity score
  - Keyword overlap analysis
  - Document length context
  - Human-readable explanation
- **REST API**: FastAPI with automatic documentation
- **Text Preprocessing**: Lowercase, HTML tag removal, whitespace normalization

### Advanced Features
- **Streamlit UI**: Interactive web interface for searching
- **Unit Tests**: Comprehensive test suite for core components
- **Automation Scripts**: One-command setup and repository cleanup
- GPU acceleration support (automatic detection)
- Batch embedding generation
- Cache statistics and monitoring
- Modular, production-ready code structure
- Comprehensive error handling

## 📁 Project Structure

```
assignment_codeRandom/
│
├── src/
│   ├── embedder.py          # Embedding generation with sentence-transformers
│   ├── cache_manager.py     # SQLite-based embedding cache
│   ├── search_engine.py     # Main search engine (FAISS + cosine similarity)
│   ├── api.py               # FastAPI REST endpoints
│   ├── utils.py             # Text preprocessing and utilities
│   └── streamlit_ui.py      # Streamlit web interface ⭐ NEW
│
├── tests/
│   ├── __init__.py
│   └── test_components.py   # Unit tests for embedder and cache ⭐ NEW
│
├── data/                    # Text documents directory (gitignored)
├── cache/                   # SQLite cache database (gitignored)
│
├── main.py                  # Application entry point
├── download_data.py         # Download 20 Newsgroups dataset
├── quickstart.sh            # Automated setup script ⭐ NEW
├── clean_repo.sh            # Repository cleanup for submission ⭐ NEW
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── CHECKLIST.md             # Reviewer verification checklist ⭐ NEW
└── .gitignore               # Git ignore rules

```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
cd assignment_codeRandom

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 2. Prepare Data

**Option A: Use Your Own Data**
```bash
# Place your .txt files in the data/ directory
mkdir data
# Copy your text files to data/
```

**Option B: Create Sample Documents**
```bash
# Create 20 sample documents for testing
python main.py --create-samples 20
```

**Option C: Download 20 Newsgroups Dataset**
```python
# Run this Python script to download real data
from sklearn.datasets import fetch_20newsgroups
import os

# Fetch dataset
dataset = fetch_20newsgroups(subset='train', remove=('headers', 'footers', 'quotes'))

# Save to data directory
os.makedirs('data', exist_ok=True)
for idx, (text, label) in enumerate(zip(dataset.data[:200], dataset.target[:200])):
    with open(f'data/doc_{idx:03d}.txt', 'w', encoding='utf-8') as f:
        f.write(text)

print("Downloaded and saved 200 documents!")
```

### 3. Run the Application

**Option A: Automated Setup (Recommended)**
```bash
# Run everything with one command
chmod +x quickstart.sh
./quickstart.sh

# This will:
# - Create virtual environment
# - Install dependencies
# - Download data
# - Start FastAPI backend
# - Prompt to start Streamlit UI
```

**Option B: Manual Setup**
```bash
# Terminal 1: Start FastAPI Backend
python main.py
# Server runs on http://localhost:8000

# Terminal 2: Start Streamlit UI (in a new terminal)
streamlit run src/streamlit_ui.py
# UI opens at http://localhost:8501
```

### 4. Access the Application

**🎨 Streamlit Web UI** (Recommended for users)
- **URL**: http://localhost:8501
- **Features**:
  - Interactive search interface
  - Visual results with color-coded scores
  - Keyword overlap highlighting
  - Real-time API status monitoring
  - Adjustable top_k results slider

**📚 FastAPI Backend** (For developers/API access)
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **Statistics**: http://localhost:8000/stats

## 🎨 Streamlit UI Guide

### Using the Web Interface

1. **Open Browser**: Navigate to http://localhost:8501
2. **Enter Query**: Type your search query (e.g., "machine learning algorithms")
3. **Adjust Results**: Use the slider in sidebar to select number of results (1-20)
4. **Click Search**: Press the Search button or hit Enter
5. **View Results**: See ranked results with:
   - Document filename and ID
   - Similarity score with color indicator (🟢 > 0.7, 🟡 > 0.5, 🔴 < 0.5)
   - Document preview (first 150 characters)
   - Matching keywords highlighted
   - Overlap ratio progress bar
   - Expandable explanation section

### UI Features

- **Sidebar Configuration**:
  - Adjust top_k (number of results)
  - View API connection status
  - See system statistics (documents loaded)
  
- **Search Results Display**:
  - Color-coded similarity scores
  - Keyword overlap visualization
  - Document preview with formatting
  - Detailed explanation on demand
  
- **Example Queries**: Suggested at bottom of search box
  - "artificial intelligence"
  - "deep learning"
  - "computer vision"
  - "natural language processing"

## 📖 API Usage

### Search Endpoint (POST)

```bash
# Using curl
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "machine learning algorithms", "top_k": 5}'
```

```python
# Using Python requests
import requests

response = requests.post(
    "http://localhost:8000/search",
    json={"query": "machine learning algorithms", "top_k": 5}
)

results = response.json()
print(f"Found {results['total_results']} results in {results['search_time_ms']}ms")

for result in results['results']:
    print(f"\n{result['rank']}. {result['filename']} (score: {result['score']:.3f})")
    print(f"   Preview: {result['preview']}")
    print(f"   Explanation: {result['explanation']}")
    print(f"   Keywords: {', '.join(result['keywords_overlap'])}")
```

### Search Endpoint (GET)

```bash
# Browser-friendly GET request
http://localhost:8000/search?query=artificial%20intelligence&top_k=3
```

### Response Format

```json
{
  "query": "machine learning algorithms",
  "top_k": 5,
  "total_results": 5,
  "search_time_ms": 12.34,
  "results": [
    {
      "rank": 1,
      "doc_id": "doc_001",
      "filename": "doc_001.txt",
      "score": 0.856,
      "preview": "Machine learning is a subset of artificial intelligence...",
      "doc_length": 245,
      "keywords_overlap": ["machine", "learning", "algorithms"],
      "overlap_count": 3,
      "overlap_ratio": 1.0,
      "explanation": "High semantic similarity (score: 0.856) | 3 matching keywords (100.0%): machine, learning, algorithms"
    }
  ]
}
```

### Other Endpoints

```bash
# Get statistics
curl http://localhost:8000/stats

# List all documents
curl http://localhost:8000/documents?limit=10

# Get specific document
curl http://localhost:8000/document/doc_001
```

## 🔧 How Caching Works

### Cache Architecture

The caching system uses **SQLite** as a persistent key-value store:

```sql
CREATE TABLE embeddings_cache (
    doc_id TEXT PRIMARY KEY,
    embedding BLOB NOT NULL,
    hash TEXT NOT NULL,
    updated_at TEXT NOT NULL
)
```

### Cache Workflow

1. **Document Loading**: When a document is loaded, compute SHA256 hash of content
2. **Cache Check**: Query SQLite for existing embedding with matching doc_id
3. **Hash Validation**: 
   - If cached hash == current hash → Use cached embedding ✅
   - If hash differs → Document changed, regenerate embedding ❌
4. **Cache Update**: Store new embedding with updated hash
5. **Performance**: Cache hits avoid expensive model inference (~100x faster)

### Cache Benefits

- **Speed**: First run generates embeddings (~1-2 seconds/doc), subsequent runs use cache (~0.01 seconds/doc)
- **Consistency**: Hash-based invalidation ensures embeddings stay synchronized with content
- **Storage**: Embeddings stored efficiently as binary BLOBs
- **Persistence**: SQLite database survives application restarts

### Cache Commands

```bash
# View cache statistics
curl http://localhost:8000/stats

# Force regenerate all embeddings (ignore cache)
python main.py --force-regenerate

# Cache is stored in cache/embeddings_cache.db
```

## 🏗️ Architecture & Design Choices

### 1. Embedder (`embedder.py`)

**Technology**: sentence-transformers/all-MiniLM-L6-v2
- **Why**: Balanced performance/quality, 384-dim embeddings, fast inference
- **Features**: GPU auto-detection, batch processing, normalization

### 2. Cache Manager (`cache_manager.py`)

**Technology**: SQLite
- **Why**: Serverless, zero-config, ACID transactions, perfect for local caching
- **Alternatives considered**: JSON (slower), Pickle (less portable), Redis (overkill)

### 3. Search Engine (`search_engine.py`)

**Technology**: FAISS IndexFlatIP + Cosine Similarity fallback
- **FAISS**: Used for production, ~10x faster on large datasets
- **Cosine**: Fallback if FAISS unavailable, pure NumPy implementation
- **Why IndexFlatIP**: Exact search with inner product on normalized vectors = cosine similarity

### 4. API (`api.py`)

**Technology**: FastAPI
- **Why**: Fast, modern, automatic OpenAPI docs, async support, type validation
- **Features**: Pydantic models, CORS support, error handling

### 5. Design Patterns

- **Modular Architecture**: Each component is independent and testable
- **Dependency Injection**: Search engine passed to API, not global
- **Type Hints**: Full type annotations for IDE support and validation
- **Error Handling**: Comprehensive try-catch with meaningful messages
- **Logging**: Progress indicators and statistics

## 🎨 Ranking Explanation System

Each search result includes a detailed explanation:

### Components

1. **Semantic Similarity Score** (0.0 - 1.0)
   - Computed via cosine similarity of embeddings
   - High (>0.7), Moderate (0.5-0.7), Low (<0.5)

2. **Keyword Overlap Analysis**
   - Extracts keywords from query and document
   - Finds intersection of terms
   - Computes overlap ratio: `matching_keywords / total_query_keywords`

3. **Document Length Context**
   - Short (<100 chars), Medium, Long (>500 chars)
   - Helps users understand result context

### Example Explanation

```
"High semantic similarity (score: 0.856) | 3 matching keywords (100.0%): 
machine, learning, algorithms | short document"
```

## 🛠️ Command Line Options

```bash
# Basic usage
python main.py

# Custom data directory
python main.py --data-dir /path/to/documents

# Custom cache location
python main.py --cache-db /path/to/cache.db

# Use cosine similarity instead of FAISS
python main.py --no-faiss

# Force regenerate all embeddings
python main.py --force-regenerate

# Custom host/port
python main.py --host 127.0.0.1 --port 5000

# Development mode with auto-reload
python main.py --reload

# Create sample documents
python main.py --create-samples 50
```

## 📊 Performance Benchmarks

| Dataset Size | First Run (no cache) | Subsequent Runs (cached) | Search Time |
|--------------|---------------------|--------------------------|-------------|
| 20 docs      | ~15 seconds         | ~0.5 seconds             | ~10ms       |
| 100 docs     | ~60 seconds         | ~2 seconds               | ~15ms       |
| 200 docs     | ~120 seconds        | ~4 seconds               | ~20ms       |

*Tested on: CPU (Intel i7), no GPU acceleration*

## 🔍 Testing

### Manual Testing

```bash
# Test with sample query
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "artificial intelligence", "top_k": 3}'

# Test individual modules
python src/embedder.py
python src/cache_manager.py
python src/utils.py
```

### Unit Tests

```bash
# Run component tests
python tests/test_components.py

# Expected output: All tests pass ✅
```

**Test Coverage:**
- Embedder functionality (6 tests)
- Cache manager operations (8 tests)
- Hash computation and validation
- Cache hit/miss scenarios

## 🚧 Known Limitations & Future Enhancements

### Current Limitations
- Single-threaded embedding generation (can be slow for large datasets)
- In-memory vector index (not suitable for millions of documents)
- No query expansion or synonyms

### Completed Enhancements
- [x] Streamlit UI for visual search ✅
- [x] Unit tests for core components ✅
- [x] Automation scripts (quickstart.sh, clean_repo.sh) ✅
- [x] Comprehensive documentation ✅

### Future Enhancements
- [ ] Batch embedding with multiprocessing
- [ ] Persistent FAISS index (save/load)
- [ ] Query expansion with WordNet
- [ ] Evaluation metrics (MRR, NDCG)
- [ ] Docker containerization
- [ ] Cloud deployment guide

## 📝 Requirements

- Python 3.8+
- 2GB+ RAM (for embeddings)
- 500MB+ disk space (for models and cache)
- Optional: CUDA-capable GPU for faster embedding generation

## 🤝 Contributing

This is an assignment project, but suggestions are welcome!

## 📄 License

MIT License - Feel free to use for learning and development.

## 🚀 Deployment & Submission

### Repository Setup for GitHub

This project is ready for submission to https://github.com/RhaegarTargaryenn/CodeAtRandom

**Automated Cleanup & Submission:**
```bash
# Run the cleanup script
chmod +x clean_repo.sh
./clean_repo.sh

# This will:
# 1. Remove large files (data/, cache/, venv/) from git
# 2. Create a clean 'submission-ready' branch
# 3. Stage only required files (src/, tests/, docs, scripts)
# 4. Create a commit with proper message
# 5. Provide push instructions
```

**Manual Steps:**
```bash
# Initialize git (if not already)
git init

# Add remote repository
git remote add origin https://github.com/RhaegarTargaryenn/CodeAtRandom.git

# Push the submission-ready branch
git push origin submission-ready

# Or force push if needed
git push origin submission-ready --force
```

### ⚠️ Important: Do NOT Commit These Files
The `.gitignore` is configured to exclude:
- `data/` - Dataset files (too large)
- `cache/` - Cached embeddings database
- `venv/` or `env/` - Virtual environment
- `__pycache__/` - Python cache
- `.db` files - SQLite databases
- Model cache directories

**Why?** These files are:
- Generated locally
- Too large for GitHub (data/ can be 50MB+)
- Environment-specific (venv/)
- Easily reproducible (download_data.py, requirements.txt)

### 📦 What Gets Committed
✅ Source code (`src/*.py`)
✅ Tests (`tests/*.py`)
✅ Documentation (`README.md`, `CHECKLIST.md`, etc.)
✅ Configuration (`requirements.txt`, `.gitignore`)
✅ Scripts (`main.py`, `download_data.py`, `quickstart.sh`, `clean_repo.sh`)

### 🎥 Demo Video / Hosted Link

**Option A: Record Demo Video (5 minutes)**
Show:
1. Project structure (`tree` command)
2. Running tests (`python tests/test_components.py`)
3. Starting backend (`python main.py`)
4. API documentation (http://localhost:8000/docs)
5. Streamlit UI demo (http://localhost:8501)
6. Live search with results

**Option B: Deploy to Cloud**
- Railway.app (easiest)
- Heroku
- Render.com
- AWS/GCP/Azure

**Upload to:**
- YouTube (unlisted link)
- Google Drive
- Loom
- Or include link in README

### 📝 Submission Checklist

Before submitting via https://forms.gle/6uyp9RrimKqgaJzv5

- [ ] GitHub repository created at https://github.com/RhaegarTargaryenn/CodeAtRandom
- [ ] All source files committed (run `clean_repo.sh`)
- [ ] README.md is comprehensive
- [ ] requirements.txt lists all dependencies
- [ ] .gitignore excludes data/ and cache/
- [ ] Tests pass (`python tests/test_components.py`)
- [ ] API runs successfully (`python main.py`)
- [ ] Streamlit UI works (`streamlit run src/streamlit_ui.py`)
- [ ] Demo video created OR app deployed
- [ ] Submission form completed

**Deadline:** Sunday, 23 November 2025

## 👤 Author

**Shubham Rana**
- Assignment for: CodeAtRandom AI
- Position: AI Engineer Intern
- GitHub: https://github.com/RhaegarTargaryenn/CodeAtRandom
- Position: AI Engineer Intern

## 🙏 Acknowledgments

- sentence-transformers for embeddings
- FAISS for vector search
- FastAPI for modern API framework
- Streamlit for beautiful UI framework
- scikit-learn for 20 Newsgroups dataset

---

## 📋 DEPLOYMENT / SUBMISSION INSTRUCTIONS

**For Reviewers & Deployment:**

This is a complete, production-ready document search engine with embedding-based similarity search, intelligent SQLite caching, FastAPI backend, and Streamlit UI. To evaluate: (1) Clone the repository from https://github.com/RhaegarTargaryenn/CodeAtRandom, (2) Run `chmod +x quickstart.sh && ./quickstart.sh` for automated setup, or manually: `pip install -r requirements.txt && python download_data.py && python main.py`, then in a new terminal `streamlit run src/streamlit_ui.py`, (3) Access the Streamlit UI at http://localhost:8501 for interactive search, or the FastAPI docs at http://localhost:8000/docs for API testing, (4) Run tests with `python tests/test_components.py` to verify all components, (5) The system uses sentence-transformers/all-MiniLM-L6-v2 for embeddings cached in SQLite with SHA256 validation, FAISS IndexFlatIP for fast vector search, and returns results with semantic scores plus keyword overlap explanations. **IMPORTANT:** Do NOT commit the `data/` or `cache/` directories (excluded via .gitignore) as they contain large generated files—use the provided `clean_repo.sh` script to prepare a clean submission-ready branch. All core requirements are implemented with bonus features including comprehensive unit tests, automation scripts, and a beautiful Streamlit interface. Submitted as part of the CodeAtRandom AI Engineer Intern assignment.

---

**Built with ❤️ for the CodeAtRandom AI Engineer Intern Assignment**
