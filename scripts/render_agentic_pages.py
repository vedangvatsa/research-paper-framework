#!/usr/bin/env python3
"""Render the review's inspection pages using captions rather than fixed page numbers."""

import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / 'papers/agentic_commerce_paper.pdf'
ALTERNATE = ROOT / 'papers/agentic_commerce_paper_ieee.pdf'


def pages(pdf):
    text = subprocess.check_output(['pdftotext', '-layout', str(pdf), '-'], text=True)
    return [page for page in text.split('\f') if page.strip()]


def matching_page(text_pages, predicate):
    matches = [number for number, text in enumerate(text_pages, 1) if predicate(text)]
    if len(matches) != 1:
        raise ValueError(f'Expected one matching page, found {matches}')
    return matches[0]


def main():
    native_pages = pages(MAIN)
    alternate_pages = pages(ALTERNATE)
    targets = [('first-page', MAIN, 1)]
    for name, number in [('protocol-table', 2), ('study-comparison', 5), ('security-table', 6)]:
        pattern = re.compile(rf'^\s*Table {number}:', re.M)
        targets.append((name, MAIN, matching_page(native_pages, pattern.search)))
    conclusion_page = matching_page(native_pages, lambda text: any(
        re.sub('[^a-z]', '', line.lower()) == 'conclusion' for line in text.splitlines()
    ))
    targets.extend([
        ('conclusion', MAIN, conclusion_page),
        ('main-references', MAIN, len(native_pages)),
        ('ieee-references', ALTERNATE, len(alternate_pages)),
    ])
    for name, pdf, page in targets:
        destination = ROOT / 'reports' / f'agentic-commerce-{name}'
        subprocess.run([
            'pdftoppm', '-f', str(page), '-l', str(page), '-scale-to', '1500',
            '-png', '-singlefile', str(pdf), str(destination),
        ], check=True)
        print(json.dumps({'image': f'{destination.relative_to(ROOT)}.png', 'pdf': str(pdf.relative_to(ROOT)), 'page': page}))


if __name__ == '__main__':
    main()
