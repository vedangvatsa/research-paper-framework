# Pre-Publication Quality Checklist

> Run through every section before finalizing any manuscript.

---

## 1. AI Phrasing Detection

LLM-drafted prose carries telltale patterns that undermine credibility with reviewers. Scrub them.

- [ ] **No Unicode dashes in source.** Search for em-dashes (`—`) and en-dashes (`–`). LaTeX Times font (`ptmr8t`) cannot render Unicode dashes. Use ASCII `---` (em-dash) and `--` (en-dash) instead.
- [ ] **No filler words.** Remove or replace: *notably, comprehensive, significant, striking, fundamental, furthermore, moreover.*
- [ ] **No AI opener patterns.** Flag and rewrite phrases like: *"has grown at an accelerating pace"*, *"in the rapidly evolving landscape"*.
- [ ] **No cliché phrases.** Remove: *"blurred boundary"*, *"double-edged sword"*, *"paradigm shift"*, *"unprecedented"*.
- [ ] **No inflated verbs.** Replace *leverage, foster, facilitate* with concrete alternatives (*use, support, enable*).
- [ ] **Run the grep.**

```bash
grep -nE '—|–|notably|comprehensive|striking|fundamental|furthermore|moreover|landscape|paradigm|unprecedented|leverage|foster|facilitate' paper.md
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

## 4. Hedging & Projection Language

Projections are guesses. Label them as such.

- [ ] **Use "could / may / can" for projections.** Never use *will*, *would*, or *should* when describing future outcomes or predictions.
- [ ] **Run the grep and review each hit in context.**

```bash
grep -nwE 'will|would|should' paper.md
```

- [ ] **Annualized projections disclose assumptions.** If extrapolating partial-year data to a full year, state: *"assuming an even distribution across months"*.
- [ ] **Projection phrasing is tentative.** Use *"on pace for approximately X"* — not *"on track for over X"*.

---

## 5. Fact & Math Verification

A single wrong number invalidates trust in every other number.

- [ ] **Cross-reference counts between sections.** If §2 says *"14 keywords"* and Table 6 has 12 rows, that's a bug. Search for every number and verify its source.
- [ ] **Verify all percentage calculations.** Formula: `(a - b) / b × 100`. Re-derive each one from raw data.
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

## 7. Internal Consistency

The paper must agree with itself everywhere.

- [ ] **Conclusion ↔ Body.** Every finding in the conclusion must appear in a body section. Don't mention a trend (e.g., SVM decline) in the conclusion if it's not discussed in the body.
- [ ] **Abstract ↔ Body.** Every claim in the abstract must be supported by a specific section. The abstract is a summary, not a press release.
- [ ] **Figure captions ↔ Figure data.** Read each caption and verify it describes what the figure actually shows — axes, time ranges, categories.
- [ ] **Reference numbers ↔ Bibliography.** Every `[N]` in the text must point to the correct entry. Re-check after any reordering.
- [ ] **Methodological claims are true.** If the paper claims *"single API call"*, verify this is actually the case for every analysis, not just most of them.

---

## 8. LaTeX-Specific

Formatting issues that are easy to miss on screen but obvious in PDF.

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
- [ ] **Wide figures are sized correctly.** Hype cycle diagrams and similar wide figures should use `0.90\textwidth` or narrower. Check for margin overflow.
- [ ] **No overfull hbox warnings.** Run `pdflatex` and review the log for `Overfull \hbox` warnings. Fix each one.

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

- [ ] Data "indicates", never "confirms" or "proves"
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
- [ ] Causal language is absent unless causation is demonstrated ("aligns with" not "caused by")

### Reviewer G: Logic / Consistency Reviewer

Checks that the paper does not contradict itself across sections.

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

1. **Pass 1 (automated):** Run all commands from §9. Fix every flagged line.
2. **Pass 2 (section-by-section):** Walk through §1–§8 manually, checking each box.
3. **Pass 3 (multi-lens review):** Read the paper ten times, each time as a different reviewer persona from §10. Check each persona's boxes.
4. **Pass 4 (fresh eyes):** Have a co-author or colleague read the paper with this checklist open.
5. **Final gate:** All boxes checked → paper is ready for submission.

> [!TIP]
> Copy this file into your paper's repository and check boxes directly in version control.
> A partially-checked checklist in the commit history shows exactly what was reviewed and when.

> [!TIP]
> For AI-assisted review, prompt the assistant: *"Act as Reviewer A (Fact Checker) and review this paper"*
> then repeat for B through J. Each pass catches different issues.

