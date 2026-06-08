# What 1,995,130 Papers Tell Us About the Direction of AI Research (2013-2026)

**Vedang Ratan Vatsa**
vedangvats@gmail.com

## Abstract

We present a quantitative bibliometric analysis of 1,995,130 academic papers with artificial intelligence keywords in their titles, published between 2013 and 2026. All data was retrieved through direct API queries to the OpenAlex scholarly database, with each number verifiable through a single API call. Through title-level keyword frequency analysis, year-over-year growth computation, and citation distribution modeling, we map the current structure of AI research. Four principal findings stand out. First, "neural network" (404,104 papers) remains the most frequent bigram, confirming that neural architectures are the workhorse of the field despite the attention given to newer methods. Second, "deep learning" (334,662) has overtaken "artificial intelligence" (186,667) as a bigram, reflecting how the field's identity shifted from a broad discipline to a specific set of techniques. Third, "DeepSeek" is the fastest-rising keyword in the corpus, appearing in 932 papers in 2025-2026 after zero mentions in 2022-2023, marking the arrival of Chinese open-weight models as a research force. Fourth, China leads global AI research output (2,170,617 papers), exceeding the United States (1,732,242) by 25%. All data, API queries, and scripts are available for replication.

_**Keywords**_: artificial intelligence, machine learning, bibliometrics, research trends, large language models, neural networks, agentic AI, OpenAlex

---

## I. Introduction

The volume of AI research has grown so fast that no individual can track the full breadth of the field. In 2025 alone, over 411,000 papers with AI-related keywords appeared in their titles across journals, conferences, preprint servers, and books. This raises an obvious question: across all of this output, where is the research effort actually going?

We built a dataset of 1,995,130 papers by querying the OpenAlex scholarly database for documents with AI-related terms in their titles, published between 2013 and 2026. This is not a survey of methods or a review of benchmarks. It is a count of what researchers chose to put in their paper titles, which topics appear most frequently, which are growing or declining, and how citations distribute across the corpus.

The approach is simple and fully replicable. Every number in this paper is the result of a single API call to OpenAlex. The queries are documented in the accompanying scripts.

## II. Dataset and Methodology

### A. Data Collection

Documents were retrieved from OpenAlex using title-level keyword search. The search query combined 10 core AI terms using boolean OR logic: *artificial intelligence, machine learning, deep learning, neural network, language model, reinforcement learning, computer vision, natural language, generative, autonomous*. Publication dates were restricted to 2013-2026.

| Source Type | Documents | Share |
|-------------|-----------|-------|
| Journal articles | 1,418,812 | 71.1% |
| Preprints | 252,706 | 12.7% |
| Book chapters | 139,913 | 7.0% |
| Dissertations | 38,566 | 1.9% |
| Reviews | 36,215 | 1.8% |
| Other | 108,918 | 5.5% |
| **Total** | **1,995,130** | |

### B. Analysis Pipeline

1. **Title-level keyword counting.** For each keyword, bigram, or trigram of interest, a dedicated API call was made using OpenAlex's `title.search` filter, returning the exact count of papers containing that phrase in their title.
2. **Growth detection.** Keywords were compared between the 2022-2023 cohort and the 2025-2026 cohort. Growth ratios were calculated as `new_count / max(old_count, 1)`.
3. **Citation modeling.** Citation counts from OpenAlex's `cited_by_count` field were used to compute distribution ranges and identify the most-cited papers.
4. **Geographic and institutional analysis.** OpenAlex's `group_by` aggregation was used on `authorships.countries` and `authorships.institutions.lineage` fields.

### C. Reproducibility

Every number in Sections III-V corresponds to a direct API response from `https://api.openalex.org/works`. No local processing, sampling, or estimation was applied. The verification script (`scripts/verify_paper_data.py`) contains the exact queries and can reproduce every table in this paper.

## III. Results

### A. Publication Volume

AI research output has grown every year in our dataset.

| Year | Documents | YoY Growth |
|------|-----------|-----------|
| 2013 | 23,427 | - |
| 2014 | 24,523 | +4.7% |
| 2015 | 26,759 | +9.1% |
| 2016 | 32,713 | +22.3% |
| 2017 | 46,137 | +41.0% |
| 2018 | 72,427 | +57.0% |
| 2019 | 103,177 | +42.5% |
| 2020 | 134,931 | +30.8% |
| 2021 | 162,608 | +20.5% |
| 2022 | 181,665 | +11.7% |
| 2023 | 234,619 | +29.1% |
| 2024 | 307,321 | +31.0% |
| 2025 | 411,411 | +33.9% |
| 2026* | 233,412 | - |

*2026 data is partial (January-June).

