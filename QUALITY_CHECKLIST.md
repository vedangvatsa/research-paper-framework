# Pre-Publication Quality Checklist

> Run through every section before finalizing any manuscript.

## 0. Research Design and Evidence Audit

Use [RESEARCH_METHODOLOGY.md](RESEARCH_METHODOLOGY.md) and the paper-specific [research protocol](templates/research_protocol.md). Start this review before the main study and finish it after analysis. Mark inapplicable items with reasons. A passed style check is not a passed methodology review.

- [ ] **Question and gap.** The primary question, target setting, closest prior work, and intended contribution are explicit and supported.
- [ ] **Choice rationale.** Consequential choices have reasons, alternatives, supporting evidence or constraints, assumptions, and sensitivity checks.
- [ ] **Claim-to-evidence map.** Each central claim has an exact target quantity or proposition, required evidence, rival explanation, and possible contradictory or inconclusive outcome.
- [ ] **Study fit.** The review, measurement, causal, computational, or theoretical method matches the question. No method is included solely to look rigorous.
- [ ] **Identification and controls.** Comparators, interventions, resource matching, assignment, and confounding assumptions support the intended interpretation.
- [ ] **Measurement validity.** Outcomes have definitions, units, denominators, aggregation rules, and validated evaluators or source-appraisal procedures.
- [ ] **Sampling and independence.** Population, coverage, sample-size rationale, clustering, repeated runs, carryover, and generalization limits are accounted for.
- [ ] **Planning and leakage.** Prior data exposure, development/test separation, stopping rules, and deviations are documented. Exploratory work and retrospective plans are labeled accurately.
- [ ] **Complete accounting.** Failures, missing values, exclusions, retries, and applicable costs are included according to declared rules.
- [ ] **Inference.** Effect sizes, uncertainty, multiple comparisons, practical importance, and equivalence margins where relevant support the wording used.
- [ ] **Proof and scope.** Formal claims have valid derivations and explicit assumptions. Empirical or simulated findings are not presented as universal proof or automatic deployment evidence.
- [ ] **Reproduction and validity.** Claims trace to data, code/configuration, analysis, and artifacts. Reproducibility is assessed separately from whether the design answers the question.
- [ ] **Alternative explanations.** The strongest objections and sensitivity analyses are addressed, including evidence against the preferred account.
- [ ] **Unknowns.** Unresolved issues have explicit consequences. Unsupported claims are narrowed or withdrawn; inconclusive results remain reportable.
- [ ] **Source support.** Central citations were checked for content and context, not merely URL reachability. Automated novelty/review outputs are treated as aids.
- [ ] **Argument closure.** Abstract and conclusion answer the stated question using only findings supported in the body, at the tested scope.

---

## 1. AI Phrasing & Structural Tone Detection

LLM-drafted prose carries telltale patterns and structural filler that undermine credibility with reviewers. Scrub them.

