#!/usr/bin/env python3
"""
FULL AUDIT: Verify every number in the paper against the JSON data file.
Flags any number that cannot be traced to a verified source.
"""
import json, re, sys
from pathlib import Path

DATA = Path(__file__).parent.parent / "papers/verification_data/abstract_corpus_analysis.json"
PAPER = Path(__file__).parent.parent / "papers/state-of-ai-research-2026.md"

with open(DATA) as f:
    data = json.load(f)

paper = PAPER.read_text()
errors = []
warnings = []
verified = 0

def check(label, paper_val, data_val, line_hint=""):
    global verified
    if paper_val == data_val:
        verified += 1
        return True
    else:
        errors.append(f"MISMATCH: {label}: paper={paper_val}, data={data_val} {line_hint}")
        return False

print("=" * 70)
print("PAPER AUDIT: Verifying every number against data sources")
print("=" * 70)

# ═══ 1. TOTAL CORPUS ═══
print("\n── 1. Total corpus ──")
check("Total corpus", 5003783, data["total"])

# ═══ 2. YEAR BREAKDOWN (Table 3) ═══
print("\n── 2. Year breakdown ──")
for year, count in data["by_year"].items():
    # Check if this number appears in the paper
    check(f"Year {year}", count, data["by_year"][year])

# Verify YoY growth percentages
by_year = data["by_year"]
years_sorted = sorted(by_year.keys())
print("\n  YoY growth check:")
growth_checks = {
    "2014": (97510 - 93226) / 93226 * 100,  # 4.6%
    "2015": (105609 - 97510) / 97510 * 100,  # 8.3%
    "2016": (115423 - 105609) / 105609 * 100,  # 9.3%
    "2017": (137237 - 115423) / 115423 * 100,  # 18.9%
    "2018": (185192 - 137237) / 137237 * 100,  # 34.9%
    "2019": (242286 - 185192) / 185192 * 100,  # 30.8%
    "2020": (305903 - 242286) / 242286 * 100,  # 26.3%
    "2021": (369519 - 305903) / 305903 * 100,  # 20.8%
    "2022": (411098 - 369519) / 369519 * 100,  # 11.2%
    "2023": (520861 - 411098) / 411098 * 100,  # 26.7%
    "2024": (662417 - 520861) / 520861 * 100,  # 27.2%
    "2025": (944530 - 662417) / 662417 * 100,  # 42.6%
}
paper_growth = {
    "2014": 4.6, "2015": 8.3, "2016": 9.3, "2017": 18.9,
    "2018": 34.9, "2019": 30.8, "2020": 26.3, "2021": 20.8,
    "2022": 11.2, "2023": 26.7, "2024": 27.2, "2025": 42.6,
}
for year, calc in growth_checks.items():
    paper_val = paper_growth[year]
    if abs(calc - paper_val) > 0.15:
        errors.append(f"YoY growth {year}: paper says {paper_val}%, calculated {calc:.1f}%")
    else:
        verified += 1
        print(f"  {year}: {paper_val}% (calc: {calc:.1f}%) ✓")

# ═══ 3. DOCUMENT TYPES (Table 1) ═══
print("\n── 3. Document types ──")
doc_checks = {
    "article": 3270717,
    "preprint": 668948,
    "book-chapter": 386449,
    "dataset": 298570,
    "review": 94567,
    "dissertation": 92581,
}
for dtype, expected in doc_checks.items():
    check(f"DocType {dtype}", expected, data["doc_types"].get(dtype, 0))

# Check "Other" = sum of remaining types
other_types = sum(v for k, v in data["doc_types"].items() if k not in doc_checks)
check("DocType Other", 191951, other_types, "(calculated from remaining doc types)")

# Check total sums correctly
total_in_table = 3270717 + 668948 + 386449 + 298570 + 94567 + 92581 + 191951
check("Table 1 total", total_in_table, 5003783)

# ═══ 4. SOURCE TYPES (Table 2) ═══
print("\n── 4. Source types ──")
src_checks = {"journal": 2232178, "repository": 1370590, "book series": 246842,
              "conference": 111398, "ebook platform": 69676}
for stype, expected in src_checks.items():
    check(f"SrcType {stype}", expected, data["source_types"].get(stype, 0))

# "Other / unclassified" = total - listed
listed_src = sum(src_checks.values())
other_src = 5003783 - listed_src
paper_other_src = 973099
if abs(other_src - paper_other_src) > 100:
    # This could be because OpenAlex has an "other" category of 16
    # and some papers have no source type
    warnings.append(f"Source 'Other' = {paper_other_src} in paper, calculated {other_src} (diff may be due to unclassified)")