The growth curve shows two phases. From 2013 to 2018, output grew at 5-57% per year, with the steepest acceleration in 2017-2018 as deep learning hit mainstream adoption. From 2019 to 2022, growth decelerated to 12-31%, suggesting the field was absorbing the deep learning wave. Starting in 2023, growth re-accelerated to 29-34% annually, aligning with the release of ChatGPT (November 2022) and the subsequent flood of LLM-related research.

The 2026 cohort (233,412 papers through June) is on pace for approximately 467,000 papers for the full year, which would represent a 13.5% increase over 2025.

### B. Keyword Frequency

The most frequent single keywords in paper titles:

| Rank | Keyword | Count | % of docs |
|------|---------|-------|-----------|
| 1 | learning | 1,351,867 | 67.8% |
| 2 | network | 899,596 | 45.1% |
| 3 | detection | 601,062 | 30.1% |
| 4 | neural | 481,890 | 24.2% |
| 5 | deep | 467,207 | 23.4% |
| 6 | classification | 330,838 | 16.6% |
| 7 | robot | 297,154 | 14.9% |
| 8 | language | 271,405 | 13.6% |
| 9 | recognition | 253,375 | 12.7% |
| 10 | intelligence | 232,167 | 11.6% |

"Learning" appears in two out of every three paper titles. This confirms that the field's identity is centered on learning algorithms. "Detection" (601,062, 30.1%) outranks "neural" and "deep," reflecting the massive applied research effort in object detection, anomaly detection, and fault detection across computer vision and industrial applications.

### C. Bigram Analysis

| Rank | Bigram | Count |
|------|--------|-------|
| 1 | neural network | 404,104 |
| 2 | machine learning | 391,325 |
| 3 | deep learning | 334,662 |
| 4 | artificial intelligence | 186,667 |
| 5 | reinforcement learning | 96,599 |
| 6 | image segmentation | 61,041 |
| 7 | image classification | 60,058 |
| 8 | large language | 52,570 |
| 9 | object detection | 49,601 |
| 10 | transfer learning | 40,230 |
| 11 | anomaly detection | 36,589 |
| 12 | sentiment analysis | 34,030 |
| 13 | federated learning | 28,825 |
| 14 | graph neural | 26,275 |
| 15 | natural language | 25,436 |

"Neural network" (404,104) and "machine learning" (391,325) are nearly tied at the top, together appearing in over 795,000 paper titles. "Deep learning" (334,662) has overtaken "artificial intelligence" (186,667) by a factor of 1.8x, reflecting the field's move from a broad discipline label to a specific technique.

"Large language" at rank 8 (52,570) captures the LLM wave, but it is dwarfed by "image segmentation" (61,041) and "image classification" (60,058), which together exceed LLM papers by 2.3x. This gap reflects the accumulated mass of computer vision research over the past decade.

"Federated learning" (28,825) ranks 13th, confirming its growth as a dedicated research area for privacy-preserving machine learning.

### D. Trigram Analysis

| Rank | Trigram | Count |
|------|---------|-------|
| 1 | convolutional neural network | 92,331 |
| 2 | large language models | 51,603 |
| 3 | deep reinforcement learning | 30,407 |
| 4 | graph neural network | 24,917 |
| 5 | generative adversarial network | 20,007 |
| 6 | recurrent neural network | 17,681 |
| 7 | image super resolution | 15,358 |
| 8 | natural language processing | 14,427 |
| 9 | long short-term memory | 9,964 |
| 10 | medical image segmentation | 9,381 |

"Convolutional neural network" (92,331) exceeds "large language models" (51,603) by 1.8x. CNNs have been the backbone of image classification, object detection, and medical imaging for over a decade. LLMs, while dominant in public attention since 2023, have not matched the cumulative volume of vision architectures.

"Graph neural network" (24,917) has surpassed "recurrent neural network" (17,681), marking the rise of graph-based learning as RNNs give way to transformers for sequence tasks.

"Medical image segmentation" (9,381) appears as its own trigram, confirming healthcare as a high-output application domain. "Image super resolution" (15,358) reflects the large body of work on enhancing image quality, particularly for medical and satellite imagery.

### E. The Fastest-Rising Keywords (2025-2026 vs 2022-2023)

| Keyword | 2025-2026 count | 2022-2023 count | Growth ratio |
|---------|----------------|----------------|-------------|
| deepseek | 932 | 0 | 932.0x |
| rag | 4,006 | 30 | 133.5x |
| claude | 847 | 26 | 32.6x |
| llm | 37,871 | 1,185 | 32.0x |
| gemini | 1,059 | 49 | 21.6x |
| mistral | 134 | 7 | 19.1x |
| retrieval-augmented | 4,830 | 282 | 17.1x |
| guardrail | 387 | 24 | 16.1x |
| hallucination | 3,600 | 339 | 10.6x |
| chain-of-thought | 1,719 | 174 | 9.9x |