- [ ] **No Unicode dashes in source.** Search for em-dashes (`—`) and en-dashes (`–`). LaTeX Times font (`ptmr8t`) cannot render Unicode dashes. In running text, avoid em-dashes entirely; use commas, parentheses, or separate sentences.
- [ ] **No filler words.** Remove or replace: *notably, comprehensive, significant, striking, fundamental, furthermore, moreover, intricately, vibrant, bespoke, pivotal, paramount, multifaceted, tapestry, testament, beacon, double-edged sword, not merely X but Y, delve, foster, facilitate, streamline, bolster, revolutionize, unprecedented, realm, seamless, leverage, empower, unlock, synergy, democratize, embark, cautious optimism, paradigm shift*.
- [ ] **No mechanical roadmap paragraphs.** Flag and delete boilerplate section roadmaps (*"The remainder of this paper is organized as follows: Section 2 describes..."*). Jump directly into content.
- [ ] **No redundant thesis or caveat repetition.** Ensure foundational caveats (e.g. *"feature presence does not predict task success"*) are stated clearly in the introduction and framework, not repeated as defensive boilerplate across 4 or 5 different results subsections.
- [ ] **No consecutive redundant conclusion paragraphs.** Combine multi-paragraph conclusions that rephrase the same human-vs-agent contrast into a single, punchy, memorable conclusion.
- [ ] **Context before technical exclusions.** Never state that a feature, condition, or edge case was excluded without providing narrative rationale upfront. Place boundaries in Scope or Limitations, explaining what the experimental protocol is designed to isolate and why active or destructive tasks require separate evaluation environments.
- [ ] **Methodological origin context.** Explicitly state how criteria, evaluation steps, taxonomy categories, or benchmark baselines were selected (e.g., recognized community benchmarks, published domain standards, or justified study design). Do not leave readers guessing whether authors created an ad hoc test or adapted established literature.
- [ ] **Immediate context for conditional metrics.** When reporting conditional or sub-sample metrics (e.g., subset success rate when overall prevalence is low), explain the prerequisite filtering and sample size ($N$) immediately adjacent to the number.
- [ ] **Demystify internal dataset identifiers.** Ensure raw snapshot codes, commit IDs, accession numbers, or internal hashes have human context (e.g., explaining that a frozen release was used to guarantee exact reproducibility).
- [ ] **Define operational concepts plainly.** Define technical concepts and proxy metrics in plain everyday English upon first mention, distinguishing observable indicators from broader downstream capabilities.
- [ ] **Respectful technical attribution.** Do not attack commercial tools, checklists, or previous research. Ground all technical comparisons neutrally in published domain standards, controlled replications, or formal proofs.
- [ ] **Heading alignment & subsection proportion.** Ensure every heading matches its contents. Club 5–6 consecutive micro-subsections under a unified parent heading with bold inline headings (`\paragraph{...}`).
- [ ] **Dynamic cross-referencing only.** Never hardcode section numbers (e.g., "Section 3.8"). Use `\label{sec:...}` and `\ref{sec:...}`.
- [ ] **No AI opener patterns.** Flag and rewrite phrases like: *"has grown at an accelerating pace"*, *"in the rapidly evolving landscape"*.
- [ ] **No cliché phrases.** Remove: *"blurred boundary"*, *"double-edged sword"*, *"paradigm shift"*, *"unprecedented"*.
- [ ] **No inflated verbs.** Replace *leverage, foster, facilitate* with concrete alternatives (*use, support, enable*).
- [ ] **Run the grep.**

```bash
grep -nE '—|–|notably|comprehensive|striking|fundamental|furthermore|moreover|landscape|paradigm|unprecedented|leverage|foster|facilitate|intricately|vibrant|bespoke|pivotal|multifaceted|tapestry|testament|beacon|delve|seamless|synergy' paper.md
```

---

## 2. Political & Sensitivity Language

Research papers get quoted in media. Every sentence about a country will be read by someone from that country.

- [ ] **No race/competition framing.** Replace *"overtaking"*, *"overtook"*, *"beat"*, *"won"* with neutral alternatives: *"exceeded"*, *"surpassed in count"*.
- [ ] **Country comparisons carry caveats.** When comparing countries, ensure caveats about volume vs. impact are placed neutrally — not adjacent to only one country's data.
- [ ] **Publication incentive caveats name ALL countries.** Don't single out one country. If discussing institutional pressures, name every country in the comparison (e.g., *"Both China and the US have institutional pressures that inflate publication counts"*).
- [ ] **Figure captions are neutral.** Captions get quoted directly. Avoid any race or competition language in them.
- [ ] **No patronizing framing for developing countries.** Replace *"deserves separate attention"* with *"shows a distinct pattern"*. Don't frame growth as surprising.
- [ ] **Lab naming is balanced.** Either name specific labs from all countries discussed, or use generic references (*"US-based labs"*, *"China-based institutions"*). Never name labs from only one side.

---

## 3. Semantic Precision

Every verb and quantifier makes a claim. Make sure you can defend each one.

