# Academic Research Paper Framework

A reusable framework for planning, evaluating, and writing academic papers for preprint repositories and research venues. Includes AI-powered pre-submission tools adapted from [SakanaAI/AI-Scientist](https://github.com/SakanaAI/AI-Scientist).

## Features

*   **Strict Stylistic & Language Enforcement:** Enforces plain everyday English over Latinate jargon, bans AI slop words and cliché openers, prohibits em-dashes and descriptive colons, eliminates mechanical roadmap paragraphs, and ensures a human-authored, respectful academic tone.
*   **Contextual Grounding & Claim Hedging:** Mandates immediate narrative context for technical exclusions, scope boundaries, dataset snapshots, and conditional metrics; requires empirical hedging for behavioral claims and zero-404 reference verification.
*   **Whitespace & Typesetting Layout Optimization:** Comprehensive LaTeX rules preventing float-page whitespace traps, ensuring proportional figure sizing, flexible table positioning, and seamless multi-page table breaks via `longtable`.
*   **3 Paper Templates:** Review paper, empirical study, and computational research (AI-Scientist style with method/experiments/ablations).
*   **Research Design Protocol:** Require reasons for methodological choices, map claims to evidence, distinguish proof from empirical support, and record unresolved questions before writing findings.
*   **AI Peer Review:** Get a structured NeurIPS-style review of your paper before submission, with scores, strengths/weaknesses, and accept/reject decision.
*   **Literature Novelty Search:** Find potentially overlapping work in Semantic Scholar or OpenAlex for a source-level comparison.
*   **Auto-Citation Finder:** Identify missing citations in your draft and get suggestions for relevant papers.
*   **Per-Section Writing Guide:** Detailed guidance for each section of your paper (Abstract, Introduction, Method, Results, etc.).
*   **Automated PDF Generation:** Convert Markdown to publication-ready PDF using Pandoc, Tectonic, and Headless Chrome.

## Setup

1.  **Prerequisites:**
    *   `pandoc` — Mac: `brew install pandoc`
    *   `tectonic` — Mac: `brew install tectonic` (for ICLR-style LaTeX papers)
    *   `Google Chrome` — for PDF generation
    *   Python 3.8+ — for AI-powered tools

2.  **Install Python dependencies** (for review, novelty check, and citation tools):
    ```bash
    pip install -r scripts/requirements.txt
    ```

3.  **Set your API key** (one of these):
    ```bash
    export ANTHROPIC_API_KEY="your-key-here"
    # or
    export OPENAI_API_KEY="your-key-here"
    ```

4.  **Optional: Semantic Scholar API key** (for higher search throughput):
    ```bash
    export S2_API_KEY="your-key-here"
    ```

5.  **Make scripts executable:**
    ```bash
    chmod +x scripts/generate_pdf.sh scripts/verify_references.sh
    ```

## Paper Types

Choose a template when starting a new paper:

| Template | Use Case | File |
|----------|----------|------|
| **Review Paper** | Synthesis, market analysis, literature reviews | `templates/review_paper.md` |
| **Empirical Study** | Original data, methodology, and results | `templates/empirical_study.md` |
| **Computational Research** | ML/AI experiments with method, baselines, ablations (AI-Scientist style) | `templates/computational_research.md` |

### Two Build Pipelines

| Pipeline | Use Case | Tools | Output |
|----------|----------|-------|--------|
| **ICLR-style LaTeX** | Formal academic papers for SSRN/arxiv | `build_tex.py` + `tectonic` | Conference-formatted PDF |
| **HTML/Chrome** | Industry reports, shorter papers | `generate_pdf.sh` + Chrome | Clean PDF with CSS styling |

For ICLR-style papers, each paper lives in its own folder under `papers/` with a `build_tex.py` and supporting assets. See `papers/agent-infrastructure-stack/` for a working example.

## Usage Workflow

### 1. Define the Question and Research Protocol

Read [RESEARCH_METHODOLOGY.md](RESEARCH_METHODOLOGY.md), [AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md), and [SECTION_GUIDE.md](SECTION_GUIDE.md). Choose a study type that can answer the question. Create the protocol alongside the intended manuscript.

```bash
cp templates/research_protocol.md papers/my_paper_protocol.md
cp templates/computational_research.md papers/my_paper.md
```

Update the copied protocol's guide link to `../RESEARCH_METHODOLOGY.md` (or `../../RESEARCH_METHODOLOGY.md` inside a paper subfolder). Replace the manuscript template with the appropriate review or empirical template when needed.

The protocol records the research gap, definitions, claim-to-evidence map, decision rationale, study design, measurements, analysis plan, deviations, and open questions. Existing studies must disclose which results were already known when the protocol was written.

Then ask the AI: *"Read the repository research instructions. Build the study's protocol, justify consequential choices, and identify which conclusions the planned evidence can and cannot support."*

### 2. Establish the Gap and Refine the Design

```bash
# Find potentially overlapping work for direct inspection
python scripts/check_novelty.py --title "My Paper Title" --abstract "We propose..."
```

Read the closest sources and record how the question, assumptions, and methods differ. Search results cannot certify novelty. Specify credible baselines, primary outcomes, sampling, uncertainty, failures, and what evidence would count against the proposed claims.

### 3. Conduct and Audit the Research

Run an appropriate pilot, then freeze the main-study plan before inspecting confirmatory results. Preserve inputs, configurations, raw records, and analysis commands. Separate exploratory findings from planned tests. Reviews and theoretical papers use the corresponding source-analysis or proof procedure in the protocol.

Complete the claim-to-evidence audit from actual results. Report mixed, negative, and inconclusive outcomes, and narrow claims when the design cannot identify the intended effect.

### 4. Draft the Paper and Check Citations

Write in the logical order of problem, gap, question, method, results, interpretation, and conclusion. Follow `AI_INSTRUCTIONS.md` and `SECTION_GUIDE.md`; derive the abstract from completed evidence.

```bash
python scripts/find_citations.py papers/my_paper.md
```

### 5. AI Peer Review (Before Submission)

```bash
# Quick single-reviewer review
python scripts/review_paper.py papers/my_paper.md

# Aggregate 3 AI review passes; not independent human peer review
python scripts/review_paper.py papers/my_paper.md --ensemble 3
```

Complete [QUALITY_CHECKLIST.md](QUALITY_CHECKLIST.md), starting with its methodological audit. Automated tools and AI reviews assist judgment; they do not certify scientific validity.

### 6. Verify References & Generate PDF

```bash
# Check all URLs
./scripts/verify_references.sh papers/my_paper.md

# Generate the PDF
./scripts/generate_pdf.sh papers/my_paper.md papers/my_paper.pdf
```

## Reproducible Research Example

[The Economics of Agent Micropayments](papers/agent-micropayments/README.md) applies the methodology protocol to an exact finite-state economic study. Its folder includes the manuscript, PDF, pre-analysis protocol, complete result tables, analytical checks, figure scripts, and an evidence audit. The results concern specified computational models rather than live LLM behavior or measured market transactions.

## Script Reference

| Script | Purpose | Usage |
|--------|---------|-------|
| `review_paper.py` | AI peer review with scores | `python scripts/review_paper.py paper.md` |
| `check_novelty.py` | Literature novelty check | `python scripts/check_novelty.py paper.md` |
| `find_citations.py` | Find missing citations | `python scripts/find_citations.py paper.md` |
| `verify_references.sh` | Check reference URLs | `./scripts/verify_references.sh paper.md` |
| `generate_pdf.sh` | Markdown to PDF | `./scripts/generate_pdf.sh paper.md paper.pdf` |

## Directory Structure

```
├── AGENTS.md                   # Entry point for coding/research agents
├── AI_INSTRUCTIONS.md          # Research, data integrity, and writing requirements
├── RESEARCH_METHODOLOGY.md     # Design rationale, evidence, proof, and inference
├── PAPER_FRAMEWORK.md          # Production pipeline, quality checklists, lessons learned
├── SECTION_GUIDE.md            # Per-section writing guidance
├── README.md                   # This file
├── templates/                  # Paper templates
│   ├── research_protocol.md    # Per-paper planning and evidence-audit record
│   ├── review_paper.md
│   ├── empirical_study.md
│   └── computational_research.md
├── scripts/                    # Automation tools
│   ├── generate_pdf.sh
│   ├── verify_references.sh
│   ├── review_paper.py
│   ├── check_novelty.py
│   ├── find_citations.py
│   ├── llm_utils.py
│   └── requirements.txt
├── papers/                     # Your research papers
│   └── agent-infrastructure-stack/  # Example: ICLR-style paper
│       ├── agent_infrastructure_stack.md   # Paper source (Markdown)
│       ├── build_tex.py                    # Markdown → LaTeX converter
│       ├── iclr2024_conference.sty         # ICLR style file
│       └── market_map.pdf                  # Figure assets
├── reports/                    # Generated reports
├── pdf-style.css               # Default PDF styling
└── pdf-style-ieee.css          # IEEE-format PDF styling
```

### New System Setup

```bash
git clone https://github.com/vedangvatsa/research-paper-framework.git
brew install tectonic pandoc
pip install -r scripts/requirements.txt
```

Then to build an ICLR-style paper:

```bash
cd papers/agent-infrastructure-stack/
python3 build_tex.py && tectonic template.tex
cp template.pdf ~/Desktop/PAPER_NAME.pdf
```

## Credits

AI-powered tools (review, novelty check, citation finder) are adapted from [SakanaAI/AI-Scientist](https://github.com/SakanaAI/AI-Scientist) (Lu et al., 2024) — rebuilt as standalone, Markdown-native Python scripts without GPU/LaTeX/Docker dependencies.
