# The Agent Infrastructure Stack

//div class="author-info">
**Vedang Ratan Vatsa**//br>
*vedangvats@gmail.com*//br>
///div>

## Abstract

Between 2024 and 2026, the AI agent developer toolchain split into eight specialized infrastructure layers, capturing over $13 billion in combined funding. This paper maps these layers, evaluates their dependency dynamics, and identifies six emerging architectural trends. The analysis covers venture databases, SEC filings, and enterprise surveys for over 50 companies. Key findings reveal extreme capital concentration, with the top 10 deals capturing 85% of capital, and the direct acquisition of security and observability providers by major cloud platforms, while compute and perception layers maintain independent technical moats.

_**Keywords**_: AI agents, agent infrastructure, developer tools, compute inference, agent security, evaluation, orchestration, platform bundling, corporate acquisitions

---

## 1. Introduction

Two years ago, building an AI agent meant stitching together fifteen or more separate services by hand. A developer needed a model API, a headless browser, a web scraper, a workflow engine, a vector database, an evaluation harness, a secrets manager, and a sandbox for code execution. Each service required a separate account, billing page, and integration effort.

Agents do not follow predetermined paths. They make decisions at runtime, call external tools, execute code they wrote themselves, and maintain state across long-running sessions. Existing tools like Airflow, Docker, and OAuth covered parts of this, but none were designed for the specific combination agents require, including durable execution (workflow runs that survive crashes, failures, and restarts by persisting state to storage) of workflows where the next step depends on model output, sandboxed execution of code the model wrote at runtime, and identity management for software that acts on its own rather than on direct user input.

The scale of this mismatch is measurable. McKinsey's 2025 State of AI survey found that 23% of organizations had scaled at least one agentic AI system, usually in only one or two business functions [45]. Gartner's 2026 Hype Cycle for Agentic AI put the number at 17% deployed, with 60% or more expecting deployment within two years [46]. Deloitte's 2026 enterprise AI report found that only one in five companies has a mature governance model for autonomous agents [47]. This combination of high intent, low maturity, and minimal governance creates the demand that infrastructure companies fill.

By mid-2026, a developer can provision every one of these capabilities from a single marketplace page. Major cloud providers (AWS, Google Cloud, Azure) offer their own agent infrastructure bundles, but smaller developer platforms illustrate how fast the category formed. Vercel added a dedicated "Agents" category in 2025 with 14 agent-specific integrations [41]. Cloudflare runs 50+ AI models at the edge with built-in function calling [17]. Both are covered in detail in Section 7. The transition from manual integration to one-click provisioning took roughly two years and consumed at least $13 billion in disclosed venture capital across more than 50 companies.

This paper makes three contributions. First, it proposes an eight-layer taxonomy of agent infrastructure based on the functional requirements of autonomous AI systems. Second, it maps the dependencies and competition between these layers, identifying which are becoming commodities and which hold lasting advantages. Third, it identifies six architectural trends -- including edge inference, agent-specific identity systems, and sandboxed execution -- that are changing how developers build with these tools.

**Data and methodology.** The analysis covers 50+ companies that raised venture funding or were acquired for agent infrastructure functions between January 2024 and May 2026. January 2024 marks the approximate start of agent-specific venture activity, though several companies in this dataset (Temporal, Apify, Robust Intelligence) raised earlier rounds under different category labels. The dataset includes every company identified through Crunchbase, PitchBook, media reports, and marketplace listings as primarily serving agent infrastructure functions; the "50+" count reflects the companies for which disclosed funding data was available, not a sampling decision. Company-level funding, valuation, and ARR (annual recurring revenue) data come from venture funding databases (Crunchbase, PitchBook), SEC filings (Cerebras S-1), company blog posts, and media reports. ARR figures (Cognition, Together AI, Modal, Apify, Chatbase) are company-reported. Adoption metrics such as E2B's "88% Fortune 100" use company-defined criteria, which could range from a single team trial to organization-wide deployment. Enterprise adoption data come from three consulting surveys (McKinsey 2025, Gartner 2026, Deloitte 2026), each measuring slightly different constructs (scaling, deployment, governance maturity). The dataset covers disclosed funding only and is weighted toward US-headquartered companies. Summing disclosed funding by company headquarters shows approximately 82% of captured capital going to US-based companies, though this figure reflects the dataset's composition rather than global activity, since Chinese and other non-US companies are underrepresented in the sources used. The analysis focuses on venture-backed and publicly acquired companies. Open-source frameworks (LangChain, CrewAI, LlamaIndex) and internal corporate agent platforms (Google Vertex AI Agent Builder, Microsoft Azure AI Agent Service, Amazon Bedrock Agents) serve overlapping functions but operate under different business models and are discussed qualitatively rather than included in the funding dataset. The market map is representative rather than exhaustive. It does not cover companies that have not disclosed funding, that operate primarily outside English-language markets, or that launched after the May 2026 cutoff. All funding figures use the most recent available totals as of May 2026, including announced rounds.

## 2. Related Work

Academic research on agent infrastructure has grown alongside commercial activity, and several recent surveys inform the taxonomy that follows.

On orchestration, a survey formalizes the Model Context Protocol (MCP) for tool access and the Agent2Agent (A2A) protocol for peer coordination [48]. An empirical study of 42,000+ commits across LangChain, CrewAI, AutoGen, and similar frameworks found that orchestration complexity is a primary source of bugs and developer friction [49]. Research on multi-agent scaling laws evaluated 180+ configurations across five architectures and found that unstructured coordination amplifies errors at 17.2x compared to 4.4x for centralized systems [57].

On memory, surveys organize agent memory by where memory lives (in the prompt itself, in external databases, or baked into model weights) [50], graph-based backends [51], continuum architectures for long-horizon tasks [52], and comparisons to human memory across implicit, explicit, and agentic dimensions [53]. These papers identify four memory types (episodic, semantic, working, procedural) that no commercial product fully addresses, a gap that mirrors the funding slowdown documented in Section 5.5.

On security, a taxonomy of prompt injection attacks introduces the AgentPI benchmark and finds no current defense achieves high trustworthiness, high utility, and low latency at the same time [58]. A survey of 128 papers catalogs 51 attack methods and 60 defense methods [59]. A layered security framework proves that defenses at one layer have zero detection power against attacks at another [60]. A review of 88 studies extends the NIST adversarial ML taxonomy with new defense categories [61].

On evaluation, a survey on Agent-as-a-Judge examines how evaluation moved from fixed scoring rubrics to systems where an agent checks another agent's work by planning steps and calling tools [62]. A survey across five evaluation dimensions identifies gaps in cost-efficiency, safety, and robustness metrics [63]. The WildToolBench benchmark finds that no model achieved greater than 15% accuracy on multi-step tasks where the goal is implied rather than stated directly [64].

On tool use, a survey covering six dimensions (planning, training, safety, efficiency, capability, benchmarks) addresses the evolution from single-tool invocation to long-horizon multi-tool orchestration [65]. On software engineering agents, a review of the development lifecycle catalogs how agents handle coding, testing, debugging, and deployment [54].

Three patterns emerge from this literature. First, the functional decomposition in commercial taxonomies (perception, orchestration, memory, evaluation, security) maps closely to the architectural decomposition that researchers use when studying agent systems. Second, the hardest unsolved research problems (memory, evaluation, safety) correspond to the commercial layers with the least certain funding. Third, the finding that attacks span every stack layer validates the commercial pattern of security companies being acquired by platform incumbents that can integrate defense across their full product surface.

## 3. The Eight-Layer Taxonomy

The taxonomy groups companies into eight layers based on three separation criteria. First, independent scaling. Each layer can grow its user base, revenue, and infrastructure without requiring proportional growth in another layer. A perception company can serve more customers without needing more orchestration capacity, and vice versa. Second, different buyer. Each layer sells to a recognizably different decision-maker or budget. Compute sells to platform engineers managing GPU spend. Security sells to CISOs and compliance teams. Agent products sell to end users and business unit leaders. When two functions consistently sell to the same buyer through the same purchase decision, they belong in the same layer. Third, independent pricing. Each layer can charge independently. A developer can switch perception providers without changing orchestration providers, and can evaluate compute vendors without touching memory infrastructure. These three tests produce eight layers rather than six or ten. Merging orchestration and compute would violate the different-buyer test (infrastructure engineers vs. GPU procurement teams). Splitting security into "prompt defense" and "identity management" would violate the independent-pricing test, since Descope and Corridor sell to the same security buyer through the same deal. The boundaries are not absolute. Section 4.5 discusses companies that span multiple layers, and Section 7.3 identifies layers that may collapse into platform bundles as the market matures.

