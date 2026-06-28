import pandas as pd
try:
    from datasets import load_dataset
    print("datasets package is installed!")
except ImportError:
    print("datasets package not installed. Installing it now...")
    import subprocess
    subprocess.run(["pip", "install", "datasets", "pandas"])
    from datasets import load_dataset

print("Loading dataset...")
try:
    dataset = load_dataset("NicolaiSivesind/human-vs-machine", split="train")
    df = pd.DataFrame(dataset)
    print(f"Dataset loaded successfully!")
    print(f"Shape: {df.shape}")
    print("Columns:", df.columns)
    print("Class distribution:\n", df['label'].value_counts())
    print("Domain distribution:\n", df['source'].value_counts() if 'source' in df.columns else "No 'source' column")
    print(df.head(2))
except Exception as e:
    print(f"Error loading human-vs-machine: {e}")

try:
    print("\nTrying alternative: Ateeqq/AI-and-Human-Generated-Text")
    dataset2 = load_dataset("Ateeqq/AI-and-Human-Generated-Text", split="train")
    df2 = pd.DataFrame(dataset2)
    print(f"Dataset 2 loaded successfully!")
    print(f"Shape: {df2.shape}")
    print("Columns:", df2.columns)
    print(df2.head(2))
except Exception as e:
    print(f"Error loading Ateeqq dataset: {e}")
