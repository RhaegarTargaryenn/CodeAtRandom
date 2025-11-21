"""
Streamlit UI for Document Search Engine
A simple web interface for searching documents using semantic similarity.
"""

import streamlit as st
import requests
import json
from typing import Dict, List, Optional
import sys
from pathlib import Path

# Configuration
API_URL = "http://localhost:8000/search"
USE_API = True  # We always use API mode in Streamlit
LOCAL_ENGINE_AVAILABLE = False  # Disabled local engine to avoid import issues


def call_api_search(query: str, top_k: int) -> Optional[Dict]:
    """
    Call the FastAPI backend to perform search.
    
    Args:
        query (str): Search query
        top_k (int): Number of results to return
        
    Returns:
        Optional[Dict]: Search results or None if error
    """
    try:
        response = requests.post(
            API_URL,
            json={"query": query, "top_k": top_k},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Could not connect to API at {API_URL}")
        st.info("Make sure the FastAPI server is running: `python main.py`")
        return None
    except Exception as e:
        st.error(f"Error calling API: {e}")
        return None


def search_documents(query: str, top_k: int) -> Optional[Dict]:
    """
    Search documents using either API or local engine.
    
    Args:
        query (str): Search query
        top_k (int): Number of results
        
    Returns:
        Optional[Dict]: Search results
    """
    if USE_API:
        return call_api_search(query, top_k)
    else:
        # Fallback to local engine (requires initialization)
        st.error("Local engine mode not configured. Please use API mode.")
        return None


def display_result(result: Dict, rank: int) -> None:
    """
    Display a single search result.
    
    Args:
        result (Dict): Result dictionary
        rank (int): Result ranking
    """
    with st.container():
        # Header with rank and score
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### {rank}. 📄 {result['filename']}")
        
        with col2:
            score = result['score']
            score_color = "🟢" if score > 0.7 else "🟡" if score > 0.5 else "🔴"
            st.markdown(f"**Score:** {score_color} {score:.3f}")
        
        # Document preview
        st.markdown("**Preview:**")
        st.text(result['preview'])
        
        # Keyword overlap
        if result['keywords_overlap']:
            st.markdown("**Matching Keywords:**")
            keywords_str = ", ".join([f"`{kw}`" for kw in result['keywords_overlap'][:10]])
            st.markdown(keywords_str)
            
            overlap_pct = result['overlap_ratio'] * 100
            st.progress(result['overlap_ratio'])
            st.caption(f"Overlap: {result['overlap_count']} keywords ({overlap_pct:.1f}%)")
        else:
            st.caption("No exact keyword matches (semantic match only)")
        
        # Explanation
        with st.expander("📊 Why this document matched"):
            st.info(result['explanation'])
            st.caption(f"Document ID: `{result['doc_id']}`")
            st.caption(f"Document Length: {result['doc_length']} characters")
        
        st.divider()


def main():
    """Main Streamlit application"""
    
    # Page configuration
    st.set_page_config(
        page_title="Document Search Engine",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header
    st.title("🔍 Document Search Engine")
    st.markdown("**Semantic search powered by AI embeddings**")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        st.markdown("---")
        st.subheader("Search Settings")
        
        top_k = st.slider(
            "Number of results (top_k)",
            min_value=1,
            max_value=20,
            value=5,
            help="Number of top results to return"
        )
        
        st.markdown("---")
        st.subheader("About")
        st.markdown("""
        This search engine uses:
        - **Embeddings**: sentence-transformers
        - **Search**: FAISS vector similarity
        - **Cache**: SQLite with hash validation
        - **API**: FastAPI backend
        """)
        
        st.markdown("---")
        st.subheader("Status")
        
        # Check API status
        try:
            health_response = requests.get("http://localhost:8000/health", timeout=2)
            if health_response.status_code == 200:
                st.success("✅ API Connected")
                stats = health_response.json().get('stats', {})
                st.metric("Documents Loaded", stats.get('total_documents', 'N/A'))
            else:
                st.error("❌ API Error")
        except:
            st.warning("⚠️ API Offline")
            st.caption("Start with: `python main.py`")
    
    # Main content
    st.markdown("---")
    
    # Search interface
    col1, col2 = st.columns([4, 1])
    
    with col1:
        query = st.text_input(
            "Enter your search query:",
            placeholder="e.g., machine learning algorithms, quantum physics, neural networks...",
            help="Type your search query here"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Spacing
        search_button = st.button("🔍 Search", type="primary", use_container_width=True)
    
    # Example queries
    st.caption("**Example queries:** artificial intelligence, deep learning, computer vision, natural language processing")
    
    # Perform search
    if search_button or (query and len(query) > 2):
        if not query or len(query.strip()) < 2:
            st.warning("⚠️ Please enter a search query (at least 2 characters)")
        else:
            with st.spinner(f"🔎 Searching for: '{query}'..."):
                results = search_documents(query, top_k)
            
            if results:
                # Display search metadata
                st.markdown("---")
                st.success(f"✅ Found {results['total_results']} results in {results['search_time_ms']:.2f}ms")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Query", f'"{results["query"]}"')
                with col2:
                    st.metric("Results Returned", results['total_results'])
                with col3:
                    st.metric("Search Time", f"{results['search_time_ms']:.2f}ms")
                
                st.markdown("---")
                
                # Display results
                if results['results']:
                    st.subheader("📑 Search Results")
                    
                    for result in results['results']:
                        display_result(result, result['rank'])
                else:
                    st.info("No results found for your query.")
            else:
                st.error("❌ Search failed. Please check if the API server is running.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray; padding: 20px;'>
            <p>Document Search Engine | Built with FastAPI, Streamlit & sentence-transformers</p>
            <p>CodeAtRandom AI Engineer Intern Assignment</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
