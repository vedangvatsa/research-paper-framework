#!/bin/bash
# Compile script for the SaaS Erosion Deep Dive Report
cd "$(dirname "$0")"

echo "Compiling full report..."
cat chapters/*.md > full_saas_erosion_report.md

echo "Running reference verification..."
../../scripts/verify_references.sh full_saas_erosion_report.md

echo "Generating IEEE PDF..."
pandoc full_saas_erosion_report.md -o /tmp/temp_full_saas.html --standalone --metadata title="" -c ../../papers/pdf-style-ieee.css --embed-resources
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --headless --disable-gpu --no-sandbox --print-to-pdf="full_saas_erosion_report.pdf" --no-pdf-header-footer --no-margins /tmp/temp_full_saas.html

echo "Compilation complete: full_saas_erosion_report.pdf"
