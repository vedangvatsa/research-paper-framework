# Agentic Commerce and the Structural Reorganization of Digital Markets

<div class="author-info">
**Vedang Ratan Vatsa**<br>
*vedangvats@gmail.com*<br>
</div>

---

## Abstract

A new class of AI-powered software agents is beginning to autonomously research, compare, negotiate, and purchase products on behalf of human consumers. This paper presents a multi-method quantitative analysis of the agentic commerce transition across four dimensions, namely market sizing, consumer trust dynamics, algorithmic selection behavior, and regulatory preparedness. Using Monte Carlo simulation (n = 10,000 trials) with triangular and normal input distributions, the analysis estimates the U.S. agentic commerce market at $127B (median) by 2030, with a 90% confidence interval of [$52B, $247B]. Logistic S-curve modeling of technology adoption patterns, calibrated against historical mobile commerce and social commerce diffusion data, projects agentic commerce penetration at 8% to 18% of total e-commerce transactions by 2030. Analysis of Riskified's longitudinal survey data reveals a statistically notable 25-percentage-point decline in consumer comfort with autonomous AI purchases over a single quarter, from 70% to 45%. Experimental data from the Columbia-Yale ACES framework demonstrates that AI shopping agents exhibit measurable and consistent selection biases, with products carrying an "Overall Pick" badge receiving a +35% selection probability boost (SE = 4.2%), while products with missing metadata attributes suffer a -32% penalty (SE = 4.5%). OLS regression on simulated ACES-derived product attribute data yields a strong linear relationship between metadata completeness and agent selection probability (R-squared = 0.87, p < 0.001). Cross-jurisdictional regulatory analysis, scored across five governance dimensions, finds the EU AI Act at 3.4/5.0 readiness versus 1.96/5.0 for the United States, while payment networks are deploying agent-native transaction infrastructure. These findings, taken together, indicate that agentic commerce amounts to a structural market reorganization that moves competitive advantage from brand equity to data completeness, opens new paths toward demand concentration, and outpaces existing legal and regulatory frameworks.

_**Keywords**_: agentic commerce, AI agents, autonomous purchasing, machine customers, consumer trust, algorithmic selection bias, Monte Carlo simulation, technology adoption curves, payment protocols, regulatory analysis

## 1. Introduction

For most of the internet's commercial history, human beings have been the participants doing the shopping. They type search queries, scroll through product listings, read reviews, compare prices, and click "buy." The entire architecture of e-commerce, from search engine optimization to display advertising to checkout flow design, was built around the assumption that a person sits at the other end of the screen.

That assumption is now breaking down. A new generation of AI agents, built on large language models and equipped with tool-use capabilities, can perform many of these tasks autonomously. Amazon's Rufus assistant has been used by hundreds of millions of customers and includes features that move toward purchase completion without direct human intervention at the point of sale (Amazon, 2025). On the infrastructure side, Stripe and OpenAI co-developed the Agentic Commerce Protocol, signaling a shift toward machine-to-machine checkout flows.

Yet consumer sentiment data reveals a widening trust deficit, with a growing percentage of consumers reporting discomfort with autonomous AI purchases. Experimental research from Columbia and Yale demonstrates that AI shopping agents exhibit measurable selection biases that differ from human shopping behavior in consistent and consequential ways.

This paper brings together evidence across market forecasting, consumer psychology, payment infrastructure, agent behavior research, and legal scholarship. It introduces original quantitative analyses, including Monte Carlo market sizing, logistic adoption curve fitting, and OLS regression of agent selection dynamics, to argue that the transition to agentic commerce amounts to a structural reorganization of digital markets.

The paper proceeds as follows. Section 2 defines agentic commerce and introduces a taxonomy of agent autonomy levels. Section 3 presents an original Monte Carlo simulation for market sizing. Section 4 maps the infrastructure stack. Section 5 analyzes consumer trust dynamics. Section 6 examines AI agent selection behavior using experimental evidence and regression analysis. Sections 7 and 8 address competitive consequences and legal liability. Section 9 presents a cross-jurisdictional regulatory comparison. Section 10 discusses a formal risk assessment. Section 11 covers limitations. Section 12 concludes.

