"""Cache current OpenAlex records and audit every stored source without altering it."""

import argparse
import gzip
import hashlib
from http.client import HTTPException
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd

from audit_recovered_data import sha256
from corrected_analysis import clean_text, normalize


PAPER = Path(__file__).resolve().parents[1]
OUTPUT = PAPER / "results/full_verification_20261005"
FIELDS = "id,doi,title,publication_year,language,type,abstract_inverted_index,is_retracted,primary_topic,primary_location,cited_by_count"


def invert(index):
    if not index:
        return ""
    positions = {}
    for word, indices in index.items():
        for i in indices:
            if i in positions:
                raise ValueError("Repeated abstract position")
            positions[i] = word
    return " ".join(positions[i] for i in sorted(positions))


def normalized_source(text):
    return clean_text(text or "").casefold()


def jaccard(a, b):
    left, right = set(a.split()), set(b.split())
    return len(left & right) / len(left | right) if left or right else 1.0


def fetch(ids, cache, singleton=False):
    key = hashlib.sha256((str(singleton) + "|".join(ids)).encode()).hexdigest()
    path = cache / (key + ".json.gz")
    if path.exists():
        with gzip.open(path, "rt") as stream:
            return json.load(stream)
    if singleton:
        url = "https://api.openalex.org/works/" + ids[0].rsplit("/", 1)[-1]
        url += "?" + urlencode({"select": FIELDS})
    else:
        url = "https://api.openalex.org/works?" + urlencode({
            "filter": "openalex_id:" + "|".join(i.rsplit("/", 1)[-1] for i in ids),
            "per_page": 100, "select": FIELDS})
    record = {"requested_ids": ids, "requested_url": url,
              "retrieved_utc": datetime.now(timezone.utc).isoformat(), "singleton": singleton}
    for attempt in range(4):
        try:
            request = Request(url, headers={"User-Agent": "Scientific-corpus-source-audit/1.0"})
            with urlopen(request, timeout=60) as response:
                raw = response.read()
                record.update({"status": response.status,
                               "response_sha256": hashlib.sha256(raw).hexdigest(),
                               "remaining_credits": response.headers.get("X-RateLimit-Remaining"),
                               "cost_usd": response.headers.get("X-RateLimit-Cost-USD"),
                               "data": json.loads(raw)})
            break
        except HTTPError as error:
            message = error.read().decode("utf-8", errors="replace")[:1500]
            record.update({"status": error.code, "error": message})
            if error.code == 429:
                # Do not retry a budget refusal in a polling loop.
                break
            if error.code not in (500, 502, 503, 504):
                break
            time.sleep(2 ** attempt)
        except (URLError, OSError, HTTPException, json.JSONDecodeError) as error:
            record.update({"status": "network_error", "error": str(error)[:500]})
            time.sleep(2 ** attempt)
    if record.get("status") == 200 or record.get("status") in (404, 410):
        with gzip.open(path, "wt") as stream:
            json.dump(record, stream)
    return record


