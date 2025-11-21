# 🚀 GETTING STARTED - Quick Reference

## For Immediate Use

### ⚡ Fastest Way to Run (3 Steps)

```powershell
# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Create sample documents
python main.py --create-samples 20

# Step 3: Start the server
python main.py
```

**That's it!** Open http://localhost:8000/docs in your browser.

---

## 🎯 What You Need

### Requirements
- ✅ Python 3.8+ installed
- ✅ Internet connection (for downloading models first time)
- ✅ ~2GB RAM
- ✅ ~500MB disk space

### Check Python Version
```powershell
python --version
# Should show: Python 3.8.x or higher
```

---

## 📝 Step-by-Step Guide

### 1️⃣ Open Terminal/PowerShell
- Press `Win + X` → Select "Windows PowerShell"
- Navigate to project: `cd "C:\Users\shubham rana\Desktop\assignment_codeRandom"`

### 2️⃣ Create Virtual Environment (Recommended)
```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\activate

# You should see (venv) in your prompt
```

### 3️⃣ Install Dependencies
```powershell
pip install -r requirements.txt
# Wait 2-5 minutes for installation
```

### 4️⃣ Prepare Data

**Option A: Quick Test (Sample Data)**
```powershell
python main.py --create-samples 20
# Creates 20 sample documents instantly
```

**Option B: Real Data (20 Newsgroups)**
```powershell
python download_data.py
# Downloads ~200 real documents (~1 minute)
```

**Option C: Your Own Data**
```powershell
# Just copy your .txt files to data/ folder
mkdir data
# Copy files here
```

### 5️⃣ Run the Application
```powershell
python main.py
```

**Expected Output:**
```
============================================================
INITIALIZING DOCUMENT SEARCH ENGINE
============================================================
✓ Found 20 text files in data
Loading model: sentence-transformers/all-MiniLM-L6-v2
Using device: cpu
✓ Loaded 20 documents
Generating embeddings...
✓ Embeddings generated
✓ Vector index built
============================================================
🚀 Server starting...
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 6️⃣ Test the API

**Open in Browser:**
- Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

**Try a Search (PowerShell):**
```powershell
$body = @{
    query = "machine learning"
    top_k = 5
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/search" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"
```

**Or using Python:**
```python
import requests

response = requests.post(
    "http://localhost:8000/search",
    json={"query": "machine learning", "top_k": 5}
)

print(response.json())
```

---

## 🧪 Test Everything Works

```powershell
python test_components.py
```

**Expected:** All 5 tests should PASS ✅

---

## ⚙️ Advanced Options

### Custom Port
```powershell
python main.py --port 8080
```

### Force Regenerate Embeddings
```powershell
python main.py --force-regenerate
```

### Use Cosine Similarity (No FAISS)
```powershell
python main.py --no-faiss
```

### Development Mode (Auto-reload)
```powershell
python main.py --reload
```

### All Options
```powershell
python main.py --help
```

---

## 🐛 Troubleshooting

### Problem: "Module not found"
**Solution:** Install dependencies
```powershell
pip install -r requirements.txt
```

### Problem: "No documents found"
**Solution:** Create sample documents
```powershell
python main.py --create-samples 20
```

### Problem: "Port already in use"
**Solution:** Use different port
```powershell
python main.py --port 8001
```

### Problem: FAISS installation fails
**Solution:** 
```powershell
# Install specific version
pip install faiss-cpu==1.7.4

# Or skip FAISS (use cosine similarity)
python main.py --no-faiss
```

### Problem: Slow embedding generation
**Expected:** First run takes 1-2 seconds per document (normal)
- Subsequent runs use cache (0.01 seconds per document)
- If you have GPU, it will automatically use it (much faster)

---

## 📊 What to Expect

### First Run (No Cache)
- **20 documents:** ~30-40 seconds
- **100 documents:** ~2-3 minutes
- **200 documents:** ~4-5 minutes

### Subsequent Runs (With Cache)
- **Any number:** ~2-3 seconds (just loading cache)

### Search Speed
- **Per query:** ~10-20 milliseconds
- **Very fast!**

---

## 🎯 Quick Tests

### Test 1: Health Check
```powershell
curl http://localhost:8000/health
```

### Test 2: Simple Search (Browser)
Open: http://localhost:8000/search?query=learning&top_k=3

### Test 3: View All Documents
```powershell
curl http://localhost:8000/documents
```

### Test 4: Get Statistics
```powershell
curl http://localhost:8000/stats
```

---

## 📚 Next Steps After Running

1. **Explore API Docs**
   - Go to http://localhost:8000/docs
   - Try different queries
   - Adjust top_k parameter

2. **Check Cache**
   - Look at `cache/embeddings_cache.db`
   - Run again to see cache working

3. **Add More Documents**
   - Add .txt files to `data/` folder
   - Restart server
   - New documents will be indexed

4. **Read Documentation**
   - `README.md` - Full documentation
   - `FILE_STRUCTURE.md` - Project structure
   - `PROJECT_SUMMARY.md` - Summary

---

## 🎓 Understanding the Flow

```
You make a search request
         ↓
FastAPI receives it
         ↓
Search engine processes:
  1. Embeds your query
  2. Compares with document embeddings
  3. Finds most similar documents
  4. Explains why they match
         ↓
Returns ranked results with explanations
```

---

## ✅ Success Indicators

When everything works, you'll see:
- ✅ Server starts without errors
- ✅ http://localhost:8000/docs loads
- ✅ Search returns results
- ✅ Results have scores and explanations
- ✅ Subsequent runs are much faster (cache working)

---

## 🆘 Still Having Issues?

1. Check Python version: `python --version` (need 3.8+)
2. Check if port 8000 is free
3. Run component tests: `python test_components.py`
4. Check `SETUP.md` for detailed troubleshooting
5. Ensure all dependencies installed correctly

---

## 🎉 You're Ready!

Once the server is running:
- ✅ API is accessible at http://localhost:8000
- ✅ Documentation at http://localhost:8000/docs
- ✅ Search engine is operational
- ✅ Caching is working

**Now you can:**
- Test searches
- Add more documents
- Prepare for demo/submission
- Create video demonstration

---

## 📞 Quick Commands Reference

```powershell
# Setup
pip install -r requirements.txt
python main.py --create-samples 20

# Run
python main.py

# Test
python test_components.py

# With options
python main.py --port 8080
python main.py --force-regenerate
python main.py --no-faiss

# Download real data
python download_data.py

# Automated setup
python quickstart.py
```

---

**Ready? Let's go! 🚀**

```powershell
python main.py
```
