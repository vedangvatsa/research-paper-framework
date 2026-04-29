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
*   **NO HALLUCINATIONS:** Never invent data, citations, or survey results. All quantitative data, legal precedents, and source material must be factual and verifiable.
*   **NO AI SLOP:** You must strictly avoid cliché, AI-generated phrasing. Never use words or phrases like: "delve", "tapestry", "testament", "navigate/navigating", "landscape" (e.g., "regulatory landscape"), "multifaceted", "robust", "foster", "pivotal", "catalyst", "transformative", "revolutionize", "unprecedented", "realm", "seamless", "leverage", "empower", "unlock", "synergy", "democratize", "embark", "beacon", "underscores", "sheds light", "cautious optimism", "paradigm shift", "double-edged sword", "not merely X but Y", or using the word "shift" to describe changes in attitudes or data. Write with a precise, objective, human tone.
*   **NO END MARKERS:** Do not write "*End of paper.*" at the end of the document.
*   **CHART GENERATION:** Do not use AI image generators to create charts, as they hallucinate text and numbers. You MUST write a Python script (using matplotlib or seaborn) to generate charts based on accurate data, save them as `.png` files, and embed them in the markdown.
*   **USE TABLES:** When presenting numerical data, survey results, or comparisons, use Markdown tables to make the data scannable and clear.
*   **VERIFIABILITY:** Prioritize industry-standard data, university-led research, and verified sources over generalities.

## 3. Formatting and Output (IEEE Style)
*   **AUTHOR BLOCK:** The author section should only contain the author's full name and email address. Do not include the date.
*   **KEYWORDS:** Do not use a separate block at the top. Use the inline standard immediately below the Abstract: `_**Keywords**_: keyword1, keyword2, etc.`
*   **REFERENCES:** All URLs in the reference section must be properly formatted as clickable Markdown links (e.g., `[https://url.com](https://url.com)`). The references section must be left-aligned (not justified) to prevent ugly word-spacing gaps caused by long URLs.
*   **MARKDOWN FIRST:** Write the paper in Markdown (`.md`), following the templates in the `templates/` directory.
*   **PDF CONVERSION:** The final output must be a well-formatted PDF suitable for submission to platforms like SSRN/IEEE. Use the provided CSS and scripts (e.g., `scripts/generate_pdf.sh`) to convert the markdown to PDF. Ensure `--no-pdf-header-footer` is used to prevent browser URLs from appearing on the printout.
*   **IMAGE SIZING:** Do not span images across columns using CSS `column-span`. Instead, ensure the `img` CSS rule has a strict `max-height` (e.g., `2.2in`) and `object-fit: contain` so images fit nicely inside a single column without forcing massive column breaks.

## 4. Paper Types
Before starting a new paper, ask the user what type of paper they want to write. You can refer to the templates:
*   `review_paper.md`: For synthesis, market analysis, or literature reviews.
*   `empirical_study.md`: For papers presenting original data, methodology, and results.
