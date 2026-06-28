import requests

def fetch_page(page, per_page=5):
    url = "https://api.openalex.org/works"
    params = {
        "filter": "has_abstract:true,language:en,publication_year:2018-2019,type:article",
        "search": "applied linguistics",
        "select": "title,abstract_inverted_index,id,doi,publication_year",
        "per-page": per_page,
        "page": page,
        "mailto": "contact@veda.ng"
    }
    
    response = requests.get(url, params=params, timeout=15)
    print(f"Status Code: {response.status_code}")
    if response.status_code != 200:
        print(response.text)
        return
        
    data = response.json()
    results = data.get("results", [])
    print(f"Number of results returned: {len(results)}")
    if results:
        work = results[0]
        print(f"Keys in first result: {work.keys()}")
        print(f"Has abstract index: {bool(work.get('abstract_inverted_index'))}")
        
if __name__ == "__main__":
    fetch_page(1)
