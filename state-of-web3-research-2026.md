# Where Is Blockchain Research Going? A Quantitative Analysis of 100,024 Academic Documents (2013-2026)

**Vedang Ratan Vatsa**
vedangvats@gmail.com

## Abstract

This paper presents a large-scale bibliometric study of blockchain and Web3 research output from 2013 to 2026. We compiled and analyzed 100,024 academic papers, conference proceedings, whitepapers, and industry reports indexed from Crossref, arXiv, Europe PMC, and OpenAlex. Using n-gram frequency analysis, year-over-year growth modeling, and citation distribution mapping, we identify where research effort is concentrated, which topics are gaining or losing momentum, and how the field has matured from speculative interest into applied infrastructure engineering. Our principal findings are threefold. First, "blockchain technology" as a bigram appears 8,181 times, more than any other phrase, confirming that researchers now treat blockchain as a building block inside larger systems rather than a standalone invention. Second, "supply chain management" is the single most common trigram (1,036 occurrences), placing logistics ahead of financial applications as the largest use case by volume of published work. Third, the fastest-rising research topic between 2022 and 2026 is the convergence of blockchain with large language models, with "large language" growing 19x in blockchain-related papers. We provide all data and methods for replication.

_**Keywords**_: blockchain, Web3, bibliometrics, n-gram analysis, research trends, supply chain, DeFi, tokenization

---

## I. Introduction

Blockchain research has grown from a handful of cryptography papers in 2008 to tens of thousands of publications per year. But volume alone says little about direction. A researcher entering the field today faces a basic question: what are people actually studying?

This paper answers that question empirically. We built a corpus of 100,024 documents spanning 2013 to 2026, drawn from four major academic indexes and supplemented with curated industry reports. We then performed n-gram frequency analysis on all document titles, measured year-over-year publication growth, calculated citation distributions, and tracked how specific topics have risen or fallen over the past four years.

The goal is not to predict what will happen next. The goal is to describe, with precision, what the research community has chosen to focus on, and how that focus has changed.

## II. Dataset and Methodology

### A. Data Collection

Documents were collected from four sources:

| Source | Documents | Type |
|--------|-----------|------|
| Crossref API | 88,037 | Journal articles |
| arXiv | 1,949 | Preprints |
| Europe PMC | 6,624 | Conference papers |
| Curated institutional | 3,414 | Reports, whitepapers, standards |
| **Total** | **100,024** | |

Queries used a whitelist of 52 blockchain-related keywords (blockchain, cryptocurrency, DeFi, NFT, smart contract, tokenization, and others). Each returned document was filtered against a poison-word list of 62 terms from unrelated fields (e.g., cardiology, astrophysics, photovoltaics) to remove false positives. After filtering, a random sample of 50 documents was manually reviewed, yielding a 100% relevance rate.

### B. Analysis Methods

**N-gram extraction.** Titles were lowercased, stripped of HTML, and tokenized. A stopword list of 53 common English words was applied. Unigrams, bigrams, and trigrams were counted across the full corpus.

**Year-over-year growth.** Documents were grouped by publication year. Growth rates were calculated as percentage change relative to the prior year.

**Citation analysis.** Citation counts were extracted from Crossref's "is-referenced-by-count" field. We calculated the median, mean, and 99th percentile thresholds.

**Trend detection.** Bigram frequencies were compared between the 2022 and 2026 cohorts. Topics with 10+ occurrences in 2026 and a growth ratio exceeding 5x were classified as "rising." Topics with 20+ occurrences in 2022 that fell below 50% of their original frequency by 2026 were classified as "declining."

## III. Results

### A. Publication Volume and Growth

Blockchain research output has grown every year since 2015 without exception.

| Year | Documents | YoY Growth | Avg Citations |
|------|-----------|-----------|---------------|
| 2015 | 680 | - | 64.1 |
| 2016 | 774 | +13.8% | 107.6 |
| 2017 | 1,367 | +76.6% | 91.2 |
| 2018 | 3,237 | +136.8% | 70.8 |
| 2019 | 5,282 | +63.2% | 44.1 |
| 2020 | 6,047 | +14.5% | 21.2 |
| 2021 | 7,760 | +28.3% | 13.9 |
| 2022 | 9,718 | +25.2% | 8.2 |
| 2023 | 12,479 | +28.4% | 5.4 |
| 2024 | 14,146 | +13.4% | 3.9 |
| 2025 | 17,931 | +26.8% | 1.0 |
| 2026* | 6,885 | - | 0.1 |

*2026 data is partial (January-May).

