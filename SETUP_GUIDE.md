# Quick Setup Guide

## For Reviewers / Testing

### Step 1: Clone Repository
```bash
git clone https://github.com/RhaegarTargaryenn/CodeAtRandom.git
cd CodeAtRandom
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Download Data (192 documents from 20 Newsgroups)
```bash
python download_data.py
```

### Step 4: Start API Server
```bash
python main.py
```
- API runs at: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Step 5: Launch Web UI (in new terminal)
```bash
streamlit run src/streamlit_ui.py
```
- UI opens at: http://localhost:8501

### Step 6: Test Queries

Try these searches in the Streamlit UI:
- "computer graphics programming"
- "space nasa rocket"
- "medical health treatment"
- "encryption security privacy"

## Testing

Run unit tests:
```bash
pytest tests/ -v
```

Expected: 13-15 tests pass

## Performance

- **First run**: 2-3 minutes (downloads model + generates embeddings)
- **Subsequent runs**: ~5 seconds (loads from cache)
- **Search speed**: ~50ms per query

## Requirements

- Python 3.8+
- 2GB RAM
- 500MB disk space

## Troubleshooting

**Port already in use?**
```bash
python main.py --port 8001
streamlit run src/streamlit_ui.py --server.port 8502
```

**Cache issues?**
```bash
python main.py --force-regenerate
```

**Missing packages?**
```bash
pip install --upgrade -r requirements.txt
```
