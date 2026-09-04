"""Summarize 50k scan results into paper tables. Recomputes layer shares from
the stored per-check map so scoring bugs surface as mismatches.
Reads: data/results.jsonl, data/sample.csv
Writes: data/summary.json (printed to stdout as well).
"""
import csv, json
from pathlib import Path
from collections import Counter, defaultdict

BASE = Path(__file__).parent
DATA = BASE / "data"

CHECKS = ["robots-ai-policy", "llms-txt", "markdown-negotiation", "bot-ua-access",
          "mcp-server-live", "openapi-spec", "https-tls", "security-txt",
          "json-ld", "seo-author-eeat", "agent-payments"]

def main() -> None:
    tiers = {}
    with open(DATA / "sample.csv") as f:
        for row in csv.DictReader(f):
            tiers[row["domain"]] = row["tier"]
    rows = []
    gentle = DATA / "results-gentle.jsonl"
    src = gentle if gentle.exists() else DATA / "results.jsonl"
    for line in open(src):
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    done = {r.get("domain") for r in rows}
    scored = [r for r in rows if "score" in r]
    errors = [r for r in rows if "error" in r]
    by_tier = defaultdict(list)
    for r in scored:
        by_tier[tiers.get(r["domain"], "unknown")].append(r["score"])
    adoption = {}
    for c in CHECKS:
        passes = sum(1 for r in scored if r.get("checks", {}).get(c) == "pass")
        adoption[c] = {"pass": passes, "n": len(scored),
                       "share": round(passes / len(scored), 4) if scored else 0.0}
    status_counts = Counter("error" if "error" in r else "completed" for r in rows)
    summary = {
        "attempted_domains": len(done),
        "completed": len(scored),
        "errors": len(errors),
        "status_counts": dict(status_counts),
        "mean_score": round(sum(r["score"] for r in scored) / len(scored), 1) if scored else None,
        "tier_means": {t: round(sum(v) / len(v), 1) for t, v in by_tier.items() if v},
        "tier_n": {t: len(v) for t, v in by_tier.items()},
        "adoption_tracked_checks": adoption,
    }
    with open(DATA / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