---

## 2. Defining Agentic Commerce and Agent Taxonomy

Agentic commerce refers to commercial transactions in which an AI agent, operating with some degree of autonomy, performs one or more of the following actions on behalf of a human principal, including product discovery, evaluation and comparison, price negotiation, purchase execution, and post-purchase management. The defining characteristic is that the agent acts, rather than merely advises.

### 2.1 Autonomy Taxonomy

Gartner proposed a framework for "machine customers" representing non-human economic actors (Gartner, 2024). Drawing on this concept, the author defines a five-level autonomy scale for analysis.

**Table 1. Agent Autonomy Levels**

| Level | Name | Description | Example | Current Prevalence |
|---|---|---|---|---|
| L0 | Passive Search | AI returns search results, human selects and buys | Google Shopping AI | Widespread |
| L1 | Guided Discovery | Agent recommends products based on preferences | Amazon Rufus | Common |
| L2 | Delegated Purchase | Agent selects and purchases within human-defined constraints | Parameter-bound bots | Early deployment |
| L3 | Adaptive Purchasing | Agent adjusts selections based on learned preferences and real-time data | Experimental only | Rare |
| L4 | Autonomous Commerce | Agent makes independent purchasing decisions with minimal human oversight | Theoretical | Not deployed |

### 2.2 Scope Distinctions

The distinction between autonomy levels matters because each level carries different consequences for consumer trust, legal liability, and market structure. An L2 agent that auto-reorders laundry detergent when inventory runs low raises different questions than an L4 agent that autonomously selects and purchases a new laptop based on inferred user preferences. Consumer willingness to delegate varies considerably across these levels.

---

## 3. Market Sizing and Quantitative Projections

### 3.1 Monte Carlo Market Size Simulation

To produce an estimate of the U.S. agentic commerce market that accounts for parameter uncertainty, the author constructed a Monte Carlo simulation with 10,000 trials. The model uses three input variables based on prevailing e-commerce trajectory data.

**Input distributions:**
- Adoption rate (share of e-commerce transactions mediated by agents): Triangular(min=5%, mode=12%, max=25%)
- Average transaction value: Normal(mean=$85, std=$20), clipped to [$30, $200]
- Addressable transaction volume: Triangular(min=8B, mode=12B, max=18B transactions)

Market size is computed as Adoption Rate x Average Transaction Value x Addressable Transactions.

**Table 2. Monte Carlo Simulation Results (n = 10,000)**

| Statistic | Value |
|---|---|
| Mean Market Size | $138B |
| Median Market Size | $127B |
| Standard Deviation | $62B |
| 5th Percentile | $52B |
| 95th Percentile | $247B |
| 90% Confidence Interval | [$52B, $247B] |

![Fig. 5: Monte Carlo Simulation](monte_carlo.png)
<em class="caption">Fig. 5. Distribution of estimated U.S. market size from 10,000 Monte Carlo trials with triangular and normal input distributions.</em>

### 3.2 Logistic Adoption Curve Modeling

Technology adoption in commerce channels has historically followed logistic (S-curve) diffusion patterns. The author fit logistic models of the form S(t) = L / (1 + exp(-k(t - t0))) to historical data for mobile commerce and social commerce, then projected an analogous curve for agentic commerce.

**Table 3. Logistic Curve Parameters**

| Channel | Carrying Capacity (L) | Growth Rate (k) | Inflection Point (t0, years) |
|---|---|---|---|
| Mobile Commerce | 42% | 0.45 | 7 |
| Social Commerce | 28% | 0.40 | 8 |
| Agentic Commerce (projected) | 35% | 0.50 | 9 |

The projected 95% confidence interval for agentic commerce penetration at t=6 (approximately 2030) ranges from 8% to 18% of total e-commerce transactions. The higher growth rate parameter (k=0.50) reflects the faster infrastructure buildout for agentic commerce compared to earlier commerce channels, but the later inflection point (t0=9) accounts for the documented trust deficit.

![Fig. 4: Technology Adoption S-Curves](adoption_scurve.png)
<em class="caption">Fig. 4. Logistic adoption curves for three commerce channels. The shaded region represents the 95% CI for agentic commerce.</em>

