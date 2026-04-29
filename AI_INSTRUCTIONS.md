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
*   **IMAGE DATA:** Do not generate images containing text or numbers that might hallucinate data. Rely on data tables for quantitative information instead.
*   **USE TABLES:** When presenting numerical data, survey results, or comparisons, use Markdown tables to make the data scannable and clear.
*   **VERIFIABILITY:** Prioritize industry-standard data, university-led research, and verified sources over generalities.

## 3. Formatting and Output
*   **MARKDOWN FIRST:** Write the paper in Markdown (`.md`), following the templates in the `templates/` directory.
*   **PDF CONVERSION:** The final output must be a well-formatted PDF suitable for submission to platforms like SSRN. Use the provided CSS and scripts (e.g., `scripts/generate_pdf.sh`) to convert the markdown to PDF.
*   **URL REFERENCES:** All references in the bibliography must include a URL where applicable.

## 4. Paper Types
Before starting a new paper, ask the user what type of paper they want to write. You can refer to the templates:
*   `review_paper.md`: For synthesis, market analysis, or literature reviews.
*   `empirical_study.md`: For papers presenting original data, methodology, and results.
