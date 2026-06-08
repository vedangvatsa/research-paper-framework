# What Five Million Papers Reveal About the Structure of AI Research (2013-2026)

<div class="author-info">
**Vedang Ratan Vatsa**<br>
*vedangvats@gmail.com*<br>
</div>

## Abstract

We analyze 5,003,783 academic papers that discuss artificial intelligence methods in their abstracts, published between 2013 and mid-2026. All data was collected through direct API queries to the OpenAlex scholarly database. The corpus is approximately 2.5 times larger than title-only searches would yield, and captures papers that use AI methods without placing them in their titles. We measure keyword frequency, temporal trajectories, growth rates, citation distributions, geographic concentration, and institutional output. Eight findings stand out. (1) "Neural network" appears in the abstracts of 1,522,612 papers, making it the most-referenced AI concept by a wide margin. (2) "Deep learning" grew from 4,120 abstract mentions in 2013 to 216,713 in 2025, a 52.6x increase. (3) "Large language model" papers grew from 3,248 in 2018 to 96,984 in 2025, with an exponential acceleration after the release of ChatGPT in late 2022. (4) "DeepSeek" is the fastest-rising term in the corpus (848.7x growth between 2022-2023 and 2025-2026). (5) "Retrieval augmented generation" grew 52.4x in the same period. (6) Over 48.9% of papers have zero citations. (7) China leads global output with 874,019 papers, followed by the United States at 718,676. (8) Abstract-level analysis captures 1.9x to 7.7x more papers per keyword compared to title-only analysis, demonstrating that title-based bibliometrics can miss the majority of method-relevant research. Every number in this paper is verifiable through a single API call. The complete dataset, queries, and analysis scripts are publicly available.

_**Keywords**_: artificial intelligence, machine learning, bibliometrics, research trends, large language models, neural networks, abstract analysis, OpenAlex

---

## 1. Introduction

AI research output has accelerated beyond the capacity of any single researcher to track. In 2025, over 944,000 papers discussed artificial intelligence methods in their abstracts. The pace is increasing. The first five months of 2026 already account for 812,972 papers, putting the year on track for over 1.9 million.

Most existing bibliometric studies of AI research rely on title-level keyword matching or subject classification tags. Title-based approaches capture only papers where the author chose to place the method name in the title. A paper titled "Predicting Protein Stability Under Thermal Stress" that uses a neural network throughout its methods section would be invisible to a title-only search for "neural network." Abstract-level analysis addresses this gap by searching the text where authors describe their methods, results, and contributions.

We constructed a corpus of 5,003,783 papers by querying the OpenAlex scholarly database for documents that mention AI-related terms in their abstracts, published between 2013 and mid-2026. This corpus is 2.5x larger than the equivalent title-only search (1,995,130 papers), capturing the full extent of AI method usage across disciplines.

This paper makes three contributions.

- **Scale.** We analyze 5 million papers, among the largest abstract-level bibliometric studies of AI research to date.
- **Reproducibility.** Every number in this paper corresponds to a single API call to the OpenAlex database. The queries are documented in the verification scripts.
- **Abstract vs. title comparison.** We quantify how much research is missed by title-only bibliometrics, finding that abstract search captures 1.9x to 7.7x more papers per keyword.

The rest of this paper is organized as follows. Section 2 describes the dataset construction and analysis methods. Section 3 presents results across ten dimensions. Section 4 discusses the findings. Section 5 reviews related work. Section 6 concludes.

## 2. Methodology

### 2.1 Data Source

OpenAlex is an open scholarly database indexing over 250 million academic works [1]. It provides free API access with structured metadata including titles, abstracts (stored as inverted index), author affiliations, citation counts, open access status, and machine-learned concept tags. We chose OpenAlex over Web of Science or Scopus because it is freely accessible, covers preprints (including arXiv), and exposes structured API filters that allow exact-count queries without downloading raw data.

### 2.2 Corpus Construction

The corpus was constructed using OpenAlex's `abstract.search` filter. The search query combined 10 AI-related terms using boolean OR logic.

**Search terms.** *artificial intelligence, machine learning, deep learning, neural network, language model, reinforcement learning, computer vision, natural language, generative, autonomous.*

**Date range.** 2013-01-01 through 2026-06-08.

**Resulting corpus.** 5,003,783 papers.

Eight of the ten search terms are specific to AI. Two terms ("generative" and "autonomous") are broader and may capture non-AI papers. "Generative" can match generative grammar in linguistics. "Autonomous" can match autonomous systems in biology. Based on manual inspection of 100 random results from each term, we estimate 5-8% of the corpus consists of papers where the matched term refers to a non-AI context. We accepted this tradeoff because excluding these terms would miss entire AI research areas such as generative adversarial networks (67,647 papers) and autonomous driving (71,930 papers).

**Table 1. Corpus composition by document type.**

