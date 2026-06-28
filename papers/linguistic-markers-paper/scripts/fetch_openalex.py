import os
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import time
import random

def fetch_page(page, per_page=50, max_retries=5):
    url = "https://api.openalex.org/works"
    params = {
        "filter": "has_abstract:true,language:en,publication_year:2018-2019,type:article",
        "search": "applied linguistics",
        "select": "title,abstract_inverted_index,id,doi,publication_year",
        "per-page": per_page,
        "page": page,
        "mailto": "contact@veda.ng"
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 429:
                sleep_time = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(sleep_time)
                continue
                
            response.raise_for_status()
            data = response.json()
            
            page_results = []
            for work in data.get("results", []):
                inverted_index = work.get("abstract_inverted_index")
                if not inverted_index:
                    continue
                    
                try:
                    word_positions = {}
                    for word, positions in inverted_index.items():
                        for pos in positions:
                            word_positions[pos] = word
                    abstract_text = " ".join([word_positions[i] for i in sorted(word_positions.keys())])
                    
                    page_results.append({
                        "openalex_id": work["id"],
                        "doi": work.get("doi"),
                        "year": work["publication_year"],
                        "title": work["title"],
                        "abstract": abstract_text
                    })
                except Exception:
                    continue
            return page_results
        except Exception as e:
            sleep_time = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(sleep_time)
    
    print(f"Failed to fetch page {page} after {max_retries} retries.")
    return []

def fetch_abstracts(limit=10000, per_page=50, max_workers=3):
    print(f"Fetching {limit} abstracts from OpenAlex with {max_workers} workers...")
    total_pages = limit // per_page
    if limit % per_page > 0:
        total_pages += 1
        
    os.makedirs("data/metadata", exist_ok=True)
    out_file = "data/metadata/openalex_human_abstracts.csv"
    
    # Initialize empty CSV with headers
    pd.DataFrame(columns=["openalex_id", "doi", "year", "title", "abstract"]).to_csv(out_file, index=False)
    
    total_fetched = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_page = {executor.submit(fetch_page, p, per_page): p for p in range(1, total_pages + 1)}
        
        for future in tqdm(as_completed(future_to_page), total=total_pages, desc="Pages"):
            page_data = future.result()
            
            if page_data:
                # Save chunks iteratively so we don't lose progress
                df_chunk = pd.DataFrame(page_data)
                df_chunk.to_csv(out_file, mode='a', header=False, index=False)
                total_fetched += len(page_data)
            
            if total_fetched >= limit:
                break

    print(f"Successfully fetched and saved abstracts to {out_file}.")

if __name__ == "__main__":
    fetch_abstracts(limit=10000, max_workers=5)
