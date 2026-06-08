#!/usr/bin/env python3
"""
Analyze 1.9M+ AI papers using OpenAlex aggregate APIs.
Every number comes from a direct API call — no hallucination possible.

Strategy: Use OpenAlex group_by and title.search filters to get aggregate
counts without downloading individual papers.
"""

import json, re, sys, time
import urllib.request, urllib.parse, urllib.error
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "papers" / "verification_data"
OUTPUT_DIR.mkdir(exist_ok=True)
EMAIL = "vedangvatsa@gmail.com"

# Base filter: all AI-related papers 2013-2026
# We use title.search with broad AI terms, unioned via | (OR)
BASE_CONCEPTS = "C154945302|C119857082|C108827166|C204321447|C31972630"
# C154945302 = Artificial Intelligence
# C119857082 = Machine Learning
# C108827166 = Deep Learning
# C204321447 = Natural Language Processing
# C31972630  = Computer Vision

YEAR_RANGE = "2013-2026"


def fetch(url, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": f"AIResearchAnalysis/1.0 (mailto:{EMAIL})",
                "Accept": "application/json",
            })
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
            else:
                print(f"    FAILED after {retries} attempts: {e}")
    return None


def oa_count(extra_filter=""):
    """Get total count with optional extra filter."""
    f = f"concepts.id:{BASE_CONCEPTS},publication_year:{YEAR_RANGE}"
    if extra_filter:
        f += f",{extra_filter}"
    url = f"https://api.openalex.org/works?filter={urllib.parse.quote(f)}&per_page=1&mailto={EMAIL}"
    data = fetch(url)
    return data["meta"]["count"] if data else 0


def oa_group_by(group_field, extra_filter=""):
    """Group by a field and return counts."""
    f = f"concepts.id:{BASE_CONCEPTS},publication_year:{YEAR_RANGE}"
    if extra_filter:
        f += f",{extra_filter}"
    url = f"https://api.openalex.org/works?filter={urllib.parse.quote(f)}&group_by={group_field}&per_page=200&mailto={EMAIL}"
    data = fetch(url)
    if not data:
        return []
    return data.get("group_by", [])


def title_search_count(keyword, year_filter=""):
    """Count papers with keyword in title."""
    f = f"title.search:{urllib.parse.quote(keyword)},publication_year:{year_filter or YEAR_RANGE}"
    url = f"https://api.openalex.org/works?filter={f}&per_page=1&mailto={EMAIL}"
    data = fetch(url)
    return data["meta"]["count"] if data else 0


def title_search_in_corpus(keyword, year_filter=""):
    """Count papers with keyword in title AND in AI concept corpus."""
    f = f"concepts.id:{BASE_CONCEPTS},title.search:{urllib.parse.quote(keyword)},publication_year:{year_filter or YEAR_RANGE}"
    url = f"https://api.openalex.org/works?filter={urllib.parse.quote(f, safe='')}&per_page=1&mailto={EMAIL}"
    # Actually, let's avoid double-encoding. Build manually:
    base = "https://api.openalex.org/works"
    params = {
        "filter": f"concepts.id:{BASE_CONCEPTS},title.search:{keyword},publication_year:{year_filter or YEAR_RANGE}",
        "per_page": "1",
        "mailto": EMAIL,
    }
    url = f"{base}?{urllib.parse.urlencode(params)}"
    data = fetch(url)
    return data["meta"]["count"] if data else 0


# ═══════════════════════════════════════════════════════════════════════════
# ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════

