# AI Assistant Guidelines for Academic Paper Generation

Whenever you are asked to write or assist in writing an academic research paper in this repository, you **MUST** strictly adhere to the following rules. These rules are designed to ensure the output is of high academic quality, human-authored in tone, and free of typical AI artifacts.

## 0. Research Design Before Writing

Read [RESEARCH_METHODOLOGY.md](RESEARCH_METHODOLOGY.md) before choosing methods, collecting main-study data, or drafting findings. Create a paper-specific record from [templates/research_protocol.md](templates/research_protocol.md) and keep it beside the manuscript.

* **JUSTIFY CONSEQUENTIAL CHOICES:** Record what is chosen, why, credible alternatives, supporting evidence, assumptions, sensitivity checks, and revision triggers.
* **MAP CLAIMS TO EVIDENCE:** Define the question, target quantity, comparator, observations, competing explanations, and limits before the main analysis. Include outcomes that could contradict the claim or remain inconclusive.
* **MATCH THE STUDY TYPE:** Reviews need source-selection and appraisal methods; descriptive studies need valid measurement and sampling; causal studies need identification; computational comparisons need fair baselines; theoretical claims need derivations. Do not force every paper into an experiment or a new algorithm.
* **PLAN BEFORE CONFIRMATION:** Separate exploration and development from held-out evaluation. Date the analysis plan, record prior data exposure, and log deviations. Do not call a retrospective plan or unregistered local document a preregistration.
* **REPORT THE RIGHT OUTCOMES:** Define metrics, denominators, costs, failures, exclusions, uncertainty, and units of analysis. Repeated runs on one task are not independent new tasks.
* **CALIBRATE THE CONCLUSION:** Distinguish proof under assumptions, empirical support, simulation, and deployment evidence. A p-value or successful replication does not by itself validate the explanation.
* **KEEP UNKNOWNS VISIBLE:** Resolve material questions, justify and examine assumptions, or narrow the claim. Never manufacture certainty or claim that every possible objection has been eliminated.
* **PRESERVE SCIENTIFIC MEANING:** Apply wording rules without distorting precise technical statements. Formal proofs and justified causal claims are permitted when their requirements in the methodology guide are met.

## 1. Stylistic and Vocabulary Constraints
*   **NO AI SLOP WORDS:** Do not use words typical of AI generation. This includes but is not limited to: *shift, implications, significant, striking, fundamental, furthermore, moreover, simultaneously, synthesize, noteworthy, notably, consequently, thus, hence, thereby, underscore, highlight, realm, emerged, emerging, landscape, paradigm, foster, facilitate, encompass, streamline, bolster, spearhead, reshape, redefine, reimagine, reconfigure, rapid rise, rapidly rising, rapidly expanding, intricately, vibrant, bespoke, pivotal, paramount, multifaceted, tapestry, testament, beacon, double-edged sword, not merely X but Y, delve, catalyze, revolutionize, unprecedented, seamless, leverage, empower, unlock, synergy, democratize, embark, cautious optimism, crucial role, pivotal role*.
*   **NO EM-DASHES:** Do not use em-dashes (`---` or `—`) or en-dashes (`–`) for punctuation in sentences. Rewrite using separate clauses, commas, or parentheses.
*   **NO COLONS IN PROSE:** Do not use colons (`:`) in running descriptive prose. Use periods, commas, or subordinating conjunctions instead. Colons are permitted only in paper titles, section headers, reference lists, and formal mathematical definitions.
*   **NO EMOJIS:** The text must be strictly professional.
*   **SIMPLE LANGUAGE OVER LATINATE JARGON:** Use simple, plain, everyday English. Avoid overly complex, Latinate, or jargon-heavy academic phrasing where a simpler, direct word works just as well. For example:
    *   Use *features* instead of *modalities*
    *   Use *use* instead of *utilize*
    *   Use *check* instead of *interrogate*
    *   Use *shows* instead of *demonstrates*
    *   Use *start* instead of *commence*
    *   Use *delivers* instead of *dispatches*
    Define operational concepts plainly upon first mention (e.g., *"In this paper, readiness refers to whether a website provides features that AI agents can use (such as APIs, sitemaps, and labeled buttons), rather than whether a specific AI model succeeds at completing a task"*).
