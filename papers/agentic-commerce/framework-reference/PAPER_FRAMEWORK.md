# Research Paper Production Framework

This document captures the production standards, style rules, structural principles, and quality checklists developed during the creation of papers in this repository. Follow these rules for every new paper.

---

## Paper Types

This repository produces two kinds of papers:

| Type | Format | Build Tool | Output | Example |
|------|--------|-----------|--------|---------|
| **Formal academic** | Markdown → LaTeX | `build_tex.py` + `tectonic` | PDF (ICLR-style) | `agent_infrastructure_stack.md` |
| **Industry report** | Markdown → HTML | Direct render | HTML page | `state-of-ai-research-2026.md` |

Both types follow the same writing and quality rules below. The build pipeline section applies only to formal academic papers.

---

## Writing Style Rules

### Voice and Tone

1. **Active voice always.** "Cisco acquired Robust Intelligence" not "Robust Intelligence was acquired by Cisco."
2. **Third person POV.** Never "we found" or "I argue." Use "the analysis shows" or "the data suggests."
3. **Simple words.** "Use" not "utilize." "Show" not "demonstrate." "Start" not "commence." "About" not "approximately" (when informal).
4. **Open/hedged language.** Use "appears to," "seems to," "may," "can," "tends to," "often" instead of absolute claims. The taxonomy is an analytical lens, not a universal truth.

### Banned Patterns

| Pattern | Why | Fix |
|---------|-----|-----|
| Em dashes (—) | AI-sounding | Use commas, parentheses, or split into two sentences |
| Colons in running prose | Reads like a listicle | Restructure the sentence |
| "It is worth noting that" | Filler | Delete and start with the point |
| "It is important to" | Filler | Delete and start with the point |
| "This is particularly relevant" | AI filler | Delete or replace with specific reason |
| "The landscape" | AI cliche | Use specific noun (market, stack, category) |
| "Underscores" (as a verb) | AI cliche | "Shows," "confirms," "reflects" |
| "Navigating" | AI cliche | "Managing," "handling," "dealing with" |
| "Leveraging" | AI cliche | "Using" |
| "Robust" (as adjective for non-technical things) | Overused | "Strong," "reliable," "durable" |
| "Ecosystem" | Vague | "Market," "stack," "set of tools" |
| "The contrast is informative/instructive" | AI padding | Cut. The contrast speaks for itself. |
| "Holistic" | AI word | Cut or use "complete," "full" |
| "Paradigm" | Jargon | "Pattern," "model," "approach" |
| "Rapid rise / rapidly rising / rapidly expanding" | AI slop | Use specific growth statistics (e.g., "grew Xx in Y years") or plain terms ("fast-growing") |
| Boastful meta-claims (e.g., "Every number is verifiable", "unprecedented depth") | Redundant and boastful | Avoid boastful/unverifiable claims. State facts objectively. |

### Formatting

1. **No URL prefixes.** Write `github.com/org/repo` not `https://github.com/org/repo`.
2. **Numbers.** Spell out one through nine. Use numerals for 10+. Always use numerals with units ($5.3B, 50+ companies).
3. **Percentages.** Use "%" with numerals (82%), not "percent."
4. **Company names.** Use the company's own capitalization (GitHub, not Github; CrewAI, not Crewai).

---

## Structural Rules

### Section and Subsection Depth

1. **Every subsection must earn its heading.** If a subsection has fewer than 3 content paragraphs, merge it into a neighbor.
2. **Audit subsection sizes** before finalizing. Run a line-count script to identify thin sections.
3. **Renumber subsections** after merges. Then grep the entire document for stale cross-references (e.g., "Section 8.4" after 8.4 was merged into 8.3).

### Avoiding Redundancy

