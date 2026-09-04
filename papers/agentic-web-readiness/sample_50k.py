"""Deterministic stratified 50k sampler: Tranco primary frame, CrUX overlap flag.

Frame sources (downloaded, see manifest):
- Tranco daily top-1m (rank, domain)
- CrUX global current (origin, rank bucket) via zakird/crux-top-lists

Design:
- Tier 1: Tranco ranks 1-10,000 -> census 10,000 domains
- Tier 2: Tranco ranks 10,001-100,000 -> random 20,000 (seed 20260903)
- Tier 3: Tranco ranks 100,001-1,000,000 -> random 20,000 (seed 20260903)
- Total: 50,000. CrUX overlap recorded as popularity cross-check, not a filter.

Outputs:
- sample.csv (domain, tranco_rank, tier, crux_overlap)
- domains.txt (one domain per line, scan order)
- manifest.json (sources, dates, sha256, seed, counts)
"""
import csv, gzip, hashlib, json, random, zipfile
from pathlib import Path
from urllib.parse import urlparse

BASE = Path(__file__).parent
DATA = BASE / "data"
SEED = 20260903

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def load_tranco() -> list[tuple[int, str]]:
    zpath = DATA / "tranco-top-1m.csv.zip"
    with zipfile.ZipFile(zpath) as z:
        name = z.namelist()[0]
        with z.open(name) as f:
            rows = []
            for line in f:
                line = line.decode().strip()
                if not line:
                    continue
                rank_s, domain = line.split(",", 1)
                rows.append((int(rank_s), domain.strip().lower()))
    return rows

def load_crux_hosts() -> set[str]:
    gpath = DATA / "crux-current.csv.gz"
    hosts = set()
    with gzip.open(gpath, "rt") as f:
        reader = csv.DictReader(f)
        for row in reader:
            origin = (row.get("origin") or "").strip()
            if not origin:
                continue
            try:
                host = urlparse(origin).hostname or ""
            except Exception:
                continue
            if host.startswith("www."):
                host = host[4:]
            if host:
                hosts.add(host.lower())
    return hosts

def main() -> None:
    rng = random.Random(SEED)
    tranco = load_tranco()
    crux = load_crux_hosts()
    by_rank = {d: r for r, d in tranco}

    tier1 = [d for r, d in tranco if 1 <= r <= 10_000]
    tier2 = [d for r, d in tranco if 10_001 <= r <= 100_000]
    tier3 = [d for r, d in tranco if 100_001 <= r <= 1_000_000]
    assert len(tier1) == 10_000, len(tier1)
    s2 = rng.sample(tier2, 20_000)
    s3 = rng.sample(tier3, 20_000)
    sample = tier1 + s2 + s3
    assert len(sample) == 50_000

    def tier_of(domain: str) -> str:
        r = by_rank[domain]
        if r <= 10_000:
            return "tier1_top10k"
        if r <= 100_000:
            return "tier2_10k_100k"
        return "tier3_100k_1m"

    with open(DATA / "sample.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["domain", "tranco_rank", "tier", "crux_overlap"])
        for d in sample:
            w.writerow([d, by_rank[d], tier_of(d), 1 if d in crux or ("www." + d) in crux else 0])

    with open(DATA / "domains.txt", "w") as f:
        for d in sample:
            f.write(d + "\n")

    # overlap stats for the paper (computed, not claimed)
    overlap = sum(1 for d in sample if d in crux)
    manifest = {
        "seed": SEED,
        "total": len(sample),
        "tiers": {
            "tier1_top10k": 10_000,
            "tier2_10k_100k": 20_000,
            "tier3_100k_1m": 20_000,
        },
        "crux_overlap_count": overlap,
        "sources": {
            "tranco": "tranco-list.eu/download/daily/top-1m.csv.zip (downloaded 2026-09-03)",
            "crux": "github.com/zakird/crux-top-lists data/global/current.csv.gz (downloaded 2026-09-03)",
        },
        "sha256": {
            "tranco-top-1m.csv.zip": sha256_file(DATA / "tranco-top-1m.csv.zip"),
            "crux-current.csv.gz": sha256_file(DATA / "crux-current.csv.gz"),
        },
    }
    with open(DATA / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    print(json.dumps({**manifest, "sha256": "omitted"}, indent=2))

if __name__ == "__main__":
    main()