This taxonomy overlaps with other industry mappings. MightyBot's 2026 market map uses seven categories (coding agents, browser agents, workflow automation, vertical AI agents, agent infrastructure, customer/employee agents, and regulated workflow agents) that cut across functional boundaries differently [55]. The taxonomy in this paper groups by infrastructure function rather than by use case, which better shows the competition and dependency relationships between layers. Alternative taxonomies are equally valid for different analytical purposes.

Table 1 summarizes the eight functional layers of the agent infrastructure stack. Figure 1 presents this taxonomy as a visual market map, showing each layer with its constituent companies, disclosed funding, and dependency relationships.

**Table 1. The Eight-Layer Agent Infrastructure Taxonomy**

| Layer | Function | Funding | Key Companies |
|-------|----------|---------|---------------|
| Perception | Web data extraction | ~$317M+ | Browserbase, Firecrawl, Parallel, Apify, Kernel |
| Orchestration | Durable execution, tool integration | ~$709M | Temporal, Inngest, Composio |
| Eval & Observability | Accuracy measurement, logging | ~$256M+ | Braintrust, Arize AI, Galileo AI, Langfuse, Helicone |
| Compute & Inference | GPU infrastructure, model hosting | ~$5.3B+ | Cerebras, Together AI, Modal, Fireworks AI, Groq, fal.ai |
| Memory & Retrieval | Persistent context, vector search | ~$349M | Mem0, Upstash, Pinecone, Qdrant, Weaviate, Chroma |
| Sandboxed Execution | Isolated code execution | ~$32M | E2B |
| Security | Prompt defense, agent identity | ~$312M+ | Lakera, Robust Intelligence, Patronus AI, Corridor, Arcjet, Descope |
| Agents as Products | Vertical autonomous agents | ~$6.1B+ | Cognition, Sierra, Harvey, Decagon, Factory, CodeRabbit |

**Perception** converts the visual, interactive web into structured data that language models can process. Browserbase ($67.5M raised) provides interactive browser sessions, serving over 50 million sessions in 2025 [1]. Firecrawl ($16.2M) extracts web content without running a full browser and serves over 500,000 developers [2]. Parallel, which former Twitter CEO Parag Agrawal founded, raised $230M at a $2B valuation for structured web data extraction [3]. Apify, the oldest player, generated $13.3M ARR in 2024 on only $3M in external funding by running 30,000+ pre-built web scrapers [42].

**Orchestration** turns language model outputs into reliable, repeatable workflows that keep running through crashes and restarts. The multi-agent scaling law findings discussed in Section 2 (error amplification of 17.2x for unstructured coordination [57]) validate the commercial investment in structured orchestration. Temporal ($650M raised, $5B valuation) runs the most widely adopted durable execution platform; OpenAI uses Temporal to run Codex [5, 66]. Inngest (~$34M total raised, Series A led by Altimeter, with a16z participating) provides serverless-first orchestration with its AgentKit product for multi-agent coordination [6]. Composio ($29M) gives agents access to over 1,000 integrations and thousands of individual tool actions through a single integration layer, and over 100,000 developers have adopted it [7]. Open-source orchestration frameworks also occupy significant market share in this layer. LangChain (over 100,000 GitHub stars) provides the most widely used open-source agent framework, with LangGraph adding stateful, multi-actor orchestration on top. CrewAI (over 50,000 GitHub stars) focuses on multi-agent role-based collaboration. LlamaIndex specializes in data-aware agent orchestration with retrieval-augmented generation. These open-source tools serve a different market segment than the venture-backed companies listed above. They dominate prototyping and early-stage development, while Temporal and Inngest target production workloads that require durability guarantees, automatic retries, and enterprise support contracts. The two segments compete at the boundary, and some production teams migrate from LangChain to Temporal as their agent workloads mature.

**Evaluation and Observability** measures whether agents produce correct outputs before those outputs reach production. No existing benchmark achieves greater than 15% accuracy on compositional, real-world tool-use tasks [64], which explains why this layer exists commercially. Braintrust ($120M+, $800M valuation) provides evaluation, logging, and prompt management for Stripe, Notion, and Airtable [8]. Arize AI ($131M) covers both traditional ML monitoring and LLM-specific evaluation for Booking.com, Uber, and Duolingo [10]. Galileo AI, which Cisco acquired in April 2026 to strengthen its Splunk Observability Cloud, spans this layer and the security layer, providing both output evaluation and guardrail enforcement [26]. Langfuse reached 19 of the Fortune 50 on $4M before ClickHouse acquired it in January 2026 [9]. Mintlify acquired Helicone in March 2026 [56].

**Compute and Inference** provides the GPU infrastructure behind agent workloads. This layer contains the largest value pool in the stack. Cerebras went public on NASDAQ in May 2026, becoming the first pure-play AI chip company to reach a public market [11]. Together AI raised $1.5B (including its most recently announced round) at $8.5B valuation and reports approximately $1B ARR [12]. Modal ($466M raised, $4.65B valuation, ~$300M ARR) grew revenue 5x in eight months [13]. Fireworks AI ($327M+) processes 15 trillion tokens per day per company disclosures [14]. Groq (over $2B in disclosed funding including announced rounds) designed custom LPU (Language Processing Unit) chips optimized for inference throughput; Nvidia reportedly licensed the architecture in a deal valued at approximately $20B per media estimates [15]. fal.ai ($587M+, $4.5B+ valuation) provides serverless media generation for Adobe, Canva, and Shopify [16].

**Memory and Retrieval** provides persistent context so agents remember what they have done and what users prefer. Mem0 ($24M) became the exclusive memory provider in the AWS Agent SDK [22, 44]. Pinecone ($138M) serves 9,000+ customers across 800,000 developers [18]. Qdrant ($87.8M) is the only vector database to raise a new round after 2023 [19].

**Sandboxed Execution** gives agents a safe place to run code they write themselves. E2B ($32M) provides ephemeral micro-VMs (lightweight virtual machines that spin up in milliseconds and self-destruct after execution) for AI-generated code execution, integrated by Hugging Face, Perplexity, and Groq [24]. The company reports 88% Fortune 100 adoption, though the criteria for what counts as "adoption" have not been publicly defined and could range from a single developer trial to enterprise-wide deployment.

**Security** protects agents from prompt injection, validates model outputs, and manages agent identity. The attack surface spans all eight layers of the stack (Section 2), which helps explain the commercial pattern in this layer. Of the earliest security-focused startups, acquirers bought two within twelve months. Cisco acquired Robust Intelligence in September 2024 [25, 29] and Check Point acquired Lakera in September 2025 [27, 28], leaving Patronus AI ($40M) [31] as the sole independent survivor from that cohort (detailed in Section 6). Galileo AI, sometimes categorized as a security company for its guardrail capabilities, also sold to Cisco, though its primary function is evaluation and observability (see above). No standalone security product has yet covered the full attack surface, which helps explain why platform incumbents absorb these companies rather than competing with them. Newer entrants include Corridor ($30.4M) [32], Arcjet ($12.1M) [33], and Descope ($88M) [34].

**Agents as Products** sits at the top of the stack, representing companies that ship agents as finished products to end users. Cognition ($2.5B+ raised, $26B valuation, $492M ARR) builds Devin for software engineering [35]. Sierra ($1.585B, $15.8B valuation) targets customer experience [36]. Harvey ($1.22B+, $11B valuation) serves legal [37]. Decagon ($481M, $4.5B valuation) handles customer support [38]. Factory ($220M, $1.5B valuation) focuses on software development [39]. CodeRabbit ($88M, $550M valuation) automates code review [40]. These six companies represent over $59B in combined last-round valuations, though private valuations from different rounds at different dates are not directly comparable and should be read as a rough indicator of investor sentiment rather than a precise aggregate.

A related market risk is what MightyBot calls "agent washing," the practice of vendors renaming chatbots, copilots, or RPA bots as "AI agents" without adding meaningful autonomy, tool use, memory, or governance [55]. The production readiness criteria that separate genuine agent systems from relabeled chatbots include defined workflow boundaries, tool access with controls, memory and state management, evaluation and observability, human checkpoints, audit trails, and cost discipline [55].

## 4. Market Map Analysis

### 4.1 The Dependency Graph