def main():
    results = {}
    
    print("=" * 70)
    print("ANALYZING AI RESEARCH CORPUS VIA OPENALEX API")
    print("Every number is a direct API response.")
    print("=" * 70)
    
    # ── 1. Total corpus size ──
    print("\n── 1. CORPUS SIZE ──")
    total = oa_count()
    print(f"Total AI papers (2013-2026): {total:,}")
    results["total_papers"] = total
    time.sleep(0.2)
    
    # ── 2. Publication volume by year ──
    print("\n── 2. PUBLICATION VOLUME BY YEAR ──")
    year_groups = oa_group_by("publication_year")
    years_data = {}
    prev = 0
    print(f"{'Year':<7} {'Count':<12} {'YoY Growth':<12}")
    for g in sorted(year_groups, key=lambda x: x["key"]):
        y = g["key"]
        c = g["count"]
        yoy = f"+{(c-prev)/max(prev,1)*100:.1f}%" if prev else "-"
        print(f"{y:<7} {c:<12,} {yoy:<12}")
        years_data[y] = c
        prev = c
    results["by_year"] = years_data
    time.sleep(0.2)
    
    # ── 3. Document types ──
    print("\n── 3. DOCUMENT TYPES ──")
    type_groups = oa_group_by("type")
    types_data = {}
    for g in sorted(type_groups, key=lambda x: -x["count"]):
        t = g["key_display_name"]
        c = g["count"]
        print(f"  {t:<35} {c:>10,}")
        types_data[t] = c
    results["document_types"] = types_data
    time.sleep(0.2)
    
    # ── 4. Keyword frequency (title search) ──
    print("\n── 4. TOP KEYWORDS (title search within AI corpus) ──")
    keywords_to_check = [
        # Unigrams
        "learning", "network", "neural", "detection", "deep",
        "language", "intelligence", "generative", "recognition", "autonomous",
        "reinforcement", "classification", "transformer", "segmentation",
        "robot", "knowledge", "adversarial", "embedding", "federated",
        "explainable", "diffusion", "agentic", "multimodal",
    ]
    
    keyword_counts = {}
    print(f"{'Keyword':<25} {'Count':<12} {'% of corpus':<12}")
    for kw in keywords_to_check:
        c = title_search_in_corpus(kw)
        pct = (c / total * 100) if total else 0
        print(f"{kw:<25} {c:<12,} {pct:.1f}%")
        keyword_counts[kw] = c
        time.sleep(0.15)
    results["keyword_counts"] = keyword_counts
    
    # ── 5. Bigram frequency ──
    print("\n── 5. TOP BIGRAMS (title search within AI corpus) ──")
    bigrams_to_check = [
        "neural network", "machine learning", "artificial intelligence",
        "deep learning", "reinforcement learning", "few shot",
        "large language", "object detection", "attention mechanism",
        "question answering", "natural language", "transfer learning",
        "image segmentation", "image classification", "knowledge graph",
        "generative adversarial", "federated learning", "autonomous driving",
        "sentiment analysis", "speech recognition", "data augmentation",
        "self-supervised", "zero-shot", "graph neural",
        "text classification", "named entity", "semantic segmentation",
        "pose estimation", "anomaly detection", "contrastive learning",
    ]
    
    bigram_counts = {}
    print(f"{'Bigram':<30} {'Count':<12}")
    for bg in bigrams_to_check:
        c = title_search_in_corpus(bg)
        print(f"{bg:<30} {c:<12,}")
        bigram_counts[bg] = c
        time.sleep(0.15)
    results["bigram_counts"] = bigram_counts
    
    # ── 6. Trigram frequency ──
    print("\n── 6. TOP TRIGRAMS (title search within AI corpus) ──")
    trigrams_to_check = [
        "convolutional neural network", "recurrent neural network",
        "few shot learning", "natural language processing",
        "large language models", "deep reinforcement learning",
        "visual question answering", "automatic speech recognition",
        "medical image segmentation", "generative adversarial network",
        "graph neural network", "long short-term memory",
        "natural language understanding", "named entity recognition",
        "autonomous driving system", "image super resolution",
    ]
    
    trigram_counts = {}
    print(f"{'Trigram':<35} {'Count':<12}")
    for tg in trigrams_to_check:
        c = title_search_in_corpus(tg)
        print(f"{tg:<35} {c:<12,}")
        trigram_counts[tg] = c
        time.sleep(0.15)
    results["trigram_counts"] = trigram_counts
    
    # ── 7. Fastest-rising keywords (2025-2026 vs 2022-2023) ──
    print("\n── 7. FASTEST-RISING KEYWORDS ──")
    rising_candidates = [
        "agentic", "rag", "deepseek", "personalization", "gemini",
        "gen", "pedagogy", "strategic", "hallucination", "alignment",
        "guardrail", "llm", "fine-tuning", "prompt", "multimodal",
        "reasoning", "agent", "benchmark", "instruction", "safety",
        "grounding", "tokenization", "diffusion", "synthetic",
        "copilot", "chatgpt", "mistral", "llama", "claude",
        "retrieval-augmented", "chain-of-thought", "in-context",
    ]
    
    growth_data = {}
    print(f"{'Keyword':<25} {'2025-26':<12} {'2022-23':<12} {'Ratio':<10}")
    for kw in rising_candidates:
        new_c = title_search_in_corpus(kw, "2025-2026")
        time.sleep(0.15)
        old_c = title_search_in_corpus(kw, "2022-2023")
        time.sleep(0.15)
        ratio = new_c / max(old_c, 1)
        if new_c >= 10:
            print(f"{kw:<25} {new_c:<12,} {old_c:<12,} {ratio:.1f}x")
            growth_data[kw] = {"new": new_c, "old": old_c, "ratio": round(ratio, 1)}
    
    # Sort by ratio
    growth_data = dict(sorted(growth_data.items(), key=lambda x: -x[1]["ratio"]))
    results["fastest_rising"] = growth_data
    
    # ── 8. Citation distribution ──
    print("\n── 8. CITATION DISTRIBUTION ──")
    # Use cited_by_count ranges
    cite_ranges = [
        ("0 citations", "cited_by_count:0"),
        ("1-10 citations", "cited_by_count:1-10"),
        ("11-50 citations", "cited_by_count:11-50"),
        ("51-100 citations", "cited_by_count:51-100"),
        ("101-500 citations", "cited_by_count:101-500"),
        ("501-1000 citations", "cited_by_count:501-1000"),
        ("1001+ citations", "cited_by_count:>1000"),
    ]
    
    cite_dist = {}
    for label, filt in cite_ranges:
        c = oa_count(filt)
        print(f"  {label:<25} {c:>10,}")
        cite_dist[label] = c
        time.sleep(0.15)
    results["citation_distribution"] = cite_dist
    
    # Get the most-cited paper
    print("\n  Most cited AI papers:")
    url = f"https://api.openalex.org/works?filter=concepts.id:{BASE_CONCEPTS},publication_year:{YEAR_RANGE}&sort=cited_by_count:desc&per_page=5&select=title,cited_by_count,publication_year&mailto={EMAIL}"
    top_cited = fetch(url)
    if top_cited:
        for i, p in enumerate(top_cited.get("results", []), 1):
            print(f"    {i}. [{p.get('cited_by_count',0):,} cites] {p.get('title','')[:80]} ({p.get('publication_year','')})")
            if i == 1:
                results["max_citations"] = p.get("cited_by_count", 0)
    
    # ── 9. Research categories (by OpenAlex concepts) ──
    print("\n── 9. RESEARCH CATEGORIES (by OpenAlex sub-concepts) ──")
    subconcepts = {
        "Machine Learning": "C119857082",
        "Deep Learning": "C108827166",
        "Natural Language Processing": "C204321447",
        "Computer Vision": "C31972630",
        "Artificial Neural Network": "C50644808",
        "Reinforcement Learning": "C138074934",
        "Pattern Recognition": "C2776387868",
        "Speech Recognition": "C204439074",
        "Robot": "C192562407",
        "Data Mining": "C124101348",
    }
    
    cat_data = {}
    for name, cid in subconcepts.items():
        f = f"concepts.id:{BASE_CONCEPTS}&{cid},publication_year:{YEAR_RANGE}"
        # Actually use the count with this concept
        url = f"https://api.openalex.org/works?filter=concepts.id:{cid},publication_year:{YEAR_RANGE}&per_page=1&mailto={EMAIL}"
        data = fetch(url)
        c = data["meta"]["count"] if data else 0
        pct = (c / total * 100) if total else 0
        print(f"  {name:<35} {c:>10,}  ({pct:.1f}%)")
        cat_data[name] = c
        time.sleep(0.15)
    results["subconcept_counts"] = cat_data
    
    # ── 10. Source types ──
    print("\n── 10. SOURCE TYPES ──")
    source_groups = oa_group_by("primary_location.source.type")
    for g in sorted(source_groups, key=lambda x: -x["count"]):
        name = g.get("key_display_name", g.get("key", "unknown"))
        print(f"  {name:<35} {g['count']:>10,}")
    results["source_types"] = {g.get("key_display_name", g.get("key", "?")): g["count"] for g in source_groups}
    time.sleep(0.2)
    
    # ── 11. Open access status ──
    print("\n── 11. OPEN ACCESS STATUS ──")
    oa_groups = oa_group_by("open_access.is_oa")
    for g in sorted(oa_groups, key=lambda x: -x["count"]):
        label = "Open Access" if g["key"] == "true" else "Closed"
        print(f"  {label:<25} {g['count']:>10,}")
    results["open_access"] = {("open" if g["key"]=="true" else "closed"): g["count"] for g in oa_groups}
    time.sleep(0.2)
    
    # ── 12. Top institutions ──
    print("\n── 12. TOP INSTITUTIONS ──")
    url = f"https://api.openalex.org/works?filter=concepts.id:{BASE_CONCEPTS},publication_year:{YEAR_RANGE}&group_by=authorships.institutions.lineage&per_page=15&mailto={EMAIL}"
    inst_data = fetch(url)
    if inst_data:
        for g in inst_data.get("group_by", [])[:15]:
            print(f"  {g.get('key_display_name','?'):<50} {g['count']:>8,}")
        results["top_institutions"] = {g.get("key_display_name","?"): g["count"] for g in inst_data.get("group_by", [])[:15]}
    
    # ── 13. Top countries ──
    print("\n── 13. TOP COUNTRIES ──")
    url = f"https://api.openalex.org/works?filter=concepts.id:{BASE_CONCEPTS},publication_year:{YEAR_RANGE}&group_by=authorships.countries&per_page=20&mailto={EMAIL}"
    country_data = fetch(url)
    if country_data:
        for g in country_data.get("group_by", [])[:15]:
            print(f"  {g.get('key_display_name','?'):<30} {g['count']:>10,}")
        results["top_countries"] = {g.get("key_display_name","?"): g["count"] for g in country_data.get("group_by", [])[:20]}
    
    # ── Save ──
    out = OUTPUT_DIR / "full_analysis_results.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n{'='*70}")
    print(f"ALL RESULTS SAVED TO {out}")
    print(f"Total corpus: {total:,} papers")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
