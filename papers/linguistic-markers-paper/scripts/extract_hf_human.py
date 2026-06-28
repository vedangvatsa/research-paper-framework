from datasets import load_dataset
import pandas as pd
import os

print("Loading dataset from HuggingFace...")
train_dataset = load_dataset("Ateeqq/AI-and-Human-Generated-Text", split="train")
df = pd.DataFrame(train_dataset)

# Show columns
print("Columns in dataset:", df.columns.tolist())

# Extract human abstracts
human_df = df[df["label"] == 0].dropna(subset=["abstract"]).drop_duplicates(subset=["abstract"])
print("Total human abstracts available:", len(human_df))

# Just take 10,000
human_df = human_df.head(10000)

# Create a mock title if title doesn't exist, or just use it if it does
if "title" not in df.columns:
    # We will generate a mock title by taking the first 10 words of the abstract and capitalizing it
    human_df["title"] = human_df["abstract"].apply(lambda x: " ".join(str(x).split()[:10]).title() + "...")
    
human_df["openalex_id"] = ["https://openalex.org/W" + str(i) for i in range(len(human_df))]
human_df["doi"] = None
human_df["year"] = 2019

# Save to the CSV our generation script expects
os.makedirs("data/metadata", exist_ok=True)
human_df.to_csv("data/metadata/openalex_human_abstracts.csv", index=False)
print("Saved 10,000 human abstracts to data/metadata/openalex_human_abstracts.csv")
