#!/usr/bin/env python3
"""
Collect comprehensive data for 5M+ AI paper analysis using OpenAlex abstract.search.
Every number is a direct API response. Outputs JSON for paper writing.
"""

import json, time, sys
import urllib.request, urllib.parse
from pathlib import Path

OUT = Path(__file__).parent.parent / "papers" / "verification_data"
OUT.mkdir(exist_ok=True)
EMAIL = "vedangvatsa@gmail.com"
SEARCH = "artificial intelligence|machine learning|deep learning|neural network|language model|reinforcement learning|computer vision|natural language|generative|autonomous"
YEARS = "2013-2026"

def fetch(url, retries=3):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": f"AI/1.0 (mailto:{EMAIL})"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            if i < retries - 1: time.sleep(2*(i+1))
            else: print(f"  FAIL: {e}"); return None

def ac(kw, year=YEARS):
    """Abstract search count."""
    params = {"filter": f"abstract.search:{kw},publication_year:{year}", "per_page": "1", "mailto": EMAIL}
    d = fetch(f"https://api.openalex.org/works?{urllib.parse.urlencode(params)}")
    return d["meta"]["count"] if d else 0

def tc(kw, year=YEARS):
    """Title search count."""
    params = {"filter": f"title.search:{kw},publication_year:{year}", "per_page": "1", "mailto": EMAIL}
    d = fetch(f"https://api.openalex.org/works?{urllib.parse.urlencode(params)}")
    return d["meta"]["count"] if d else 0

def group_by(field, extra_filter=""):
    """Group by with abstract search base."""
    f = f"abstract.search:{SEARCH},publication_year:{YEARS}"
    if extra_filter: f += f",{extra_filter}"
    params = {"filter": f, "group_by": field, "per_page": "200", "mailto": EMAIL}
    d = fetch(f"https://api.openalex.org/works?{urllib.parse.urlencode(params)}")
    return d.get("group_by", []) if d else []

results = {}

# ════════════════════════════════════════════════════════════════════
print("=" * 70)
print("COLLECTING DATA: 5M+ AI PAPERS VIA ABSTRACT SEARCH")
print("=" * 70)

# 1. Total
print("\n── 1. TOTAL CORPUS ──")
total = ac(SEARCH)
print(f"  Abstract corpus: {total:,}")
results["total"] = total

# 2. Year breakdown
print("\n── 2. YEAR BREAKDOWN ──")
yg = group_by("publication_year")
by_year = {}
for g in sorted(yg, key=lambda x: x["key"]):
    print(f"  {g['key']}: {g['count']:,}")
    by_year[str(g["key"])] = g["count"]
results["by_year"] = by_year

# 3. Document types
print("\n── 3. DOCUMENT TYPES ──")
tg = group_by("type")
doc_types = {}
for g in sorted(tg, key=lambda x: -x["count"]):
    if g["count"] > 1000:
        print(f"  {g['key_display_name']:<35} {g['count']:>10,}")
        doc_types[g["key_display_name"]] = g["count"]
results["doc_types"] = doc_types

# 4. Source types
print("\n── 4. SOURCE TYPES ──")
sg = group_by("primary_location.source.type")
src_types = {}
for g in sorted(sg, key=lambda x: -x["count"]):
    print(f"  {g.get('key_display_name', g['key']):<35} {g['count']:>10,}")
    src_types[g.get("key_display_name", g["key"])] = g["count"]
results["source_types"] = src_types

# 5. Open access
print("\n── 5. OPEN ACCESS ──")
oag = group_by("open_access.is_oa")
oa = {}
for g in oag:
    label = "open" if g["key"] == "true" else "closed"
    print(f"  {label}: {g['count']:,}")
    oa[label] = g["count"]
results["open_access"] = oa

# 6. Countries
print("\n── 6. COUNTRIES (top 20) ──")
cg = group_by("authorships.countries")
countries = {}
for g in sorted(cg, key=lambda x: -x["count"])[:20]:
    print(f"  {g['key_display_name']:<45} {g['count']:>10,}")
    countries[g["key_display_name"]] = g["count"]
results["countries"] = countries

# 7. Institutions
print("\n── 7. INSTITUTIONS (top 20) ──")
ig = group_by("authorships.institutions.lineage")
institutions = {}
for g in sorted(ig, key=lambda x: -x["count"])[:20]:
    print(f"  {g['key_display_name']:<55} {g['count']:>8,}")
    institutions[g["key_display_name"]] = g["count"]