- [ ] **"confirms" → "indicates" or "suggests".** Abstract mentions don't *confirm* anything. They *indicate* or *suggest*.
- [ ] **"collect citations" → "receive citations".** Citations happen passively; papers don't *collect* them.
- [ ] **"has not plateaued" → "has not yet shown signs of plateauing".** Don't make definitive claims about ongoing trends.
- [ ] **"moved from X to Y" → "expanding from X toward Y".** Don't imply the old thing stopped unless it actually did.
- [ ] **"replaced" → "supplemented".** Don't claim one method *replaced* another unless adoption of the old method actually dropped to near-zero.
- [ ] **No double-counting language.** *"3.7 million paper abstracts"* implies unique papers. If a single paper can match multiple search terms, say *"abstract mentions"* instead.
- [ ] **Don't overstate culture shifts.** Don't call something a *"preprint-first culture"* if journal publications still dominate (e.g., 44.6% journal vs. 27.4% preprint).

---

## 4. Hedging, Projection & Operational Scope Language

Projections and operational claims must be properly hedged. Label them as such.

- [ ] **Use "could / may / can" for projections.** Never use *will*, *would*, or *should* when describing future outcomes or predictions.
- [ ] **Mandatory hedging for operational and behavioral claims.** When describing system behaviors, human interactions, model outputs, or real-world execution, use hedged empirical phrasing (*"appears to"*, *"often"*, *"tends to"*, *"suggests"*) unless backed by direct experimental ground-truth evidence in the study.
- [ ] **Distinguish syntax and structure from ground truth and execution.**
  - Valid schema, code, or format syntax does not prove factual correctness.
  - A published public policy or API declaration does not prove runtime compliance or execution.
  - An isolated observable indicator or static proxy does not guarantee downstream end-to-end task completion.
- [ ] **Run the grep and review each hit in context.**

```bash
grep -nwE 'will|would|should' paper.md
```

- [ ] **Annualized projections disclose assumptions.** If extrapolating partial-year data to a full year, state: *"assuming an even distribution across months"*.
- [ ] **Projection phrasing is tentative.** Use *"on pace for approximately X"* — not *"on track for over X"*.

---

## 5. Fact & Math Verification

A single wrong number invalidates trust in every other number.

- [ ] **Cross-reference counts between sections.** If the text specifies a set size (e.g., *"18 evaluation criteria"* or *"6 baseline models"*), the corresponding summary table must list exactly that count. If the Discussion cites an outcome rate, verify it matches the Results tables exactly.
- [ ] **Check conditional vs. full-population rates.** Ensure text does not confuse full-population prevalence with conditional subset match rates. Explicitly state denominators and sample sizes for both.
- [ ] **Demystify internal dataset identifiers.** Ensure raw snapshot codes, commit IDs, accession numbers, or internal hashes have human context (e.g., explaining that a frozen release was used to guarantee exact reproducibility).
- [ ] **Verify all percentage calculations.** A share is `part / total × 100`; relative change is `(new - old) / old × 100`; a percentage-point difference subtracts percentages. Use the formula the claim requires, state denominators, and handle zero denominators explicitly.
- [ ] **Verify all ratio calculations.** Formula: `a / b`. Check numerator and denominator match the claim.
- [ ] **Conclusion numbers appear in the body.** Every number in the conclusion must trace back to a specific section with supporting data.
- [ ] **"Spanning X years" is correct.** Count carefully. 2013 to mid-2026 = 13.5 years, not 13. Inclusive vs. exclusive counting matters.
- [ ] **Temporal phrases match actual date ranges.** *"First five months"* should match the actual date range in the dataset (e.g., Jan–May, not Jan–June).

---

## 6. Contribution Framing

Contributions describe what the paper *does*, not what the dataset *is*.

- [ ] **Each contribution is an action, not a property.**
  - ❌ Bad: *"Scale. The corpus contains 5M papers"* (this is a property of the dataset)
  - ✅ Good: *"Abstract-level analysis. The corpus was built by searching abstracts rather than titles"* (this is a methodological choice)
- [ ] **Contributions don't overlap.** Each item in the contributions list should be clearly distinct. If two items could be merged without losing information, they overlap.
- [ ] **Contributions are falsifiable.** A reader should be able to look at the paper and confirm each contribution was actually delivered.

---

## 7. Internal Consistency & Zero-404 Reference Integrity

The paper must agree with itself everywhere, and every cited link must be verified.