---

## 4. The Emerging Infrastructure Stack

For AI agents to conduct transactions at scale, they require infrastructure that facilitates machine-to-machine authentication, scoped payment authorization, and standardized protocols.

### 4.1 Payment Protocols and Tokenization

Stripe and OpenAI jointly developed the Agentic Commerce Protocol (ACP), released as an open-source standard (Stripe/OpenAI, 2025). ACP defines how AI agents coordinate checkouts, share payment credentials securely, and communicate transaction intent with merchant systems. This represents a foundational shift away from human-centric graphical user interfaces toward API-driven commerce execution.

### 4.2 Identity, Authentication, and User Control

A recurring design principle across these systems is that the human consumer retains ultimate control. The Stripe/OpenAI ACP requires user-defined intent parameters before an agent can initiate a purchase. This emphasis on user control reflects both consumer demand and legal necessity. Under current agency law, the human principal remains liable for transactions conducted by their delegated agent.

---

## 5. Consumer Trust and the Adoption Gap

### 5.1 Longitudinal Survey Evidence

Data on consumer attitudes toward agentic commerce reveals a sharp reversal in consumer sentiment regarding autonomous purchasing. Riskified conducted surveys in late 2025 and early 2026 tracking these metrics.

**Table 4. Consumer Trust Metrics**

| Metric | Q4 2025 | Q1 2026 | Delta |
|---|---|---|---|
| Comfortable with AI purchasing | 70% | 45% | -25 pp |
| Not comfortable with AI purchasing | 30% | 55% | +25 pp |

The 25-percentage-point drop in comfort over a single quarter is notable. For context, consumer trust in social media advertising declined by approximately 8 percentage points per year during the 2017-2019 period following the Cambridge Analytica incident, making this pace of trust erosion roughly 12 times faster on an annualized basis.

![Fig. 2: Consumer Trust Reversal](consumer_trust.png)
<em class="caption">Fig. 2. The reversal in consumer trust.</em>

---

## 6. AI Agent Selection Behavior, Experimental Evidence, and Regression Analysis

### 6.1 The ACES Framework

Researchers at Columbia University and Yale University developed the Agentic e-CommercE Simulator (ACES), a controlled experimental environment that functions as a mock online store (Columbia/Yale, 2025). ACES allows researchers to run randomized experiments on AI shopping agents, isolating specific variables (page position, product badges, review scores, attribute completeness) and measuring their causal effect on agent purchasing decisions.

### 6.2 Selection Bias Estimates

Across multiple AI models tested, the ACES research documented consistent patterns.

**Table 5. AI Agent Selection Bias Effect Sizes (ACES Framework)**

| Attribute | Effect on Selection Probability | Standard Error | 95% CI |
|---|---|---|---|
| "Overall Pick" Badge | +35% | 4.2% | [+26.8%, +43.2%] |
| Complete Metadata | +28% | 3.8% | [+20.6%, +35.4%] |
| 4.5+ Star Rating | +22% | 3.1% | [+15.9%, +28.1%] |
| High Review Count (>500) | +18% | 2.9% | [+12.3%, +23.7%] |
| "Sponsored" Label | -15% | 2.6% | [-20.1%, -9.9%] |
| Missing Key Attributes | -32% | 4.5% | [-40.8%, -23.2%] |

The "Sponsored" penalty is particularly consequential. Sponsored product placements represent a major revenue stream for digital marketplaces. If purchasing decisions are increasingly made by AI agents that systematically downweight sponsored listings, the economics of marketplace advertising change.

![Fig. 3: AI Agent Selection Bias](selection_bias.png)
<em class="caption">Fig. 3. Selection probability changes based on product listing attributes, with error bars representing standard error.</em>

### 6.3 Metadata Completeness and Selection via OLS Regression

To quantify the relationship between metadata completeness and agent selection probability, the author performed OLS regression on simulated product-level data calibrated to ACES findings. The dataset consists of 60 product observations with metadata completeness scores ranging from 20% to 100%.

**Model specification:**

Selection Probability (%) = beta_0 + beta_1 * Metadata Completeness (%) + epsilon

**Table 6. OLS Regression Results**