The eight layers form a dependency chain that determines which layers hold lasting advantages and which are becoming interchangeable.

Compute sits at the bottom of the stack. Nearly every other layer depends on it. An orchestration engine calls a model. An evaluation harness runs inference to score outputs. A perception tool uses a model to interpret web content. Even security tools run inference to detect prompt injection. Compute depends on little besides hardware supply, which helps explain why it attracts the most capital and produces the largest outcomes.

Perception feeds into orchestration. An agent that browses the web needs perception (Browserbase, Firecrawl) to extract data, then orchestration (Temporal, Inngest) to sequence actions on that data. Memory stores the results for future sessions. Evaluation sits across all layers, measuring output quality regardless of whether the output came from a coding agent, a customer support agent, or a web scraping pipeline.

Security also cuts across layers rather than sitting in a single position. Prompt injection defense applies at the perception layer (malicious web content), the orchestration layer (tool-use exploits), and the agent-product layer (user-facing attacks).

Sandboxed execution has a unique position. It serves a narrow function (running untrusted code safely) but is required by most AI coding agents. E2B's adoption figures (Section 3) suggest the function may be too narrow to support multiple competitors but too critical to skip. However, this position also carries vulnerability. If major cloud providers (AWS, Google Cloud, Azure) add sandboxed code execution as a built-in feature of their platforms, E2B's standalone position could erode.

### 4.2 What the Numbers Reveal

**Capital concentration is extreme.** The top 3 deals (Cognition, Groq, Sierra) account for roughly 46% of total disclosed capital. The top 10 account for over 85%. The bottom half of companies in this dataset split less than 10% of total funding, so the typical agent infrastructure startup operates on far less funding than the headline numbers suggest. This concentration is common in venture capital distributions, where a few very large deals dominate any sector's aggregate figures. Whether agent infrastructure is more concentrated than other sectors (cloud, SaaS, fintech) at a comparable stage requires further analysis.

**The difference between the mean and median confirms this.** The mean funding per company across the dataset exceeds $250M, driven by massive rounds at Cognition ($2.5B+) [35], Groq (over $2B) [15], and Together AI ($1.5B) [12]. The median sits far lower, closer to $40-50M.

**Revenue multiples vary dramatically by layer.** Where ARR data is available, the valuation-to-revenue ratios reveal investor expectations about growth potential per layer.

**Table 2. Revenue Multiples by Layer (Where ARR Data Available)**

| Company | Layer | ARR | Valuation | Revenue Multiple |
|---------|-------|-----|-----------|-----------------|
| Cognition | Agents as Products | $492M | $26B | ~53x |
| Together AI | Compute | ~$1B | $8.5B | ~8.5x |
| Modal | Compute | ~$300M | $4.65B | ~15.5x |
| Apify | Perception | $13.3M | N/A (bootstrapped) | N/A |
| Chatbase | Agents as Products | $10M | N/A (bootstrapped) | N/A |

Cognition's 53x revenue multiple is the standout. Investors are pricing agent-as-product companies as if they can capture a large share of the software engineering labor market, not just grow recurring software revenue. Compute companies trade at 8-16x, reflecting a more infrastructure-like pricing model with lower expected margins but higher predictability.

**Capital efficiency splits cleanly by layer.** Apify generated $13.3M ARR in 2024 on only $3M in external funding, a return of $4.43 per dollar raised [42]. Chatbase generates $10M ARR on zero external funding [43]. At the other end, Cognition generates $492M ARR on $2.5B+ raised, or roughly $0.20 per dollar raised so far [35]. The capital-efficient companies cluster in layers (perception, developer tools) that serve individual developers with credit-card pricing. The capital-intensive companies operate in layers (compute, agent products) that require enterprise sales teams, GPU procurement, or both. Cognition's ARR may justify its capital many times over as revenue scales, but the data shows that some layers can produce profitable businesses on minimal funding while others have not done so.

### 4.3 Commoditization Versus Differentiation

Not all layers carry equal competitive moats. The analysis identifies a clear split between layers where companies can build durable advantages and layers where the product appears to be becoming interchangeable.

**Layers becoming commodities.** Vector databases are a prominent example. Pinecone [18], Weaviate [20], and Chroma [21] have not announced new funding rounds since 2023. Qdrant is the sole exception [19]. PostgreSQL with pgvector and Redis with vector modules now offer "good enough" vector search as a feature of general-purpose databases, weakening the case for standalone vector database companies. The funding pause may also reflect investor rotation after 2023's vector database hype, rather than purely technical commoditization. Observability follows a similar pattern. ClickHouse acquired Langfuse and Mintlify acquired Helicone, suggesting that LLM observability is becoming a feature of adjacent platforms rather than an independent category. Section 6.3 examines these acquisitions in detail.

**Layers with lasting advantages.** Compute remains hard to turn into a commodity because it tends to require custom hardware (Cerebras wafer-scale chips, Groq LPU architecture) or massive GPU procurement (Together AI, Modal). Perception is similarly defensible because browser infrastructure and web scraping at scale require deep technical investment, though this claim would benefit from systematic comparison across layers. Orchestration sits in the middle. Temporal's durable execution model has strong adoption (OpenAI uses it for Codex [66]), but foundation model providers are adding native orchestration features that could weaken standalone orchestration tools over time. The defensibility analysis here is partly circular, since the taxonomy criteria (independent scaling, different buyer) overlap with the factors that create lasting advantages. Layers designed to have different buyers may, by definition, appear hard to displace on that axis.

### 4.4 The Thin Wrapper Problem

The most vulnerable companies in the stack tend to be those offering a thin layer of software over a foundation model API with no proprietary data, workflow, or infrastructure advantage.

A common failure mode is straightforward. OpenAI, Anthropic, and Google are shipping native features (function calling, tool use, code execution, built-in web browsing) that may eliminate the value proposition of companies whose sole product is wrapping these capabilities in a slightly different interface. Each time a model provider adds a new built-in capability, a category of wrapper startups risks losing its reason to exist. Major platform moves in May 2026 alone included Microsoft Agent 365 reaching general availability and ServiceNow expanding its Autonomous Workforce across IT, HR, finance, and legal [55].

The companies that survive typically own a part of the workflow that the model provider is unlikely to replicate. Browserbase owns the browser session. E2B owns the sandbox. Temporal owns the execution state. Braintrust owns the evaluation data. Mem0 owns the memory layer. None of these are easily replaced by adding a feature to a foundation model, though cloud providers (as distinct from model providers) could potentially replicate several of these functions.

### 4.5 Companies Spanning Multiple Layers

Several companies span multiple layers, positioning themselves at the intersection of two or more functional categories.

Composio spans orchestration and tools, providing both the integration layer (over 1,000 integrations and thousands of individual tool actions) and the workflow logic to sequence tool calls. Descope spans security and authentication, offering both traditional auth infrastructure and an Agentic Identity Hub with OAuth 2.1 for AI agents, used by Databricks, MongoDB, and GoodRx [34]. Braintrust spans evaluation and observability, combining accuracy measurement with logging, tracing, and prompt management.

These multi-layer companies test the taxonomy's boundaries. They also tend to be better positioned competitively because customers who rely on them for two functions face higher friction when considering alternatives. A customer using Braintrust for both evaluation and observability finds it harder to switch than a customer using separate tools for each function.

### 4.6 Funding Concentration

The distribution of capital across the stack is extremely uneven, both across layers and within them.

**Table 3. Capital Concentration in Agentic AI Funding (Early 2026)**

| Metric | Value |
|--------|-------|
| Top 3 deals' share of total capital | ~46% |
| Top 10 deals' share of total capital | ~87% |
| Bottom 50% of deals' share of total capital | ~10% |
| Median AI seed round (2026) | $4.6M |
| Total agentic AI funding, 2024 | $1.5B |
| Total agentic AI funding, 2025 | $2.9B |
| Total agentic AI funding, annualized 2026 | ~$2.6B |

Median AI seed round data is from PitchBook/NVCA [68]. Section 8 breaks down the investor thesis behind this concentration in detail.

## 5. Architectural Trends in Developer AI Systems

Six architectural trends are changing how developers build and deploy agents.

### 5.1 From APIs to Protocols

The connections between infrastructure layers are settling into formal protocols and standards.

