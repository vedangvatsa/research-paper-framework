# Section-by-Section Writing Guide

This guide provides structured advice for writing each section of an academic paper. These tips are adapted from best practices in AI-assisted scientific writing (including patterns from the [AI-Scientist](https://github.com/SakanaAI/AI-Scientist) project) and tailored to produce human-quality, SSRN-ready output.

Always follow the stylistic rules in `AI_INSTRUCTIONS.md` alongside this guide.

---

## Abstract

- **TL;DR of the entire paper.** A reader should get the full story in one paragraph.
- What are we trying to do and why is it relevant?
- Why is this hard?
- How do we solve it (our contribution)?
- How do we verify that we solved it (experiments and results)?
- Write this as one continuous paragraph with no line breaks.
- Keep it under 250 words for most venues.

---

## Introduction

- This is a longer version of the Abstract with more context.
- Motivate the problem with concrete data or real-world impact.
- Explain why existing approaches fall short.
- Clearly state your contribution (use bullet points).
- Provide a roadmap of the paper: "Section 2 covers..., Section 3 describes..."
- If there is space, mention potential future directions.

---

## Background

- Cover all concepts and prior work that a reader needs to understand your method.
- Include a **Problem Setting** subsection that formally introduces notation and assumptions.
- If your paper introduces a novel problem setting, consider giving it its own section.
- Do not just list prior work here. Save comparison for Related Work.

---

## Method

- Describe what you do and why you do it.
- Build on the notation and foundations from Background.
- Be precise enough that a competent researcher could reproduce your method.
- Use equations, algorithms, or pseudocode where they add clarity.
- Avoid vague language like "we process the data" — specify how.

---

## Experimental Setup

- Describe how you test your approach. Be specific about:
  - Datasets: source, size, preprocessing, splits
  - Baselines: what you compare against and why
  - Metrics: what you measure and why those metrics matter
  - Hyperparameters: key choices and how they were tuned
  - Implementation: framework, hardware, training time
- **Do not fabricate hardware or infrastructure details.**

---

## Results

- Present results that have actually been computed. **Never hallucinate numbers.**
- Use tables for quantitative comparisons across methods.
- Use figures for trends, distributions, and visualizations.
- Compare to baselines with statistical measures (standard deviation, confidence intervals) when available.
- Include ablation studies showing which components of your method matter.
- Discuss limitations of the results honestly.
- Keep all experimental results (figures and tables) in this section, not scattered throughout.

---

## Related Work

- These are the **academic siblings** of your work — alternative attempts at solving the same problem.
- **Compare and contrast.** For each cited work, explain:
  - How does their approach differ in assumptions or method?
  - If their method applies to your problem setting, include an experimental comparison.
  - If it does not apply, explain why clearly.
- Just describing what another paper does is not sufficient.
- Be concise. Discuss only the most relevant work.
- Ensure every paragraph has enough citations (at least 2-3).

---

## Conclusion

- Brief recap of the problem, your approach, and key findings.
- Think of future work as "potential academic offspring."
- Be honest about limitations.
- End with the broader impact or open questions.
- Keep this section short (half a page or less).

---

## General Tips

### For All Sections
- Before writing each paragraph, mentally note what you plan to say (or add a comment).
- Ensure each section flows naturally into the next.
- Avoid redundancy — do not repeat the same information across sections.
- Use active voice and declarative sentences.
- When in doubt, be more concise.

### For Charts and Figures
- Generate charts programmatically using Python (matplotlib, seaborn) to avoid hallucinated numbers.
- Every figure must have a descriptive caption.
- Reference every figure in the text.
- Do not include a figure unless you discuss it.

### For Citations
- Every factual claim needs a supporting citation.
- Use `scripts/find_citations.py` to find papers you may have missed.
- Verify that all cited papers actually exist.

### Pre-Submission Checklist
- Run `scripts/review_paper.py` for an AI peer review before submitting.
- Run `scripts/check_novelty.py` to verify your angle is not already covered.
- Run `scripts/verify_references.sh` to check all URLs.
- Run `scripts/generate_pdf.sh` to generate the final PDF.
