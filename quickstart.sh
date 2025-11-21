#!/bin/bash

# QuickStart Script for Document Search Engine
# Automates setup, data download, and server startup

set -e  # Exit on error

echo "============================================================"
echo "DOCUMENT SEARCH ENGINE - QUICKSTART"
echo "============================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Check Python
echo "Step 1: Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓ Found: $PYTHON_VERSION${NC}"
echo ""

# Step 2: Create virtual environment
echo "Step 2: Creating virtual environment..."
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment already exists${NC}"
    read -p "Do you want to recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        echo -e "${GREEN}✓ Virtual environment recreated${NC}"
    fi
else
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi
echo ""

# Step 3: Activate virtual environment
echo "Step 3: Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Step 4: Upgrade pip
echo "Step 4: Upgrading pip..."
python -m pip install --upgrade pip --quiet
echo -e "${GREEN}✓ Pip upgraded${NC}"
echo ""

# Step 5: Install requirements
echo "Step 5: Installing dependencies..."
echo "This may take 2-5 minutes..."
pip install -r requirements.txt --quiet
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Step 6: Download data
echo "Step 6: Downloading dataset..."
if [ -d "data" ] && [ "$(ls -A data/*.txt 2>/dev/null)" ]; then
    echo -e "${YELLOW}⚠️  Data directory already contains files${NC}"
    read -p "Do you want to re-download data? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python download_data.py
        echo -e "${GREEN}✓ Data downloaded${NC}"
    else
        echo "Skipping data download..."
    fi
else
    python download_data.py
    echo -e "${GREEN}✓ Data downloaded${NC}"
fi
echo ""

# Step 7: Generate embeddings and start API
echo "Step 7: Starting FastAPI server..."
echo "This will load documents and generate embeddings (may take 1-2 minutes first time)..."
echo ""

# Start FastAPI in background
echo "Starting API server on http://localhost:8000..."
python main.py &
API_PID=$!

# Wait for API to be ready
echo "Waiting for API to start..."
sleep 5

# Check if API is running
if ps -p $API_PID > /dev/null; then
    echo -e "${GREEN}✓ API server started (PID: $API_PID)${NC}"
    echo "  - API Docs: http://localhost:8000/docs"
    echo "  - Health: http://localhost:8000/health"
else
    echo -e "${RED}❌ Failed to start API server${NC}"
    exit 1
fi
echo ""

# Step 8: Start Streamlit UI
echo "Step 8: Starting Streamlit UI..."
echo ""
echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}🚀 SETUP COMPLETE!${NC}"
echo -e "${GREEN}============================================================${NC}"
echo ""
echo "Services running:"
echo "  ✓ FastAPI: http://localhost:8000"
echo "  ✓ API Docs: http://localhost:8000/docs"
echo ""
echo "To start Streamlit UI, run in a new terminal:"
echo -e "${YELLOW}  source venv/bin/activate${NC}"
echo -e "${YELLOW}  streamlit run src/streamlit_ui.py${NC}"
echo ""
echo "Or press ENTER to start Streamlit now (Ctrl+C to stop)..."
read

# Start Streamlit
streamlit run src/streamlit_ui.py

# Cleanup on exit
echo ""
echo "Stopping servers..."
kill $API_PID 2>/dev/null || true
echo "Done!"