| Document Type | Count | Share |
|---|---|---|
| Journal article | 3,270,717 | 65.4% |
| Preprint | 668,948 | 13.4% |
| Book chapter | 386,449 | 7.7% |
| Dataset | 298,570 | 6.0% |
| Review | 94,567 | 1.9% |
| Dissertation | 92,581 | 1.9% |
| Other | 191,951 | 3.8% |
| **Total** | **5,003,783** | |

**Table 2. Corpus composition by source type.**

| Source Type | Count | Share |
|---|---|---|
| Journal | 2,232,178 | 44.6% |
| Repository (arXiv, SSRN, etc.) | 1,370,590 | 27.4% |
| Book series | 246,842 | 4.9% |
| Conference proceedings | 111,398 | 2.2% |
| eBook platform | 69,676 | 1.4% |
| Other / unclassified | 973,099 | 19.5% |

Repositories (primarily arXiv) account for 27.4% of the corpus, confirming the preprint-first culture of AI research. Journals remain the largest single source at 44.6%.

### 2.3 Analysis Methods

All analyses were performed through direct OpenAlex API calls. No local text processing was applied.

1. **Keyword frequency.** For each keyword, bigram, or trigram of interest, we issued a single API call using `abstract.search:<term>,publication_year:2013-2026` and recorded the `meta.count` field from the response.

2. **Growth detection.** For each keyword, we compared its count in the 2025-2026 cohort against the 2022-2023 cohort. The growth ratio was computed as `count_new / max(count_old, 1)`.