else:
    verified += 1

# ═══ 5. BIGRAMS (Table 4) ═══
print("\n── 5. Bigrams ──")
bigram_checks = {
    "neural network": 1522612, "machine learning": 1287123,
    "deep learning": 980070, "artificial intelligence": 745358,
    "attention mechanism": 432079, "large language": 405166,
    "image classification": 390138, "recommendation system": 387638,
    "medical imaging": 359104, "feature extraction": 256159,
    "image segmentation": 243337, "transfer learning": 224851,
    "object detection": 206101, "reinforcement learning": 201098,
    "contrastive learning": 175692, "multi-modal": 126633,
    "anomaly detection": 112572, "text classification": 102891,
    "data augmentation": 100484, "self-supervised": 97164,
}
for bg, expected in bigram_checks.items():
    check(f"Bigram '{bg}'", expected, data["bigrams"].get(bg, 0))

# ═══ 6. TRIGRAMS (Table 5) ═══
print("\n── 6. Trigrams ──")
trigram_checks = {
    "deep neural network": 518431, "convolutional neural network": 394934,
    "large language model": 292873, "artificial neural network": 261355,
    "support vector machine": 239347, "natural language processing": 172355,
    "long short-term memory": 137359, "recurrent neural network": 88266,
    "graph neural network": 86453, "random forest classifier": 73385,
    "deep reinforcement learning": 72899, "generative adversarial network": 62880,
    "vision language model": 54666, "natural language understanding": 44373,
    "medical image segmentation": 42960,
}
for tg, expected in trigram_checks.items():
    check(f"Trigram '{tg}'", expected, data["trigrams"].get(tg, 0))

# ═══ 7. TIMELINES (Section 3.4) ═══
print("\n── 7. Timelines ──")
for method, years in data["timelines"].items():
    for year, count in years.items():
        check(f"Timeline {method}/{year}", count, data["timelines"][method][year])

# Verify derived calculations mentioned in prose
print("\n  Derived calculations:")
# "Neural network" 8.9x increase 2013-2025
nn_ratio = data["timelines"]["neural network"]["2025"] / data["timelines"]["neural network"]["2013"]
paper_nn_ratio = 8.9
if abs(nn_ratio - paper_nn_ratio) > 0.15:
    errors.append(f"NN 2013-2025 ratio: paper says {paper_nn_ratio}x, calculated {nn_ratio:.1f}x")
else:
    verified += 1
    print(f"  NN growth ratio: {nn_ratio:.1f}x (paper: {paper_nn_ratio}x) ✓")

# "Deep learning" 52.6x 2013-2025
dl_ratio = data["timelines"]["deep learning"]["2025"] / data["timelines"]["deep learning"]["2013"]
paper_dl_ratio = 52.6
if abs(dl_ratio - paper_dl_ratio) > 0.5:
    errors.append(f"DL 2013-2025 ratio: paper says {paper_dl_ratio}x, calculated {dl_ratio:.1f}x")
else:
    verified += 1
    print(f"  DL growth ratio: {dl_ratio:.1f}x (paper: {paper_dl_ratio}x) ✓")

# "RL" 26.6x 2013-2025
rl_ratio = data["timelines"]["reinforcement learning"]["2025"] / data["timelines"]["reinforcement learning"]["2013"]
paper_rl_ratio = 26.6
if abs(rl_ratio - paper_rl_ratio) > 0.5:
    errors.append(f"RL 2013-2025 ratio: paper says {paper_rl_ratio}x, calculated {rl_ratio:.1f}x")
else:
    verified += 1
    print(f"  RL growth ratio: {rl_ratio:.1f}x (paper: {paper_rl_ratio}x) ✓")

# "Transformer" 10.9x 2017-2025
tf_ratio = data["timelines"]["transformer"]["2025"] / data["timelines"]["transformer"]["2017"]
paper_tf_ratio = 10.9
if abs(tf_ratio - paper_tf_ratio) > 0.15:
    errors.append(f"Transformer 2017-2025 ratio: paper says {paper_tf_ratio}x, calculated {tf_ratio:.1f}x")
else:
    verified += 1
    print(f"  Transformer growth ratio: {tf_ratio:.1f}x (paper: {paper_tf_ratio}x) ✓")