1. **One home for each claim.** If a point is made in Section 3, do not restate it in Sections 6 and 9. Reference it instead: "As discussed in Section 3..."
2. **Do not restate tables.** If Table 6 shows the data, the paragraph after it should analyze the data, not repeat the numbers.
3. **Kill abstract restatements.** If a concrete paragraph with data is followed by an abstract restatement of the same point, delete the abstract one.
4. **Kill setup sentences.** "The data allows us to analyze X" adds nothing. Start with the analysis.

### Analytical Depth

1. **Every section must answer "so what?"** Description is not analysis. "Cloudflare runs 50+ models at the edge" is description. "This creates a segmentation problem for standalone compute companies" is analysis.
2. **Challenge your own framework.** If Section 3 proposes a taxonomy, a later section should ask whether the taxonomy breaks down under certain conditions (e.g., marketplace bundling).
3. **Connect investor behavior to structural predictions.** Don't just list who invested where. Explain what different investment theses predict about the market's future.
4. **Close causal chains.** If Section 4 shows a dependency graph and Section 6 shows acquisition patterns, explicitly connect them: "Company X was acquired because it occupies a position in the dependency graph that platform incumbents need."

---

## Reference Integrity

### ABSOLUTE RULES

1. **NEVER fabricate a URL.** If you cannot verify a URL loads a real page, do not include it. This is the single most important integrity rule.
2. **Every reference MUST have a URL.** No exceptions. Even paywalled reports (McKinsey, Gartner, Deloitte, PitchBook) must include the landing page URL. "Company disclosures" without a URL is only acceptable when the company's domain is confirmed dead (e.g., post-acquisition).
3. **Verify every link before finalizing.** Use the batch URL verification script below. Check ALL URLs in one pass, not piecemeal.
4. **Prefer stable sources.** SEC filings > company newsrooms/press releases > industry news sites > company blog posts. Blog posts get restructured and URLs break.
5. **When a URL is dead,** replace it with a stable alternative (e.g., Cisco Newsroom press release instead of Cisco blog post) or note it as "Company disclosure; original domain no longer active" if no public URL exists.
6. **Every reference MUST be cited in-text.** Never list references in the Bibliography/References section that are not explicitly cited in the body of the paper (e.g., using `[N]` or `\cite{...}`). Avoid "dead" or unused references.

### URL Stability Hierarchy

Sources break at different rates. Prefer higher-ranked sources:

| Rank | Source Type | Why | Example |
|------|-----------|-----|---------|
| 1 | SEC filings (EDGAR) | Government-maintained, permanent | sec.gov/cgi-bin/browse-edgar |
| 2 | Company newsroom / press releases | Formal, rarely restructured | newsroom.cisco.com/... |
| 3 | arxiv papers | Permanent DOI-like IDs | arxiv.org/abs/2601.13671 |
| 4 | Major news outlets | Usually stable | securityweek.com/... |
| 5 | Company blog posts | **HIGH RISK** - restructure frequently | blogs.cisco.com/... |
| 6 | Original company domains | **HIGHEST RISK** - die after acquisitions | robustintelligence.com (dead) |

### Domains Die After Acquisitions

When a company is acquired, its original domain may go offline. This happened with:
- `robustintelligence.com` (acquired by Cisco, domain dead)
- Blog URLs at acquirer sites also break during restructuring (e.g., `blogs.cisco.com/security/cisco-acquires-robust-intelligence` returned 404)

**Rule:** When referencing an acquired company, use the acquirer's official announcement URL (newsroom or press release), not the acquired company's domain.

### Distinguishing 403 (Bot-Blocked) from 404 (Truly Broken)

Many sites block automated `curl` requests but work fine for human visitors in a browser:

| Status | Meaning | Action |
|--------|---------|--------|
| **200** | Working | No action needed |
| **301** | Redirect | Usually fine, follow the redirect to verify destination |
| **403** | Bot-blocked | **NOT a broken link.** OpenAI, Gartner, PitchBook, Crunchbase all return 403 to curl. Leave as-is. |
| **404** | Truly broken | **MUST fix.** Find a replacement URL or mark as dead. |
| **000** | Connection refused | Domain is dead (e.g., post-acquisition). Replace URL. |