*   **NO MECHANICAL ROADMAP PARAGRAPHS:** Do not write boilerplate section roadmap paragraphs (*"The remainder of this paper is organized as follows: Section 2 describes... Sections 3 to 5 present..."*). Modern empirical papers in top venues skip these mechanical listings. Jump directly from the contributions, scope, and problem statement into the substantive content.
*   **NO REDUNDANT THESIS OR CAVEAT REPETITION:** State primary definitions, scope limits, and foundational caveats (such as *"feature presence does not predict end-to-end task success"*) clearly once in the Introduction and Methodology. Do not repeat the exact same caveat across 4 or 5 different sections. Keep empirical and results sections strictly focused on reporting, contextualizing, and interpreting immediate data.
*   **NO CONSECUTIVE REDUNDANT CONCLUSIONS:** Avoid writing two consecutive concluding paragraphs that restate the core thesis or human-vs-agent contrast with minor lexical variations. Combine concluding observations into a single, cohesive, punchy conclusion.
*   **CONTEXT BEFORE TECHNICAL EXCLUSIONS (NO ORPHAN DEFENSIVE CLAIMS):** Never drop unexplained technical terms or defensive claims (e.g., suddenly stating *"branding graphics, traffic counters, and prompt injection defense require interactive accounts and are not simulated"*) into a section without clear narrative context. If specific capabilities were intentionally excluded from an evaluation, place that explanation in the Experimental Scope or Limitations section with its explicit rationale.
*   **RESPECTFUL TECHNICAL ATTRIBUTION (ZERO UNPROVABLE ATTACKS):** Never disparage commercial tools, vendor checklists, or previous research (e.g., do not accuse tools of "hallucinating criteria" or "making unproven claims"). Maintain an objective, respectful, academic tone. Explain technical differences neutrally by reference to established, published internet standards (such as IETF RFCs, W3C Recommendations, and ISO specifications).
*   **IMMEDIATE CONTEXT FOR CONDITIONAL METRICS:** When reporting conditional metrics (such as a check where positive match over assessed applicable $P/A = 100\%$ while cohort-wide adoption is $<0.1\%$), explain the prerequisite filtering context immediately so the reader understands why the conditional rate is high.
*   **HEADING ALIGNMENT & SUBSECTION PROPORTION:** Ensure every heading accurately reflects the content inside. Avoid micro-subsections (e.g., 5–6 consecutive 1-paragraph subsections); club related groups under a unified parent subsection (e.g., `\subsection{Evaluated functional groups}`) with bold inline headings (`\paragraph{...}`). Always use dynamic cross-referencing (`\label{sec:...}` and `\ref{sec:...}`) rather than hardcoding section numbers (e.g., "Section 3.8").
*   **ACTIVE VOICE:** Use active voice and declarative sentences.
*   **NO RACE LANGUAGE IN COUNTRY COMPARISONS:** When comparing countries' research output, do not use competitive framing (e.g., 'overtaking', 'overtook', 'beat', 'won the race'). Use neutral language: 'exceeded', 'surpassed in count', 'produced more'. Figure captions are especially important as they get quoted in media.
*   **HEDGED TREND CLAIMS:** Do not make definitive claims about ongoing trends. Say 'has not yet shown signs of plateauing' instead of 'has not plateaued'. Say 'expanding from X toward Y' instead of 'moving from X to Y'.
*   **PASSIVE ATTRIBUTION:** Use 'receive citations' not 'collect citations'. Use 'indicates' not 'confirms' when describing what data shows.
*   **BALANCED CAVEATS:** When discussing limitations that apply to multiple countries/entities, name all of them explicitly. Do not place a caveat only adjacent to one country's data.
*   **NO CLICHES:** In addition to the existing banned list, also ban: 'blurred boundary/boundaries', 'at an accelerating pace', 'deserves separate attention', 'attracted the most attention'.
*   **THIRD PERSON FOR SINGLE-AUTHOR PAPERS:** Unless the paper has multiple authors, never use first-person plural pronouns ('we', 'our', 'us'). Use 'this study', 'the corpus', 'the analysis', 'the data' instead. For multi-author papers, 'we' is acceptable.