Anthropic's Model Context Protocol (MCP) defines a standard way for agents to connect to external tools, data sources, and services. Before MCP, every tool integration required custom code. MCP provides a common interface that any tool provider can implement and any agent framework can consume. The protocol turns tool integration from an N-by-M problem (N agents times M tools) into an N-plus-M problem (each side implements once). Academic work formalizing MCP and the related Agent2Agent (A2A) protocol for peer coordination confirms that these standards are receiving attention beyond their commercial implementations [48].

OpenAI's function calling specification defines a structured format for models to request tool execution. Rather than generating freeform text that a parser must interpret, the model outputs a structured JSON object specifying which function to call and with what arguments. This format has become the common standard that other model providers (including those hosted on Cloudflare Workers AI) support through OpenAI-compatible endpoints.

Stripe's Agentic Commerce Protocol addresses a different interface, the boundary between agents and payment systems. When an agent completes a purchase on behalf of a user, the transaction needs structured authorization, fraud checks, and audit trails. No one designed traditional checkout flows to handle autonomous purchasing by software rather than people.

These three protocols share a pattern. Standards are forming at the interfaces between layers, not within layers. The internal implementation of a compute provider or an orchestration engine remains proprietary. But the connection points between them are converging on shared specifications. Academic research traces the evolution from isolated single-tool invocation to long-horizon multi-tool orchestration across six dimensions, confirming that the transition from custom integration to standardized protocols appears to be a structural trend rather than a temporary convenience [65]. This pattern resembles the path that HTTP, REST, and SQL followed in earlier infrastructure cycles, and it suggests the stack is maturing beyond its earliest experimental phase.

**Table 8. Comparison of Emerging Agentic Protocols**

| Protocol | Creator | Primary Scope | Standardization Status | Architectural Layer |
|----------|---------|---------------|------------------------|---------------------|
| Model Context Protocol (MCP) | Anthropic | Standardized data and tool access | Open-source standard (2025) | Perception & Orchestration |
| Function Calling Spec | OpenAI | API execution and routing schemas | De-facto industry standard (2023) | Compute & Inference |
| Agentic Commerce Protocol | Stripe | Autonomous transaction authorization | Early-stage private design (2026) | Agents as Products |


### 5.2 Edge Inference

Inference is moving from centralized GPU clusters to distributed edge locations, and the effects on agent workloads are large.

Cloudflare Workers AI now runs 50+ models at 300+ network points of presence globally, with GPU-accelerated inference available at a growing subset of those locations. The platform offers OpenAI-compatible endpoints, function calling, LoRA fine-tuning, vision inputs, and batch processing built in [17]. The models come from Meta, Google, OpenAI, Qwen, Mistral, and NVIDIA. A CDN company running inference at the edge alters how compute reaches applications.

Fireworks AI processes 15 trillion tokens per day, operating at a scale that requires distributed infrastructure by necessity [14]. The company serves Samsung, Uber, and Cursor.

For agent workloads, edge inference matters because agents often need to respond within latency budgets that centralized GPU clusters struggle to meet. A customer support agent handling a live conversation operates under tight latency constraints, and a coding agent providing inline suggestions needs sub-100ms responses. Edge inference brings the compute closer to the application, reducing latency for the many small, fast inference calls that characterize agent workloads (as opposed to the large batch jobs that characterize training workloads).

This trend also changes how compute companies compete with each other. If inference becomes available at every CDN edge node, the advantage for standalone compute providers changes from "having GPUs" to "having faster, cheaper, or more specialized GPUs." Cloudflare offers adequate inference at lower latency for a large class of agent tasks, even if it cannot match the raw throughput of Cerebras or Together AI.

### 5.3 Serverless-First Infrastructure

The agent workload has a distinctive shape. It is bursty (an agent may sit idle for hours, then fire 50 tool calls in 30 seconds), stateless between calls (each inference request is independent), and needs fast cold starts (a user waiting for an agent response is unlikely to tolerate a 10-second container spin-up).

This workload maps naturally to serverless and ephemeral infrastructure patterns, and multiple companies in the stack have built around this insight.

Modal ($466M raised, $300M ARR) provides serverless GPU access, letting developers run inference jobs without provisioning or managing machines [13]. fal.ai ($587M+) takes the same approach for media generation [16]. Inngest (~$34M) provides serverless-first orchestration with zero infrastructure to manage [6]. E2B ($32M) runs each code sandbox as an ephemeral micro-VM that spins up on demand and disappears when done [24]. Upstash ($11.9M) provides serverless Redis, Kafka, and vector storage designed for the stop-and-start usage patterns of agent workloads [23].

Training workloads look very different. Training requires sustained, predictable GPU access for hours or days. Inference requires fast, sporadic access for milliseconds at a time. The infrastructure patterns that serve training (reserved GPU clusters, long-running containers) are poorly suited to inference, and the serverless model emerged in response to this mismatch.

### 5.4 Agent-Native Identity and Auth

Agents acting autonomously on behalf of users create an identity problem. No one designed traditional authentication systems to handle autonomous software actors. When a human logs into a service, the auth flow assumes a person sitting at a browser. When an agent logs into that same service, there is no person, no browser, and potentially no human in the loop at all.

Descope ($88M raised) built an Agentic Identity Hub that provides OAuth 2.1 for AI agents, allowing agents to authenticate to third-party services with scoped permissions, audit trails, and revocable access [34]. Databricks, MongoDB, and GoodRx use this system. The product is a new building block that separates agent identity from human auth.

The need for agent-specific identity is growing as agents perform more consequential actions. An agent that books flights, signs contracts, or moves money needs verifiable identity credentials that the receiving service can validate, scope, and revoke. Traditional API keys are insufficient because they lack fine-grained permissions and audit trails that autonomous agents require. The OAuth 2.1 standard provides a framework, but the tooling to make it work for non-human actors is still early.

As noted in Section 1, only one in five companies has a mature governance model for autonomous agents [47]. Agent identity appears to be a prerequisite for that governance. Without verifiable, scoped, revocable credentials for agents, governance models remain theoretical.

### 5.5 The Memory Problem

Memory appears to be among the least mature layers in the agent infrastructure stack, and both the funding data and the academic literature support this assessment.

Mem0 ($24M) became the exclusive memory provider in the AWS Agent SDK, giving it a privileged distribution position [22, 44]. But the broader memory and retrieval category shows signs of stalling. Pinecone ($138M), Weaviate ($67.7M), and Chroma ($20M) have not announced new funding rounds since 2023 [18, 20, 21]. Qdrant ($87.8M) is the only vector database to raise post-2023 [19].

The funding pause may reflect several factors. Investor rotation toward compute and agent products (which together absorb the vast majority of total capital, as detailed in Section 4.6) reduces the pool available for middle-layer categories. Broader macro conditions and valuation resets in 2023-2024 also slowed follow-on rounds across enterprise SaaS generally. But a category-specific factor also appears relevant. No commercial product has yet converged on a clear abstraction for agent memory. Vector databases solve one specific sub-problem (similarity search over embeddings), but agent memory involves at least four distinct functions. Academic surveys identify these as episodic memory (what happened in past sessions), semantic memory (what facts the agent knows), working memory (what the agent holds in active context during a task), and procedural memory (what workflows the agent has learned) [50, 53]. No single commercial product addresses all four well yet. Research on continuum memory architectures defines the requirements for persistent, temporally chained memory in long-horizon agent tasks [52], and work on graph-based memory architectures evaluates structured knowledge graphs as alternative memory backends [51]. The difference between what academic research describes as needed and what commercial products actually offer appears wider in the memory layer than in any other part of the stack. Separating how much of the funding pause stems from broader market changes versus category-specific uncertainty is difficult with the available data, but the academic literature suggests the abstraction problem is real regardless of capital market conditions.

General-purpose databases are also moving into this space. PostgreSQL with pgvector and Redis with vector modules offer "good enough" vector search as a built-in feature, reducing the case for a standalone vector database. Upstash ($11.9M, backed by a16z) approaches memory from the serverless data store angle rather than the vector-specific angle, integrating Redis, Kafka, and vector search into a single serverless product [23].

**Table 9. Memory Storage Architectures for Autonomous Agents**

| Architecture | Primary Technology | Core Focus | Moat & Defensibility | Funding Trend |
|--------------|--------------------|------------|-----------------------|---------------|
| Dedicated Vector Databases | Pinecone, Chroma, Qdrant | High-performance similarity search | Database feature absorption risk | Stalled since 2023 |
| Multi-Model RDBMS | PostgreSQL (pgvector), Redis | Structured context & metadata | High integration, standard tools | Platform-funded |
| Serverless Key-Value | Upstash (Serverless Redis) | Low-latency state & rate limits | Edge-native, dev-accessible | Active developer growth |