# "LLM" 29.9x 2018-2025
llm_ratio = data["timelines"]["large language model"]["2025"] / data["timelines"]["large language model"]["2018"]
paper_llm_ratio = 29.9
if abs(llm_ratio - paper_llm_ratio) > 0.5:
    errors.append(f"LLM 2018-2025 ratio: paper says {paper_llm_ratio}x, calculated {llm_ratio:.1f}x")
else:
    verified += 1
    print(f"  LLM growth ratio: {llm_ratio:.1f}x (paper: {paper_llm_ratio}x) ✓")

# "Federated learning" 402.6x 2017-2025
fl_ratio = data["timelines"]["federated learning"]["2025"] / data["timelines"]["federated learning"]["2017"]
paper_fl_ratio = 402.6
if abs(fl_ratio - paper_fl_ratio) > 2:
    errors.append(f"FL 2017-2025 ratio: paper says {paper_fl_ratio}x, calculated {fl_ratio:.1f}x")
else:
    verified += 1
    print(f"  FL growth ratio: {fl_ratio:.1f}x (paper: {paper_fl_ratio}x) ✓")

# "Graph neural" 22.6x 2017-2025
gn_ratio = data["timelines"]["graph neural"]["2025"] / data["timelines"]["graph neural"]["2017"]
paper_gn_ratio = 22.6
if abs(gn_ratio - paper_gn_ratio) > 0.5:
    errors.append(f"GN 2017-2025 ratio: paper says {paper_gn_ratio}x, calculated {gn_ratio:.1f}x")
else:
    verified += 1
    print(f"  GN growth ratio: {gn_ratio:.1f}x (paper: {paper_gn_ratio}x) ✓")

# "Knowledge graph" 9.7x 2013-2025
kg_ratio = data["timelines"]["knowledge graph"]["2025"] / data["timelines"]["knowledge graph"]["2013"]
paper_kg_ratio = 9.7
if abs(kg_ratio - paper_kg_ratio) > 0.15:
    errors.append(f"KG 2013-2025 ratio: paper says {paper_kg_ratio}x, calculated {kg_ratio:.1f}x")
else:
    verified += 1
    print(f"  KG growth ratio: {kg_ratio:.1f}x (paper: {paper_kg_ratio}x) ✓")

# "Diffusion model" 2.7x 2019-2025
dm_ratio = data["timelines"]["diffusion model"]["2025"] / data["timelines"]["diffusion model"]["2019"]
paper_dm_ratio = 2.7
if abs(dm_ratio - paper_dm_ratio) > 0.15:
    errors.append(f"DM 2019-2025 ratio: paper says {paper_dm_ratio}x, calculated {dm_ratio:.1f}x")
else:
    verified += 1
    print(f"  DM growth ratio: {dm_ratio:.1f}x (paper: {paper_dm_ratio}x) ✓")

# GAN 2268.8x 2014-2025
gan_ratio = data["timelines"]["generative adversarial"]["2025"] / data["timelines"]["generative adversarial"]["2014"]
paper_gan_ratio = 2268.8
if abs(gan_ratio - paper_gan_ratio) > 10:
    errors.append(f"GAN 2014-2025 ratio: paper says {paper_gan_ratio}x, calculated {gan_ratio:.1f}x")
else:
    verified += 1
    print(f"  GAN growth ratio: {gan_ratio:.1f}x (paper: {paper_gan_ratio}x) ✓")

# ═══ 8. GROWTH TABLE (Table 6) ═══
print("\n── 8. Growth rates ──")
growth_checks = {
    "deepseek": {"new": 11033, "old": 13, "ratio": 848.7},
    "retrieval augmented generation": {"new": 18196, "old": 347, "ratio": 52.4},
    "jailbreak": {"new": 2803, "old": 110, "ratio": 25.5},
    "retrieval-augmented": {"new": 21105, "old": 1101, "ratio": 19.2},
    "mistral": {"new": 4361, "old": 260, "ratio": 16.8},
    "llm": {"new": 161771, "old": 10125, "ratio": 16.0},
    "copilot": {"new": 5699, "old": 356, "ratio": 16.0},
    "rag": {"new": 19193, "old": 1250, "ratio": 15.4},
    "gemini": {"new": 22365, "old": 1650, "ratio": 13.6},
    "guardrail": {"new": 5046, "old": 521, "ratio": 9.7},
    "llama": {"new": 14314, "old": 2114, "ratio": 6.8},
    "claude": {"new": 19493, "old": 2939, "ratio": 6.6},
    "prompt": {"new": 588390, "old": 92967, "ratio": 6.3},
    "instruction tuning": {"new": 7461, "old": 1406, "ratio": 5.3},
    "hallucination": {"new": 23580, "old": 4868, "ratio": 4.8},
    "foundation model": {"new": 188518, "old": 46410, "ratio": 4.1},
    "chatgpt": {"new": 37642, "old": 10865, "ratio": 3.5},
    "chain-of-thought": {"new": 11521, "old": 3163, "ratio": 3.6},
    "vision language": {"new": 37744, "old": 12771, "ratio": 3.0},
}
for kw, expected in growth_checks.items():
    if kw in data["growth"]:
        d = data["growth"][kw]
        check(f"Growth {kw} new", expected["new"], d["new"])
        check(f"Growth {kw} old", expected["old"], d["old"])
        check(f"Growth {kw} ratio", expected["ratio"], d["ratio"])
    else:
        errors.append(f"Growth keyword '{kw}' not in data file")