### Reference Format

For Markdown source files that compile to LaTeX:

```
1. Author/Company. "Title." Source, Date. url.com/path (accessed Month Year).
```

Rules:
- No `https://` or `http://` prefixes in the markdown source
- The build script auto-detects URLs matching `https?://` and converts them to `\href{}` in LaTeX
- Escape underscores in URLs for LaTeX compatibility (handled by build script, but verify)
- Use "(accessed Month Year)" for web sources
- For arxiv papers, always append `arxiv.org/abs/XXXX.XXXXX` at the end
- For paywalled reports, use the public landing page URL even if content is gated

### Reference Completeness Checklist

Before finalizing, verify EVERY reference has:
- [ ] A URL (domain path, not just company name)
- [ ] Correct title in quotes
- [ ] Date or year
- [ ] "(accessed Month Year)" for web sources

Run this to find references missing URLs:
```bash
# Find references that are just "Company disclosures. domain.com" with no path
grep -n '^\d\+\.' YOUR_PAPER.md | grep -v 'arxiv.org\|\.com/\|\.dev/\|\.io/\|\.ai/\|\.html'
```

---

## Quality Checklists

### Pre-submission Checklist

- [ ] **AI language scan.** Read every sentence and flag AI-sounding phrases (see banned patterns above).
- [ ] **Redundancy scan.** For each claim, verify it appears only once. Search for key phrases to find duplicates.
- [ ] **Filler scan.** Identify paragraphs that do not add new information. Delete or merge.
- [ ] **Subsection audit.** Run line-count script. Merge any subsection with < 3 content paragraphs.
- [ ] **Cross-reference check.** After any renumbering, grep for all "Section X.Y" references and verify they point to the right place.
- [ ] **Reference completeness.** Every reference must have a URL. No exceptions (see Reference Integrity above).
- [ ] **URL verification.** Batch-check ALL URLs in one pass. Fix any that return 404 or 000. Ignore 403 (bot-blocked).
- [ ] **Hedge check.** Verify definitive claims use hedging language ("appears to," "seems to," "the data suggests") unless the claim is directly supported by verifiable data.
- [ ] **In-text citation check.** Verify that every reference listed in the Bibliography is cited in the body of the paper, and that no un-cited bibliography entries exist.
- [ ] **Chart text overlap check.** Verify that all generated chart images have clean layouts, with labels, titles, and legends not overlapping or clipping. Ensure no redundant titles exist inside chart images.
- [ ] **Table consistency check.** Verify that all tables have consistent text/font sizing (e.g., using `\footnotesize` consistently in LaTeX) and fit within margins/columns without overflow.
- [ ] **Build test.** Run `python3 build_tex.py && tectonic template.tex` and verify clean compilation with no errors.
- [ ] **Last-page check.** Open the PDF and verify the last page of references has a reasonable number of items (not just 2-3 orphans). If orphaned, see Bibliography Formatting below.
- [ ] **Copy to Desktop.** `cp template.pdf ~/Desktop/PAPER_NAME.pdf`

### Subsection Size Audit Script

```python
# Run from papers/ directory
import re
with open('YOUR_PAPER.md') as f:
    lines = f.readlines()
headings = []
for i, line in enumerate(lines):
    if line.startswith('#'):
        level = len(line.split()[0])
        headings.append((i+1, level, line.strip()))
for idx in range(len(headings)):
    start = headings[idx][0]
    end = headings[idx+1][0] if idx+1 < len(headings) else len(lines)
    non_empty = sum(1 for l in lines[start:end-1] if l.strip())
    indent = '  ' * (headings[idx][1] - 1)
    print(f'L{start:3d} {indent}{headings[idx][2]:60s} | {non_empty:2d} lines')
```

### Batch URL Verification Script

