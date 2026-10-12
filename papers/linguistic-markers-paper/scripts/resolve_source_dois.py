"""Try documented DOI singleton lookups for missing source IDs; preserve the ID audit."""

import gzip
import hashlib
import json
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from http.client import HTTPException
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

import pandas as pd

from audit_all_sources import FIELDS, compare
from audit_recovered_data import sha256

PAPER = Path(__file__).resolve().parents[1]
ROOT = PAPER / "results/full_verification_20261005"


def lookup(row):
    url = "https://api.openalex.org/works/" + quote(row.doi, safe="") + "?" + urlencode({"select": FIELDS})
    path = ROOT / "openalex_cache" / ("doi_" + hashlib.sha256(url.encode()).hexdigest() + ".json.gz")
    if path.exists():
        with gzip.open(path, "rt") as stream:
            return json.load(stream)
    record = {"requested_ids": [row.openalex_id], "requested_url": url, "singleton": True,
              "resolution_method": "doi", "retrieved_utc": datetime.now(timezone.utc).isoformat()}
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers={"User-Agent": "Scientific-corpus-source-audit/1.0"}), timeout=45) as response:
                data = response.read()
                record.update({"status": response.status, "response_sha256": hashlib.sha256(data).hexdigest(),
                               "data": json.loads(data)})
            break
        except HTTPError as error:
            record.update({"status": error.code, "error": error.read().decode(errors="replace")[:500]})
            if error.code not in (500, 502, 503, 504):
                break
        except (URLError, OSError, HTTPException, json.JSONDecodeError) as error:
            record.update({"status": "network_error", "error": str(error)[:300]})
        time.sleep(2 ** attempt)
    with gzip.open(path, "wt") as stream:
        json.dump(record, stream)
    return record


def main():
    checks = pd.read_csv(ROOT / "source_checks.csv.gz", low_memory=False)
    original = pd.read_csv(PAPER / "data/metadata/openalex_human_abstracts.csv", keep_default_na=False)
    missing = set(checks.loc[checks.source_status.eq("unresolved"), "source_id"])
    candidates = original[original.openalex_id.isin(missing) & original.doi.str.match(r"https://doi\.org/10\.\d{4,9}/\S+")]
    rows = list(candidates.itertuples(index=False))
    indexed = checks.set_index("source_id", drop=False)
    details, resolved = [], 0
    with ThreadPoolExecutor(max_workers=4) as executor:
        for row, response in zip(rows, executor.map(lookup, rows)):
            data = response.get("data")
            valid = bool(response.get("status") == 200 and data and
                         str(data.get("doi", "")).lower() == row.doi.lower())
            details.append({"source_id": row.openalex_id, "doi": row.doi,
                            "status": response.get("status"), "resolved_by_matching_doi": valid})
            if valid:
                result = compare(row, data, response)
                result["in_revision2"] = indexed.at[row.openalex_id, "in_revision2"]
                for key, value in result.items():
                    indexed.at[row.openalex_id, key] = value
                resolved += 1
    combined = indexed.reset_index(drop=True)
    combined.to_csv(ROOT / "source_checks_resolved.csv.gz", index=False, compression={"method": "gzip", "mtime": 0})
    summary = json.loads((ROOT / "source_summary.json").read_text())
    summary["doi_fallback"] = {"attempted": len(rows), "resolved": resolved, "results": details}
    for label, subset in (("all", combined), ("revision2", combined[combined.in_revision2.map(lambda v: str(v).lower() == "true")])):
        summary[label] = {"records": len(subset), "status_counts": subset.source_status.value_counts().to_dict()}
        for col in ["title_agrees", "doi_agrees", "year_agrees", "current_has_abstract", "abstract_exact_clean_match", "abstract_word_sequence_match", "source_consistent", "current_retracted"]:
            summary[label][col] = int(subset[col].map(lambda v: str(v).lower() == "true").sum())
        for col in ["current_language", "current_type", "current_source_type", "domain"]:
            summary[label][col] = subset[col].fillna("unknown").value_counts().to_dict()
    summary["resolved_checks_sha256"] = sha256(ROOT / "source_checks_resolved.csv.gz")
    (ROOT / "source_summary_resolved.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({"doi_fallback_attempts": len(rows), "doi_fallback_resolved": resolved,
                      "all_statuses": summary["all"]["status_counts"],
                      "retained_statuses": summary["revision2"]["status_counts"],
                      "source_consistent_retained_pairs": summary["revision2"]["source_consistent"]}, indent=2))


if __name__ == "__main__":
    main()
