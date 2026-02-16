"""
Verify project setup and dependencies
Run this to ensure everything is configured correctly
"""
import sys
import os
from pathlib import Path

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("  ⚠️  Warning: Python 3.8+ recommended")
        return False
    return True


def check_virtual_env():
    """Check if running in virtual environment"""
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    if in_venv:
        print("✓ Virtual environment is active")
        return True
    else:
        print("✗ Not in virtual environment")
        print("  Run: .\\venv\\Scripts\\Activate.ps1")
        return False


def check_dependencies():
    """Check if all dependencies are installed"""
    required_packages = {
        'streamlit': 'Streamlit',
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'openai': 'OpenAI',
        'langchain': 'LangChain',
        'faiss': 'FAISS',
        'pydantic': 'Pydantic',
        'requests': 'Requests',
    }
    
    all_installed = True
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"✓ {name}")
        except ImportError:
            print(f"✗ {name} - NOT INSTALLED")
            all_installed = False
    
    return all_installed


def check_env_file():
    """Check if .env file exists and has API key"""
    env_path = Path(".env")
    if env_path.exists():
        print("✓ .env file exists")
        
        with open(env_path, 'r') as f:
            content = f.read()
            if 'OPENAI_API_KEY=' in content:
                # Check if key is set
                for line in content.split('\n'):
                    if line.startswith('OPENAI_API_KEY='):
                        key = line.split('=')[1].strip()
                        if key and key != 'your_openai_api_key_here':
                            print("  ✓ OpenAI API Key configured")
                            return True
                        else:
                            print("  ✗ OpenAI API Key NOT SET")
                            print("    Edit .env and add your key")
                            return False
    else:
        print("✗ .env file NOT found")
        print("  Create from .env.example: copy .env.example .env")
        return False


def check_data_files():
    """Check if data files exist"""
    data_dir = Path("backend/data")
    
    files = {
        'banking_docs.txt': 'Banking FAQs',
        'branch_data.json': 'Branch information',
        'transactions.json': 'Transaction data',
    }
    
    all_exist = True
    for filename, description in files.items():
        file_path = data_dir / filename
        if file_path.exists():
            print(f"✓ {description}")
        else:
            print(f"✗ {description} - NOT FOUND")
            all_exist = False
    
    if not all_exist:
        print("  Run: python backend/data_init.py")
    
    return all_exist


def check_project_structure():
    """Check if project structure is correct"""
    required_dirs = {
        'backend': 'Backend directory',
        'backend/agent': 'Agent module',
        'backend/data': 'Data directory',
        'frontend': 'Frontend directory',
        'vectorstore': 'Vector store directory',
    }
    
    all_exist = True
    for dir_path, description in required_dirs.items():
        if Path(dir_path).exists():
            print(f"✓ {description}")
        else:
            print(f"✗ {description} - NOT FOUND")
            all_exist = False
    
    return all_exist


def check_ports():
    """Check if required ports are available"""
    import socket
    
    ports = {
        8000: 'Backend (FastAPI)',
        8501: 'Frontend (Streamlit)',
    }
    
    for port, service in ports.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        
        if result != 0:
            print(f"✓ {service} (port {port}) - Available")
        else:
            print(f"⚠️  {service} (port {port}) - Already in use")


def main():
    """Run all checks"""
    print("\n" + "="*50)
    print("Banking AI Agent - Setup Verification")
    print("="*50 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Virtual Environment", check_virtual_env),
        ("Project Structure", check_project_structure),
        ("Dependencies", check_dependencies),
        ("Configuration", check_env_file),
        ("Data Files", check_data_files),
        ("Network Ports", check_ports),
    ]
    
    results = []
    for title, check_func in checks:
        print(f"\n{title}:")
        print("-" * 50)
        try:
            result = check_func()
            results.append((title, result))
        except Exception as e:
            print(f"✗ Error checking {title}: {e}")
            results.append((title, False))
    
    # Summary
    print("\n" + "="*50)
    print("Summary:")
    print("="*50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for title, result in results:
        status = "✓" if result else "✗"
        print(f"{status} {title}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ All checks passed! You're ready to start.\n")
        print("Next steps:")
        print("1. Terminal 1: python -m uvicorn backend.main:app --reload")
        print("2. Terminal 2: streamlit run frontend/app.py")
        print("3. Open: http://localhost:8501\n")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.\n")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
