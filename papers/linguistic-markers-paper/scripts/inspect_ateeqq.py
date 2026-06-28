from datasets import load_dataset
import pandas as pd

print("Loading splits...")
train_dataset = load_dataset("Ateeqq/AI-and-Human-Generated-Text", split="train")
test_dataset = load_dataset("Ateeqq/AI-and-Human-Generated-Text", split="test")

df_train = pd.DataFrame(train_dataset)
df_test = pd.DataFrame(test_dataset)

df = pd.concat([df_train, df_test], ignore_index=True)
print(f"Total dataset shape: {df.shape}")
print("Label counts:\n", df['label'].value_counts())

print("\n--- SAMPLE LABEL 0 ---")
sample_0 = df[df['label'] == 0].iloc[0]
print("Title:", sample_0['title'])
print("Abstract:", sample_0['abstract'][:400] + "...")

print("\n--- SAMPLE LABEL 1 ---")
sample_1 = df[df['label'] == 1].iloc[0]
print("Title:", sample_1['title'])
print("Abstract:", sample_1['abstract'][:400] + "...")
