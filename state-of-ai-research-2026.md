# What 137,068 Papers Tell Us About the Direction of AI Research (2013-2026)

**Vedang Ratan Vatsa**
vedangvats@gmail.com

## Abstract

We present a quantitative bibliometric study of artificial intelligence research output from 2013 to 2026, covering 137,068 academic papers, conference proceedings, whitepapers, and industry reports. Documents were indexed from Crossref, arXiv, Europe PMC, OpenAlex, and curated institutional sources. Through title-level n-gram frequency analysis, year-over-year growth rate computation, citation distribution modeling, and cohort-based trend detection, we map the structure of AI research as it stands today. Three principal findings stand out. First, "neural network" (12,449 occurrences) remains the top bigram, confirming that neural architectures are still the workhorse of the field despite the attention given to newer methods. Second, "agentic" is the fastest-rising keyword in the entire corpus, growing 457x between the 2022 and 2025-2026 cohorts, marking the transition from passive model inference to autonomous multi-step AI systems. Third, "few shot" (4,466) has nearly matched "large language" (4,449) in bigram frequency, suggesting that data-efficient learning methods receive as much research attention as the large language models themselves. All data and methods are available for replication.

_**Keywords**_: artificial intelligence, machine learning, bibliometrics, n-gram analysis, research trends, agentic AI, large language models, neural networks

---

## I. Introduction

The volume of AI research has grown so rapidly that no individual researcher can track the full breadth of the field. In 2025 alone, over 34,000 papers with AI-related titles were published in the databases we indexed. This raises an obvious question: across all of this output, where is the research effort actually going?

We built a dataset of 137,068 documents and measured what the field is producing. This is not a survey of methods or a review of state-of-the-art benchmarks. It is a count of what researchers chose to put in their paper titles, how frequently certain topics appear, which topics are growing or shrinking, and how citations are distributed across the corpus.

The approach is simple and replicable. We extract n-grams from titles, group documents by year, and compute ratios. The results are descriptive, not predictive.

## II. Dataset and Methodology

### A. Data Collection

| Source | Documents | Type |
|--------|-----------|------|
| Crossref API | 96,108 | Journal articles |
| Conference proceedings | 22,935 | Conference papers |
| Books/chapters | 12,381 | Book contributions |
| Industry reports | 3,871 | Reports, whitepapers, standards |
| Preprints (arXiv) | 1,773 | Preprints |
| **Total** | **137,068** | |

Documents were retrieved using a whitelist of 120+ AI-related keywords (artificial intelligence, machine learning, neural network, large language model, transformer, reinforcement learning, computer vision, and others). A poison-word filter removed false positives from unrelated fields. A random sample of 50 entries was manually verified, yielding 100% domain relevance.

### B. Analysis Pipeline

1. **Tokenization.** Each title was lowercased, HTML-stripped, and split into tokens. A 53-word stopword list removed common English function words plus generic academic terms ("study," "approach," "review").
2. **N-gram counting.** Unigrams, bigrams, and trigrams were tabulated across the full corpus and within yearly cohorts.
3. **Growth detection.** Keywords and bigrams were compared between the 2022-2023 cohort (22,612 papers) and the 2025-2026 cohort (48,998 papers). Growth ratios were calculated as new_count / max(old_count, 1).
4. **Citation modeling.** Citation counts from Crossref were used to compute percentile distributions and identify the most-cited papers.

## III. Results

### A. Publication Volume

AI research output has grown every year in our dataset.

| Year | Documents | YoY Growth | Avg Citations |
|------|-----------|-----------|---------------|
| 2015 | 2,186 | - | 48.7 |
| 2016 | 2,607 | +19.3% | 52.3 |
| 2017 | 3,369 | +29.2% | 46.8 |
| 2018 | 4,988 | +48.1% | 35.2 |
| 2019 | 6,421 | +28.7% | 24.6 |
| 2020 | 7,848 | +22.2% | 17.3 |
| 2021 | 8,132 | +3.6% | 12.1 |
| 2022 | 8,581 | +5.5% | 8.0 |
| 2023 | 14,031 | +63.5% | 4.6 |
| 2024 | 22,584 | +60.9% | 2.1 |
| 2025 | 34,275 | +51.8% | 0.5 |
| 2026* | 14,723 | - | 0.1 |

*2026 data is partial (January-May).

The growth curve shows two distinct phases. From 2015 to 2022, output grew at a steady 3-48% per year. Starting in 2023, growth accelerated sharply to 51-63% annually. This inflection point aligns with the release of ChatGPT (November 2022) and the subsequent flood of LLM-related research. The 2023 cohort alone (14,031 papers) nearly matched the entire 2022 output (8,581), a 63.5% jump in a single year.

### B. Keyword Frequency

The ten most frequent single keywords:

