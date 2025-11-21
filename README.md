# 🔍 Document Search Engine

A semantic search engine powered by AI embeddings for searching across text documents using natural language queries.

## Features

- **Semantic Search**: Uses sentence-transformers for understanding query intent
- **Vector Search**: FAISS-based fast similarity search
- **Smart Caching**: SQLite cache with hash validation to avoid recomputing embeddings
- **REST API**: FastAPI backend with auto-generated documentation
- **Web UI**: Interactive Streamlit interface
- **Ranking Explanations**: Shows why documents matched your query

## Tech Stack

- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Vector Search**: FAISS (Facebook AI Similarity Search)
- **Cache**: SQLite with SHA256 validation
- **API**: FastAPI + Uvicorn
- **UI**: Streamlit
- **Data**: 20 Newsgroups dataset (192 documents)

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download Data

```bash
python download_data.py
```

This downloads 192 documents from the 20 Newsgroups dataset.

### 3. Start API Server

```bash
python main.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs

### 4. Launch Web UI (Optional)

In a new terminal:

```bash
streamlit run src/streamlit_ui.py
```

The UI will open at http://localhost:8501

## API Usage

### Search Endpoint

```bash
POST http://localhost:8000/search
Content-Type: application/json

{
  "query": "computer graphics programming",
  "top_k": 5
}
```

### Example Response

```json
{
  "query": "computer graphics programming",
  "top_k": 5,
  "total_results": 5,
  "search_time_ms": 45.2,
  "results": [
    {
      "rank": 1,
      "doc_id": "newsgroup_0099_cat1",
      "filename": "newsgroup_0099_cat1.txt",
      "score": 0.423,
      "preview": "graphics workshop shareware program...",
      "keywords_overlap": ["graphics", "program"],
      "explanation": "High semantic similarity with keyword matches"
    }
  ]
}
```

## Example Queries

Try these in the Streamlit UI or via API:

- `computer graphics hardware drivers`
- `space nasa rocket satellite`
- `medical health disease treatment`
- `baseball hockey sports team`
- `encryption security privacy`
- `religion god atheism belief`

## Project Structure

```
assignment_codeRandom/
├── src/
│   ├── embedder.py          # Embedding generation
│   ├── cache_manager.py     # SQLite caching
│   ├── search_engine.py     # Main search logic
│   ├── api.py               # FastAPI endpoints
│   ├── streamlit_ui.py      # Web interface
│   └── utils.py             # Helper functions
├── tests/
│   └── test_components.py   # Unit tests
├── data/                    # Text documents (192 files)
├── cache/                   # SQLite cache database
├── main.py                  # API server entry point
├── download_data.py         # Data downloader
└── requirements.txt         # Python dependencies
```

## How It Works

1. **Document Processing**: Loads text documents from `data/` directory
2. **Embedding Generation**: Converts text to 384-dimensional vectors using sentence-transformers
3. **Caching**: Stores embeddings in SQLite to avoid recomputation
4. **Vector Index**: Builds FAISS index for fast similarity search
5. **Query Processing**: Embeds user query and finds most similar documents
6. **Ranking**: Returns results with similarity scores and explanations

## Testing

Run unit tests:

```bash
pytest tests/ -v
```

## Performance

- **First run**: ~2-3 minutes (downloads model + generates embeddings)
- **Subsequent runs**: ~5 seconds (loads from cache)
- **Search latency**: ~50ms per query
- **Documents**: 192 text files from 20 Newsgroups
- **Model size**: ~90MB (all-MiniLM-L6-v2)

## Requirements

- Python 3.8+
- 2GB RAM minimum
- 500MB disk space (for model + cache)

## License

MIT License - Created for CodeAtRandom AI Engineer Intern Assignment

---

**Built with FastAPI, Streamlit & sentence-transformers**