results["institutions"] = institutions

# 8. Bigrams (abstract search)
print("\n── 8. BIGRAMS (abstract.search) ──")
bigrams_list = [
    "neural network", "machine learning", "artificial intelligence",
    "deep learning", "reinforcement learning", "natural language",
    "large language", "object detection", "transfer learning",
    "image segmentation", "image classification", "attention mechanism",
    "knowledge graph", "generative adversarial", "federated learning",
    "autonomous driving", "sentiment analysis", "speech recognition",
    "data augmentation", "self-supervised", "zero-shot", "graph neural",
    "text classification", "named entity", "semantic segmentation",
    "anomaly detection", "contrastive learning", "pose estimation",
    "few shot", "question answering", "medical imaging",
    "recommendation system", "feature extraction", "adversarial attack",
    "domain adaptation", "multi-modal", "vision transformer",
    "prompt engineering", "instruction tuning", "human feedback",
]
bigrams = {}
for bg in bigrams_list:
    c = ac(bg)
    if c > 0:
        print(f"  {bg:<30} {c:>10,}")
        bigrams[bg] = c
    time.sleep(0.12)
results["bigrams"] = bigrams

# 9. Trigrams
print("\n── 9. TRIGRAMS (abstract.search) ──")
trigrams_list = [
    "convolutional neural network", "recurrent neural network",
    "large language model", "deep reinforcement learning",
    "generative adversarial network", "graph neural network",
    "natural language processing", "long short-term memory",
    "medical image segmentation", "natural language understanding",
    "named entity recognition", "few shot learning",
    "image super resolution", "automatic speech recognition",
    "visual question answering", "point cloud processing",
    "deep neural network", "artificial neural network",
    "random forest classifier", "support vector machine",
    "recurrent neural network", "retrieval augmented generation",
    "vision language model", "instruction fine tuning",
    "chain of thought", "human feedback reinforcement",
]
trigrams = {}
for tg in trigrams_list:
    c = ac(tg)
    if c > 0:
        print(f"  {tg:<40} {c:>10,}")
        trigrams[tg] = c
    time.sleep(0.12)
results["trigrams"] = trigrams

# 10. Single keywords
print("\n── 10. KEYWORDS (abstract.search) ──")
keywords_list = [
    "learning", "network", "neural", "detection", "deep",
    "language", "intelligence", "classification", "recognition",
    "optimization", "prediction", "segmentation", "transformer",
    "generative", "autonomous", "robot", "knowledge", "adversarial",
    "embedding", "federated", "explainable", "diffusion", "multimodal",
    "fairness", "privacy", "interpretability", "clinical", "medical",
    "healthcare", "diagnosis", "fine-tuning", "distillation", "pruning",
    "pre-training", "benchmark", "reasoning", "hallucination",
    "guardrail", "alignment", "safety", "agent",
]
keywords = {}
for kw in keywords_list:
    c = ac(kw)
    if c > 0:
        print(f"  {kw:<25} {c:>10,}")
        keywords[kw] = c
    time.sleep(0.12)
results["keywords"] = keywords

# 11. Growth analysis (2025-2026 vs 2022-2023)
print("\n── 11. FASTEST-RISING (abstract.search, 2025-26 vs 2022-23) ──")
growth_candidates = [
    "deepseek", "rag", "claude", "llm", "gemini", "mistral",
    "retrieval-augmented", "guardrail", "hallucination",
    "chain-of-thought", "llama", "copilot", "reasoning",
    "multimodal", "fine-tuning", "prompt", "benchmark",
    "alignment", "tokenization", "diffusion", "synthetic",
    "chatgpt", "in-context", "instruction tuning",
    "preference optimization", "reward model", "human feedback",
    "vision language", "text-to-image", "code generation",
    "agentic", "foundation model", "distillation",
    "retrieval augmented generation", "grounding",
    "safe", "red teaming", "jailbreak",
]
growth = {}
print(f"{'Keyword':<35} {'2025-26':<12} {'2022-23':<12} {'Ratio':<10}")
for kw in growth_candidates:
    nc = ac(kw, "2025-2026")
    time.sleep(0.1)
    oc = ac(kw, "2022-2023")
    time.sleep(0.1)
    ratio = nc / max(oc, 1)
    if nc >= 50:
        print(f"  {kw:<33} {nc:<12,} {oc:<12,} {ratio:.1f}x")
        growth[kw] = {"new": nc, "old": oc, "ratio": round(ratio, 1)}
