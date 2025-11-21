"""
Quick Start Script
Automates the setup and running of the search engine.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"Step: {description}")
    print(f"Command: {command}")
    print('='*60)
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False


def check_python():
    """Check Python version"""
    print("\n" + "█"*60)
    print("CHECKING PYTHON INSTALLATION")
    print("█"*60)
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    
    print("✓ Python version compatible")
    return True


def install_dependencies():
    """Install required packages"""
    print("\n" + "█"*60)
    print("INSTALLING DEPENDENCIES")
    print("█"*60)
    
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found")
        return False
    
    print("Installing packages from requirements.txt...")
    print("This may take several minutes on first run...")
    
    success = run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Install dependencies"
    )
    
    if success:
        print("\n✓ All dependencies installed")
    
    return success


def prepare_data():
    """Prepare sample data"""
    print("\n" + "█"*60)
    print("PREPARING DATA")
    print("█"*60)
    
    # Check if data directory has files
    data_dir = Path("data")
    txt_files = list(data_dir.glob("*.txt")) if data_dir.exists() else []
    
    if len(txt_files) > 0:
        print(f"✓ Found {len(txt_files)} existing documents in data/")
        return True
    
    print("No documents found. Creating sample documents...")
    
    success = run_command(
        f"{sys.executable} main.py --create-samples 20",
        "Create sample documents"
    )
    
    if success:
        print("\n✓ Sample documents created")
    
    return success


def run_tests():
    """Run component tests"""
    print("\n" + "█"*60)
    print("RUNNING TESTS")
    print("█"*60)
    
    print("Testing individual components...")
    
    success = run_command(
        f"{sys.executable} test_components.py",
        "Run component tests"
    )
    
    return success


def start_server():
    """Start the FastAPI server"""
    print("\n" + "█"*60)
    print("STARTING SERVER")
    print("█"*60)
    
    print("\n🚀 Starting Document Search Engine...")
    print("\nOnce started, you can access:")
    print("  - API Docs: http://localhost:8000/docs")
    print("  - ReDoc: http://localhost:8000/redoc")
    print("  - Health: http://localhost:8000/health")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        subprocess.run(
            f"{sys.executable} main.py",
            shell=True,
            check=True
        )
    except KeyboardInterrupt:
        print("\n\n⏹️  Server stopped")


def main():
    """Main quick start workflow"""
    print("█"*60)
    print("DOCUMENT SEARCH ENGINE - QUICK START")
    print("█"*60)
    
    # Step 1: Check Python
    if not check_python():
        print("\n❌ Setup failed: Python version incompatible")
        sys.exit(1)
    
    # Step 2: Install dependencies
    print("\nDo you want to install dependencies? (y/n)")
    if input().lower() == 'y':
        if not install_dependencies():
            print("\n❌ Setup failed: Could not install dependencies")
            sys.exit(1)
    else:
        print("Skipping dependency installation...")
    
    # Step 3: Prepare data
    if not prepare_data():
        print("\n⚠️  Warning: Could not prepare data")
        print("You may need to manually add documents to data/ directory")
    
    # Step 4: Run tests (optional)
    print("\nDo you want to run component tests? (y/n)")
    if input().lower() == 'y':
        if not run_tests():
            print("\n⚠️  Warning: Some tests failed")
            print("Do you want to continue anyway? (y/n)")
            if input().lower() != 'y':
                sys.exit(1)
    else:
        print("Skipping tests...")
    
    # Step 5: Start server
    print("\nReady to start the server!")
    print("Press Enter to start, or Ctrl+C to exit")
    input()
    
    start_server()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Quick start cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
