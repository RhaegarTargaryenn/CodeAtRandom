#!/bin/bash

# Clean Repository Script for Submission
# Prepares a clean branch for GitHub submission

set -e  # Exit on error

echo "============================================================"
echo "REPOSITORY CLEANUP FOR SUBMISSION"
echo "============================================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo -e "${RED}❌ Not a git repository!${NC}"
    echo "Initialize git first: git init"
    exit 1
fi

echo "Step 1: Checking current status..."
git status
echo ""

# Step 2: Remove large files from tracking
echo "Step 2: Removing large files from git tracking..."

# Remove data directory if tracked
if git ls-files --error-unmatch data/ >/dev/null 2>&1; then
    echo "Removing data/ from tracking..."
    git rm -r --cached data/ 2>/dev/null || true
fi

# Remove cache directory if tracked
if git ls-files --error-unmatch cache/ >/dev/null 2>&1; then
    echo "Removing cache/ from tracking..."
    git rm -r --cached cache/ 2>/dev/null || true
fi

# Remove venv if tracked
if git ls-files --error-unmatch venv/ >/dev/null 2>&1; then
    echo "Removing venv/ from tracking..."
    git rm -r --cached venv/ 2>/dev/null || true
fi

# Remove any .db files
git rm --cached **/*.db 2>/dev/null || true

# Remove pycache
git rm -r --cached **/__pycache__/ 2>/dev/null || true

echo -e "${GREEN}✓ Large files removed from tracking${NC}"
echo ""

# Step 3: Create submission branch
echo "Step 3: Creating submission-ready branch..."

# Check if branch already exists
if git show-ref --verify --quiet refs/heads/submission-ready; then
    echo -e "${YELLOW}⚠️  Branch 'submission-ready' already exists${NC}"
    read -p "Do you want to delete and recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git branch -D submission-ready
        git checkout -b submission-ready
        echo -e "${GREEN}✓ Branch recreated${NC}"
    else
        git checkout submission-ready
        echo "Using existing branch..."
    fi
else
    git checkout -b submission-ready
    echo -e "${GREEN}✓ Branch created${NC}"
fi
echo ""

# Step 4: Stage required files only
echo "Step 4: Staging required files..."

# Add core files
git add src/*.py 2>/dev/null || true
git add tests/*.py 2>/dev/null || true
git add requirements.txt
git add README.md
git add .gitignore
git add quickstart.sh
git add clean_repo.sh
git add download_data.py
git add main.py
git add CHECKLIST.md 2>/dev/null || true
git add SETUP.md 2>/dev/null || true
git add GET_STARTED.md 2>/dev/null || true

echo -e "${GREEN}✓ Required files staged${NC}"
echo ""

# Step 5: Show what will be committed
echo "Step 5: Files to be committed:"
git status --short
echo ""

# Step 6: Create clean commit
echo "Step 6: Creating commit..."
read -p "Proceed with commit? (Y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    git commit -m "Assignment: CodeAtRandom - submission-ready

Multi-Document Embedding Search Engine with Caching
- FastAPI backend with REST endpoints
- Streamlit UI for search interface
- SQLite caching with hash validation
- FAISS vector search with cosine fallback
- sentence-transformers embeddings
- Complete documentation and tests

All requirements implemented and tested.
" || echo "No changes to commit"
    
    echo -e "${GREEN}✓ Commit created${NC}"
else
    echo "Commit cancelled"
    exit 0
fi
echo ""

# Step 7: Instructions for pushing
echo "============================================================"
echo -e "${GREEN}✓ REPOSITORY CLEANED AND READY FOR SUBMISSION${NC}"
echo "============================================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Review the commit:"
echo -e "   ${YELLOW}git log -1 --stat${NC}"
echo ""
echo "2. Push to GitHub (create repository first if needed):"
echo -e "   ${YELLOW}git remote add origin https://github.com/RhaegarTargaryenn/CodeAtRandom.git${NC}"
echo -e "   ${YELLOW}git push origin submission-ready${NC}"
echo ""
echo "   Or force push if branch exists:"
echo -e "   ${YELLOW}git push origin submission-ready --force${NC}"
echo ""
echo "3. On GitHub, create a Pull Request or set as default branch"
echo ""
echo "⚠️  WARNING: Do NOT commit these directories:"
echo "   - data/ (contains dataset files)"
echo "   - cache/ (contains cached embeddings)"
echo "   - venv/ (virtual environment)"
echo "   - **/__pycache__/ (Python cache)"
echo ""
echo "These are excluded via .gitignore"
echo ""
echo -e "${GREEN}Ready for submission! 🚀${NC}"
