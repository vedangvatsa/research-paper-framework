# A Review of Agentic Commerce

- [Main PDF](../agentic_commerce_paper.pdf)
- [Alternate IEEE-style PDF](../agentic_commerce_paper_ieee.pdf)
- [Markdown manuscript](../agentic_commerce_paper.md)
- [Source and evidence ledger](../agentic_commerce_paper_sources.md)
- [Claim audit](../agentic_commerce_fact_check.md)
- [Reviewer findings and responses](reviewer-response.md)
- [Research comparison matrix](literature-expansion/review-matrix.md)

Authors: Vedang Ratan Vatsa, Author2, and Author3. Website: [veda.ng](https://veda.ng).

## Build the main PDF

From the repository root, with Python 3 and Tectonic installed:

```sh
python3 papers/agentic-commerce/build_tex.py --compile
```

This produces `papers/agentic-commerce/template.tex`, `template.pdf`, and `template.log` using the included ICLR style. The Markdown file is the editable source for author names, the website link, prose, tables, and references.

The complete PDF/HTML build uses `node scripts/build_agentic_commerce.mjs --local-only` and also requires Pandoc, Playwright, and Chromium. An existing browser can be selected through `CHROMIUM_EXECUTABLE`.

## Audit records

The ledger, study matrix, search records, and retrieval manifests document the selected sources and their limits. The paper contains 15 research works among 40 references; this is a narrative review, not 15 independent experiments.

Downloaded third-party full texts and prior local PDF bundles form the working audit cache. Retrieval records identify their original URLs and hashes. The full `scripts/verify_agentic_commerce.py --local-only` check requires those cached source files as well as Poppler and the rebuilt PDF/log. `scripts/expand_agentic_review.py --source <key> <url>` retrieves an individual source; fresh downloads can differ from the dated files recorded in the audit.

The current validation report is `reports/agentic_commerce_validation_2026-10-13.json`. Build and document checks do not independently reproduce the research studies or validate their findings.
