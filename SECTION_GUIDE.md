# Section-by-Section Writing Guide

This guide provides structured advice for writing each section of an academic paper. These tips are adapted from best practices in AI-assisted scientific writing (including patterns from the [AI-Scientist](https://github.com/SakanaAI/AI-Scientist) project) and tailored to produce human-quality, SSRN-ready output.

Always follow the stylistic rules in `AI_INSTRUCTIONS.md` alongside this guide.

## Before Outlining

Complete the planning sections of [templates/research_protocol.md](templates/research_protocol.md) using [RESEARCH_METHODOLOGY.md](RESEARCH_METHODOLOGY.md). Give each section a role in the argument. Connect the problem, supported gap, question, method, observations, interpretation, and bounded conclusion. Adjust section order to the study and venue without breaking those dependencies.

Finalize findings, conclusion, and abstract only after the relevant analysis and evidence audit. A coherent narrative must include inconvenient results and unresolved explanations.

---

## Abstract

- **TL;DR of the entire paper.** A reader should get the full story in one paragraph.
- What are we trying to do and why is it relevant?
- Why is this hard?
- How do we solve it (our contribution)?
- What evidence answers the question, with what uncertainty and limits? Do not assume the proposed solution succeeds.
- Write this as one continuous paragraph with no line breaks.
- Keep it under 250 words for most venues.

---

## Introduction

- This is a longer version of the Abstract with more context.
- Motivate the problem with concrete data or real-world impact.
- Explain why existing approaches fall short.
- Clearly state your contribution (use bullet points).
- **Omit mechanical roadmap paragraphs** ("Section 2 covers..., Section 3 describes..."). Readers skip them and they waste vertical space. Instead, end the Introduction with clear contributions or move directly into the first substantive section.
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
- Explain consequential design choices and alternatives using the protocol. State identifying assumptions for causal claims and premises for theoretical claims. Keep test answers and hindsight information out of the tested method.

---

## Experimental Setup

- Describe how you test your approach. Be specific about:
  - Datasets: source, size, preprocessing, splits
  - Baselines: what you compare against and why
  - Metrics: what you measure and why those metrics matter
  - Hyperparameters: key choices and how they were tuned
  - Implementation: framework, hardware, training time
- **Do not fabricate hardware or infrastructure details.**
- Define the target quantity, experimental unit, sampling and assignment, repeated-run dependence, resource matching, evaluator validation, failures, exclusions, and stopping rule.
- Justify sample size or precision and identify which analyses were planned before outcomes were inspected.

---

## Results

- Present results that have actually been computed. **Never hallucinate numbers.**
- Use tables for quantitative comparisons across methods.
- Use figures for trends, distributions, and visualizations. Size figures proportionally (height `2.2in` to `3.4in`, width `0.75\textwidth` to `0.88\textwidth`) to prevent LaTeX from generating accidental blank float-only pages.
- Use flexible table floats (`[!htbp]`) rather than rigid `[H]` so narrative text flows naturally around tables.
- **Provide immediate context for conditional metrics.** If an indicator shows a high match rate (e.g. $P/A = 100\%$) due to prerequisite filtering while overall cohort adoption is low ($<0.1\%$), explain the denominator filtering right where the number is presented.
- **Do not repeat the primary caveat in every subsection.** If Section 1 or 3 defined that "readiness measures feature availability rather than task success," do not repeat that caveat after every table. Focus purely on interpreting the immediate results.
- Compare to baselines with statistical measures (standard deviation, confidence intervals) when available.
- Where applicable, use ablations to test whether components affect outcomes; account for changes in resources or information caused by removal.
- Report effect sizes and uncertainty for the primary comparisons, including negative and inconclusive findings. State the source of variation and the unit used to calculate intervals.
- Discuss limitations of the results honestly.
- Keep all experimental results (figures and tables) in this section, not scattered throughout.

---

## Related Work

- These are the **academic siblings** of your work — alternative attempts at solving the same problem.
- **Compare and contrast.** For each cited work, explain:
  - How does their approach differ in assumptions or method?
  - If their method applies to your problem setting, include an experimental comparison.
  - If it does not apply, explain why clearly.
- **No unprovable attacks or polemics.** Never disparage commercial tools, vendor checklists, or previous research. Maintain an objective, respectful, academic tone grounded in established, neutral internet standards (IETF, W3C, ISO).
- Just describing what another paper does is not sufficient.
- Be concise. Discuss only the most relevant work.
- Cite the sources needed for each substantive comparison. Citation count is not a quality target; a citation must actually support its associated statement.

---

## Discussion and Limits of Inference

- Interpret results in relation to the original questions and the closest prior work.
- Examine the strongest alternative explanations, measurement problems, sampling limits, and sensitivity to assumptions.
- Distinguish statistical detectability from practical value, and internal validity from transfer to new settings.
- State whether each central claim is supported within scope, mixed, contradicted, or inconclusive. A simulation result or non-significant test does not by itself establish a deployment claim or equivalence.
- Explain unresolved questions and how they limit conclusions; do not simply append generic caveats.

---

## Conclusion

- Brief recap of the problem, your approach, and key findings.
- **Write a single, unified conclusion.** Avoid writing two consecutive concluding paragraphs that repeat the core thesis or human-vs-agent contrast in slightly different words.
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
- Use active voice, simple words, and declarative sentences.
- Avoid micro-subsections: club 5–6 tiny 1-paragraph sections under a single parent subsection with bold inline headings (`\paragraph{...}`).
- Use dynamic cross-references only (`\label{sec:...}` and `\ref{sec:...}`).
- When in doubt, be more concise.

### For Charts and Figures
- Generate charts programmatically using Python (matplotlib, seaborn) to avoid hallucinated numbers.
- Every figure must have a descriptive caption.
- Reference every figure in the text.
- Do not include a figure unless you discuss it.
- Size figures proportionally to avoid LaTeX's float-page whitespace trap.

### For Appendices and Multi-Page Tables
- Use `longtable` for tables with >15 rows in appendices so they flow across page breaks rather than leaving large white space holes.
- In `longtable`, keep `\endfoot` completely empty if rows end with `\\ \midrule` to avoid the double-line bug at intermediate page breaks.
- Tune table padding (`\LTpre`, `\LTpost`, `\arraystretch`) to prevent orphan single-row appendix pages before the bibliography.

### For Citations
- Support externally sourced factual claims with citations and original findings with traceable analyses. Identify definitions, assumptions, and deductions as such.
- Use `scripts/find_citations.py` to find papers you may have missed.
- Verify that all cited papers actually exist.
- Verify that the cited passage supports the claim, including its population, date, method, and uncertainty.

### Pre-Submission Checklist
- Complete the protocol's evidence audit and Section 0 of `QUALITY_CHECKLIST.md`.
- Run `scripts/review_paper.py` for an AI peer review before submitting.
- Run `scripts/check_novelty.py` to find overlapping work and inspect the closest sources directly.
- Run `scripts/verify_references.sh` to check all URLs.
- Run `scripts/generate_pdf.sh` to generate the final PDF.
