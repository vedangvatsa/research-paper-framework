# Academic Research Paper Framework

A reusable framework for generating high-quality, human-authored academic papers suitable for SSRN, IEEE, and other academic repositories. Includes AI-powered pre-submission tools adapted from [SakanaAI/AI-Scientist](https://github.com/SakanaAI/AI-Scientist).

## Features

*   **Strict Stylistic Enforcement:** Prevents AI jargon ("slop words"), em-dashes, and emojis, ensuring the output reads as a professionally written human document.
*   **3 Paper Templates:** Review paper, empirical study, and computational research (AI-Scientist style with method/experiments/ablations).
*   **AI Peer Review:** Get a structured NeurIPS-style review of your paper before submission, with scores, strengths/weaknesses, and accept/reject decision.
*   **Literature Novelty Check:** Verify your research angle is not already covered by searching Semantic Scholar or OpenAlex.
*   **Auto-Citation Finder:** Identify missing citations in your draft and get suggestions for relevant papers.
*   **Per-Section Writing Guide:** Detailed guidance for each section of your paper (Abstract, Introduction, Method, Results, etc.).
*   **Automated PDF Generation:** Convert Markdown to publication-ready PDF using Pandoc and Headless Chrome.

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

### 1. Start a New Paper

```bash
# Copy a template to the papers directory
cp templates/computational_research.md papers/my_paper.md
```

Then ask the AI: *"I want to write a new paper. Read the `AI_INSTRUCTIONS.md` and `SECTION_GUIDE.md` files first."*

### 2. Check Novelty (Before Writing)

```bash
# Verify your angle is not already covered
python scripts/check_novelty.py --title "My Paper Title" --abstract "We propose..."
```

### 3. Draft the Paper

The AI will assist in drafting based strictly on the rules in `AI_INSTRUCTIONS.md` with per-section guidance from `SECTION_GUIDE.md`.

### 4. Find Missing Citations

```bash
python scripts/find_citations.py papers/my_paper.md
```

### 5. AI Peer Review (Before Submission)

```bash
# Quick single-reviewer review
python scripts/review_paper.py papers/my_paper.md

# Higher quality: 3 independent reviewers aggregated
python scripts/review_paper.py papers/my_paper.md --ensemble 3
```

### 6. Verify References & Generate PDF

```bash
# Check all URLs
./scripts/verify_references.sh papers/my_paper.md

# Generate the PDF
./scripts/generate_pdf.sh papers/my_paper.md papers/my_paper.pdf
```

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
├── AI_INSTRUCTIONS.md          # Stylistic rules the AI must follow
├── PAPER_FRAMEWORK.md          # Production pipeline, quality checklists, lessons learned
├── SECTION_GUIDE.md            # Per-section writing guidance
├── README.md                   # This file
├── templates/                  # Paper templates
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