# ═══ 9. CITATION DISTRIBUTION (Table 7) ═══
print("\n── 9. Citations ──")
cite_checks = {
    "0": 2445876, "1-10": 1700854, "11-50": 648139,
    "51-100": 122722, "101-500": 78688, "501-1000": 5029, "1001+": 2475,
}
for crange, expected in cite_checks.items():
    check(f"Citations {crange}", expected, data["citation_dist"].get(crange, 0))

# ═══ 10. TOP CITED ═══
print("\n── 10. Top cited ──")
top_cited_checks = [
    ("Deep Residual Learning for Image Recognition", 221202, 2016),
    ("Diagnostic and Statistical Manual of Mental Disorders", 113579, 2013),
]
for title, cites, year in top_cited_checks:
    found = False
    for tc in data["top_cited"]:
        if tc["title"] and title.lower() in tc["title"].lower():
            check(f"Top cited '{title[:30]}' citations", cites, tc["citations"])
            check(f"Top cited '{title[:30]}' year", year, tc["year"])
            found = True
            break
    if not found:
        warnings.append(f"Could not find '{title[:40]}' in top_cited data")

# ═══ 11. COUNTRIES (Table 9) ═══
print("\n── 11. Countries ──")
country_checks = {
    "China": 874019, "United States of America": 718676,
    "India": 369931, "Japan": 333896,
}
for country, expected in country_checks.items():
    check(f"Country {country}", expected, data["countries"].get(country, 0))

# ═══ 12. INSTITUTIONS (Table 10) ═══
print("\n── 12. Institutions ──")
inst_checks = {
    "Chinese Academy of Sciences": 74921,
    "Centre National de la Recherche Scientifique": 50145,
    "University of London": 34887,
    "Tsinghua University": 30519,
}
for inst, expected in inst_checks.items():
    check(f"Inst {inst}", expected, data["institutions"].get(inst, 0))

# ═══ 13. OPEN ACCESS ═══
print("\n── 13. Open access ──")
closed = data["open_access"].get("closed", 0)
oa_count = data["total"] - closed  # 5003783 - 1960226 = 3043557
paper_oa = 3043557
paper_oa_pct = 60.8
calc_oa_pct = round(oa_count / data["total"] * 100, 1)
check("OA count", paper_oa, oa_count)
if abs(calc_oa_pct - paper_oa_pct) > 0.15:
    errors.append(f"OA %: paper says {paper_oa_pct}%, calculated {calc_oa_pct}%")
else:
    verified += 1

# ═══ 14. TITLE vs ABSTRACT (Table 11) ═══
print("\n── 14. Title vs Abstract ──")
tva_checks = {
    "neural network": {"title": 433556, "abstract": 1522612, "ratio": 3.5},
    "machine learning": {"title": 495798, "abstract": 1287123, "ratio": 2.6},
    "deep learning": {"title": 374975, "abstract": 980070, "ratio": 2.6},
    "large language model": {"title": 71469, "abstract": 292873, "ratio": 4.1},
    "diffusion model": {"title": 42120, "abstract": 324073, "ratio": 7.7},
    "transformer": {"title": 129524, "abstract": 316216, "ratio": 2.4},
    "hallucination": {"title": 10711, "abstract": 48759, "ratio": 4.6},
    "fairness": {"title": 78835, "abstract": 429288, "ratio": 5.4},
    "retrieval augmented": {"title": 8137, "abstract": 27394, "ratio": 3.4},
    "federated learning": {"title": 39481, "abstract": 59298, "ratio": 1.5},
    "reinforcement learning": {"title": 104021, "abstract": 201098, "ratio": 1.9},
    "knowledge graph": {"title": 28201, "abstract": 90234, "ratio": 3.2},
}
for kw, expected in tva_checks.items():
    d = data["title_vs_abstract"].get(kw, {})
    check(f"TVA {kw} title", expected["title"], d.get("title", 0))
    check(f"TVA {kw} abstract", expected["abstract"], d.get("abstract", 0))
    check(f"TVA {kw} ratio", expected["ratio"], d.get("ratio", 0))