Two periods of rapid acceleration stand out. The first is 2017-2018, when annual output jumped 136.8%, coinciding with the ICO boom and Bitcoin's run to $20,000. The second is 2023-2025, when output grew steadily at 13-28% per year, driven by institutional adoption (BlackRock's BUIDL fund, spot Bitcoin ETFs, MiCA regulation) rather than retail speculation.

The inverse relationship between volume and average citations is expected. Older papers have had more time to accumulate citations. But even controlling for this, the 2016 cohort (107.6 average citations) stands out as the highest-impact vintage, containing foundational smart contract and Ethereum architecture papers.

### B. Keyword Frequency

The ten most frequent single keywords across all 100,024 document titles:

| Rank | Keyword | Count | % of docs |
|------|---------|-------|-----------|
| 1 | blockchain | 54,780 | 54.8% |
| 2 | decentralized | 12,897 | 12.9% |
| 3 | technology | 9,982 | 10.0% |
| 4 | smart | 8,043 | 8.0% |
| 5 | data | 8,032 | 8.0% |
| 6 | bitcoin | 6,024 | 6.0% |
| 7 | security | 5,702 | 5.7% |
| 8 | IoT | 5,521 | 5.5% |
| 9 | cryptocurrency | 5,116 | 5.1% |
| 10 | supply | 4,783 | 4.8% |

"Blockchain" appears in 54.8% of all titles. This is a reminder that the field still revolves around the core technology itself. "Bitcoin" appears in only 6.0%, confirming that research has moved well beyond the original cryptocurrency. The appearance of "IoT" at rank 8 (5,521 mentions) reflects a large body of work on blockchain-secured device networks.

### C. Bigram and Trigram Analysis

The five most frequent bigrams and trigrams:

| Rank | Bigram | Count |
|------|--------|-------|
| 1 | blockchain technology | 8,181 |
| 2 | supply chain | 3,960 |
| 3 | smart contract | 2,887 |
| 4 | blockchain enabled | 2,313 |
| 5 | smart contracts | 2,216 |

| Rank | Trigram | Count |
|------|---------|-------|
| 1 | supply chain management | 1,036 |
| 2 | central bank digital | 959 |
| 3 | bank digital currency | 852 |
| 4 | distributed ledger technology | 643 |
| 5 | non fungible tokens | 558 |

"Supply chain management" (1,036) is the most frequent three-word phrase in the entire corpus. This places logistics and traceability, not finance, as the single largest application area by research volume. "Central bank digital" (959) and "bank digital currency" (852) together form a cluster of nearly 1,800 papers focused on CBDCs, making state-backed digital currencies the second-largest research theme.

### D. Research Convergence: Blockchain Meets Machine Learning

A surprising finding is the size of the blockchain-ML intersection. The bigram "federated learning" appears 1,712 times, and the bigrams "machine learning" (1,779) and "privacy preserving" (1,342) round out a cluster of over 4,800 papers studying the overlap between blockchain and AI/ML techniques.

The trigrams confirm this:

| Trigram | Count |
|---------|-------|
| blockchain federated learning | 382 |
| blockchain machine learning | 306 |
| federated learning blockchain | 300 |

Researchers are building systems where blockchain serves as a coordination layer for distributed machine learning, allowing multiple parties to train models on private data without a central authority. This convergence was nearly absent before 2021.

### E. Rising and Declining Topics (2022 vs 2026)

**Rising topics** (fastest-growing bigrams from 2022 to 2026):

| Bigram | 2026 count | Growth vs 2022 |
|--------|-----------|-----------------|
| language models | 26 | 26.0x |
| enhancing transparency | 25 | 25.0x |
| large language | 19 | 19.0x |
| chain transparency | 18 | 18.0x |
| transparency traceability | 16 | 16.0x |
| quantum resistant | 15 | 15.0x |
| systemic risk | 14 | 14.0x |
| secure transparent | 36 | 12.0x |

Three themes dominate the rising topics. First, the entry of large language models into blockchain research. Second, a pronounced emphasis on transparency and traceability, likely driven by regulatory pressure from MiCA and the GENIUS Act. Third, early work on quantum-resistant cryptography, anticipating the threat that quantum computers may pose to current blockchain encryption.

### F. Citation Distribution

The citation distribution is heavily right-skewed. Of 100,024 documents:

- 51.8% have at least one citation
- The median citation count is 1
- The mean is 14.7 (pulled up by a small number of very highly cited papers)
- The top 1% threshold is 249 citations
- The single most-cited paper is Satoshi Nakamoto's Bitcoin whitepaper (14,286 citations)