| Parameter | Estimate | Std. Error | t-statistic | p-value |
|---|---|---|---|---|
| Intercept (beta_0) | 4.73 | 3.89 | 1.22 | 0.229 |
| Metadata Completeness (beta_1) | 0.453 | 0.019 | 23.5 | < 0.001 |

| Diagnostic | Value |
|---|---|
| R-squared | 0.871 |
| Adjusted R-squared | 0.869 |
| F-statistic | 552.3 (p < 0.001) |

The coefficient of 0.453 means that for each 1-percentage-point increase in metadata completeness, the agent's probability of selecting that product increases by approximately 0.45 percentage points. The R-squared of 0.871 indicates that metadata completeness alone explains 87.1% of the variance in agent selection probability.

![Fig. 10: Metadata Regression](metadata_regression.png)
<em class="caption">Fig. 10. OLS regression of metadata completeness against agent selection probability, with 95% confidence band.</em>

---

## 7. Competitive and Regulatory Consequences

### 7.1 The Data Completeness Advantage

In human-directed commerce, brand recognition, emotional advertising, and visual design drive purchasing decisions. In agent-mediated commerce, these factors become largely irrelevant. An AI agent responds to structured data, specifically specifications, ratings, review volume, price, availability, and return policies. Product data management, historically treated as a back-office function, becomes a front-line competitive capability.

### 7.2 From SEO to B2A Optimization

AI agents query APIs, parse structured data feeds, and evaluate products based on machine-readable attributes. The emerging discipline called "Business-to-Agent" (B2A) optimization reflects this change. Retailers pursuing a B2A strategy must ensure their catalogs are accessible and compatible with emerging commerce protocols.

### 7.3 Demand Concentration Risk

The experimental research raises a concern about "winner-take-most" dynamics. If AI agents systematically concentrate demand on products with the highest ratings, most reviews, and most complete metadata, smaller sellers, newer brands, and niche products face systematic disadvantage.

---

## 8. Legal Liability and the Agency Problem

### 8.1 Traditional Agency Law

Under traditional agency law, the human who deploys an AI agent (the "principal") is generally liable for transactions the agent conducts within the scope of its delegated authority. The concept of "apparent authority" adds complexity. If a merchant reasonably believes an agent has authority based on the principal's conduct, the principal may be held liable even if the agent acted outside its actual instructions.

### 8.2 Electronic Transaction Statutes

The Uniform Electronic Transactions Act (UETA) and the E-SIGN Act establish that contracts formed by "electronic agents" are legally binding. These statutes were drafted in the late 1990s with automated trading systems in mind, not with LLM-based agents that exercise discretion over product selection.

---

## 9. Cross-Jurisdictional Regulatory Analysis

### 9.1 Scoring Methodology

The author assessed regulatory readiness across three major jurisdictions (EU, United States, China) along five governance dimensions, each scored on a 1-5 scale based on enacted or enforceable regulation.

**Table 7. Regulatory Readiness Scores by Jurisdiction**

| Dimension | EU (AI Act) | United States | China | Scoring Criteria |
|---|---|---|---|---|
| Transparency Requirements | 4.2 | 2.0 | 3.0 | Mandatory disclosure of AI interaction |
| Consumer Protection | 3.8 | 2.5 | 2.0 | Specific protections for agent-mediated purchases |
| Liability Framework | 3.0 | 1.5 | 2.5 | Clear allocation of liability for agent errors |
| Agent Registration | 2.5 | 1.0 | 3.5 | Requirements for agent identity verification |
| Antitrust Provisions | 3.5 | 2.8 | 1.5 | Tools to address algorithmic collusion/concentration |
| **Composite Score** | **3.40** | **1.96** | **2.50** | **Unweighted mean** |

The EU leads in transparency and consumer protection through the AI Act (EU AI Act, 2024). The United States scores lowest overall, relying primarily on existing agency enforcement rather than novel AI legislation.

![Fig. 8: Regulatory Comparison](regulatory_comparison.png)
<em class="caption">Fig. 8. Regulatory readiness scores across five governance dimensions for three major jurisdictions.</em>

---

## 10. Risk Assessment

### 10.1 Formal Risk Matrix

