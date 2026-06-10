# Pre-Publication Quality Checklist

> Lessons learned from editing the *State of AI Research* paper.
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

## 9. Automated Checks

Run these commands before every submission. Fix every hit or justify why it's acceptable.

### AI phrasing & dashes
```bash
grep -nE '—|–|notably|comprehensive|striking|fundamental|furthermore|moreover|landscape|paradigm|unprecedented|leverage|foster|facilitate' paper.md
```

### Hedging violations
```bash
grep -nwE 'will|would|should' paper.md
```

### Race/competition language
```bash
grep -niE 'overtaking|overtook|beat|won|race|dominate|dominance|leader|leading' paper.md
```

### Sensitivity red flags
```bash
grep -niE 'deserves|surprising|impressive|remarkable|notably' paper.md
```

### Definitive claims about trends
```bash
grep -niE 'has (not )?plateaued|replaced|confirms|prove[sd]?' paper.md
```

### LaTeX dash check (find Unicode dashes in .tex files)
```bash
grep -Pn '[\x{2013}\x{2014}]' paper.tex
```

### Overfull boxes
```bash
pdflatex paper.tex 2>&1 | grep -i 'overfull'
```

### Cross-reference number audit
```bash
# Extract all numbers from the conclusion and search for them in the body
# (manual review required — run and inspect)
grep -oE '[0-9]+(\.[0-9]+)?' conclusion.tex | sort -u | while read n; do
  echo "=== $n ==="
  grep -n "$n" body.tex
done
```

---

## How to Use This Checklist

1. **First pass (automated):** Run all commands from §9. Fix every flagged line.
2. **Second pass (section-by-section):** Walk through §1–§8 manually, checking each box.
3. **Third pass (fresh eyes):** Have a co-author or reviewer read the paper with this checklist open.
4. **Final gate:** All boxes checked → paper is ready for submission.

> [!TIP]
> Copy this file into your paper's repository and check boxes directly in version control.
> A partially-checked checklist in the commit history shows exactly what was reviewed and when.