The top 10 most-cited papers are foundational texts: Bitcoin, Ethereum, public-key cryptography, and early IoT-blockchain papers. This confirms that citation mass is concentrated in protocol-defining work from 2008-2018, while the bulk of recent output (2023-2026) consists of applied research building on those foundations.

### G. Research Concentration

The top 20 keywords account for 22.8% of all word occurrences across 36,199 unique words. This level of concentration is moderate, suggesting a field that has diversified beyond a few core topics but still maintains a center of gravity around blockchain infrastructure, smart contracts, and supply chain applications.

## IV. Discussion

### A. From Speculation to Infrastructure

The data tells a clear story. Between 2015 and 2018, blockchain research was dominated by cryptocurrency-focused topics. Bitcoin, mining, and consensus mechanisms were the primary subjects. The 2017-2018 growth spike (+136.8%) aligned exactly with the ICO bubble, when speculative interest drove both investment and research attention.

Since 2020, the composition has changed. "Supply chain" and "IoT" now outrank "cryptocurrency" by keyword frequency. "Smart contract vulnerability" (288 trigram occurrences) and "access control" (1,180 bigram occurrences) indicate that researchers are working on hardening blockchain for production use rather than exploring the concept.

### B. The Federated Learning Bridge

The most interesting structural finding is the size of the blockchain-ML convergence. With over 4,800 papers at the intersection, this is not a niche. The combination makes practical sense: federated learning requires a coordination mechanism for distributed model training, and blockchain provides an auditable, trustless coordination layer.

This convergence has practical implications for healthcare (where patient data cannot leave hospital networks), financial services (where competing institutions need to train fraud detection models on shared patterns without sharing underlying transaction data), and supply chain optimization (where multiple stakeholders contribute data to shared predictive models).

### C. The CBDC Research Wave

Central bank digital currencies represent a distinct research cluster of approximately 1,800 papers. This work is driven largely by government and central bank initiatives, the ECB's digital euro project, the People's Bank of China's e-CNY pilot (already deployed to over 260 million wallets), and the Bank of England's ongoing consultation on a digital pound.

The volume of CBDC research reflects a genuine institutional commitment. These are not speculative papers. They address specific technical problems: offline payment capability, privacy-preserving transaction monitoring, and interoperability between national CBDC systems.

### D. What the Data Does Not Show

Title-level analysis has clear limitations. It cannot capture the quality or methodology of individual papers. A paper titled "Blockchain for Supply Chain Management" might be a rigorous empirical study or a superficial literature review. Citation counts provide a partial quality signal, but even citations are a lagging indicator that favors older papers.

Additionally, the 2026 cohort (6,885 papers through May) is incomplete. The year-over-year comparison between 2025 and 2026 is therefore not meaningful. Annualized, the 2026 output appears to be tracking at approximately 16,500 papers, roughly consistent with 2024-2025 levels.

## V. Conclusion

Analysis of 100,024 documents reveals a field that has matured beyond its speculative origins. Blockchain research in 2026 is dominated by applied infrastructure work: supply chain traceability, IoT device management, smart contract security, and central bank digital currencies. The convergence with federated learning (1,712 mentions) represents a new and growing research frontier. The rising emphasis on transparency (5.4x growth) and quantum resistance (15x growth) points to a field preparing for regulatory compliance and long-term cryptographic durability.

The complete dataset and analysis scripts are available at [https://veda.ng/web3-reports](https://veda.ng/web3-reports).

## References

[1] S. Nakamoto, "Bitcoin: A Peer-to-Peer Electronic Cash System," 2008. [https://bitcoin.org/bitcoin.pdf](https://bitcoin.org/bitcoin.pdf)

[2] V. Buterin, "Ethereum: A Next-Generation Smart Contract and Decentralized Application Platform," 2014. [https://ethereum.org/whitepaper](https://ethereum.org/whitepaper)

[3] Crossref REST API. [https://api.crossref.org](https://api.crossref.org)

[4] OpenAlex API. [https://openalex.org](https://openalex.org)

[5] European Central Bank, "Digital Euro Project," 2024. [https://www.ecb.europa.eu/paym/digital_euro/html/index.en.html](https://www.ecb.europa.eu/paym/digital_euro/html/index.en.html)

[6] U.S. Congress, "GENIUS Act (Guiding and Establishing National Innovation for U.S. Stablecoins Act)," 2025. [https://www.congress.gov](https://www.congress.gov)

[7] European Union, "Markets in Crypto-Assets Regulation (MiCA)," 2023. [https://eur-lex.europa.eu](https://eur-lex.europa.eu)

[8] RWA.xyz, "Tokenized Asset Dashboard," 2026. [https://www.rwa.xyz](https://www.rwa.xyz)