- [ ] **Zero 404 links permitted.** Run `./scripts/verify_references.sh`. Ensure 0 links return 404. Replace any broken link with a permanent DOI, official standards repository (IETF RFC, W3C, ISO), or archived source.
- [ ] **Browser check for 403 / 000 responses.** If a URL returns 403 (anti-bot protection) or 000 (timeout), test it in a desktop browser to confirm the landing page is authentic.
- [ ] **Conclusion ↔ Body.** Every finding in the conclusion must appear in a body section. Don't mention a trend in the conclusion if it's not discussed in the body.
- [ ] **Abstract ↔ Body.** Every claim in the abstract must be supported by a specific section. The abstract is a summary, not a press release.
- [ ] **Figure captions ↔ Figure data.** Read each caption and verify it describes what the figure actually shows — axes, time ranges, categories.
- [ ] **Reference numbers ↔ Bibliography.** Every `[N]` in the text must point to the correct entry. Re-check after any reordering.
- [ ] **Methodological claims are true.** If the paper claims *"single API call"*, verify this is actually the case for every analysis, not just most of them.

---

## 8. LaTeX-Specific & Typesetting Layout Audit

Formatting and whitespace issues that are easy to miss on screen but immediately degrade PDF quality.

- [ ] **Tune float fractions in preamble.** Prevent LaTeX from stranding figures on dedicated float-only pages:
  ```latex
  \renewcommand{\topfraction}{0.90}
  \renewcommand{\bottomfraction}{0.90}
  \renewcommand{\textfraction}{0.10}
  \renewcommand{\floatpagefraction}{0.85}
  ```
- [ ] **Proportional figure sizing.** Keep figure height between `2.2in` and `3.4in` (width `0.75\textwidth` to `0.88\textwidth`). Avoid `4.5in`+ or `5.7in` figures that force LaTeX into creating empty pages.
- [ ] **Flexible table placement.** Avoid rigid `\begin{table}[H]` on medium/large body tables where small vertical constraints push the table and leave multi-inch blank holes. Use `\begin{table}[!htbp]`.
- [ ] **Whitespace audit (no empty pages).** Inspect the compiled PDF page by page. No body page should end with >1 inch of unexplained blank white space.
- [ ] **Multi-page appendix tables (`longtable`).** For tables with >15 rows in appendices, use `longtable` rather than a single rigid tabular block to allow clean breaks across pages.
- [ ] **Eliminate `longtable` double lines.** In `longtable`, if rows end with `\\ \midrule`, ensure `\endfoot` is completely empty (`\endfoot`), NOT `\midrule\endfoot`. Otherwise, every intermediate page break draws two horizontal rules 2.3 pt apart.
- [ ] **Prevent orphan rows before References.** Adjust `\LTpre`, `\LTpost`, or `\arraystretch` so a multi-page table does not spill just 1 or 2 orphan rows onto an otherwise empty page before the bibliography.
- [ ] **Literal tab check.** Ensure regex string replacements didn't leave literal tabs (`\t`) in LaTeX source (e.g. `domain\textquotesingle s` turning into `domain\textquotesingle s` with a tab).
- [ ] **No double line breaks before rules.** Check that no table rows end with `\\ \\` before `\bottomrule`.
- [ ] **Reduce hyphenation.** Add to preamble:
  ```latex
  \hyphenpenalty=5000
  \tolerance=1000
  ```
- [ ] **Enable microtypography.** Add to preamble:
  ```latex
  \usepackage{microtype}
  ```
- [ ] **ASCII dashes only.** Times font requires `---` (em-dash) and `--` (en-dash). Unicode `—` and `–` will render as missing glyphs or blank spaces.
- [ ] **Tables don't overflow margins.** Use `\footnotesize` consistently for table text. Check PDF output at 100% zoom.
- [ ] **Wide figures are sized correctly.** Check for margin overflow.
- [ ] **No overfull hbox warnings.** Run compiler and review log for `Overfull \hbox` warnings. Fix each one.

---

## 9. Automated Checks (Single Script)

Run `scripts/quality_check.sh` before every submission. It checks all categories in one pass:

```bash
./scripts/quality_check.sh papers/my_paper.md
```

