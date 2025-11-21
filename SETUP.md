# Quick Setup Guide

## Step 1: Install Dependencies
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

## Step 2: Prepare Data

### Option A: Create Sample Documents (Fastest)
```powershell
python main.py --create-samples 20
```

### Option B: Download 20 Newsgroups Dataset
```powershell
# Create a script download_data.py and run it
python download_data.py
```

## Step 3: Run the Application
```powershell
python main.py
```

## Step 4: Test the API

Open your browser and go to:
- http://localhost:8000/docs

Or use curl:
```powershell
curl -X POST "http://localhost:8000/search" -H "Content-Type: application/json" -d '{\"query\": \"machine learning\", \"top_k\": 5}'
```

Or use PowerShell:
```powershell
$body = @{
    query = "machine learning"
    top_k = 5
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/search" -Method Post -Body $body -ContentType "application/json"
```

## Troubleshooting

### Issue: No documents found
**Solution**: Create sample documents first
```powershell
python main.py --create-samples 20
```

### Issue: FAISS not available
**Solution**: Install faiss-cpu
```powershell
pip install faiss-cpu
```

### Issue: Port already in use
**Solution**: Use a different port
```powershell
python main.py --port 8001
```

## Project Status
✓ All core requirements implemented
✓ Caching system working
✓ API endpoints functional
✓ Documentation complete

Ready for submission!