## 2. Research, Fact-Checking, and Data Integrity
*   **FACT-CHECK EVERY CLAIM AND NUMBER (ZERO TOLERANCE FOR INCONSISTENCIES):** Every single number, percentage, count, date range, and technical identifier must be verified against the raw empirical tables or underlying data artifacts.
    *   **Cross-Sectional Numeric Consistency:** Numbers mentioned in the Abstract, Introduction, Results, Discussion, and Conclusion must be 100% consistent with each other. If Table 2 reports `7.16%` adoption across the full cohort, do not write *"fewer than 2%"* in the Discussion. If Table 2 reports MCP initialization at `<0.1%`, do not write *"fewer than 8%"*.
    *   **Distinguish Full-Cohort vs. Conditional Denominators:** Never confuse a conditional match rate (such as positive over assessed applicable $P/A$) with a full-cohort adoption rate ($P/\text{cohort}$). Explicitly state denominators for both.
    *   **Table Row Count Match:** If the methodology or text states *"18 illustrative criteria"*, the corresponding table must have exactly 18 rows.
*   **MANDATORY HEDGING FOR OPERATIONAL & BEHAVIORAL CLAIMS:** When describing agent workflows, browser interaction habits, or real-world execution, always use hedged, empirical phrasing (*"appears to"*, *"often"*, *"tends to"*, *"can represent"*, *"is likely to"*, *"suggests"*, *"in benchmarks such as WebArena [6] and RADAR [7]"*) unless backed by direct experimental task success data in the paper.
    *   Never claim that passing a syntactic check *"guarantees"* task completion, or that having structured data *"proves"* factual correctness.
    *   Explicitly separate public declarations (e.g. published pricing routes or terms links) from runtime enforcement (e.g. executing a live purchase transaction).
    *   Never make definitive assertions about how agents "must" browse without citing published agent benchmark literature or experimental ground truth.
*   **STRICT NON-404 LINK GUARANTEE & BATCH URL VERIFICATION:**
    *   Before finalizing any paper, run `./scripts/verify_references.sh`. **Zero 404 links are permitted.**
    *   If a link returns 404, find the permanent DOI, official standards repository (IETF RFC at `rfc-editor.org`, W3C at `w3.org`, WHATWG at `html.spec.whatwg.org`), or archived corporate press release.
    *   Investigate 403 or 000 responses in a live browser to confirm the endpoint is authentic rather than a broken or hallucinated URL path.
    *   **Never fabricate a URL path.**
*   **DEMYSTIFY TECHNICAL JARGON & INTERNAL IDENTIFIERS:** Never drop unexplained internal snapshot codes, commit hashes, or dataset IDs into prose without clear human context. For example, never write *"fixed to list release Y83YG [5]"*; always explain it: *"using the permanent snapshot list Y83YG to ensure reproducibility [5]"*. Always state how operational steps, criteria, or tool configurations were gathered so the reader understands their methodological origin.
*   **NO HALLUCINATIONS OR DATE BUMPING:** Never invent data, citations, or survey results. Never artificially bump publication years to make research seem "newer." All quantitative data, legal precedents, and source material must be fiercely fact-checked, factual, and verifiable. Avoid making over-broad, boastful, or unverifiable meta-claims (e.g., "Every number in this paper is verifiable through a single API call" or "unprecedented depth"). Every claim must be strictly objective, precise, and backed directly by verifiable sources or clear methodologies.
*   **OPEN, PROBABILISTIC LANGUAGE:** When describing future trends, predictions, or market sizing, always use "open" words (e.g., *can, may, could, is likely to, is expected to, appears to*) instead of "closed" definitive words (e.g., *will, should, must, shall*). This ensures the analysis remains semantically accurate regardless of how the future unfolds.
*   **USE SYMBOLS FOR DATA:** Always use the `%` symbol instead of writing out "percent" or "per cent."
*   **NO AI SLOP:** You must strictly avoid cliché, AI-generated phrasing. Never use words or phrases like: "delve", "tapestry", "testament", "navigate/navigating", "landscape" (e.g., "regulatory landscape"), "multifaceted", "robust", "foster", "pivotal", "catalyst", "transformative", "revolutionize", "unprecedented", "realm", "seamless", "leverage", "empower", "unlock", "synergy", "democratize", "embark", "beacon", "underscores", "sheds light", "cautious optimism", "paradigm shift", "double-edged sword", "not merely X but Y", or using the word "shift" to describe changes in attitudes or data. Write with a precise, objective, human tone.
*   **NO END MARKERS:** Do not write "*End of paper.*" at the end of the document.
*   **CHART GENERATION:** Do not use AI image generators to create charts, as they hallucinate text and numbers. You MUST write a Python script (using matplotlib or seaborn) to generate charts based on accurate data, save them as `.png` files, and embed them in the markdown. Ensure all charts have clean layouts: labels, titles, and legends must never overlap. Do not include redundant titles inside the chart image itself (rely on LaTeX/Markdown captions instead). Use proper padding, margins, label rotation (e.g., 45 degrees), and consistent font sizes to prevent text clipping.
*   **USE TABLES:** When presenting numerical data, survey results, or comparisons, use Markdown tables to make the data scannable and clear. Ensure table text and font sizing are highly consistent across the entire document (e.g., use `\footnotesize` consistently for LaTeX tables). Tables must fit within the page margins/columns without overflow or clipping.
*   **VERIFIABILITY:** Prioritize industry-standard data, university-led research, and verified sources over generalities.
*   **CONTRIBUTION FRAMING:** Each listed contribution must describe an ACTION the paper takes, not a PROPERTY of the dataset. Bad: 'Scale. 5 million papers.' Good: 'Abstract-level analysis. Built by searching abstracts instead of titles.'
*   **DOUBLE-COUNTING AWARENESS:** When summing counts across keywords that a single paper can match multiple times, say 'abstract mentions' not 'paper abstracts' or 'papers'.
*   **PROJECTION MATH:** Always show the math behind annualized projections (e.g., 812,972 papers through 159 days × 365/159 = 1.87M). Round honestly. 'Approximately 1.9 million' is OK; 'over 1.9 million' when the math gives 1.87M is not.