The script checks for: AI phrasing, Unicode dashes, hedging violations, race/competition language, sensitivity red flags, AI opener patterns, cliché phrases, causal language, semantic overstatement, and LaTeX issues.

Fix every hit or justify why it's acceptable.


---

## 10. Multi-Lens Reviewer Personas

Before submission, review the paper from ten distinct perspectives. Each reviewer persona catches issues the others miss.

### Reviewer A: Fact Checker

Verifies every number, claim, and cross-reference against the paper's own data.

- [ ] Re-derive every percentage and ratio from raw numbers
- [ ] Verify every number in the abstract/conclusion traces to a body section
- [ ] Check that table row counts match prose claims ("14 keywords" vs 12-row table)
- [ ] Confirm figure captions describe what the figure actually shows
- [ ] Check that partial-year projections show honest math (e.g., 812K × 365/159 = 1.87M, not "over 1.9M")
- [ ] Verify which country/entity a number belongs to when pairs are presented ("15,008 vs 14,735" — which is which?)

### Reviewer B: Sensitivity Reader

Checks political, cultural, and regional framing for bias or implied judgment.

- [ ] Country comparisons use neutral language (no "overtaking", "race", "dominance")
- [ ] Caveats about volume vs impact are placed neutrally, not adjacent to one country
- [ ] Publication incentive critiques name ALL countries in the comparison
- [ ] Figure captions (which get quoted in media) contain no race framing
- [ ] Developing country framing is not patronizing ("shows a distinct pattern" not "deserves attention")
- [ ] Lab/company naming is balanced across countries, or uses generic references
- [ ] Subjective phrases like "most attention" are replaced with measurable ones ("fastest growth")

### Reviewer C: Semantic Reviewer

Checks that every sentence says exactly what it means — no ambiguity, overstatement, or logical gap.

