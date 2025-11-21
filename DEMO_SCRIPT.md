# 🎬 DEMO SCRIPT FOR VIDEO PRESENTATION
# Document Search Engine - CodeAtRandom AI Engineer Intern Assignment

## 📋 VIDEO STRUCTURE (5-7 minutes)

---

## 1️⃣ INTRODUCTION (30 seconds)
**What to say:**
"Hello! I'm presenting my Document Search Engine for the CodeAtRandom AI Engineer Intern position. This is a semantic search engine that understands natural language queries and finds relevant documents using AI embeddings."

**Show on screen:**
- GitHub repository: https://github.com/RhaegarTargaryenn/CodeAtRandom
- Project name on terminal/IDE

---

## 2️⃣ PROJECT OVERVIEW (1 minute)
**What to say:**
"The project has three main components:
1. A FastAPI backend for the REST API
2. A Streamlit web interface for easy interaction
3. An AI-powered search engine using sentence-transformers

It searches across 192 documents from the 20 Newsgroups dataset using semantic similarity, not just keyword matching."

**Show on screen:**
- Open README.md (scroll through features)
- Show project structure in VS Code explorer

**Files to open:**
- README.md (lines 1-20: Title, Features, Tech Stack)

---

## 3️⃣ CODE WALKTHROUGH (2 minutes)

### A. Core Components
**What to say:**
"Let me walk you through the main components:"

**File 1: src/embedder.py**
**Show lines 1-30:**
- "This handles converting text to 384-dimensional vectors using sentence-transformers"
- "We use the all-MiniLM-L6-v2 model for fast, efficient embeddings"

**File 2: src/cache_manager.py**
**Show lines 1-40:**
- "The cache manager stores embeddings in SQLite to avoid recomputing them"
- "It uses SHA256 hashing to validate if document content changed"

**File 3: src/search_engine.py**
**Show lines 1-50:**
- "The search engine combines everything: loads documents, generates embeddings, builds FAISS index"
- "FAISS gives us fast vector similarity search"

**File 4: src/api.py**
**Show lines 1-30 and search endpoint around line 50-80:**
- "FastAPI provides the REST API with automatic documentation"
- "The search endpoint accepts a query and returns ranked results"

---

## 4️⃣ LIVE DEMO - API (1 minute)

**Terminal commands to run:**

```bash
# Start the API server (already running in background)
# Show the terminal output with initialization logs
```

**What to say:**
"The server initializes quickly because embeddings are cached from previous runs."

**Open browser: http://localhost:8000/docs**
**What to show:**
- FastAPI auto-generated documentation
- Expand the POST /search endpoint
- Click "Try it out"

**Demo query:**
```json
{
  "query": "computer graphics programming",
  "top_k": 5
}
```

**What to say:**
"Let me search for 'computer graphics programming'. The API returns results in under 50 milliseconds with similarity scores and keyword overlap analysis."

**Show the JSON response** (scroll through results)

---

## 5️⃣ LIVE DEMO - WEB UI (2 minutes)

**Open browser: http://localhost:8501**

**What to say:**
"Now let's use the Streamlit web interface for a more user-friendly experience."

**Demo Queries (do 3-4):**

**Query 1:** `computer graphics hardware drivers`
**What to say:**
"Searching for computer graphics... You can see it found 9 relevant documents. The first result is about graphics workshop software. Notice the green keyword highlights showing which words matched."

**Query 2:** `space nasa rocket satellite astronomy`
**What to say:**
"Now searching for space-related content... The search understands the semantic meaning, not just exact keyword matches."

**Query 3:** `medical health disease treatment`
**What to say:**
"And here's a medical query... Each result shows:
- A similarity score
- Document preview
- Keyword overlap visualization
- An explanation of why it matched"

**Show the sidebar:**
"I can adjust the number of results from 1 to 20 using this slider."

**Expand a result:**
"Clicking the dropdown shows more details about why this document was ranked here."

---

## 6️⃣ TECHNICAL HIGHLIGHTS (1 minute)

**What to say:**
"Key technical features implemented:

1. **Smart Caching**: Embeddings are cached in SQLite with SHA256 validation. First run takes 2-3 minutes, subsequent runs load in 5 seconds.

2. **FAISS Vector Search**: Uses Facebook's FAISS library for fast similarity search across 192 documents.

3. **Ranking Explanations**: Not just results - the system explains WHY each document matched using keyword overlap and semantic similarity.

4. **Production-Ready**: Includes unit tests, clean code structure, comprehensive documentation, and both API and UI interfaces."

**Show on screen:**
- Run tests: `pytest tests/ -v`
- Show test results (13-15 tests passing)

---

## 7️⃣ PROJECT STRUCTURE (30 seconds)

**Open VS Code Explorer**

**What to say:**
"The project is well-organized:
- `src/` contains all the core modules
- `tests/` has unit tests for components
- `data/` holds the 192 text documents
- `cache/` stores the embedding cache
- Clean separation of concerns: embedder, cache, search, API, and UI"

**Files to briefly show:**
- src/ folder expanded
- tests/test_components.py
- requirements.txt

---

## 8️⃣ CONCLUSION (30 seconds)

**What to say:**
"To summarize, this is a complete semantic search engine with:
- AI-powered embeddings for understanding query intent
- Fast vector search using FAISS
- Smart caching for performance
- Both REST API and web interface
- Clean, tested, production-ready code

The code is available on GitHub, and I'm excited about the opportunity to contribute to CodeAtRandom. Thank you for watching!"

**Show on screen:**
- GitHub repository: https://github.com/RhaegarTargaryenn/CodeAtRandom
- Your contact information (optional)

---

## 📝 QUICK REFERENCE - FILES TO OPEN

**In order of appearance:**

1. **README.md** (lines 1-20) - Project overview
2. **src/embedder.py** (lines 1-30) - Embedding generation
3. **src/cache_manager.py** (lines 1-40) - Caching system
4. **src/search_engine.py** (lines 1-50) - Search engine core
5. **src/api.py** (lines 1-30, 50-80) - FastAPI endpoints
6. **Browser: http://localhost:8000/docs** - API documentation
7. **Browser: http://localhost:8501** - Streamlit UI
8. **tests/test_components.py** (show pytest output)
9. **VS Code Explorer** - Project structure

---

## 🎯 KEY POINTS TO EMPHASIZE

1. **Semantic search**, not just keyword matching
2. **Fast performance**: 50ms search, cached embeddings
3. **Production-ready**: Tests, docs, clean code
4. **Full stack**: Backend API + Frontend UI
5. **Smart features**: Caching, ranking explanations, keyword overlap

---

## 🚨 BEFORE RECORDING CHECKLIST

- [ ] Both servers running (API on :8000, Streamlit on :8501)
- [ ] Browser tabs open and ready
- [ ] VS Code with all files open
- [ ] Terminal visible with clean prompt
- [ ] Test the queries beforehand to ensure they work
- [ ] Clear browser cache/cookies if needed
- [ ] Check audio/video quality
- [ ] Prepare your introduction

---

## 💡 TIPS FOR RECORDING

- **Speak clearly and at moderate pace**
- **Use cursor/mouse to highlight what you're talking about**
- **Don't worry about minor mistakes - they show authenticity**
- **Keep it under 7 minutes - reviewers appreciate brevity**
- **Show enthusiasm but stay professional**
- **Zoom in on code when showing specific lines**

---

**GOOD LUCK! 🚀**