| Rank | Keyword | Count | % of docs |
|------|---------|-------|-----------|
| 1 | learning | 35,068 | 25.6% |
| 2 | network | 15,570 | 11.4% |
| 3 | neural | 14,965 | 10.9% |
| 4 | detection | 11,495 | 8.4% |
| 5 | deep | 11,253 | 8.2% |
| 6 | language | 8,936 | 6.5% |
| 7 | intelligence | 8,911 | 6.5% |
| 8 | generative | 8,142 | 5.9% |
| 9 | recognition | 6,759 | 4.9% |
| 10 | autonomous | 6,653 | 4.9% |

"Learning" appears in one out of every four paper titles. This confirms that the field's identity is still centered on learning algorithms rather than, say, symbolic reasoning or expert systems. "Generative" (8,142, 5.9%) has entered the top 10, reflecting the post-2022 wave of generative model research.

### C. Bigram Analysis

| Rank | Bigram | Count |
|------|--------|-------|
| 1 | neural network | 12,449 |
| 2 | machine learning | 10,278 |
| 3 | artificial intelligence | 8,054 |
| 4 | deep learning | 7,788 |
| 5 | reinforcement learning | 4,856 |
| 6 | few shot | 4,466 |
| 7 | large language | 4,449 |
| 8 | object detection | 4,292 |
| 9 | attention mechanism | 4,238 |
| 10 | question answering | 3,843 |

The near-parity between "few shot" (4,466) and "large language" (4,449) is one of the more notable findings. While public discourse has focused heavily on large language models, the research community has devoted nearly equal attention to few-shot learning, the problem of making models work with very little labeled data. This makes sense practically: most enterprises do not have millions of labeled examples for their specific use cases.

"Attention mechanism" at rank 9 (4,238) captures the transformer architecture's dominance. The trigram "convolutional neural network" (4,216) and "recurrent neural network" (3,621) show that CNNs and RNNs remain heavily studied even as transformers gain ground.

### D. Trigram Analysis

| Rank | Trigram | Count |
|------|---------|-------|
| 1 | convolutional neural network | 4,216 |
| 2 | recurrent neural network | 3,621 |
| 3 | few shot learning | 2,002 |
| 4 | natural language processing | 1,561 |
| 5 | large language models | 1,541 |
| 6 | deep reinforcement learning | 1,277 |
| 7 | visual question answering | 658 |
| 8 | automatic speech recognition | 583 |
| 9 | medical image segmentation | 457 |
| 10 | machine learning techniques | 441 |

"Convolutional neural network" (4,216) exceeds "large language models" (1,541) by a factor of 2.7x. This gap reflects the accumulated mass of computer vision research over the past decade. CNNs have been the workhorse of image classification, object detection, and medical imaging for years. LLMs, while dominant in public attention since 2023, have not yet matched the cumulative research volume of vision architectures.

"Medical image segmentation" (457) appears as a standalone trigram, confirming healthcare as the highest-stakes application domain. "Deep reinforcement learning" (1,277) captures the robotics and control systems research cluster.

### E. The Fastest-Rising Keywords (2025-2026 vs 2022-2023)

| Keyword | 2025-2026 count | Growth ratio |
|---------|----------------|-------------|
| agentic | 457 | 457.0x |
| rag | 149 | 149.0x |
| deepseek | 123 | 123.0x |
| personalization | 106 | 35.3x |
| gemini | 143 | 28.6x |
| gen | 153 | 25.5x |
| pedagogy | 89 | 29.7x |
| strategic | 334 | 33.4x |

"Agentic" is the single fastest-rising keyword, growing from near-zero in 2022 to 457 mentions in 2025-2026. This word barely existed in AI research before 2024. Its sudden appearance marks a real shift in what researchers are building: not models that answer questions when prompted, but systems that plan, execute multi-step workflows, and act on their own.

"RAG" (retrieval-augmented generation) grew 149x, confirming its adoption as the standard pattern for connecting language models to private enterprise data. "DeepSeek" (123x) marks the arrival of Chinese open-weight foundation models as a competitive force in global AI research. "Gemini" (28.6x) reflects Google's multi-modal model family entering research benchmarks.

The appearance of "pedagogy" (29.7x growth) is worth noting. It signals a growing body of work studying how AI changes teaching and learning, a topic that moved from the margins to a dedicated research cluster following the widespread adoption of ChatGPT in educational settings.

### F. Citation Distribution

| Metric | Value |
|--------|-------|
| Documents with 1+ citations | 68.2% |
| Median citations | 3 |
| Mean citations | 18.4 |
| 99th percentile | 312 |
| Maximum | 38,412 |

The distribution is extremely right-skewed. A small number of foundational papers (attention mechanism papers, ResNet, BERT, GPT) collect thousands of citations, while the median paper has only 3. This pattern is consistent with other mature scientific fields.

### G. Research Categories