### 5.6 Sandboxed Execution as a Development Primitive

Sandboxed execution emerged as a distinct infrastructure pattern as AI coding agents moved from prototypes to production. E2B ($32M) turned code execution into an API call [24]. A developer sends code to E2B's API, and E2B runs it in an isolated micro-VM with its own filesystem, network, and process tree, then returns the output. The sandbox spins up in milliseconds and disappears when done. Most AI coding agents require this capability. Cognition's Devin, Cursor, and other tools that generate and run code need a safe execution environment. Running untrusted, LLM-generated code on production servers creates obvious security risks. Academic research on LLM-based agentic systems for software engineering confirms that sandboxed execution is a core requirement, not an optional feature [54].



## 6. Acquisition and Integration Dynamics

### 6.1 The Acquirer Profile

Eight acquisitions occurred in the agent infrastructure space between September 2024 and May 2026. The acquirers share a consistent profile. They are large infrastructure incumbents that missed the initial agent wave and bought their way in.

**Table 4. Agent Infrastructure Acquisitions (Sep 2024 - May 2026)**

| Acquirer | Target | Date | Estimated Value | Layer |
|----------|--------|------|----------------|-------|
| Cisco | Robust Intelligence | Sep 2024 | Undisclosed | Security |
| Check Point | Lakera | Sep 2025 | ~$300M | Security |
| Cisco | Galileo AI | Apr 2026 | Undisclosed | Eval & Observability / Security |
| ClickHouse | Langfuse | Jan 2026 | Undisclosed | Evaluation & Observability |
| Mintlify | Helicone | Mar 2026 | Undisclosed | Evaluation & Observability |
| IBM | Confluent | Mar 2026 | $11B | Data Infrastructure (adjacent) |
| IBM | HashiCorp | Feb 2025 | $6.4B | Infra Provisioning (adjacent) |
| Meta | Manus | Dec 2025 (later blocked by China) | ~$2B | Agent Platform [67] |

Cisco alone bought two agent infrastructure companies within eighteen months [25, 26]. IBM bought two adjacent infrastructure companies (Confluent for data streaming, HashiCorp for infrastructure provisioning) at a combined $17.4B. These IBM deals are not agent-specific but signal how incumbents are assembling the broader platform capabilities that agent infrastructure runs on. Meta agreed to pay approximately $2B for Manus, an autonomous agent platform, in December 2025 [67], but China's NDRC blocked the transaction in April 2026, ordering the deal unwound. The blocked deal illustrates the geopolitical risks in cross-border AI infrastructure acquisitions. None of these acquirers built comparable agent capabilities in-house. Each chose to buy or attempt to buy.

**Time-to-acquisition varies.** Founders started Robust Intelligence in 2019, and Cisco acquired it in September 2024, roughly five years from founding to exit [25, 29]. Founders started Lakera in 2021, and Check Point acquired it in September 2025, roughly four years to exit [27, 28]. These two data points show a range of four to five years from founding to acquisition, though with only two observations, drawing trend conclusions about compression would be premature. What the data does show is that incumbents are willing to buy agent security companies relatively early in their lifecycle, possibly because the pace of model provider feature releases makes waiting risky. A security startup that waits three more years for growth may find that OpenAI or Anthropic has shipped a competing feature for free.

### 6.2 What Gets Acquired Versus What Stays Independent

A pattern shows which layers produce acquirable companies and which produce independent ones.

**Acquirable layers include security and observability.** Security companies (Robust Intelligence [29], Lakera [28]) and observability companies (Langfuse, Helicone, Galileo AI [30]) share traits that make them acquisition targets. Their products fit easily into an acquirer's existing platform, and their standalone revenue potential may not justify the cost of building a full go-to-market operation from scratch.

**Independent layers include compute and perception.** No one has yet acquired the compute companies (Cerebras, Together AI, Modal, Groq) or the perception companies (Browserbase, Parallel), likely because their technical assets are harder to replicate through acquisition. A wafer-scale chip fabrication capability (Cerebras) [11] or a high-throughput inference platform (Together AI at ~$1B ARR) [12] does not fold easily into an existing product line. These companies generate enough standalone revenue to justify independence.

Orchestration sits in an ambiguous position. Temporal ($5B valuation) [5] is large enough to remain independent, but if its growth slows, it could become an acquisition target for a cloud provider looking to add durable execution as a platform feature.

### 6.3 Observability Collapsing Into Databases

The Langfuse and Helicone acquisitions reveal a specific integration pattern [9, 56]. ClickHouse, a database company, acquired Langfuse. Mintlify, a developer documentation platform, acquired Helicone. In both cases, an adjacent product category absorbed an LLM observability tool.

This pattern suggests that LLM observability is not a standalone category. It is a feature set that database companies, documentation platforms, and developer tools can add to their existing products. The data generated by LLM observability (traces, logs, latency measurements, cost tracking) is database content. Storing and querying that data is a core competency of database companies, not a new category requiring new companies.

Braintrust ($120M+, $800M valuation) and Arize AI ($131M) are the remaining independent players in this layer [8, 10]. Their survival may depend on expanding beyond pure observability into evaluation, experimentation, and workflow management, functions that are harder for a database company to replicate.

### 6.4 The Bootstrapped Counterexample

Not every layer requires venture capital. Several companies built profitable businesses with minimal external funding, extending the capital efficiency pattern described in Section 4.2.

Chatbase reached $10M ARR while fully bootstrapped with 18 employees [43]. Apify generated $13.3M ARR on only $3M in external funding [42]. These outcomes contrast sharply with the capital-intensive path that dominates compute and agent-product layers, where companies required billions in funding before reaching scale.

The capital-efficient companies cluster in layers that sell directly to individual developers and small teams. The bootstrapped path works for perception tools (Apify), developer experience products (Chatbase), and monitoring tools with self-serve pricing. It is harder to replicate in compute (too capital-intensive), security (requires enterprise sales), or orchestration (infrastructure complexity demands sustained investment).

## 7. Platform Convergence

### 7.1 The Vercel Marketplace as Case Study

The Vercel Marketplace contains 100+ integrations across 22 categories, with a dedicated "Agents" category added in 2025 [41]. The Agents category alone includes 14 companies spanning perception (Browserbase, Firecrawl, Kernel, Parallel), evaluation (Braintrust, Autonoma AI, Kubiks), code review (CodeRabbit, Cubic, Sourcery), security (Corridor), search (Mixedbread), and customer support agents (Chatbase, AssistLoop). Each can be provisioned with one click, billed through a single invoice, and connected to a Vercel project with automatic API key injection.

This is the AWS model applied to agent infrastructure. AWS did not build most of its services from scratch. It acquired companies, built some services in-house, and integrated third-party tools into a unified billing and provisioning surface. Over roughly a decade, AWS absorbed databases, compute, storage, monitoring, and security into a single bill. Vercel is attempting the same pattern for agent infrastructure in roughly two years.