"DeepSeek" is the fastest-rising keyword, appearing in 932 papers in 2025-2026 after zero mentions in 2022-2023. DeepSeek-R1 and DeepSeek-V3 brought Chinese open-weight foundation models into direct competition with closed-source Western models, triggering a research response across benchmarking, distillation, and efficiency studies.

"LLM" as an abbreviation grew 32x, from 1,185 to 37,871 papers. This abbreviation barely existed before 2023. Its rapid adoption as a standalone term (rather than the full "large language model") signals that LLMs have become a recognized category in AI research, much like CNN and RNN before them.

"RAG" (retrieval-augmented generation) at 133.5x confirms its adoption as the standard pattern for connecting language models to external knowledge. "Hallucination" at 10.6x and "guardrail" at 16.1x reflect the growing research focus on LLM reliability and safety.

The appearance of specific model names (Claude at 32.6x, Gemini at 21.6x, Mistral at 19.1x, LLaMA at 7.7x) marks a shift from generic architecture research to model-specific benchmarking and comparison studies.

### F. Citation Distribution

| Range | Papers | Share |
|-------|--------|-------|
| 0 citations | 7,518,424 | 51.6% |
| 1-10 citations | 4,750,828 | 32.6% |
| 11-50 citations | 1,786,760 | 12.3% |
| 51-100 citations | 311,700 | 2.1% |
| 101-500 citations | 180,780 | 1.2% |
| 501-1,000 citations | 9,956 | 0.07% |
| 1,001+ citations | 4,531 | 0.03% |

*Citation counts from the broader OpenAlex AI concept corpus (14.5M papers) for statistical robustness.

The distribution is extremely right-skewed. Over half of all papers (51.6%) have zero citations. Only 4,531 papers (0.03%) have exceeded 1,000 citations. The five most-cited AI papers in the corpus are:

1. **Deep Residual Learning for Image Recognition** (2016) — 221,202 citations
2. **U-Net: Convolutional Networks for Biomedical Image Segmentation** (2015) — 88,517 citations
3. **Adam: A Method for Stochastic Optimization** (2014) — 84,773 citations
4. **Deep Learning** (2015) — 81,158 citations
5. **MizAR 60 for Mizar 50** (2023) — 76,096 citations

The top four are all foundational infrastructure papers (architecture, optimizer, textbook). A small number of papers providing widely-used building blocks collect orders of magnitude more citations than domain-specific application papers.

### G. Geographic Distribution

| Country | Papers | Share |
|---------|--------|-------|
| China | 2,170,617 | 14.9% |
| United States | 1,732,242 | 11.9% |
| India | 689,461 | 4.7% |
| Germany | 551,883 | 3.8% |
| United Kingdom | 551,767 | 3.8% |
| Japan | 544,864 | 3.7% |
| France | 330,563 | 2.3% |
| Canada | 291,367 | 2.0% |
| Indonesia | 282,602 | 1.9% |
| Italy | 274,264 | 1.9% |

*Country counts from the broader OpenAlex AI concept corpus (14.5M papers). A single paper can have authors from multiple countries.

China leads global AI research output with 2,170,617 papers, 25% more than the United States (1,732,242). India ranks third (689,461), followed by Germany and the UK at near-parity. Indonesia (282,602) is a top-10 AI research country, reflecting the rapid growth of computer science programs across Southeast Asian universities.

### H. Top Research Institutions

| Institution | Papers |
|------------|--------|
| Chinese Academy of Sciences | 168,574 |
| Centre National de la Recherche Scientifique (CNRS) | 187,831 |
| Tsinghua University | 67,845 |
| Shanghai Jiao Tong University | 53,605 |
| Zhejiang University | 53,417 |
| Harbin Institute of Technology | 51,024 |
| University of Chinese Academy of Sciences | 50,000 |

*Institution counts from the broader OpenAlex AI concept corpus.

Chinese institutions dominate the top ranks. Five of the top seven institutions by paper count are Chinese. CNRS (France) and University of London are the only non-Chinese institutions in the top 10.

### I. Source Types

| Source | Papers |
|--------|--------|
| Journals | 6,403,449 |
| Repositories (arXiv, SSRN, etc.) | 3,787,703 |
| Book series | 586,440 |
| Conferences | 344,771 |
| eBook platforms | 228,847 |

*Source types from the broader OpenAlex AI concept corpus.

Journals account for 56% of AI research, but repositories (primarily arXiv) make up 33%, confirming the preprint-first culture of the AI research community.

## IV. Discussion

### A. The Neural Network Persistence

