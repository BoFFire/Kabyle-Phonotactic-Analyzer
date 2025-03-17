import sys
import subprocess
import nltk

def install_nltk():
    """Install NLTK if not present"""
    try:
        import nltk
    except ImportError:
        print("Installing NLTK...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "nltk"])

def ensure_punkt():
    """Download Punkt tokenizer if not already present"""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading Punkt tokenizer...")
        nltk.download('punkt', quiet=True)