- [ ] Empirical wording matches the evidence and scope. Reserve "proves" for a valid formal proof with explicit assumptions.
- [ ] Ongoing trends use hedged language ("has not yet shown signs of plateauing")
- [ ] "Expanding toward" not "moving from" (don't imply the old thing stopped)
- [ ] "Supplemented" not "replaced" (unless adoption actually dropped to near-zero)
- [ ] Aggregated counts say "mentions" not "papers" when double-counting is possible
- [ ] Culture claims match the data (don't say "preprint-first" when journals dominate)
- [ ] Comparisons that skip items are flagged ("exceeded only by X" when Y is also higher)
- [ ] Clichés are replaced with precise descriptions ("boundary blurred" → say what actually happened)

### Reviewer D: Ethics / Legal Reviewer

Checks for claims that could be misquoted, weaponized, or taken out of context.

- [ ] Headlines in the conclusion include necessary caveats (e.g., "half uncited" must mention recency inflation)
- [ ] Country quality judgments are never implied — state explicitly "this study does not measure quality"
- [ ] Projection language uses "could/may", never "will/would"
- [ ] Method lifecycle claims don't prematurely declare methods dead ("plateau candidate" not "dead")
- [ ] Correlation is never implied as causation ("16x more papers does not mean 16x more useful")

### Reviewer E: AI Phrasing Detector

Identifies language patterns that reveal AI-generated text and undermine credibility.

- [ ] No filler words: *notably, comprehensive, significant, striking, fundamental, furthermore, moreover*
- [ ] No AI opener patterns: *"has grown at an accelerating pace"*, *"in the rapidly evolving landscape"*
- [ ] No cliché phrases: *"blurred boundary"*, *"double-edged sword"*, *"paradigm shift"*, *"unprecedented"*
- [ ] No inflated verbs: *leverage, foster, facilitate, underscore, highlight*
- [ ] No Unicode em-dashes or en-dashes in source (use ASCII `---` and `--`)
- [ ] No "AI summary" sentence patterns: *"This paper provides a comprehensive analysis..."*
- [ ] Prose reads like a human wrote it, not like a prompt response

### Reviewer F: Hedging / Claims Reviewer

Ensures all predictions, projections, and trend claims use appropriately open language.

- [ ] Projections use "could / may / can", never "will / would / should"
- [ ] Annualized projections from partial-year data disclose the assumption ("assuming even distribution")
- [ ] Use "on pace for approximately" not "on track for over"
- [ ] Trend continuations say "has not yet shown signs of" not "has not" (definitive)
- [ ] Comparisons between time periods don't imply the old category stopped ("expanding toward" not "moving from")
- [ ] Causal claims name the intervention, comparator, target population, and identifying assumptions; association alone is not enough.

### Reviewer G: Logic / Consistency Reviewer

Checks that the paper does not contradict itself across sections.

- [ ] Challenge the design using Section 0 and the protocol, including the strongest rival explanation and what each experiment cannot establish
- [ ] Verify that uncertainty, negative results, and unresolved questions are reflected in the final claim wording
- [ ] Every finding in the conclusion appears in a body section with supporting data
- [ ] Every claim in the abstract is supported by a specific section
- [ ] Terms used in the conclusion are actually discussed as trends in the body (don't mention SVM decline if undiscussed)
- [ ] Contribution list items are actions (not dataset properties) and don't overlap
- [ ] Section roadmap in the introduction matches the actual section structure
- [ ] Methodological claims ("single API call", "14 keywords") match the actual methods used
- [ ] Reference numbers in text match bibliography entries after any reordering

### Reviewer H: Copy Editor

Catches typos, grammar issues, and formatting inconsistencies.

- [ ] No typos (e.g., "upto" → "up to")
- [ ] Consistent spelling throughout (e.g., British vs American English)
- [ ] All acronyms defined on first use
- [ ] Consistent number formatting (commas in thousands, decimal places)
- [ ] Consistent table formatting (same font size, alignment, border style)
- [ ] No orphaned or dangling references ("as shown in Figure X" where X doesn't exist)
- [ ] Consistent use of past vs present tense within sections

### Reviewer I: LaTeX / Typesetting Reviewer

Checks the rendered PDF for formatting problems invisible in the source.

- [ ] No overfull hbox warnings (check build log)
- [ ] No excessive word hyphenation (add `\hyphenpenalty=5000`, `\tolerance=1000`)
- [ ] Microtypography enabled (`\usepackage{microtype}`)
- [ ] ASCII dashes only — Times font cannot render Unicode em/en-dashes
- [ ] Tables fit within margins at `\footnotesize`
- [ ] Wide figures use `0.90\textwidth` or narrower
- [ ] No words cut off at page/column edges
- [ ] Figure and table placement doesn't create large whitespace gaps

### Reviewer J: Structural / Flow Reviewer

Evaluates whether the paper tells a coherent story from start to finish.

- [ ] Each section flows logically into the next (no abrupt topic changes)
- [ ] Transitions between subsections exist and make sense
- [ ] No redundancy — the same information isn't repeated across sections
- [ ] The introduction motivates the problem before stating contributions
- [ ] Related work positions this paper relative to prior work, not just lists papers
- [ ] Discussion adds interpretation beyond what Results already stated
- [ ] Conclusion doesn't introduce new data or claims not in the body

---

## How to Use This Checklist

1. **Pass 0 (methodology):** Complete Section 0 and the protocol's final evidence audit. Resolve invalid inferences by improving the design or narrowing the claim.
2. **Pass 1 (automated):** Run applicable commands from §9. Review flags in context and record unavailable checks.
3. **Pass 2 (section-by-section):** Walk through §1–§8 manually, checking applicable items with evidence.
4. **Pass 3 (multi-lens review):** Review from each perspective in §10. AI passes are not independent human peer review.
5. **Pass 4 (fresh eyes):** Seek a co-author or colleague's review; record whether it actually occurred.
6. **Final report:** State which checks passed, what was corrected, what was unavailable, and which limits remain. Checklist completion alone does not guarantee correctness or acceptance.

> [!TIP]
> Copy this file into your paper's repository and check boxes directly in version control.
> A partially-checked checklist in the commit history shows exactly what was reviewed and when.

> [!TIP]
> For AI-assisted review, prompt the assistant: *"Act as Reviewer A (Fact Checker) and review this paper"*
> then repeat for B through J. Each pass catches different issues.