growth = dict(sorted(growth.items(), key=lambda x: -x[1]["ratio"]))
results["growth"] = growth

# 12. Year-by-year timelines for key methods
print("\n── 12. METHOD TIMELINES ──")
timeline_kws = {
    "neural network": range(2013, 2027),
    "deep learning": range(2013, 2027),
    "reinforcement learning": range(2013, 2027),
    "large language model": range(2018, 2027),
    "generative adversarial": range(2014, 2027),
    "diffusion model": range(2019, 2027),
    "federated learning": range(2017, 2027),
    "graph neural": range(2017, 2027),
    "transformer": range(2017, 2027),
    "knowledge graph": range(2013, 2027),
}
timelines = {}
for kw, yrs in timeline_kws.items():
    print(f"\n  {kw}:")
    tl = {}
    for y in yrs:
        c = ac(kw, str(y))
        print(f"    {y}: {c:,}")
        tl[str(y)] = c
        time.sleep(0.1)
    timelines[kw] = tl
results["timelines"] = timelines

# 13. Citation distribution
print("\n── 13. CITATION DISTRIBUTION ──")
cite_ranges = [
    ("0", "cited_by_count:0"),
    ("1-10", "cited_by_count:1-10"),
    ("11-50", "cited_by_count:11-50"),
    ("51-100", "cited_by_count:51-100"),
    ("101-500", "cited_by_count:101-500"),
    ("501-1000", "cited_by_count:501-1000"),
    ("1001+", "cited_by_count:>1000"),
]
cite_dist = {}
for label, filt in cite_ranges:
    f = f"abstract.search:{SEARCH},publication_year:{YEARS},{filt}"
    params = {"filter": f, "per_page": "1", "mailto": EMAIL}
    d = fetch(f"https://api.openalex.org/works?{urllib.parse.urlencode(params)}")
    c = d["meta"]["count"] if d else 0
    print(f"  {label:<20} {c:>10,}")
    cite_dist[label] = c
    time.sleep(0.15)
results["citation_dist"] = cite_dist

# Most cited
print("\n  Most cited papers:")
params = {
    "filter": f"abstract.search:{SEARCH},publication_year:{YEARS}",
    "sort": "cited_by_count:desc",
    "per_page": "10",
    "select": "title,cited_by_count,publication_year,authorships",
    "mailto": EMAIL,
}
d = fetch(f"https://api.openalex.org/works?{urllib.parse.urlencode(params)}")
top_cited = []
if d:
    for i, p in enumerate(d.get("results", []), 1):
        authors = p.get("authorships", [])
        first_author = authors[0]["author"]["display_name"] if authors else "Unknown"
        entry = {
            "title": p.get("title", ""),
            "citations": p.get("cited_by_count", 0),
            "year": p.get("publication_year", ""),
            "first_author": first_author,
        }
        top_cited.append(entry)
        print(f"  {i}. [{entry['citations']:,}] {entry['title'][:70]} ({entry['year']})")
results["top_cited"] = top_cited

# 14. Title vs Abstract comparison
print("\n── 14. TITLE vs ABSTRACT COMPARISON ──")
compare_kws = [
    "neural network", "machine learning", "deep learning",
    "large language model", "reinforcement learning",
    "generative adversarial", "diffusion model", "federated learning",
    "retrieval augmented", "hallucination", "transformer",
    "knowledge graph", "explainable", "fairness",
]
comparison = {}
print(f"  {'Keyword':<30} {'Title':<12} {'Abstract':<12} {'Ratio':<8}")
for kw in compare_kws:
    t_c = tc(kw)
    time.sleep(0.1)
    a_c = ac(kw)
    time.sleep(0.1)
    ratio = a_c / max(t_c, 1)
    print(f"  {kw:<30} {t_c:<12,} {a_c:<12,} {ratio:.1f}x")
    comparison[kw] = {"title": t_c, "abstract": a_c, "ratio": round(ratio, 1)}
results["title_vs_abstract"] = comparison

# Save
outfile = OUT / "abstract_corpus_analysis.json"
with open(outfile, "w") as f:
    json.dump(results, f, indent=2)
print(f"\n{'='*70}")
print(f"ALL DATA SAVED TO {outfile}")
print(f"Total corpus: {total:,} papers")
print(f"{'='*70}")