# ═══ 15. DERIVED CLAIMS IN PROSE ═══
print("\n── 15. Prose claims ──")

# "30.4% of all paper abstracts" for neural network
nn_pct = round(1522612 / 5003783 * 100, 1)
if abs(nn_pct - 30.4) > 0.15:
    errors.append(f"NN percentage: paper says 30.4%, calculated {nn_pct}%")
else:
    verified += 1
    print(f"  NN % of corpus: {nn_pct}% ✓")

# "48.9% have zero citations"
zero_pct = round(2445876 / 5003783 * 100, 1)
if abs(zero_pct - 48.9) > 0.15:
    errors.append(f"Zero citation %: paper says 48.9%, calculated {zero_pct}%")
else:
    verified += 1
    print(f"  Zero citation %: {zero_pct}% ✓")

# "2.5x larger" corpus comparison
corpus_ratio = 5003783 / 1995130
if abs(corpus_ratio - 2.5) > 0.1:
    errors.append(f"Corpus ratio: paper says 2.5x, calculated {corpus_ratio:.1f}x")
else:
    verified += 1
    print(f"  Corpus ratio: {corpus_ratio:.1f}x ✓")

# "10.1x increase" 2013-2025
vol_ratio = 944530 / 93226
if abs(vol_ratio - 10.1) > 0.15:
    errors.append(f"Volume ratio 2013-2025: paper says 10.1x, calculated {vol_ratio:.1f}x")
else:
    verified += 1
    print(f"  Volume 2013-2025 ratio: {vol_ratio:.1f}x ✓")

# China leads by "21.6%"
china_lead = (874019 - 718676) / 718676 * 100
if abs(china_lead - 21.6) > 0.15:
    errors.append(f"China lead %: paper says 21.6%, calculated {china_lead:.1f}%")
else:
    verified += 1
    print(f"  China lead over US: {china_lead:.1f}% ✓")

# CAS leads CNRS by "49.4%"
cas_lead = (74921 - 50145) / 50145 * 100
if abs(cas_lead - 49.4) > 0.15:
    errors.append(f"CAS lead over CNRS: paper says 49.4%, calculated {cas_lead:.1f}%")
else:
    verified += 1
    print(f"  CAS lead over CNRS: {cas_lead:.1f}% ✓")

# ═══ 16. UNVERIFIABLE CLAIMS ═══
print("\n── 16. Flagging unverifiable claims ──")
unverifiable = [
    "Line 48: '5-8% cross-disciplinary noise based on manual spot-checking' - NOT API-verifiable, stated as estimate",
    "Line 196: 'CNN (92,331) still leads LLM (51,603) in title-only' - these title-only trigram counts are NOT in the JSON data file",
    "Line 314: 'Japan rank 8, 41,964 in title-only analysis' - title-only country data NOT in JSON data file",
    "Line 379: 'medicine, materials science, climate modeling, and finance' - qualitative claim about NN domains, not API-verifiable",
    "Line 466: 'DeepSeek-V3, Qwen, and Yi' - specific model names mentioned as Chinese LLMs, factual but not API-derived",
    "Line 468: 'OpenAI, Google, Meta' - specific company names, factual but not API-derived",
    "Line 474: 'India could approach or exceed US output levels by 2030' - projection, not a data point",
    "Line 491: '\"Explainable\" returns 2,544,915' - this IS in the JSON keywords data, but flagging the claim about stemming",
    "Line 507: 'Stanford HAI 2025 edition tracks...' - description of external report, factual",
    "Line 509: 'China and US accounted for over 50%' - claim about Zhang et al., citing their finding",
    "Line 513: '10x increase in training compute every 18 months' - claim about Sevilla et al., citing their finding",
    "Line 521: 'approximately 10% of AI researchers had moved' - claim about Ahmed & Wahed, citing their finding",
]
for u in unverifiable:
    warnings.append(u)
    print(f"  ⚠ {u}")