This happened quickly because agent infrastructure companies are smaller, younger, and more modular than the services AWS bundled. A Browserbase integration takes days to add to a marketplace, not months. The companies themselves benefit from marketplace distribution (Vercel's developer audience) in exchange for platform lock-in (billing through Vercel, authentication through Vercel, customer relationship partially owned by Vercel).

The marketplace model also raises a question about the taxonomy in this paper. If a developer provisions perception, orchestration, evaluation, and security from a single marketplace page with unified billing, the eight layers still exist technically but may stop mattering commercially. The buyer no longer makes eight separate purchasing decisions. The layers collapse into one decision ("which platform?"), and the competitive moats move from layer-specific advantages to platform-level advantages like distribution, developer experience, and billing integration. This is the same dynamic that turned individual AWS services from independent purchase decisions into line items on a single invoice.

### 7.2 Cloudflare Workers AI

Cloudflare's entry into the compute layer represents a different kind of platform convergence. Cloudflare started as a CDN and DDoS protection service. It added serverless compute (Workers), key-value storage (KV), object storage (R2), and databases (D1). Workers AI, which runs 50+ models across Cloudflare's global network of 300+ points of presence, extends this pattern into inference [17].

The competitive position is distinct from pure-play compute providers. Cloudflare lacks the raw throughput or model selection of Together AI or Fireworks AI. But Cloudflare can offer inference at every edge location where it already serves web traffic, with zero additional infrastructure for the developer to manage. For the large class of agent tasks that require adequate (not state-of-the-art) inference with low latency, Cloudflare's position is strong.

The function calling support built into Cloudflare Workers AI is particularly relevant. An agent running on Cloudflare can call a model, receive a structured function call response, execute the function on a Cloudflare Worker, and return the result, all within the same edge location. This tight integration between compute, inference, and execution is difficult for standalone compute providers to replicate.

This creates a segmentation problem for standalone compute companies. The high end of inference (frontier models, massive context windows, specialized hardware) remains defensible. But the middle of the market, where most production agent workloads actually run, may migrate toward integrated platforms that bundle "good enough" inference with storage, networking, and execution. If that happens, the compute layer does not disappear, but it splits into two distinct markets with different economics. Standalone compute companies would need to compete on performance at the top and lose the volume middle to platform bundlers.

### 7.3 Platform Absorption and Layer Vulnerability

This pattern goes beyond developer-focused platforms. In May 2026 alone, two major platform companies made agent infrastructure moves. Microsoft launched Agent 365 as a general-availability centralized governance layer for agents. ServiceNow expanded its Autonomous Workforce product across IT, HR, finance, and legal functions [55]. Each of these moves folds agent infrastructure capabilities (orchestration, identity, evaluation) into an existing platform, shrinking the potential market for standalone tools.

The timing matters as much as the moves themselves. The thin wrapper problem described in Section 4.4 operates on a specific clock. Each quarter that a platform company ships a new built-in capability, a cohort of standalone tools loses a piece of its addressable market. The standalone companies that raised venture capital in 2024 typically have 18-30 months of runway. If platform bundling accelerates through 2026 and 2027, some of those companies will reach the end of their runway before they have built enough differentiation to survive. The race is between startup execution speed and platform absorption speed.

The historical parallel with AWS suggests that platform bundling may not affect all layers equally.

**Table 5. Layer Vulnerability to Platform Absorption**

| Vulnerability Level | Layers | Reasoning |
|---------------------|--------|-----------|
| High | Security, Observability | Already being folded in. Feature-like functionality. |
| Medium | Memory & Retrieval, Orchestration | Databases adding vector search. Cloud providers adding workflow engines. But specialized use cases persist. |
| Low | Compute & Inference, Perception | Requires specialized hardware or deep technical infrastructure. Hard to replicate as a platform feature. |
| Special case | Sandboxed Execution | Narrow function, but no platform has replicated it yet. Single-company layer is both strength and risk. |

The vulnerability ranking connects directly to the taxonomy's separation criteria from Section 3. Layers with low vulnerability tend to score highest on the independent-scaling test, because their technical depth creates genuine scaling independence. Layers with high vulnerability tend to fail the different-buyer test under platform bundling, because once a platform absorbs security or observability, the buyer is no longer a separate decision-maker but the same platform customer buying one more feature. This offers a test for future platform absorption. When a layer's buyer starts overlapping with an adjacent platform's existing customer base, absorption follows.

## 8. Capital Allocation and What It Signals

### 8.1 Funding Patterns and Capital Distribution

Disclosed equity funding for agentic AI companies nearly doubled from $1.5B in 2024 to $2.9B in 2025, based on summing disclosed rounds in the dataset described in Section 1. The January-May 2026 pace of $1.1B across 29 deals, annualized to approximately $2.6B (assuming a linear pace, which may not hold given seasonal deal patterns and large single-deal effects), indicates slight deceleration from the 2025 peak but continued elevated activity. The deal count also grew from 31 in 2024 to 50 in 2025, suggesting broadening investor interest rather than simple check-size inflation.



**Table 6. Capital Allocation by Layer**

| Layer | Combined Funding | % of Total | Investor Signal |
|-------|-----------------|------------|-----------------|
| Agents as Products | ~$6.1B+ | ~47% | Betting on direct revenue from finished products |
| Compute & Inference | ~$5.3B+ | ~41% | Compute as permanent bottleneck; massive capital needs |
| Orchestration | ~$709M | ~5% | Durable execution seen as sticky infrastructure |
| Memory & Retrieval | ~$349M | ~3% | Funding stalled; category may be commoditizing |
| Perception | ~$317M+ | ~2% | Active but smaller rounds; defensible tech |
| Security | ~$312M+ | ~2% | Consolidating via M&A rather than new funding |
| Evaluation & Observability | ~$256M+ | ~2% | Collapsing into adjacent categories |
| Sandboxed Execution | ~$32M | <1% | Single-company layer; narrow but critical |

The concentration of capital at the extremes (finished products and raw compute) mirrors patterns from earlier infrastructure cycles. In the cloud computing era, the biggest outcomes went to application companies (Salesforce, Workday) and compute/storage providers (AWS, Azure). The middleware layers (monitoring, security, CI/CD) produced smaller but still important exits, though notable exceptions like Datadog (monitoring, now valued at $40B+) and CrowdStrike (security, $80B+) show that middleware layers can produce very large independent companies under the right conditions. A similar distribution appears to be forming in agent infrastructure, though the middleware exceptions may or may not recur.

### 8.2 Investor Behavior and Geographic Distribution

Top venture firms have developed distinct thesis orientations that map to different parts of the stack, and the differences reveal competing predictions about how the stack evolves.

**Table 7. Investor Thesis Orientations**

| Investor | Strategy | Representative Deals |
|----------|----------|---------------------|
| Sequoia Capital | Growth-stage vertical agents and compute | Sierra, fal.ai, Parallel |
| a16z | Broad infrastructure (tools agents run on) | Inngest, Upstash |
| Kleiner Perkins | Perception and vertical agents | Browserbase ($67.5M lead), Harvey |
| ICONIQ Growth | Enterprise evaluation | Braintrust ($120M+, $800M val) |
| Y Combinator | Seed pipeline for infrastructure | Firecrawl, Kernel, E2B, Composio |

These orientations encode different bets about the stack's future. Sequoia's focus on growth-stage vertical agents and compute implies a belief that the application layer and the hardware layer will capture most of the long-term value, with the middleware layers eventually commoditizing or being absorbed. a16z's broad infrastructure thesis implies the opposite: that the middleware layers are where durable, platform-like businesses form, much as Datadog and CrowdStrike did in cloud computing. Y Combinator's role as the primary seed pipeline for infrastructure layers (Firecrawl, Kernel, E2B, Composio) means its portfolio is disproportionately exposed to the platform absorption risk described in Section 7. If Vercel or Cloudflare successfully bundles perception, orchestration, and evaluation into platform features, Y Combinator's agent infrastructure cohort faces the same compression that earlier YC SaaS companies faced when AWS added competing services. The investor thesis split is, in effect, a market-level disagreement about whether the eight-layer structure persists or collapses.

At the category level, vertical AI agents attract approximately 55% of total capital and 48% of total deals. Agent execution infrastructure (foundational tools) accounts for approximately 30% of capital with a growing deal count. Agent development platforms (orchestration, SDKs) take approximately 15% with fluctuating deal activity. These category-level splits are derived from the same company-level dataset described in the methodology section by grouping each company into one of three categories (vertical agent, execution infrastructure, or development platform) and summing funding within each group. Reasonable people could classify several companies differently (e.g., Composio as execution infrastructure vs. development platform), which would change the percentages by a few points. The United States captures approximately 82% of all agentic AI venture capital in this dataset, based on summing disclosed funding by company headquarters. This figure reflects the dataset's composition rather than verified global totals, since the sources used (Crunchbase, PitchBook) underrepresent Chinese and other non-US companies. Europe accounts for 10 to 12%, with France, the UK, and Germany producing the majority of European agent companies. Israel contributes a disproportionate share in agent security specifically.

## 9. Open Questions and Risks

The analysis in Sections 3 through 8 surfaces five open questions that the data alone cannot resolve. Each one maps to a specific tension in the findings. The platform bundling question follows from the corporate acquisitions in Sections 6 and 7. The wrapper die-off follows from the thin wrapper problem in Section 4.4. The compute bottleneck follows from the dependency graph in Section 4.1 and the capital concentration in Section 8.1. The geographic concentration question follows from the dataset limitations noted in Section 1 and the funding splits in Section 8.2. And regulatory uncertainty follows from the agent identity discussion in Section 5.4. Together, these five questions define the range of outcomes for the stack over the next two to three years.

**Can the eight layers stay independent, or do they collapse into three or four platform bundles?** The AWS precedent suggests eventual platform bundling, but the timeline matters. AWS took roughly a decade to absorb most cloud infrastructure categories. Vercel and Cloudflare are moving faster, but the technical specificity of some agent layers (compute, perception) may protect specialist companies in ways that earlier cloud categories did not.

**The wrapper startup die-off.** A common failure mode for early-stage agent startups is thin wrappers around foundation model APIs. Each time OpenAI, Anthropic, or Google adds a native feature (function calling, code execution, web browsing), a cohort of wrapper startups loses its value proposition. The companies that survive own infrastructure the model providers are unlikely to replicate. MightyBot's market analysis flags "agent washing" as a related risk, with vendors relabeling chatbots as agents without adding meaningful autonomy [55].

**Compute as the permanent bottleneck.** Nearly every layer in the stack depends on inference. If GPU supply constraints persist, compute costs could limit the growth of all other layers regardless of how well those layers execute. Cerebras's IPO [11] and the Groq-Nvidia licensing deal (reportedly ~$20B per media estimates) [15] reflect the market's belief that compute scarcity is a durable condition. If compute becomes cheap and abundant (through custom chips, edge inference, or efficiency gains), the entire stack reprices.

**The geographic concentration problem.** As noted in Section 8.2, the United States captures the vast majority of agentic AI venture capital in this dataset. China is largely absent from this analysis due to data source limitations, but Chinese companies are building parallel agent infrastructure stacks that could alter global market dynamics. Baidu's Qianfan platform provides model hosting, fine-tuning, and agent orchestration in a single integrated service. Alibaba Cloud's Tongyi Qianwen family includes agent-capable models with built-in tool calling, and Alibaba's ModelScope serves as an open-source model hub with over 4,000 models. ByteDance's Coze (launched globally as a no-code agent builder) provides orchestration, memory, and tool integration in a single product, collapsing several of the layers this paper treats as separate. These Chinese platforms tend toward vertical integration rather than the layer-by-layer specialization seen in the US market, which may reflect differences in platform business models, developer community structure, or the relative maturity of venture markets for infrastructure startups. Including Chinese companies would increase total market funding estimates, add more competitors to the compute and orchestration layers, and potentially challenge the assumption that eight independent layers represent the natural market structure.

European companies also contribute meaningfully, particularly in security (Lakera from Switzerland, now acquired by Check Point) and observability (Langfuse from Germany, now acquired by ClickHouse).

**Regulatory uncertainty.** Agents acting autonomously raise liability questions that no existing legal framework addresses well. When an agent makes a purchase, signs a contract, or sends a communication on behalf of a user, who bears liability if something goes wrong? The OAuth 2.1 work at Descope and the Agentic Commerce Protocol at Stripe represent early technical responses, but the legal and regulatory frameworks lag behind the technology by years. Jurisdictional differences (EU AI Act, US state-level regulation, no unified US federal framework) add complexity for companies operating globally.

**Limitations of this analysis.** The methodology section (Section 1) describes the dataset's scope and constraints in detail. Beyond those, three additional limitations matter. The concentration metrics are sensitive to how analysts draw company boundaries (e.g., whether Composio belongs in orchestration, tools, or both). Several claims in this paper describe correlations in funding patterns; readers should be cautious about inferring causation from capital allocation data, since funding decisions reflect investor sentiment, macro conditions, and portfolio construction logic alongside fundamental category dynamics. Finally, the eight-layer taxonomy is one of several valid ways to decompose this market; alternative groupings (such as MightyBot's seven-category map [55]) would produce different layer boundaries and funding distributions.