## 3. Formatting, Output, and LaTeX Typesetting (IEEE / Conference Style)
*   **AUTHOR BLOCK:** The author section should only contain the author's full name and email address. Do not include the date.
*   **KEYWORDS:** Do not use a separate block at the top. Use the inline standard immediately below the Abstract: `_**Keywords**_: keyword1, keyword2, etc.`
*   **REFERENCES:** All URLs in the reference section must be properly formatted as clickable Markdown links (e.g., `[https://url.com](https://url.com)`). The references section must be left-aligned (not justified) to prevent ugly word-spacing gaps caused by long URLs.
*   **IN-TEXT CITATIONS:** Every reference listed in the References/Bibliography section MUST be explicitly cited in-text in the body of the paper (e.g., using `[N]` in Markdown or `\cite{refN}` in LaTeX). Ensure all citations are mapped correctly. Do not include "dead" or unused references in the bibliography.
*   **URL AND SOURCE VERIFICATION:** Run `./scripts/verify_references.sh papers/your_paper.md` before finalizing references. Its reachability checks do not verify source content. Investigate 403, connection failures, and server errors rather than automatically treating them as working or permanently dead. Verify the specific article through a browser, stable DOI, or archive where needed. A publisher's homepage does not substantiate an article-level claim. Record unavailable evidence and narrow or remove unsupported claims. Never fabricate a URL path.
*   **MARKDOWN FIRST:** Write the paper in Markdown (`.md`), following the templates in the `templates/` directory.
*   **PDF CONVERSION:** The final output must be a well-formatted PDF suitable for submission to platforms like SSRN/IEEE. Use the provided CSS and scripts (e.g., `scripts/generate_pdf.sh`) to convert the markdown to PDF. Ensure `--no-pdf-header-footer` is used to prevent browser URLs from appearing on the printout.
*   **FIGURE SIZING & FLOAT PLACEMENT (AVOIDING THE BLANK-PAGE TRAP):** Sizing figures excessively tall (such as `4.6in` or `5.7in`) triggers LaTeX's `\floatpagefraction=0.50`, stranding figures alone on dedicated float pages and leaving huge blank spaces across body pages.
    *   Size figures proportionally: height between `2.2in` and `3.4in`, width between `0.75\textwidth` and `0.88\textwidth`.
    *   Tune float placement parameters in the LaTeX preamble:
        ```latex
        \renewcommand{\topfraction}{0.90}
        \renewcommand{\bottomfraction}{0.90}
        \renewcommand{\textfraction}{0.10}
        \renewcommand{\floatpagefraction}{0.85}
        ```
    *   Avoid rigid `\begin{table}[H]` on body tables where space constraints could push the table and leave multi-inch gaps; use `[!htbp]` so text flows naturally around tables.