```bash
# Extract ALL domain URLs from the paper and check them in one pass
# Run from papers/ directory

echo "=== Checking all URLs ==="

# Extract URLs, add https:// if missing, batch check
cat YOUR_PAPER.md | tr ' ' '\n' | \
  grep -E '\.(com|dev|io|ai|co|tech|html)' | \
  grep -v '^\*\*' | grep -v '^_' | grep '\.' | \
  sed 's/[().,]$//g' | sort -u | while read url; do
  [[ "$url" != http* ]] && url="https://$url"
  code=$(curl -o /dev/null -s -w "%{http_code}" -L --max-time 10 "$url")
  if [ "$code" = "404" ] || [ "$code" = "000" ]; then
    echo "BROKEN  $code $url"
  elif [ "$code" = "403" ]; then
    echo "BOTBLK  $code $url"
  else
    echo "OK      $code $url"
  fi
done

echo ""
echo "=== Checking arxiv URLs ==="
grep -oE 'arxiv\.org/abs/[0-9.]+' YOUR_PAPER.md | sort -u | while read url; do
  code=$(curl -o /dev/null -s -w "%{http_code}" -L --max-time 10 "https://$url")
  echo "$code https://$url"
done
```

---

## Build Pipeline (Formal Academic Papers)

### Workflow

```
Markdown source → build_tex.py → template.tex → tectonic → template.pdf → Desktop copy
```

### Commands

```bash
cd papers/
python3 build_tex.py          # Generates template.tex from markdown
tectonic template.tex          # Compiles PDF
cp template.pdf ~/Desktop/PAPER_NAME.pdf   # Copy to Desktop
```

### What build_tex.py Does

The build script (`build_tex.py`) performs these transformations:

1. **Extracts sections** from the markdown: abstract, body, references
2. **Escapes LaTeX special characters**: `$`, `%`, `&`, `#` in running text; `_` in bibliography
3. **Converts citations**: `[XX]` → `\cite{refXX}`, `[XX, YY]` → `\cite{refXX,refYY}`
4. **Converts inline formatting**: `**bold**` → `\textbf{}`, `*italic*` → `\textit{}`
5. **Converts quotes**: straight quotes → LaTeX smart quotes (`` `` '' ``)
6. **Renders tables**: pipe-delimited markdown tables → `\begin{tabular}` with `\resizebox` for 3+ columns
7. **Builds bibliography**: numbered references → `\bibitem` entries with `\href{}` for URLs
8. **Inserts figures**: market map PDF inserted before Section 4

### Bibliography Formatting

The bibliography uses `\small` font (standard academic convention). This is set in `build_tex.py` line 244:

```python
return '\\small\n\\begin{thebibliography}{65}\n\\raggedright\n\n' + ...
```

**DO NOT use `\itemsep` or `\parsep` reduction** to fix spacing. This makes the references look cramped and inconsistent with the rest of the paper. The `\small` font is the correct approach - it reduces text size slightly while keeping normal line spacing.

**If references orphan onto a last page** (only 2-3 items on the final page):
1. First try `\small` font (already set) - this usually fixes it
2. If still orphaned, shorten the longest reference texts slightly (remove redundant words)
3. As a last resort, use `\footnotesize` instead of `\small`
4. **NEVER** use `\itemsep{0pt}` or `\parsep{0pt}` - it looks terrible

### LaTeX Template Structure

The generated `template.tex` uses:
- **Document class**: `article` with `iclr2024_conference` style
- **Key packages**: `hyperref`, `booktabs`, `graphicx`, `float`, `microtype`
- **`\raggedbottom`**: prevents LaTeX from stretching vertical space
- **`\iclrfinalcopy`**: camera-ready mode (no "Under review" header)
- **Tables**: `[H]` float positioning (exact placement)
- **`\clearpage`** before bibliography: forces references to start on a new page

### Known Issues