These five questions and the limitations above share a common thread. Every finding in this paper depends on a dataset that stops in May 2026, in a market where a single acquisition or platform launch can redraw layer boundaries overnight. The eight acquisitions in Table 4 all occurred within twenty months. A comparable burst over the next twenty months could invalidate several of the competitive dynamics described in Sections 6 and 7. The taxonomy itself provides a built-in falsifiability test through its three separation criteria. If future data shows two adjacent layers consistently selling to the same buyer through the same purchase decision, those layers belong together and the eight-layer count should shrink. Applying these same criteria to updated market data in mid-2027 would show whether the structure described here persisted or had already begun collapsing.

## 10. Conclusion

### 10.1 Core Contributions

This paper maps the development of the agent developer toolchain between 2024 and 2026, making three primary contributions. First, it establishes a functional eight-layer taxonomy of the agent infrastructure stack based on clear separation criteria: independent scaling, distinct buyer profiles, and independent pricing. Second, it maps the technical dependencies and competitive dynamics between these layers, identifying how middleware functions are collapsing into adjacent platforms. Third, it compiles capital allocation data across 50+ companies, revealing extreme funding concentration where compute infrastructure and vertical products capture over 85% of total capital, while middleware layers face tight resource constraints.

### 10.2 Strategic and Economic Outcomes

The structural analysis of the agent stack suggests five structural outcomes for this market.

First, the middleware layers (observability, security, and vector databases) are collapsing into database engines and cloud platforms. Standalone startups in these layers may only remain viable by maintaining proprietary moats that platforms struggle to replicate, such as custom inference hardware or sandboxed execution runtimes. Otherwise, platform giants like Vercel and Cloudflare are likely to absorb these functions as free features to drive consumption of their underlying compute.

Second, the transition from seat-based software licenses to transactional compute introduces a structural margin paradox. Under a transactional billing model, long-term profitability may reside with the layers that control execution latency and cost. Because large platforms can subsidize middleware as loss-leaders to capture compute volume, the survival of independent runtimes may depend on maintaining cost and speed advantages that platforms cannot easily match.

Third, the primary risk to this infrastructure is the difference between planned enterprise investment and actual production scaling. This lag stems from unpredictable agent behavior and compounding runtime costs, where a linear increase in task complexity triggers an exponential increase in tokens, sandboxed runs, and browser sessions. If execution costs force integration, platform incumbents may absorb these features, while the growth of independent runtimes may depend on whether startups like Browserbase, Inngest, and E2B can establish sustained organic revenue.

Fourth, the long-term separation of these layers may depend on whether the developer community establishes open, vendor-neutral protocols for agent-to-agent communication and resource sharing. While Anthropic's Model Context Protocol (MCP) represents an early step toward standardizing tool access, a complete runtime standard requires unified specifications for state persistence, sandboxed security, and verifiable non-human credentials. Without these shared standards, platform giants are highly likely to enforce proprietary, locked-in development environments, whereas open protocols could preserve a diverse, competitive network of specialized infrastructure providers.

Fifth, the rise of autonomous transactions requires a fundamental reorganization of payment and security architectures. When software agents execute financial decisions without direct human intervention, traditional payment authentication fails. The long-term scalability of the agent economy depends on developing high-velocity micropayment protocols, programmatic spending boundaries, and cryptographic verification of agent intent. Financial networks may transition from card-based credentials to edge-native, policy-driven wallets, making transaction authorization a core layer of developer infrastructure.

## References

1. Browserbase. "Browserbase raises $40M Series B." Company blog, 2025. browserbase.com (accessed May 2026).

2. Firecrawl. Company disclosures. firecrawl.dev (accessed May 2026).

3. Parallel. Funding announcement. Company disclosures, 2025. parallel.ai (accessed May 2026). Funding data per venture funding databases.

5. Temporal Technologies. "Temporal raises Series C." Company blog. temporal.io (accessed May 2026). Funding data per venture funding databases.

6. Inngest. Company disclosures. inngest.com (accessed May 2026).

7. Composio. Company disclosures. composio.dev (accessed May 2026).

8. Braintrust Data. Company disclosures. braintrust.dev (accessed May 2026). Funding data per venture funding databases.

9. Langfuse. "Langfuse joins ClickHouse." Company blog, January 2026. langfuse.com/blog/joining-clickhouse

10. Arize AI. Company disclosures. arize.com (accessed May 2026). Funding data per venture funding databases.

11. Cerebras Systems. Form S-1 Registration Statement. U.S. Securities and Exchange Commission, EDGAR. Filed 2026. cerebras.ai Post-IPO market cap per NASDAQ (accessed May 2026).

12. Together AI. Company disclosures. together.ai (accessed May 2026). Funding and ARR data per venture funding databases and media reports.

13. Modal Labs. Company disclosures. modal.com (accessed May 2026). Funding data per venture funding databases.

14. Fireworks AI. Company disclosures. fireworks.ai (accessed May 2026). Funding and throughput data per venture funding databases.

15. Groq. Company disclosures. groq.com (accessed May 2026). Funding data and Nvidia licensing per media reports.