*   **MULTI-PAGE TABLES IN APPENDICES (`longtable`):** For appendix tables with more than 15 rows, always use `longtable` rather than a single rigid tabular environment. This allows table rows to break across pages cleanly without stranding 4-to-6 inches of blank space on preceding pages.
*   **THE DOUBLE-LINE LONGTABLE BUG:** In `longtable`, if individual rows terminate with `\\ \midrule`, setting `\midrule\endfoot` causes LaTeX to output both the row's `\midrule` AND `\endfoot`'s rule on every intermediate page break, creating unsightly double lines (2.3 pt apart) at the bottom of pages. To eliminate double lines:
    *   Define `\endfoot` as completely empty: `\endfoot`
    *   Use `\bottomrule\endlastfoot` to terminate only the final page of the table.
*   **ORPHAN ROW PREVENTION:** Adjust table vertical margins (`\setlength{\LTpre}{...}`, `\setlength{\LTpost}{...}`) or row padding (`\renewcommand{\arraystretch}{...}`) to prevent a multi-page table from spilling just 1 or 2 orphan rows onto an otherwise empty page before the bibliography.
*   **LITERAL CHARACTER & ESCAPE HYGIENE:**
    *   Verify that regex string replacements in build scripts do not convert `\textquotesingle` into literal tab characters (`\t`) followed by `extquotesingle`.
    *   Verify there are no double line breaks (`\\ \\`) preceding `\bottomrule`.
*   **IMAGE SIZING (HTML/CSS):** For HTML builds, do not span images across columns using CSS `column-span`. Instead, ensure the `img` CSS rule has a strict `max-height` (e.g., `2.2in`) and `object-fit: contain` so images fit nicely inside a single column without forcing massive column breaks.

## 4. Paper Types
Before starting a new paper, ask the user what type of paper they want to write. You can refer to the templates:
*   `review_paper.md`: For synthesis, market analysis, or literature reviews.
*   `empirical_study.md`: For papers presenting original data, methodology, and results.
*   `computational_research.md`: For computational/ML research papers with method, experiments, baselines, and ablation studies (modeled after the [AI-Scientist](https://github.com/SakanaAI/AI-Scientist) structure).

For detailed per-section writing guidance (what to cover in each section, common pitfalls), refer to `SECTION_GUIDE.md`.

## 5. Pre-Submission Tools
Before finalizing any paper, use these automated tools:
*   **AI Peer Review:** `python scripts/review_paper.py papers/my_paper.md` — Get a structured academic review with scores, strengths, weaknesses, and accept/reject decision. Use `--ensemble 3` for a more reliable multi-reviewer assessment.
*   **Novelty Check:** `python scripts/check_novelty.py papers/my_paper.md` — Find potentially overlapping work in Semantic Scholar or OpenAlex, then read and compare the relevant sources. This tool cannot certify novelty.
*   **Citation Finder:** `python scripts/find_citations.py papers/my_paper.md` — Identify missing citations and get suggestions for where to add them.
*   **URL Verification:** `./scripts/verify_references.sh papers/my_paper.md` — Check all reference URLs for 404s.
*   **PDF Generation:** `./scripts/generate_pdf.sh papers/my_paper.md papers/my_paper.pdf` — Generate the final PDF.

## 6. Mandatory Quality Review (Automatic)

Before presenting any paper as "done" or "ready", you **MUST** automatically run the full quality review defined in `QUALITY_CHECKLIST.md`. Do not wait to be asked. This is as mandatory as avoiding slop words.

The checklist includes:
1. **Methodological audit** — complete Section 0 of the checklist and the protocol's final claim-to-evidence audit
2. **Automated checks** — run applicable checks and review flags in context; record unavailable checks
3. **Ten-reviewer pass (A–J)** — review the paper from each perspective, including research design and inference; these passes are not independent human peer review
4. **Summary report** — report issues found, corrections, actual checks completed, and unresolved limits; do not imply that tool approval establishes scientific validity

**Do NOT skip this step.** A paper that has not been through the full quality review is not ready.
