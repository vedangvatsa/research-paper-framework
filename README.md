# Academic Research Paper Framework

A reusable framework for generating high-quality, human-authored academic papers suitable for SSRN and other academic repositories.

## Features
*   **Strict Stylistic Enforcement:** Prevents the use of AI jargon ("slop words"), em-dashes, and emojis, ensuring the output reads as a professionally written human document.
*   **Structured Templates:** Includes starting templates for `review_paper` and `empirical_study` to maintain structural consistency.
*   **Data Integrity Focus:** Encourages the use of tables for quantitative data and forbids hallucination in data representation.
*   **Automated PDF Generation:** Includes a script (`generate_pdf.sh`) to convert Markdown to a beautifully formatted PDF using Pandoc and Headless Chrome.

## Setup

1.  **Prerequisites:** You need `pandoc` and `Google Chrome` installed to generate PDFs.
    *   Mac: `brew install pandoc`
2.  **Make script executable:**
    ```bash
    chmod +x scripts/generate_pdf.sh
    ```

## Usage Workflow

1.  **Start a new paper:** 
    *   Ask the AI: "I want to write a new paper. Read the `AI_INSTRUCTIONS.md` file first."
    *   Choose a template from the `templates/` directory (e.g., Review Paper or Empirical Study) and copy it to a new file in the `papers/` directory.
2.  **Drafting:** 
    *   The AI will assist in drafting the paper based strictly on the rules in `AI_INSTRUCTIONS.md`.
3.  **Generating the PDF:**
    *   Run the script from the root of this repo:
    ```bash
    ./scripts/generate_pdf.sh papers/my_new_paper.md papers/my_new_paper.pdf
    ```

## Directory Structure

*   `AI_INSTRUCTIONS.md`: **Crucial.** This contains the prompt/rules the AI must follow. Point the AI here at the start of any session.
*   `templates/`: Markdown templates for different paper types.
*   `scripts/`: Automation scripts (e.g., PDF generation).
*   `papers/`: Your actual research papers go here.
*   `pdf-style.css`: The CSS rules that format the final PDF.