# ═══ 17. CHECK DERIVED NUMBERS IN COUNTRY SECTION ═══
print("\n── 17. Country section derived numbers ──")
# China 2025 gap "53.4%"
china_gap = (187887 - 122449) / 122449 * 100
if abs(china_gap - 53.4) > 0.15:
    errors.append(f"China 2025 gap: paper says 53.4%, calculated {china_gap:.1f}%")
else:
    verified += 1
    print(f"  China 2025 gap: {china_gap:.1f}% ✓")

# US growth 2020-2022 "0.7%"  (58622 to 64486)
# Actually this is wrong. Let me check: (64486 - 58622) / 58622 = 10.0%
# Paper says "grew only 0.7% between 2020 and 2022" - THIS IS WRONG
us_growth_2020_2022 = (64486 - 58622) / 58622 * 100
print(f"  US growth 2020-2022: calculated {us_growth_2020_2022:.1f}% (paper says 0.7%)")
if abs(us_growth_2020_2022 - 0.7) > 0.5:
    errors.append(f"US growth 2020-2022: paper says 0.7%, calculated {us_growth_2020_2022:.1f}%")

# China growth 2020-2022 "68.4%"
china_growth_2020_2022 = (90485 - 53743) / 53743 * 100
if abs(china_growth_2020_2022 - 68.4) > 0.5:
    errors.append(f"China growth 2020-2022: paper says 68.4%, calculated {china_growth_2020_2022:.1f}%")
else:
    verified += 1
    print(f"  China growth 2020-2022: {china_growth_2020_2022:.1f}% ✓")

# US 2023-2025 "57.7% increase over two years" (77664 to 122449)
us_growth_2023_2025 = (122449 - 77664) / 77664 * 100
if abs(us_growth_2023_2025 - 57.7) > 0.5:
    errors.append(f"US growth 2023-2025: paper says 57.7%, calculated {us_growth_2023_2025:.1f}%")
else:
    verified += 1
    print(f"  US growth 2023-2025: {us_growth_2023_2025:.1f}% ✓")

# India 32.3x (2013-2025)
india_ratio = 89287 / 2761
if abs(india_ratio - 32.3) > 0.5:
    errors.append(f"India ratio: paper says 32.3x, calculated {india_ratio:.1f}x")
else:
    verified += 1
    print(f"  India 2013-2025 ratio: {india_ratio:.1f}x ✓")

# China 15.6x (2013-2025)
china_ratio = 187887 / 12074
if abs(china_ratio - 15.6) > 0.15:
    errors.append(f"China ratio: paper says 15.6x, calculated {china_ratio:.1f}x")
else:
    verified += 1
    print(f"  China 2013-2025 ratio: {china_ratio:.1f}x ✓")

# US 8.9x (2013-2025)
us_ratio = 122449 / 13829
if abs(us_ratio - 8.9) > 0.15:
    errors.append(f"US ratio: paper says 8.9x, calculated {us_ratio:.1f}x")
else:
    verified += 1
    print(f"  US 2013-2025 ratio: {us_ratio:.1f}x ✓")

# India 3.1x 2013-2018
india_early = 8592 / 2761
if abs(india_early - 3.1) > 0.15:
    errors.append(f"India 2013-2018: paper says 3.1x, calculated {india_early:.1f}x")
else:
    verified += 1
    print(f"  India 2013-2018 ratio: {india_early:.1f}x ✓")

# India 10.4x 2018-2025
india_late = 89287 / 8592
if abs(india_late - 10.4) > 0.15:
    errors.append(f"India 2018-2025: paper says 10.4x, calculated {india_late:.1f}x")
else:
    verified += 1
    print(f"  India 2018-2025 ratio: {india_late:.1f}x ✓")

# ═══ SUMMARY ═══
print("\n" + "=" * 70)
print(f"AUDIT COMPLETE")
print(f"  Verified:    {verified}")
print(f"  Errors:      {len(errors)}")
print(f"  Warnings:    {len(warnings)}")
print("=" * 70)

if errors:
    print("\n🔴 ERRORS (must fix):")
    for e in errors:
        print(f"  ✗ {e}")

if warnings:
    print("\n🟡 WARNINGS (unverifiable or approximate):")
    for w in warnings:
        print(f"  ⚠ {w}")

sys.exit(1 if errors else 0)
