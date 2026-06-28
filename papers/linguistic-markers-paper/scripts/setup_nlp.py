import subprocess
import sys

def check_and_install():
    print("Installing spacy model...")
    subprocess.run([sys.executable, "-m", "pip", "install", "spacy", "scikit-learn", "scipy", "matplotlib", "seaborn", "lexicalrichness"])
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    print("NLP packages and model setup complete!")

if __name__ == "__main__":
    check_and_install()