def compare(row, fetched, record):
    result = {"source_id": row.openalex_id, "fetch_status": record.get("status"),
              "retrieved_utc": record.get("retrieved_utc"),
              "response_sha256": record.get("response_sha256", "")}
    if not fetched:
        result["source_status"] = "unresolved"
        return result
    try:
        current_text = invert(fetched.get("abstract_inverted_index"))
    except ValueError:
        result["source_status"] = "malformed_current_abstract"
        return result
    old_text, new_text = normalized_source(row.abstract), normalized_source(current_text)
    old_words, new_words = normalize(row.abstract), normalize(current_text)
    location = fetched.get("primary_location") or {}
    source = location.get("source") or {}
    topic = fetched.get("primary_topic") or {}
    result.update({
        "source_status": "retrieved", "current_id": fetched.get("id"),
        "id_agrees": row.openalex_id == fetched.get("id"),
        "title_agrees": normalize(row.title) == normalize(fetched.get("title") or ""),
        "title_word_jaccard": jaccard(normalize(row.title), normalize(fetched.get("title") or "")),
        "stored_title": row.title, "current_title": fetched.get("title"),
        "doi_agrees": normalized_source(row.doi) == normalized_source(fetched.get("doi")),
        "stored_doi": row.doi, "current_doi": fetched.get("doi"),
        "stored_year": row.year, "current_year": fetched.get("publication_year"),
        "year_agrees": float(row.year) == fetched.get("publication_year"),
        "current_language": fetched.get("language"), "current_type": fetched.get("type"),
        "current_retracted": fetched.get("is_retracted"), "current_source_type": source.get("type"),
        "current_source_name": source.get("display_name"), "current_has_abstract": bool(current_text),
        "abstract_exact_clean_match": bool(current_text) and old_text == new_text,
        "abstract_word_sequence_match": bool(current_text) and old_words == new_words,
        "abstract_word_jaccard": jaccard(old_words, new_words) if current_text else None,
        "stored_word_count": len(old_words.split()), "current_word_count": len(new_words.split()),
        "domain": (topic.get("domain") or {}).get("display_name"),
        "field": (topic.get("field") or {}).get("display_name"),
        "cited_by_count": fetched.get("cited_by_count"),
        "current_abstract_sha256": hashlib.sha256(current_text.encode()).hexdigest(),
    })
    result["source_consistent"] = bool(result["title_agrees"] and result["year_agrees"]
                                        and result["abstract_exact_clean_match"]
                                        and result["current_language"] == "en"
                                        and result["current_type"] == "article"
                                        and result["current_retracted"] is False)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--batch-cap", type=int, default=990)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    args.output.mkdir(exist_ok=True, parents=True)
    cache = args.output / "openalex_cache"
    cache.mkdir(exist_ok=True)
    source_path = PAPER / "data/metadata/openalex_human_abstracts.csv"
    human = pd.read_csv(source_path, keep_default_na=False)
    retained = set(pd.read_csv(PAPER / "results/correction_20261005/revision2/features.csv.gz", usecols=["pair_id"]).pair_id)
    indexed = human.set_index("openalex_id", drop=False)
    ids = sorted(retained) + sorted(set(human.openalex_id) - retained)
    batches = [ids[i:i+100] for i in range(0, min(len(ids), args.batch_cap*100), 100)]
    rows, pending, request_errors = [], [], []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        for i, record in enumerate(executor.map(lambda batch: fetch(batch, cache), batches), 1):
            results = (record.get("data") or {}).get("results", [])
            lookup = {r["id"]: r for r in results}
            for oid in record["requested_ids"]:
                if oid in lookup:
                    rows.append(compare(indexed.loc[oid], lookup[oid], record))
                else:
                    pending.append(oid)
            if record.get("status") != 200:
                request_errors.append({key: record.get(key) for key in ["requested_ids", "status", "error"]})
            if i % 25 == 0:
                print(f"Source audit: {i}/{len(batches)} batches; {len(rows):,} retrieved; {len(pending):,} pending singleton checks", flush=True)
    pending += ids[len(batches)*100:]
    # Single-entity retrieval is free under the documented API pricing. It also
    # resolves IDs that the service may redirect to merged records.
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        for i, record in enumerate(executor.map(lambda oid: fetch([oid], cache, True), pending), 1):
            data = record.get("data") if record.get("status") == 200 else None
            rows.append(compare(indexed.loc[record["requested_ids"][0]], data, record))
            if i % 100 == 0:
                print(f"Singleton checks: {i}/{len(pending)}", flush=True)
    table = pd.DataFrame(rows)
    assert len(table) == len(human) and table.source_id.is_unique
    table["in_revision2"] = table.source_id.isin(retained)
    table.to_csv(args.output / "source_checks.csv.gz", index=False, compression={"method": "gzip", "mtime": 0})
    summary = {"source_input_sha256": sha256(source_path), "records_checked": len(table),
               "retained_records": len(retained), "checks_completed_utc": datetime.now(timezone.utc).isoformat(),
               "batch_errors": request_errors, "scope": "Current OpenAlex index consistency, not independent verification of all publishers"}
    for label, subset in (("all", table), ("revision2", table[table.in_revision2])):
        summary[label] = {"records": len(subset), "status_counts": subset.source_status.value_counts().to_dict()}
        for col in ["title_agrees", "doi_agrees", "year_agrees", "current_has_abstract", "abstract_exact_clean_match", "abstract_word_sequence_match", "source_consistent", "current_retracted"]:
            summary[label][col] = int(subset[col].fillna(False).astype(bool).sum())
        for col in ["current_language", "current_type", "current_source_type", "domain"]:
            summary[label][col] = subset[col].fillna("unknown").value_counts().to_dict()
    (args.output / "source_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
