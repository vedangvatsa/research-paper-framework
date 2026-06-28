import pandas as pd
import requests
import os
import argparse
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

csv_lock = threading.Lock()
thread_local = threading.local()

def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session

# Load API keys from environment
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "YOUR_GROQ_API_KEY")
COHERE_API_KEY = os.environ.get("COHERE_API_KEY", "YOUR_COHERE_API_KEY")
NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "YOUR_NVIDIA_API_KEY")

PROVIDERS = [
    ("https://api.groq.com/openai/v1/chat/completions", f"Bearer {GROQ_API_KEY}", "llama-3.1-8b-instant"),
    ("https://integrate.api.nvidia.com/v1/chat/completions", f"Bearer {NVIDIA_API_KEY}", "minimaxai/minimax-m3"),
    ("https://api.cohere.com/compatibility/v1/chat/completions", f"Bearer {COHERE_API_KEY}", "command-r-08-2024"),
 ]

def generate_abstract(row, out_file):
    title = row.get('title', '')
    messages = [
        {"role": "system", "content": "You are a scientific author. Write an academic abstract for a paper with the following title. Respond ONLY with the abstract text, nothing else."},
        {"role": "user", "content": f"Title: {title}"}
    ]
    
    max_retries = 9
    text = ""
    session = get_session()
    
    for attempt in range(max_retries):
        idx = random.randint(0, len(PROVIDERS) - 1)
        url, auth, model = PROVIDERS[idx]
        headers = {"Authorization": auth, "Content-Type": "application/json"}
        payload = {"model": model, "messages": messages, "max_tokens": 200, "temperature": 0.7, "top_p": 0.95}
        
        try:
            response = session.post(url, headers=headers, json=payload, timeout=25)
            if response.status_code == 429:
                time.sleep((1.5 ** attempt) + random.uniform(0, 1))
                continue
            response.raise_for_status()
            data = response.json()
            text = data['choices'][0]['message']['content'].strip()
            if text:
                break
        except Exception:
            time.sleep((1.5 ** attempt) + random.uniform(0, 1))
            
    result = {
        "openalex_id": row["openalex_id"],
        "doi": row["doi"],
        "year": row["year"],
        "title": title,
        "human_abstract": row["abstract"],
        "ai_abstract": text
    }
    
    with csv_lock:
        df_row = pd.DataFrame([result])
        df_row.to_csv(out_file, mode='a', header=not os.path.exists(out_file), index=False)
        
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=10000)
    parser.add_argument("--workers", type=int, default=100)
    args = parser.parse_args()

    try:
        df = pd.read_csv("data/metadata/openalex_human_abstracts.csv")
    except FileNotFoundError:
        print("Error: human abstracts not found.")
        return
        
    if len(df) > args.limit:
        df = df.head(args.limit)
        
    os.makedirs("data/metadata", exist_ok=True)
    out_file = "data/metadata/synthetic_abstracts_multi_api.csv"
    
    processed_ids = set()
    if os.path.exists(out_file):
        try:
            existing_df = pd.read_csv(out_file)
            processed_ids = set(existing_df['openalex_id'].values)
            print(f"Found {len(processed_ids)} already generated abstracts. Resuming...")
        except:
            pass

    rows_to_process = [row for _, row in df.iterrows() if row["openalex_id"] not in processed_ids]
    
    if not rows_to_process:
        print("All requested abstracts are already generated!")
        return

    print(f"Generating {len(rows_to_process)} abstracts with {len(PROVIDERS)} verified endpoints and {args.workers} workers...")
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        future_to_row = {executor.submit(generate_abstract, row, out_file): row for row in rows_to_process}
        for future in tqdm(as_completed(future_to_row), total=len(rows_to_process), desc="Generating"):
            try:
                future.result()
            except:
                pass

    elapsed = time.time() - start_time
    print(f"Finished {len(rows_to_process)} abstracts in {elapsed:.2f}s ({elapsed/len(rows_to_process):.2f}s/abstract).")

if __name__ == "__main__":
    main()