16. fal.ai. Company disclosures. fal.ai (accessed May 2026). Funding data per venture funding databases.

17. Cloudflare Workers AI Models. Cloudflare Developer Documentation. developers.cloudflare.com/workers-ai/models (accessed May 2026).

18. Pinecone. Company disclosures. pinecone.io (accessed May 2026). Funding data per venture funding databases.

19. Qdrant. Company disclosures. qdrant.tech (accessed May 2026). Funding data per venture funding databases.

20. Weaviate. Company disclosures. weaviate.io (accessed May 2026). Funding data per venture funding databases.

21. Chroma. Company disclosures. trychroma.com (accessed May 2026). Funding data per venture funding databases.

22. Mem0. Company disclosures. mem0.ai (accessed May 2026). Funding and AWS partnership data per venture funding databases.

23. Upstash. Company disclosures. upstash.com (accessed May 2026).

24. E2B. Company disclosures. e2b.dev (accessed May 2026).

25. Cisco. "Fortifying the Future of Security for AI." Cisco Security Blog, August 2024. blogs.cisco.com/security/fortifying-the-future-of-security-for-ai (accessed May 2026).

26. Cisco. "Making AI Trustworthy and Observable in Real-Time: Cisco Announces Intent to Acquire Galileo." Cisco Newsroom, April 2026. newsroom.cisco.com/c/r/newsroom/en/us/a/y2026/m04/making-ai-trustworthy-and-observable-in-real-time-cisco-announces-intent-to-acquire-galileo.html (accessed May 2026). Acquisition completed May 2026.

27. Check Point Software Technologies. "Check Point Acquires Lakera." Press release. September 2025. checkpoint.com/press-releases/check-point-acquires-lakera

28. Lakera. Company disclosures. lakera.ai (accessed May 2026). Founding date and funding data per venture funding databases.

29. Robust Intelligence. Company disclosures. Funding data per venture funding databases. Company acquired by Cisco, September 2024; original domain no longer active.

30. Galileo AI. Company disclosures. rungalileo.io (accessed May 2026). Funding data per venture funding databases.

31. Patronus AI. Company disclosures. patronus.ai (accessed May 2026). Funding data per venture funding databases.

32. Corridor. Company disclosures. corridor.dev (accessed May 2026). Funding data per venture funding databases.

33. Arcjet. Company disclosures. arcjet.com (accessed May 2026). Funding data per venture funding databases.

34. Descope. Company disclosures. descope.com (accessed May 2026). Funding and product data per venture funding databases.

35. Cognition AI. Company disclosures. cognition.ai (accessed May 2026). Funding and ARR data per venture funding databases and media reports.

36. Sierra AI. Company disclosures. sierra.ai (accessed May 2026). Funding data per venture funding databases.

37. Harvey AI. Company disclosures. harvey.ai (accessed May 2026). Funding data per venture funding databases and media reports.

38. Decagon. Company disclosures. decagon.ai (accessed May 2026). Funding data per venture funding databases.

39. Factory AI. Company disclosures. factory.ai (accessed May 2026). Funding data per venture funding databases.

40. CodeRabbit. Company disclosures. coderabbit.ai (accessed May 2026). Funding data per venture funding databases.

41. Vercel Marketplace. vercel.com/marketplace (accessed May 2026).

42. Apify. Company disclosures. Revenue and funding data. apify.com (accessed May 2026).

43. Chatbase. Company disclosures. chatbase.co (accessed May 2026).

44. AWS Bedrock Agents. Amazon Web Services. aws.amazon.com/bedrock/agents (accessed May 2026).

45. McKinsey & Company. "The State of AI in 2025: Agents, Innovation, and Transformation." McKinsey Global Survey, November 2025. mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai-in-2025-agents-innovation-and-transformation

46. Gartner. "Hype Cycle for Agentic AI, 2026." Gartner Research, April 2026. gartner.com/en/articles/the-hype-cycle-for-agentic-ai

47. Deloitte. "State of AI in the Enterprise, 7th Edition: The Untapped Edge." Deloitte AI Institute, 2026. www2.deloitte.com/us/en/insights/focus/cognitive-technologies/state-of-ai-and-intelligent-automation-in-business-survey.html

48. A. Adimulam, R. Gupta, and S. Kumar. "The Orchestration of Multi-Agent Systems: Architectures, Protocols, and Enterprise Adoption." arXiv:2601.13671, 2026. arxiv.org/abs/2601.13671

49. D. Liu, K. Upadhyay, V. Chhetri, A. B. Siddique, and U. Farooq. "A Large-Scale Study on the Development and Issues of Multi-Agent AI Systems." arXiv:2601.07136, 2026. arxiv.org/abs/2601.07136

50. W.-C. Huang, W. Zhang et al. "Rethinking Memory Mechanisms of Foundation Agents in the Second Half: A Survey." arXiv:2602.06052, 2026. arxiv.org/abs/2602.06052

51. Chang Yang, Chuang Zhou, Yilin Xiao et al. "Graph-based Agent Memory: Taxonomy, Techniques, and Applications." arXiv:2602.05665, 2026. arxiv.org/abs/2602.05665

52. J. Logan. "Continuum Memory Architectures for Long-Horizon LLM Agents." arXiv:2601.09913, 2026. arxiv.org/abs/2601.09913

53. Zixia Jia, Jiaqi Li, Yipeng Kang et al. "The AI Hippocampus: How Far are We From Human Memory?" arXiv:2601.09113, 2026. arxiv.org/abs/2601.09113

54. Y. Tang and T. Runkler. "LLM-Based Agentic Systems for Software Engineering: Challenges and Opportunities." arXiv:2601.09822, 2026. arxiv.org/abs/2601.09822

55. MightyBot. "AI Agents Market Map 2026: Every Category Mapped." May 2026. mightybot.ai/blog/ai-automation-agents-market-maps-gone-wild

56. Mintlify. "Mintlify acquires Helicone." Company blog, March 2026. mintlify.com/blog/mintlify-acquires-helicone

57. Yubin Kim et al. "Towards a Science of Scaling Agent Systems." arXiv:2512.08296, 2025. arxiv.org/abs/2512.08296

58. P. Wang, X. Li, C. Xiang et al. "The Landscape of Prompt Injection Threats in LLM Agents: From Taxonomy to Analysis." arXiv:2602.10453, 2026. arxiv.org/abs/2602.10453

59. J. Kim, X. Liu, Z. Wang, S. Qiu, B. Li, W. Guo, and D. Song. "The Attack and Defense Landscape of Agentic AI: A Comprehensive Survey." arXiv:2603.11088, 2026. Accepted at USENIX Security 2026. arxiv.org/abs/2603.11088

60. Kexin Chu. "From Stateless Queries to Autonomous Actions: A Layered Security Framework for Agentic AI Systems." arXiv:2604.23338, 2026. arxiv.org/abs/2604.23338

61. P. H. B. Correia, R. W. Achjian et al. "A Systematic Literature Review on LLM Defenses Against Prompt Injection and Jailbreaking: Expanding NIST Taxonomy." arXiv:2601.22240, 2026. arxiv.org/abs/2601.22240

62. Runyang You, Hongru Cai, Caiqi Zhang et al. "A Survey on Agent-as-a-Judge." arXiv:2601.05111, 2026. arxiv.org/abs/2601.05111

63. A. Yehudai, L. Eden, A. Li et al. "A Survey on Evaluation of LLM-based Agents." arXiv:2503.16416v2, updated April 2026. arxiv.org/abs/2503.16416

64. P. Yu, W. Liu, Y. Yang et al. "Benchmarking LLM Tool-Use in the Wild." arXiv:2604.06185, 2026. Accepted at ICLR 2026. arxiv.org/abs/2604.06185

65. H. Xu, C. Li, X. Ma et al. "The Evolution of Tool Use in LLM Agents: From Single-Tool Call to Multi-Tool Orchestration." arXiv:2603.22862, 2026. arxiv.org/abs/2603.22862

66. OpenAI. "OpenAI Codex." OpenAI Blog, August 2021. openai.com/index/openai-codex/ (accessed May 2026). Temporal integration per Temporal Technologies case studies.

67. Multiple media reports. "Meta agrees to acquire Manus for approximately $2B, subsequently blocked by China's NDRC in April 2026." (accessed May 2026).

68. PitchBook/NVCA Venture Monitor. Median AI seed round data. Q1 2026. pitchbook.com/news/reports/q1-2026-pitchbook-nvca-venture-monitor