| Category | Documents | Share |
|----------|-----------|-------|
| ML Foundations | 58,903 | 43.0% |
| NLP and Language | 25,132 | 18.3% |
| Computer Vision | 15,382 | 11.2% |
| Robotics and RL | 12,733 | 9.3% |
| Generative AI | 8,294 | 6.0% |
| AI in Healthcare | 4,702 | 3.4% |
| AI Ethics and Safety | 4,056 | 3.0% |
| Knowledge and Graphs | 1,767 | 1.3% |
| Industry and Enterprise | 837 | 0.6% |

ML Foundations (43.0%) encompasses core methodology papers on training, optimization, regularization, and architecture design. NLP (18.3%) has grown to become the second-largest category, driven by the LLM wave. Computer Vision (11.2%) remains the third pillar. AI Ethics and Safety (3.0%, 4,056 papers) has grown from a negligible fraction to a visible research area, likely in response to the EU AI Act and similar regulatory initiatives.

## IV. Discussion

### A. The Neural Network Persistence

Despite the transformer revolution, "neural network" (12,449) remains the most frequent bigram by a wide margin. "Convolutional neural network" (4,216 as a trigram) and "recurrent neural network" (3,621) together account for nearly 8,000 papers. Transformers are growing rapidly, but they have not displaced the accumulated mass of CNN and RNN research.

This has a practical implication. The average enterprise deploying AI in 2026 is more likely to use a CNN for image classification or an RNN for time-series forecasting than a large language model for text generation. The research corpus reflects this deployment reality.

### B. The Few-Shot Gap

The near-parity between "few shot" (4,466) and "large language" (4,449) points to a disconnect between public perception and research priorities. Media coverage has focused almost entirely on large language models. But the research community has devoted equal effort to few-shot learning, a set of techniques for making models work with minimal labeled data.

This makes sense for enterprise adoption. Most companies do not have the millions of labeled examples required for traditional supervised learning. Few-shot methods (meta-learning, prompt-based learning, and in-context learning) address this bottleneck directly.

### C. The Agentic Turn

The 457x growth of "agentic" between 2022 and 2025-2026 is the most dramatic shift in the dataset. Combined with the 149x growth of "RAG" and the rise of "autonomous" (6,653 mentions total), these numbers describe a field that is moving from building better models to building systems that use those models to take action.

The practical manifestation is already visible. Salesforce, Microsoft, and Google have all shipped agent-based products (Agentforce, Copilot Agents, Gemini Agents) that go beyond question-answering to execute multi-step workflows: booking travel, processing invoices, managing customer support tickets. The research corpus shows that this product-level shift has a corresponding academic foundation.

### D. Limitations

Title-level analysis captures what researchers choose to emphasize but not the full content of their work. A paper titled "Deep Learning for Medical Image Segmentation" may also contribute to transfer learning or data augmentation without those topics appearing in the title. Our analysis therefore provides a lower-bound estimate of topic frequency.

Citation counts from Crossref are incomplete. Some publishers do not report citation data to Crossref, and self-citations are not distinguished from independent citations. The citation analysis should be treated as directional rather than exact.

The 2026 cohort covers only January through May. Annualized, the 2026 output appears to be tracking at approximately 35,000 papers, roughly consistent with 2025 levels. However, seasonal publication patterns (conference deadlines, journal review cycles) could affect this projection.

## V. Conclusion

137,068 documents reveal an AI research field in a specific phase of maturity. The foundational architectures (CNNs, RNNs, transformers) are established. The current growth is concentrated in three areas: large language models and few-shot learning methods (combined 8,915 bigram occurrences), agentic AI systems (457x growth), and retrieval-augmented generation (149x growth). Healthcare (4,702 papers) and AI ethics (4,056 papers) have established themselves as dedicated application and governance domains. The raw numbers suggest that the field's center of gravity is moving from "building better models" to "building systems that use models to do things in the world."

The complete dataset and analysis code are available at [https://veda.ng/ai-reports](https://veda.ng/ai-reports).

## References

[1] A. Vaswani et al., "Attention Is All You Need," NeurIPS, 2017. [https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)

[2] J. Devlin et al., "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding," 2018. [https://arxiv.org/abs/1810.04805](https://arxiv.org/abs/1810.04805)

[3] T. Brown et al., "Language Models are Few-Shot Learners," NeurIPS, 2020. [https://arxiv.org/abs/2005.14165](https://arxiv.org/abs/2005.14165)

[4] P. Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," NeurIPS, 2020. [https://arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)

[5] Crossref REST API. [https://api.crossref.org](https://api.crossref.org)

[6] OpenAlex API. [https://openalex.org](https://openalex.org)

[7] European Union, "AI Act," 2024. [https://artificialintelligenceact.eu](https://artificialintelligenceact.eu)

[8] Stanford HAI, "AI Index Report 2025." [https://aiindex.stanford.edu](https://aiindex.stanford.edu)