1. **Underscores in references.** The build script escapes underscores in bibliography text but must unescape them inside `\href{}` URLs. The `clean_url` function handles this. Verify the `.tex` output if URLs contain underscores.
2. **Citations inside tables.** The build script strips citations from table cells. Place all citations in the prose surrounding the table.
3. **Table floats.** LaTeX `[H]` positioning is used. If a table splits a paragraph awkwardly, adjust placement in the Markdown source by adding whitespace or restructuring.
4. **Figure placement.** Figure 1 (market map) is included as `market_map.pdf` and inserted before Section 4. Its placement is controlled by the build script, not LaTeX float logic.
5. **Long URLs in references.** Adding long URLs (e.g., Cisco Newsroom press releases) can push references to an extra page. The `\small` font compensates, but very long URLs may still cause orphaning.

---

## Paper Structure Template

For formal academic papers, use this section structure:

```
# Title

Author info

## Abstract
## 1. Introduction (includes Data and Methodology)
## 2. Related Work
## 3-6. Core Analysis Sections (varies by paper)
## N-1. Open Questions and Risks (includes Limitations)
## N. Conclusion
## References
```

### Section Guidelines

| Section | Purpose | Common mistakes |
|---------|---------|----------------|
| Abstract | Concrete findings with numbers | Too vague, no specific claims |
| Introduction | Problem, gap, contributions, methodology | Methodology buried or missing |
| Related Work | Position your paper relative to existing work | Just listing papers without connecting to your analysis |
| Core sections | Original analysis with data | Describing without analyzing |
| Open Questions | Unresolved tensions from the analysis | Random questions not connected to findings |
| Limitations | Honest constraints on the analysis | Restating methodology caveats already in Section 1 |
| Conclusion | Summary + forward-looking implications | Hedging without committing to any view |




## Lessons Learned

1. **The biggest integrity risk is fabricated URLs.** AI can generate plausible-looking URLs that don't exist. Verify every single one.
2. **Every reference must have a URL.** During the agent infrastructure stack paper, references 45-47 (McKinsey, Gartner, Deloitte reports), 59, 63, 64 (arxiv papers), and 68 (PitchBook) were all missing URLs. The user caught these. Even paywalled reports need their landing page URL.
3. **Domains die after acquisitions.** `robustintelligence.com` went offline after Cisco acquired the company. Always use the acquirer's press release URL, not the acquired company's domain.
4. **Blog URLs break during site restructuring.** `blogs.cisco.com/security/cisco-acquires-robust-intelligence` returned 404 months after publication. The Cisco Newsroom URL was stable. Prefer newsroom/press-release URLs over blog posts.
5. **403 is not 404.** OpenAI, Gartner, PitchBook, and Crunchbase all return 403 to automated curl requests but work fine in browsers. Do not "fix" these - they are bot-blocked, not broken.
6. **Check ALL URLs in one batch.** Do not check URLs piecemeal or claim "all links are fixed" without running the full batch verification script. The user will find the ones you missed.
7. **Bibliography spacing: use \small, never \itemsep.** Reducing `\itemsep`/`\parsep` makes the references look cramped compared to the body text. Using `\small` font is the standard academic convention and looks intentional.
8. **Redundancy creeps in across sessions.** When a paper is written over multiple sessions, the same point gets restated in different sections. Do a full-paper redundancy scan before finalizing.
9. **AI language is most visible in transitions and conclusions.** The phrases "It is worth noting," "The contrast is informative," and "This underscores" almost always signal AI-generated text.
10. **Thin subsections signal weak analysis.** If a subsection has only one paragraph, it either needs more depth or should be merged into a neighbor.
11. **Cross-references break after structural edits.** Always grep for "Section X" after merging or renumbering subsections.
12. **The "so what" test is the single best quality check.** Read each paragraph and ask: does this tell the reader something they could not infer from the data alone? If not, either add analysis or cut it.
13. **Always copy the final PDF to Desktop.** The user expects it at `~/Desktop/PAPER_NAME.pdf`. Rebuild and re-copy after every change.
14. **Rebuild after every markdown edit.** The PDF does not auto-update. Run `python3 build_tex.py && tectonic template.tex` after every change to the markdown source.
