# AI Assistant Guidelines for Academic Paper Generation

Whenever you are asked to write or assist in writing an academic research paper in this repository, you **MUST** strictly adhere to the following rules. These rules are designed to ensure the output is of high academic quality, human-authored in tone, and free of typical AI artifacts.

## 1. Stylistic and Vocabulary Constraints
*   **NO AI SLOP WORDS:** Do not use words typical of AI generation. This includes but is not limited to: *shift, implications, significant, striking, fundamental, furthermore, moreover, simultaneously, synthesize, noteworthy, notably, consequently, thus, hence, thereby, underscore, highlight, realm, emerged, emerging, landscape, paradigm, foster, facilitate, encompass, streamline, bolster, spearhead, reshape, redefine, reimagine, reconfigure*.
*   **NO EM-DASHES:** Do not use em-dashes (`—`) or en-dashes (`–`) for punctuation in sentences.
*   **NO COLONS IN PROSE:** Do not use colons (`:`) in running prose. Use periods or commas instead. (Colons are permitted in titles, section headers, and reference lists).
*   **NO EMOJIS:** The text must be strictly professional.
*   **SIMPLE LANGUAGE:** Use simple, plain, everyday English. Avoid overly complex, convoluted, or jargon-heavy academic phrasing where a simpler word works just as well. 
*   **ACTIVE VOICE:** Use active voice and declarative sentences.

## 2. Research and Data Integrity
*   **NO HALLUCINATIONS OR DATE BUMPING:** Never invent data, citations, or survey results. Never artificially bump publication years to make research seem "newer." All quantitative data, legal precedents, and source material must be fiercely fact-checked, factual, and verifiable.
*   **OPEN, PROBABILISTIC LANGUAGE:** When describing future trends, predictions, or market sizing, always use "open" words (e.g., *can, may, could, is likely to, is expected to, appears to*) instead of "closed" definitive words (e.g., *will, should, must, shall*). This ensures the analysis remains semantically accurate regardless of how the future unfolds.
*   **USE SYMBOLS FOR DATA:** Always use the `%` symbol instead of writing out "percent" or "per cent."
*   **NO AI SLOP:** You must strictly avoid cliché, AI-generated phrasing. Never use words or phrases like: "delve", "tapestry", "testament", "navigate/navigating", "landscape" (e.g., "regulatory landscape"), "multifaceted", "robust", "foster", "pivotal", "catalyst", "transformative", "revolutionize", "unprecedented", "realm", "seamless", "leverage", "empower", "unlock", "synergy", "democratize", "embark", "beacon", "underscores", "sheds light", "cautious optimism", "paradigm shift", "double-edged sword", "not merely X but Y", or using the word "shift" to describe changes in attitudes or data. Write with a precise, objective, human tone.
*   **NO END MARKERS:** Do not write "*End of paper.*" at the end of the document.
*   **CHART GENERATION:** Do not use AI image generators to create charts, as they hallucinate text and numbers. You MUST write a Python script (using matplotlib or seaborn) to generate charts based on accurate data, save them as `.png` files, and embed them in the markdown.
*   **USE TABLES:** When presenting numerical data, survey results, or comparisons, use Markdown tables to make the data scannable and clear.
*   **VERIFIABILITY:** Prioritize industry-standard data, university-led research, and verified sources over generalities.

## 3. Formatting and Output (IEEE Style)
*   **AUTHOR BLOCK:** The author section should only contain the author's full name and email address. Do not include the date.
*   **KEYWORDS:** Do not use a separate block at the top. Use the inline standard immediately below the Abstract: `_**Keywords**_: keyword1, keyword2, etc.`
*   **REFERENCES:** All URLs in the reference section must be properly formatted as clickable Markdown links (e.g., `[https://url.com](https://url.com)`). The references section must be left-aligned (not justified) to prevent ugly word-spacing gaps caused by long URLs.
*   **URL VERIFICATION:** Before committing any paper, run `./scripts/verify_references.sh papers/your_paper.md` to curl-check every reference URL. The script will flag any URL returning 404 or 5xx. Fix all broken URLs before committing. URLs returning 403 or 000 are acceptable (these are bot-blocked sites like McKinsey, Gartner, and Mastercard that work in browsers). Never fabricate a URL path. If the specific article URL cannot be verified, link to the publisher's root domain instead.
*   **MARKDOWN FIRST:** Write the paper in Markdown (`.md`), following the templates in the `templates/` directory.
*   **PDF CONVERSION:** The final output must be a well-formatted PDF suitable for submission to platforms like SSRN/IEEE. Use the provided CSS and scripts (e.g., `scripts/generate_pdf.sh`) to convert the markdown to PDF. Ensure `--no-pdf-header-footer` is used to prevent browser URLs from appearing on the printout.
*   **IMAGE SIZING:** Do not span images across columns using CSS `column-span`. Instead, ensure the `img` CSS rule has a strict `max-height` (e.g., `2.2in`) and `object-fit: contain` so images fit nicely inside a single column without forcing massive column breaks.

## 4. Paper Types
Before starting a new paper, ask the user what type of paper they want to write. You can refer to the templates:
*   `review_paper.md`: For synthesis, market analysis, or literature reviews.
*   `empirical_study.md`: For papers presenting original data, methodology, and results.
*   `computational_research.md`: For computational/ML research papers with method, experiments, baselines, and ablation studies (modeled after the [AI-Scientist](https://github.com/SakanaAI/AI-Scientist) structure).

For detailed per-section writing guidance (what to cover in each section, common pitfalls), refer to `SECTION_GUIDE.md`.

## 5. Pre-Submission Tools
Before finalizing any paper, use these automated tools:
*   **AI Peer Review:** `python scripts/review_paper.py papers/my_paper.md` — Get a structured academic review with scores, strengths, weaknesses, and accept/reject decision. Use `--ensemble 3` for a more reliable multi-reviewer assessment.
*   **Novelty Check:** `python scripts/check_novelty.py papers/my_paper.md` — Verify that your research angle is not already covered by searching Semantic Scholar or OpenAlex.
*   **Citation Finder:** `python scripts/find_citations.py papers/my_paper.md` — Identify missing citations and get suggestions for where to add them.
*   **URL Verification:** `./scripts/verify_references.sh papers/my_paper.md` — Check all reference URLs for 404s.
*   **PDF Generation:** `./scripts/generate_pdf.sh papers/my_paper.md papers/my_paper.pdf` — Generate the final PDF.