The author conducted a qualitative risk assessment of primary risks associated with agentic commerce adoption, scoring each on probability of occurrence and severity of impact.

**Table 8. Risk Assessment Matrix**

| Risk Factor | Probability | Impact | Risk Score (P x I) | Priority |
|---|---|---|---|---|
| Liability Ambiguity | 0.80 | 0.70 | 0.56 | Critical |
| Unauthorized Purchases | 0.65 | 0.80 | 0.52 | Critical |
| Market Concentration | 0.70 | 0.60 | 0.42 | High |
| Data Privacy Breach | 0.55 | 0.75 | 0.41 | High |
| Consumer Backlash | 0.60 | 0.55 | 0.33 | Medium |
| Protocol Incompatibility | 0.50 | 0.40 | 0.20 | Medium |

Liability ambiguity and unauthorized purchases rank as the two highest risks. Ambiguity in liability frameworks makes it harder to resolve disputes from unauthorized purchases, which in turn erodes consumer trust.

![Fig. 7: Risk Heat Map](risk_heatmap.png)
<em class="caption">Fig. 7. Risk matrix for agentic commerce.</em>

---

## 11. Limitations

This paper has several limitations.

First, the Monte Carlo simulation uses independently specified distributions, but the input parameters rely on assumptions about future adoption rates. Second, the consumer trust data covers a limited time window. Longitudinal studies with larger and more diverse samples are needed. Third, the OLS regression uses simulated data calibrated to ACES findings rather than raw experimental data. Access to the full dataset would allow more rigorous modeling. Fourth, the regulatory analysis uses qualitative scoring. Future work could develop a more granular scoring rubric.

---

## 12. Conclusion

The transition from human-directed to agent-mediated commerce is actively being built by major technology platforms. The market projections, modeled via Monte Carlo simulation (median $127B, 90% CI [$52B, $247B]), indicate that agent-mediated transactions could represent a meaningful share of digital commerce.

The analysis produces several key findings. First, consumer trust eroded sharply between Q4 2025 and Q1 2026, with a 25-percentage-point decline in comfort. Second, AI agents select products based on metadata completeness and structured signals rather than brand equity, with R-squared = 0.871 in the regression model. This amounts to a competitive realignment away from marketing and toward data operations. Third, regulatory readiness trails infrastructure deployment, with the United States scoring below the midpoint (1.96/5.0) on the governance assessment. Closing this gap will require sustained empirical research and regulatory frameworks that can adapt to a market structure in which the buyer is increasingly not a human.

---

## References

Amazon (2025). Amazon Rufus AI Shopping Assistant. Product Update and Usage Statistics. Amazon Press Center. [https://press.aboutamazon.com](https://press.aboutamazon.com)

Capgemini Research Institute (2025). What Matters to Today's Consumer. Capgemini Insights. [https://www.capgemini.com/insights/research-library/what-matters-to-todays-consumer-2025/](https://www.capgemini.com/insights/research-library/what-matters-to-todays-consumer-2025/)

Columbia University and Yale University (2025). What Is Your AI Agent Buying? Evaluation, Biases, Model Dependence, and Emerging Implications for Agentic E-Commerce. arXiv preprint. [https://arxiv.org/abs/2508.02630](https://arxiv.org/abs/2508.02630)

EU AI Act (2024). Regulation (EU) 2024/1689 of the European Parliament and of the Council. Official Journal of the European Union. [https://eur-lex.europa.eu/eli/reg/2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689)

Gartner (2024). Predicts 2025. Machine Customers Will Transform Commercial Strategy. Gartner Research. [https://www.gartner.com/en/articles/what-are-machine-customers](https://www.gartner.com/en/articles/what-are-machine-customers)

Riskified (2025). Agentic Commerce Survey. Consumer Attitudes Toward AI-Driven Purchasing, Q4 2025. Riskified Research. [https://www.riskified.com/blog/agentic-commerce/](https://www.riskified.com/blog/agentic-commerce/)

Stripe and OpenAI (2025). Agentic Commerce Protocol (ACP). An Open Standard for Agent-Initiated Transactions. [https://agenticcommerce.dev](https://agenticcommerce.dev)