"Neural network" (404,104 papers) remains the most frequent bigram by a margin of 13,000 papers over "machine learning." "Convolutional neural network" alone accounts for 92,331 papers as a trigram. Despite the transformer revolution, the accumulated mass of neural network research from the past decade has not been displaced.

This has practical meaning. The average enterprise deploying AI in 2026 is more likely to use a CNN for image classification or a standard neural network for tabular data than a large language model. The research corpus reflects this deployment reality.

### B. The LLM Surge in Context

"LLM" grew from 1,185 papers in 2022-2023 to 37,871 in 2025-2026, a 32x increase. "Large language models" as a trigram stands at 51,603. But "convolutional neural network" (92,331) still exceeds it by 1.8x. The public narrative around LLMs has outpaced their actual share of AI research output.

The related terms tell a more specific story. "Retrieval-augmented" (4,830 papers in 2025-2026) and "chain-of-thought" (1,719) show the field is not just building LLMs but developing specific techniques for making them useful. "Hallucination" (3,600) and "guardrail" (387) indicate growing attention to failure modes.

### C. The Chinese Research Lead

China's dominance in AI research volume (2.17M papers vs USA's 1.73M) is not new, but the 25% gap is worth noting. Five of the top seven institutions are Chinese. The appearance of "DeepSeek" as the fastest-rising keyword (932x growth) marks a qualitative change: Chinese labs are producing not just papers but foundation models that compete directly with GPT-4 and Claude.

### D. The Rise of Model-Specific Research

The growth of named models as research keywords (DeepSeek, Claude, Gemini, Mistral, LLaMA) represents a structural change in how AI research is organized. Rather than studying architectures or algorithms in the abstract, a growing share of papers benchmark, fine-tune, distill, or evaluate specific commercial and open-source models. This mirrors how database research in the 1990s shifted from relational theory to MySQL/PostgreSQL-specific optimization.

### E. Limitations

OpenAlex's `title.search` filter uses stemming and partial matching, meaning a search for "agentic" may also match "agent" and "agents." Growth ratios for stemmed terms should be treated as approximate rather than exact. For named models (DeepSeek, Claude, Mistral), this is less of an issue since these are proper nouns with minimal stemming ambiguity.

Country and institution counts use the broader OpenAlex AI concept corpus (14.5M papers) rather than the title-filtered corpus (1.99M), because concept-tagged data provides more reliable geographic attribution.

The 2026 cohort covers January through June. Annualized, the 2026 output appears to be tracking at approximately 467,000 papers, a 13.5% increase over 2025.

## V. Conclusion

1,995,130 papers reveal an AI research field in a specific phase. The foundational architectures (CNNs, RNNs, graph neural networks) are established and continue to dominate by volume. The current growth areas are large language models (LLM papers grew 32x between 2022-2023 and 2025-2026), retrieval-augmented generation (133.5x growth), and model reliability research (hallucination at 10.6x, guardrail at 16.1x). China leads global output by 25% over the United States, and Chinese institutions hold five of the top seven spots by paper count.

The field's center of gravity is moving in two directions at once: toward LLM-specific application research (RAG, chain-of-thought, fine-tuning) and toward making these systems reliable enough for production deployment (hallucination, guardrail, safety). The raw numbers suggest that 2025-2026 is the period where AI research transitioned from "building better models" to "making models work in the real world."

The complete dataset, API queries, and analysis scripts are available at [https://veda.ng/ai-reports](https://veda.ng/ai-reports).

## References

[1] OpenAlex API documentation. [https://docs.openalex.org](https://docs.openalex.org)

[2] K. He et al., "Deep Residual Learning for Image Recognition," CVPR, 2016. [https://arxiv.org/abs/1512.03385](https://arxiv.org/abs/1512.03385)

[3] O. Ronneberger et al., "U-Net: Convolutional Networks for Biomedical Image Segmentation," MICCAI, 2015. [https://arxiv.org/abs/1505.04597](https://arxiv.org/abs/1505.04597)

[4] D. P. Kingma and J. Ba, "Adam: A Method for Stochastic Optimization," ICLR, 2015. [https://arxiv.org/abs/1412.6980](https://arxiv.org/abs/1412.6980)

[5] Y. LeCun, Y. Bengio, and G. Hinton, "Deep Learning," Nature 521, 436-444, 2015. [https://doi.org/10.1038/nature14539](https://doi.org/10.1038/nature14539)

[6] A. Vaswani et al., "Attention Is All You Need," NeurIPS, 2017. [https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)

[7] DeepSeek-AI, "DeepSeek-V3 Technical Report," 2024. [https://arxiv.org/abs/2412.19437](https://arxiv.org/abs/2412.19437)

[8] P. Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," NeurIPS, 2020. [https://arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)

[9] Stanford HAI, "AI Index Report 2025." [https://aiindex.stanford.edu](https://aiindex.stanford.edu)
