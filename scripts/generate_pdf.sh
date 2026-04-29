#!/bin/bash

# A simple script to convert a markdown paper into an SSRN-ready PDF using Pandoc and Google Chrome headless.

if [ "$#" -ne 2 ]; then
    echo "Usage: ./generate_pdf.sh <input_markdown_file> <output_pdf_file>"
    echo "Example: ./generate_pdf.sh ../papers/my_paper.md ../papers/my_paper.pdf"
    exit 1
fi

INPUT_FILE=$1
OUTPUT_FILE=$2
TEMP_HTML="/tmp/temp_paper.html"
CSS_FILE="$(dirname "$0")/../pdf-style.css"

echo "Step 1: Converting Markdown to HTML using Pandoc..."
pandoc "$INPUT_FILE" -o "$TEMP_HTML" --standalone --metadata title="" -c "$CSS_FILE" --embed-resources

if [ $? -ne 0 ]; then
    echo "Error: Pandoc conversion failed. Is Pandoc installed? (brew install pandoc)"
    exit 1
fi

echo "Step 2: Converting HTML to PDF using Headless Chrome..."
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --headless --disable-gpu --no-sandbox --print-to-pdf="$OUTPUT_FILE" --no-margins "$TEMP_HTML"

if [ $? -ne 0 ]; then
    echo "Error: Chrome PDF generation failed."
    exit 1
fi

echo "Success! PDF generated at: $OUTPUT_FILE"
rm "$TEMP_HTML"