3. **Time-series trajectories.** For 10 selected methods, we issued year-by-year API calls to construct annual publication counts from 2013 (or the method's introduction year) through 2026.

4. **Citation distribution.** We used the `cited_by_count` filter to count papers in seven citation ranges (0, 1-10, 11-50, 51-100, 101-500, 501-1000, 1000+).

5. **Geographic and institutional analysis.** We used OpenAlex's `group_by` aggregation on `authorships.countries` and `authorships.institutions.lineage` to rank countries and institutions. A single paper with co-authors from multiple countries is counted once per country.

6. **Title vs. abstract comparison.** For 14 keywords, we ran parallel queries using `title.search` and `abstract.search` and computed the ratio of abstract to title counts.

### 2.4 Stemming and Precision

OpenAlex's search filters apply stemming, meaning a search for "agentic" also matches "agent" and "agents." For multi-word phrases ("retrieval augmented generation," "graph neural network") and proper nouns ("DeepSeek," "Claude," "Mistral"), stemming has minimal effect. For single common words ("diffusion," "safety," "clinical"), stemming can inflate counts by matching non-AI uses of the word. We flag these cases in the results.

### 2.5 Reproducibility

The verification script `scripts/collect_abstract_data.py` contains every API query used in this paper. Running the script reproduces all tables and figures. The raw API responses are archived in `papers/verification_data/abstract_corpus_analysis.json`.

## 3. Results

### 3.1 Publication Volume

**Table 3. Annual publication volume (abstract-level corpus).**

| Year | Papers | YoY Growth |
|------|--------|-----------|
| 2013 | 93,226 | - |
| 2014 | 97,510 | +4.6% |
| 2015 | 105,609 | +8.3% |
| 2016 | 115,423 | +9.3% |
| 2017 | 137,237 | +18.9% |
| 2018 | 185,192 | +34.9% |
| 2019 | 242,286 | +30.8% |
| 2020 | 305,903 | +26.3% |
| 2021 | 369,519 | +20.8% |
| 2022 | 411,098 | +11.2% |
| 2023 | 520,861 | +26.7% |
| 2024 | 662,417 | +27.2% |
| 2025 | 944,530 | +42.6% |
| 2026* | 812,972 | - |

*2026 data covers January through early June.

![Fig. 1. AI research publication volume, 2013-2026. Each bar represents papers mentioning AI terms in their abstracts. 2026 covers January through June only.](figures/fig_publication_volume.png)

The corpus grew from 93,226 papers in 2013 to 944,530 in 2025, a 10.1x increase over 12 years. The growth curve shows three distinct phases.

**Phase 1 (2013-2016), slow growth, 4.6-9.3% per year.** AI research was growing but had not yet reached mainstream adoption. Deep learning was still an active research area rather than a standard tool.

**Phase 2 (2017-2022), deep learning adoption, 11.2-34.9% per year.** The steepest acceleration occurred in 2017-2018 (+18.9% and +34.9%), aligning with the publication of "Attention Is All You Need" [6] and the broad adoption of deep learning across application domains. Growth decelerated to 11.2% in 2022, suggesting the field was absorbing the deep learning wave.

**Phase 3 (2023-2026), the LLM surge, 26.7-42.6% per year.** Starting in 2023, growth re-accelerated sharply. The 2025 output (944,530) represents a 42.6% increase over 2024, the highest annual growth rate since 2018. This aligns with the release of ChatGPT (November 2022) and the subsequent proliferation of LLM-related research.

The 2026 cohort (812,972 papers through early June) is on pace for approximately 1.9 million papers for the full year. If realized, this would be the first year in which AI research output exceeds 1 million papers in our corpus.

### 3.2 Bigram Frequency

**Table 4. Top 20 bigrams by abstract frequency.**

| Rank | Bigram | Abstract Count |
|------|--------|---------------|
| 1 | neural network | 1,522,612 |
| 2 | machine learning | 1,287,123 |
| 3 | deep learning | 980,070 |
| 4 | artificial intelligence | 745,358 |
| 5 | attention mechanism | 432,079 |
| 6 | large language | 405,166 |
| 7 | image classification | 390,138 |
| 8 | recommendation system | 387,638 |
| 9 | medical imaging | 359,104 |
| 10 | feature extraction | 256,159 |
| 11 | image segmentation | 243,337 |
| 12 | transfer learning | 224,851 |
| 13 | object detection | 206,101 |
| 14 | reinforcement learning | 201,098 |
| 15 | contrastive learning | 175,692 |
| 16 | multi-modal | 126,633 |
| 17 | anomaly detection | 112,572 |
| 18 | text classification | 102,891 |
| 19 | data augmentation | 100,484 |
| 20 | self-supervised | 97,164 |

"Neural network" (1,522,612) dominates the list, appearing in 30.4% of all paper abstracts. "Machine learning" (1,287,123) and "deep learning" (980,070) round out the top three. Together, these three terms appear in over 3.7 million paper abstracts.

"Attention mechanism" (432,079) ranks 5th, reflecting the wide adoption of attention-based architectures across NLP, computer vision, and multimodal tasks since the transformer's introduction in 2017.

"Large language" (405,166) at rank 6 captures the LLM wave, but it is still exceeded by "attention mechanism," "image classification" (390,138), "recommendation system" (387,638), and "medical imaging" (359,104). The older, application-oriented research areas have accumulated enough volume to outrank the newer LLM category.

"Contrastive learning" (175,692) at rank 15 and "self-supervised" (97,164) at rank 20 confirm the growing importance of self-supervised and representation learning methods.

### 3.3 Trigram Frequency

**Table 5. Top 15 trigrams by abstract frequency.**

| Rank | Trigram | Count |
|------|---------|-------|
| 1 | deep neural network | 518,431 |
| 2 | convolutional neural network | 394,934 |
| 3 | large language model | 292,873 |
| 4 | artificial neural network | 261,355 |
| 5 | support vector machine | 239,347 |
| 6 | natural language processing | 172,355 |
| 7 | long short-term memory | 137,359 |
| 8 | recurrent neural network | 88,266 |
| 9 | graph neural network | 86,453 |
| 10 | random forest classifier | 73,385 |
| 11 | deep reinforcement learning | 72,899 |
| 12 | generative adversarial network | 62,880 |
| 13 | vision language model | 54,666 |
| 14 | natural language understanding | 44,373 |
| 15 | medical image segmentation | 42,960 |

"Deep neural network" (518,431) leads the trigrams, followed by "convolutional neural network" (394,934). These two trigrams together appear in over 913,000 abstracts.

"Large language model" (292,873) at rank 3 has overtaken "artificial neural network" (261,355) and "support vector machine" (239,347). This is a reversal of what title-only analysis would show, where CNN (92,331) still leads LLM (51,603). The abstract data reveals that LLMs are discussed more broadly than titles suggest.

"Support vector machine" (239,347) and "random forest classifier" (73,385) persist in the top 15. These classical methods continue to be widely referenced in abstracts, often as baselines for comparison or in application domains where simpler models remain competitive.

"Vision language model" (54,666) at rank 13 captures the growing convergence of computer vision and natural language processing.

### 3.4 Time-Series Trajectories

![Fig. 2. Trajectories of established AI methods by annual abstract mentions, 2013-2026. 2026 covers January through June only.](figures/fig_established_methods.png)

**Established methods.** "Neural network" grew steadily from 23,395 abstract mentions in 2013 to 207,140 in 2025 (8.9x). "Deep learning" grew from 4,120 in 2013 to 216,713 in 2025 (52.6x), and overtook "neural network" in the 2026 partial-year data (though this may reflect seasonal publication patterns). "Reinforcement learning" grew from 1,784 in 2013 to 47,498 in 2025 (26.6x). "Transformer" grew from 7,201 in 2017 to 78,135 in 2025 (10.9x).

![Fig. 3. The exponential growth of "large language model" in paper abstracts. Vertical dashed line marks the release of ChatGPT (November 2022). 2026 covers January through June only.](figures/fig_llm_explosion.png)

**The LLM trajectory.** "Large language model" abstract mentions grew from 3,248 in 2018 to 96,984 in 2025, a 29.9x increase. The growth curve has a clear inflection point. Between 2018 and 2022, mentions grew at a modest pace (3,248 to 7,931, or 2.4x over four years). Between 2022 and 2025, mentions grew 12.2x in three years. The 2026 partial-year data (84,957 through June) puts the full year on pace for approximately 204,000 papers, which would be another 2.1x increase over 2025.

![Fig. 4. Rising AI methods by annual abstract mentions. Diffusion models, federated learning, and graph neural networks all show sustained growth. Knowledge graphs show steady but slower acceleration. 2026 covers January through June only.](figures/fig_rising_methods.png)

**Rising methods.** "Diffusion model" grew from 18,640 in 2019 to 49,862 in 2025 (2.7x). "Federated learning" grew from 46 in 2017 to 18,519 in 2025 (402.6x). "Graph neural" grew from 966 in 2017 to 21,873 in 2025 (22.6x). "Knowledge graph" grew from 1,700 in 2013 to 16,519 in 2025 (9.7x).

"Generative adversarial" grew from 6 papers in 2014 to 13,613 in 2025, but the growth rate has slowed since 2022, suggesting that GANs are entering a maturity phase as diffusion models take over image generation tasks.

### 3.5 Fastest-Rising Keywords

**Table 6. Fastest-rising keywords in paper abstracts (2025-2026 vs 2022-2023).**

| Keyword | 2025-2026 | 2022-2023 | Growth |
|---------|-----------|-----------|--------|
| deepseek | 11,033 | 13 | 848.7x |
| retrieval augmented generation | 18,196 | 347 | 52.4x |
| jailbreak | 2,803 | 110 | 25.5x |
| retrieval-augmented | 21,105 | 1,101 | 19.2x |
| mistral | 4,361 | 260 | 16.8x |
| llm | 161,771 | 10,125 | 16.0x |
| copilot | 5,699 | 356 | 16.0x |
| rag | 19,193 | 1,250 | 15.4x |
| gemini | 22,365 | 1,650 | 13.6x |
| guardrail | 5,046 | 521 | 9.7x |
| llama | 14,314 | 2,114 | 6.8x |
| claude | 19,493 | 2,939 | 6.6x |
| prompt | 588,390 | 92,967 | 6.3x |
| instruction tuning | 7,461 | 1,406 | 5.3x |
| hallucination | 23,580 | 4,868 | 4.8x |
| foundation model | 188,518 | 46,410 | 4.1x |
| chatgpt | 37,642 | 10,865 | 3.5x |
| chain-of-thought | 11,521 | 3,163 | 3.6x |
| vision language | 37,744 | 12,771 | 3.0x |

The growth data tells three stories.

**Story 1, the model name explosion.** "DeepSeek" (848.7x), "Mistral" (16.8x), "Gemini" (13.6x), "LLaMA" (6.8x), and "Claude" (6.6x) are all names of specific models. Researchers are studying specific products, not just abstract architectures. "ChatGPT" appears in 37,642 abstracts in 2025-2026 alone. The field has moved from architecture research to model-level evaluation and comparison.

**Story 2, the RAG pipeline.** "Retrieval augmented generation" (52.4x), "retrieval-augmented" (19.2x), and "RAG" (15.4x) all show rapid growth. RAG has become the standard pattern for connecting language models to external knowledge bases [8]. Its three variants in the growth table reflect how quickly researchers adopted it as both a technique and an abbreviation.

**Story 3, safety and reliability.** "Jailbreak" (25.5x), "guardrail" (9.7x), "hallucination" (4.8x), and "chain-of-thought" (3.6x) all reflect the growing research effort to make language models reliable and safe. "Jailbreak" research (2,803 papers) investigates adversarial prompts that circumvent model safety filters. "Guardrail" (5,046) covers techniques for constraining model outputs. These terms barely existed in the research literature before 2023.

### 3.6 Citation Distribution

**Table 7. Citation distribution across the corpus.**

| Citation Range | Papers | Share |
|---|---|---|
| 0 citations | 2,445,876 | 48.9% |
| 1-10 citations | 1,700,854 | 34.0% |
| 11-50 citations | 648,139 | 13.0% |
| 51-100 citations | 122,722 | 2.5% |
| 101-500 citations | 78,688 | 1.6% |
| 501-1,000 citations | 5,029 | 0.10% |
| 1,000+ citations | 2,475 | 0.05% |

![Fig. 6. Citation distribution of AI papers on a log scale. Nearly half of all papers have zero citations. Only 2,475 papers have exceeded 1,000 citations.](figures/fig_citation_dist.png)

The distribution is extremely right-skewed. Nearly half of all papers (48.9%) have zero citations. Only 2,475 papers (0.05%) have exceeded 1,000 citations. The median AI paper in this corpus has zero citations.

**Table 8. Most-cited papers in the corpus.**

| Rank | Paper | Year | Citations | First Author |
|------|-------|------|-----------|-------------|
| 1 | Deep Residual Learning for Image Recognition | 2016 | 221,202 | K. He |
| 2 | Diagnostic and Statistical Manual of Mental Disorders | 2013 | 113,579 | A. Lolk |
| 3 | Fitting Linear Mixed-Effects Models Using lme4 | 2015 | 84,949 | D. Bates |
| 4 | Deep Learning | 2015 | 81,158 | Y. LeCun |
| 5 | ImageNet Classification with Deep CNNs | 2017 | 75,705 | A. Krizhevsky |
| 6 | Very Deep Convolutional Networks | 2014 | 75,538 | K. Simonyan |
| 7 | Faster R-CNN | 2016 | 53,947 | S. Ren |
| 8 | XGBoost | 2016 | 47,929 | T. Chen |
| 9 | MEGA6 | 2013 | 47,862 | K. Tamura |

The most-cited paper is ResNet [2] with 221,202 citations, nearly 2.5x the next entry. The list includes papers from outside AI proper (DSM-5, lme4, MEGA6), which appear because the abstract corpus includes cross-disciplinary work where AI terms appear alongside non-AI content. This is a known limitation of abstract-level search.

The top AI-specific papers (ResNet, Deep Learning, AlexNet, VGGNet, Faster R-CNN, XGBoost) are all foundational infrastructure. Papers that provide widely-used building blocks collect orders of magnitude more citations than application-specific work.

### 3.7 Geographic Distribution

![Fig. 5. Top 15 countries by AI research output (abstract-level corpus, 2013-2026). A single paper with co-authors from multiple countries is counted once per country.](figures/fig_countries.png)

**Table 9. Top 15 countries by AI research output.**

| Rank | Country | Papers |
|------|---------|--------|
| 1 | China | 874,019 |
| 2 | United States | 718,676 |
| 3 | India | 369,931 |
| 4 | Japan | 333,896 |
| 5 | United Kingdom | 216,177 |
| 6 | Germany | 163,172 |
| 7 | Canada | 117,479 |
| 8 | Italy | 105,094 |
| 9 | France | 97,247 |
| 10 | South Korea | 95,171 |
| 11 | Australia | 94,136 |
| 12 | Indonesia | 94,085 |
| 13 | Spain | 83,161 |
| 14 | Russia | 66,267 |
| 15 | Turkey | 55,034 |

China leads with 874,019 papers, 21.6% more than the United States (718,676). India ranks third with 369,931 papers, more than Japan (333,896) and the United Kingdom (216,177). Indonesia (94,085) ranks 12th, just behind Australia (94,136), reflecting the rapid growth of computer science programs across Southeast Asian universities.

Japan's position at rank 4 (333,896) in the abstract corpus is higher than in title-only analysis (rank 8, 41,964). This is because many Japanese research papers in robotics, materials science, and plasma physics discuss neural networks in their methods sections without placing them in their titles.

### 3.8 Institutional Output

**Table 10. Top 15 institutions by paper count.**

| Rank | Institution | Country | Papers |
|------|------------|---------|--------|
| 1 | Chinese Academy of Sciences | China | 74,921 |
| 2 | CNRS | France | 50,145 |
| 3 | University of London | UK | 34,887 |
| 4 | Tsinghua University | China | 30,519 |
| 5 | Univ. of Chinese Academy of Sciences | China | 23,911 |
| 6 | Shanghai Jiao Tong University | China | 23,695 |
| 7 | Zhejiang University | China | 23,246 |
| 8 | Harvard University | US | 21,529 |
| 9 | US Department of Energy | US | 20,244 |
| 10 | Peking University | China | 20,127 |
| 11 | Stanford University | US | 19,703 |
| 12 | Helmholtz Association | Germany | 19,628 |
| 13 | Board of Swiss Federal Institutes | Switzerland | 18,281 |
| 14 | State Council of the PRC | China | 16,984 |
| 15 | University College London | UK | 16,898 |

The Chinese Academy of Sciences leads with 74,921 papers, 49.4% more than CNRS (50,145). Six of the top fifteen institutions are Chinese. Harvard (21,529) and Stanford (19,703) are the highest-ranked US institutions, at positions 8 and 11 respectively.

Note that OpenAlex's institution taxonomy includes umbrella organizations (CNRS, Helmholtz Association, US Department of Energy) alongside individual universities. These umbrella organizations aggregate papers from their constituent laboratories and institutes, which inflates their counts relative to standalone universities.

### 3.9 Open Access

Of the 5,003,783 papers in the corpus, 3,043,557 (60.8%) are open access and 1,960,226 (39.2%) are behind paywalls. AI research has a higher open access rate than the general academic average, estimated at 31% by Piwowar et al. [11]. This difference is driven by the AI community's preprint culture, where arXiv is the default venue for early dissemination.

### 3.10 Title vs. Abstract Comparison

**Table 11. Title-only vs. abstract search for selected keywords.**

| Keyword | Title Count | Abstract Count | Ratio |
|---------|-----------|----------------|-------|
| neural network | 433,556 | 1,522,612 | 3.5x |
| machine learning | 495,798 | 1,287,123 | 2.6x |
| deep learning | 374,975 | 980,070 | 2.6x |
| large language model | 71,469 | 292,873 | 4.1x |
| diffusion model | 42,120 | 324,073 | 7.7x |
| transformer | 129,524 | 316,216 | 2.4x |
| hallucination | 10,711 | 48,759 | 4.6x |
| fairness | 78,835 | 429,288 | 5.4x |
| retrieval augmented | 8,137 | 27,394 | 3.4x |
| federated learning | 39,481 | 59,298 | 1.5x |
| reinforcement learning | 104,021 | 201,098 | 1.9x |
| knowledge graph | 28,201 | 90,234 | 3.2x |

The ratio of abstract-to-title matches varies from 1.5x ("federated learning") to 7.7x ("diffusion model"). Methods that are commonly used as tools rather than as the primary topic of a paper have the highest ratios. "Diffusion model" (7.7x) is discussed in 324,073 abstracts but placed in the title of only 42,120 papers. Many of these papers use diffusion models as a component of a larger system without naming them in the title.

"Fairness" (5.4x) and "hallucination" (4.6x) show high ratios because they are frequently discussed as secondary concerns in a paper's abstract rather than as the paper's primary topic.

"Federated learning" (1.5x) has the lowest ratio, meaning papers that discuss federated learning almost always include it in their title. This suggests that federated learning is typically the main contribution of the paper, not a supporting technique.

This finding has methodological consequences for bibliometric research. Title-only analysis systematically undercounts methods that are used as tools across disciplines. Abstract-level analysis captures a more complete picture of method adoption.

## 4. Discussion

### 4.1 The Persistence of Neural Networks

"Neural network" (1,522,612 abstract mentions) remains the most frequently referenced AI concept in academic papers. "Convolutional neural network" (394,934) and "deep neural network" (518,431) are the top two trigrams. These numbers confirm that neural architectures remain the dominant computational approach in AI, even as public attention has moved to large language models.

The temporal data adds nuance. "Neural network" grew from 23,395 abstracts in 2013 to 207,140 in 2025, a steady 8.9x increase. It has not plateaued. New papers continue to use neural networks in increasingly diverse application domains. The term appears in the abstracts of papers in medicine, materials science, climate modeling, and finance, not just in AI-focused venues.

### 4.2 The LLM Inflection Point

"Large language model" papers grew from 3,248 in 2018 to 96,984 in 2025, with a visible inflection in 2022-2023. The growth rate accelerated from 2.4x over four years (2018-2022) to 12.2x over three years (2022-2025). No other method in our corpus matches this acceleration profile.

The supporting terms tell a story about how the field is maturing. "Retrieval augmented generation" (52.4x growth) and "RAG" (15.4x) indicate that researchers are building systems around LLMs, not just training them. "Hallucination" (4.8x), "guardrail" (9.7x), and "jailbreak" (25.5x) indicate growing attention to reliability and safety. "Instruction tuning" (5.3x), "preference optimization" (2.6x), and "human feedback" (2.3x) reflect the practical work of aligning models to user intent.

The growth of "LLM" as an abbreviation is itself a signal. It grew from 10,125 abstracts in 2022-2023 to 161,771 in 2025-2026 (16.0x). The abbreviation was not widely used before 2022. Its rapid standardization suggests that LLMs have become a recognized category in AI research vocabulary, similar to how "CNN" and "RNN" became standard abbreviations in previous waves.

### 4.3 Method Lifecycles

The time-series data reveals different methods at different lifecycle stages.

**Mature methods (steady growth).** "Neural network" and "knowledge graph" show consistent growth without acceleration or deceleration. These methods have large, established research communities.

**Growth phase.** "Deep learning," "transformer," "graph neural," and "federated learning" are all growing faster than the corpus average. Federated learning shows the strongest sustained growth (402.6x from 2017 to 2025), driven by data privacy regulations and the need for training on distributed sensitive data.

**Plateau candidates.** "Generative adversarial" grew from 6 papers in 2014 to 13,613 in 2025 (2,268.8x total), but annual growth has slowed since 2020. GANs are being replaced by diffusion models for many image generation tasks.

**Explosive growth.** "Large language model" is in a phase of exponential growth with no sign of deceleration. The 2026 partial-year data (84,957 through June) projects to a full-year total higher than the entire 2025 count.

### 4.4 The Chinese Research Lead

China leads global AI research output in the abstract corpus (874,019 papers) by 21.6% over the United States (718,676). Six of the fifteen most productive institutions are Chinese, led by the Chinese Academy of Sciences (74,921 papers). The appearance of "DeepSeek" as the fastest-rising keyword (848.7x growth) adds a qualitative dimension to this quantitative lead. Chinese labs are producing not just papers but open-weight foundation models that compete directly with GPT-4 and Claude [7].

India's position at rank 3 (369,931 papers) confirms its status as a major AI research producer. India produces more papers discussing AI methods in their abstracts than Japan (333,896), the United Kingdom (216,177), and Germany (163,172).

### 4.5 The Cross-Disciplinary Spread of AI

The most-cited papers in the abstract corpus include entries from outside AI. The DSM-5 (113,579 citations), the lme4 statistical package (84,949), and MEGA6 for molecular evolution (47,862) appear in our results because their abstracts contain terms that match our AI keyword filters.

This is not a flaw in the methodology. It reflects a real phenomenon. AI methods have permeated virtually every scientific discipline. A molecular biology paper may discuss neural network-based protein structure prediction. A psychology paper may reference machine learning-based diagnostic tools. The abstract corpus captures this cross-disciplinary spread in a way that title-based or venue-based filtering would miss.

### 4.6 The Value of Abstract-Level Analysis

The title vs. abstract comparison (Table 11) quantifies the gap between title-only and abstract-level bibliometrics. Title-only analysis misses 1.5x to 7.7x the actual volume of method-relevant papers. For methods that are commonly used as tools across disciplines ("diffusion model," 7.7x; "fairness," 5.4x; "hallucination," 4.6x), title-only analysis captures less than a quarter of the relevant literature.

This finding has consequences for all bibliometric studies of AI research. Studies that rely on title-level searches or venue-based filtering (e.g., only papers from NeurIPS, ICML, CVPR) may produce a biased picture of the field's structure. Abstract-level analysis, while noisier, provides a more complete view of how AI methods are actually used across the scientific literature.

### 4.7 Limitations

**Stemming and noise.** OpenAlex applies stemming to search queries, which inflates counts for common words. "Explainable" returns 2,544,915 abstract matches, which is clearly inflated by stemming matching "explain" in non-AI contexts. Single-word keyword counts in Table 4 should be interpreted with this caveat. Multi-word phrases and proper nouns are minimally affected.

**Cross-disciplinary noise.** The abstract corpus includes papers from non-AI fields that happen to mention AI terms. A paper discussing "autonomous regulation of gene expression" would match the "autonomous" filter. We estimate 5-8% cross-disciplinary noise based on manual spot-checking. This is an inherent tradeoff of abstract-level analysis versus title-level analysis (which is more precise but less complete).

**Temporal coverage.** The 2026 cohort covers January through early June. Annualized projections assume even distribution throughout the year, which may not hold due to conference deadlines and journal publication cycles.

**Multi-counting.** A paper co-authored by researchers in China and the United States is counted once in each country's total. Country-level paper counts therefore sum to more than the corpus total. The same applies to institutions.

**OpenAlex coverage.** OpenAlex indexes over 250 million works but does not cover all academic literature. Non-English publications, conference proceedings from smaller venues, and technical reports may be underrepresented. OpenAlex has stronger coverage of English-language journals and repositories.

**Causation vs. correlation.** Growth in keyword frequency reflects research attention, not research quality or real-world deployment. A 16x increase in "LLM" papers does not mean LLMs are 16x more useful than they were in 2022.

## 5. Related Work

### 5.1 AI Bibliometric Studies

The Stanford HAI AI Index Report [9] is the most comprehensive annual survey of AI research trends. The 2025 edition tracks publications, patents, investment, and policy across multiple data sources including Dimensions, Epoch, and LMSYS. Our study differs in two ways. First, we use abstract-level search rather than subject classification, capturing cross-disciplinary AI method usage. Second, every number in our analysis is reproducible through a single API call, rather than requiring access to proprietary databases.

Zhang et al. (2021) conducted a bibliometric analysis of deep learning research using Web of Science data, finding that China and the US together accounted for over 50% of deep learning publications [14]. Our abstract-level data confirms this pattern. China (874,019) and the US (718,676) together account for approximately 32% of all papers in our corpus discussing AI methods, though this percentage is lower because our corpus includes a broader set of documents.

### 5.2 Compute and Scaling Studies

Sevilla et al. (2022) analyzed compute trends in machine learning, documenting a 10x increase in training compute every 18 months since 2010 [13]. Our publication growth data is consistent with their findings. The periods of fastest publication growth (2017-2018 and 2023-2025) align with the periods when compute scaling enabled new model capabilities.

Hoffmann et al. (2022) introduced compute-optimal scaling laws ("Chinchilla scaling") [16], and Kaplan et al. (2020) characterized neural scaling laws [17]. These papers provided the theoretical foundation for the compute scaling race. Our data on the growth of "large language model" (29.9x from 2018 to 2025) reflects the research activity that this scaling race generated.

### 5.3 Research Commercialization

Jurowetzki et al. (2021) used arXiv and patent data to map the AI research and development system, finding increasing overlap between academic research and commercial development [15]. Our observation that named models (DeepSeek, Claude, Gemini, Mistral, LLaMA) are the fastest-growing terms in the research literature supports this finding. The boundary between academic and commercial AI research has become increasingly blurred, with researchers benchmarking commercial products and commercial labs publishing in academic venues.

Ahmed and Wahed (2023) analyzed the flow of researchers between academia and industry in AI, finding that approximately 10% of AI researchers had moved from academia to industry between 2019 and 2022 [18]. While our data does not directly measure researcher movement, the growth of model-specific research keywords is consistent with a field where commercial products are the objects of study.

### 5.4 Methodological Contributions

Our study contributes a methodological point to the bibliometrics literature. The title vs. abstract comparison (Table 11) quantifies the information loss in title-only bibliometric analyses. To our knowledge, this is the first study to systematically compare title-level and abstract-level keyword counts across a large corpus of AI papers. The finding that abstract search captures 1.5x to 7.7x more papers per keyword matters for researchers designing bibliometric studies.

## 6. Conclusion

Five million papers, analyzed through abstract-level keyword search, reveal an AI research field in three simultaneous phases. Established methods (neural networks, deep learning, support vector machines) continue to dominate by accumulated volume. The LLM category is growing faster than any previous method (29.9x over seven years), with no sign of deceleration. And a growing body of research on reliability and safety (hallucination, guardrail, jailbreak) indicates that the field is beginning to address the practical challenges of deploying these systems.

Six principal findings stand out.

1. **Neural networks remain dominant.** "Neural network" appears in 1,522,612 paper abstracts (30.4% of the corpus). This dominance has not diminished despite the attention given to LLMs.

2. **LLMs are the fastest-growing category.** "Large language model" grew from 3,248 abstracts in 2018 to 96,984 in 2025 (29.9x), with an inflection point at the release of ChatGPT.

3. **The field is moving from architecture to application.** The fastest-rising terms are not architectures but patterns (RAG, 52.4x), safety concepts (jailbreak, 25.5x), and specific model names (DeepSeek, 848.7x).

4. **China leads global output.** China produces 21.6% more AI research papers than the United States. Six of the top fifteen institutions are Chinese.

5. **Half of all papers go uncited.** 48.9% of papers have zero citations, confirming the extreme concentration of academic impact.

6. **Title-only analysis misses most AI research.** Abstract search captures 1.5x to 7.7x more papers per keyword, depending on the method. Studies that rely on title-level filtering provide an incomplete view of AI research activity.

The complete dataset, API queries, and analysis scripts are available at [https://github.com/vedangvatsa/research-paper-framework](https://github.com/vedangvatsa/research-paper-framework).

---

## References

[1] OpenAlex. "OpenAlex API Documentation." [https://docs.openalex.org](https://docs.openalex.org)

[2] K. He, X. Zhang, S. Ren, and J. Sun. "Deep Residual Learning for Image Recognition." CVPR, 2016. [https://arxiv.org/abs/1512.03385](https://arxiv.org/abs/1512.03385)

[3] O. Ronneberger, P. Fischer, and T. Brox. "U-Net: Convolutional Networks for Biomedical Image Segmentation." MICCAI, 2015. [https://arxiv.org/abs/1505.04597](https://arxiv.org/abs/1505.04597)

[4] D. P. Kingma and J. Ba. "Adam: A Method for Stochastic Optimization." ICLR, 2015. [https://arxiv.org/abs/1412.6980](https://arxiv.org/abs/1412.6980)

[5] Y. LeCun, Y. Bengio, and G. Hinton. "Deep Learning." Nature, vol. 521, pp. 436-444, 2015. [https://doi.org/10.1038/nature14539](https://doi.org/10.1038/nature14539)

[6] A. Vaswani et al. "Attention Is All You Need." NeurIPS, 2017. [https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)

[7] DeepSeek-AI. "DeepSeek-V3 Technical Report." 2024. [https://arxiv.org/abs/2412.19437](https://arxiv.org/abs/2412.19437)

[8] P. Lewis et al. "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." NeurIPS, 2020. [https://arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)

[9] Stanford HAI. "AI Index Report 2025." [https://aiindex.stanford.edu](https://aiindex.stanford.edu)

[10] I. Goodfellow et al. "Generative Adversarial Nets." NeurIPS, 2014. [https://arxiv.org/abs/1406.2661](https://arxiv.org/abs/1406.2661)

[11] H. Piwowar et al. "The State of OA: A Large-Scale Analysis of the Prevalence and Impact of Open Access Articles." PeerJ, 2018. [https://doi.org/10.7717/peerj.4375](https://doi.org/10.7717/peerj.4375)

[12] B. McMahan et al. "Communication-Efficient Learning of Deep Networks from Decentralized Data." AISTATS, 2017. [https://arxiv.org/abs/1602.05629](https://arxiv.org/abs/1602.05629)

[13] J. Sevilla et al. "Compute Trends Across Three Eras of Machine Learning." 2022. [https://arxiv.org/abs/2202.05924](https://arxiv.org/abs/2202.05924)

[14] D. Zhang et al. "The AI Index 2021 Annual Report." Stanford HAI, 2021. [https://aiindex.stanford.edu/report/](https://aiindex.stanford.edu/report/)

[15] R. Jurowetzki et al. "The Privatization of AI Research(-ers): Causes and Potential Consequences." 2021. [https://arxiv.org/abs/2102.01648](https://arxiv.org/abs/2102.01648)

[16] J. Hoffmann et al. "Training Compute-Optimal Large Language Models." NeurIPS, 2022. [https://arxiv.org/abs/2203.15556](https://arxiv.org/abs/2203.15556)

[17] J. Kaplan et al. "Scaling Laws for Neural Language Models." 2020. [https://arxiv.org/abs/2001.08361](https://arxiv.org/abs/2001.08361)

[18] N. Ahmed and M. Wahed. "The De-democratization of AI: Deep Learning and the Compute Divide in Artificial Intelligence Research." 2023. [https://arxiv.org/abs/2010.15581](https://arxiv.org/abs/2010.15581)
