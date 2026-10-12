# High Accuracy, Poor Transfer

**A Case Study of AI-Generated Abstract Detection**

- [Paper PDF](linguistic_markers_paper.pdf) · [Markdown](linguistic_markers_paper.md)
- [Methods supplement PDF](supplementary_methods.pdf) · [Markdown](SUPPLEMENTARY_METHODS.md)
- [Numerical reproduction package](results/defensibility_20261006/high_accuracy_poor_transfer_reproduction.zip)

The study audits a collection of 100,000 recorded published/generated abstract pairs. Eligibility retains 74,513 pairs, or 149,026 texts, in 73,886 related-record groups. The eight-feature forest reaches **95.99% internal accuracy**, but **53.89% external accuracy** and **11.73% external generated-text recall**. The paper reports the source checks, simpler baselines, fixed-threshold external evaluation and post hoc sensitivity analyses.

## Contents

The current paper and supplement are the PDFs linked above. Their four figures are in `results/full_verification_20261005/revision4/figures/`. The older `results/figures/`, `results/tables/` and `latex_build/` directories belong to the earlier analysis and are not the current results.

Measured features, group assignments, saved scores, audit summaries and scientific protocols are distributed in the reproduction ZIP. Numerical datasets are kept in that package rather than duplicated as separate large files in the checkout. The included SHA-256 manifest identifies its contents. Analysis, build and verification scripts are also available in `scripts/` for inspection.

## Reproduce the numerical results

Use **Python 3.13** with the recorded dependencies. Run these commands from this paper's directory in a Python environment:

```bash
python -m pip install -r requirements-corrected.txt
python scripts/reproduce_scores.py results/defensibility_20261006/high_accuracy_poor_transfer_reproduction.zip --refit
```

The checker verifies all **22 prediction sets**. The optional `--refit` step trains the main forest from the supplied features and compares its external scores with the saved predictions. Prediction CSVs use round-trip float parsing to preserve score ordering and ties.

For the additional threshold and diagnostic checks, extract the ZIP into a fresh directory and follow its `README_REPRODUCTION.md`. The extracted package supports `scripts/verify_defensibility.py` as well as the numerical checker.

Known-answer tests can run from this checkout:

```bash
python -m pytest scripts/test_corrected_analysis.py scripts/test_full_verification.py scripts/test_defensibility_checks.py scripts/test_score_precision.py -q
```

Set `PUNKT_ARCHIVE` to the pinned English Punkt archive to include the real-tokenizer test. Without it, that test is skipped. The resource revision, SHA-256, dictionaries, prompt templates and fold rule are recorded in the methods supplement.

## Build the PDFs

Install Pandoc and Tectonic, then run:

```bash
python scripts/build_corrected_paper.py
```

This builds the paper and the methods supplement from Markdown and the supplied figures. On macOS, `--desktop` also copies both PDFs to the Desktop. The compatibility entry point is `scripts/build_paper_tex.py`.

## Data and interpretation

The external corpus is [NicolaiSivesind/ChatGPT-Research-Abstracts](https://huggingface.co/datasets/NicolaiSivesind/ChatGPT-Research-Abstracts/tree/07857e2a97571ab553421ed645ef470bef6fa05c), pinned to revision `07857e2a97571ab553421ed645ef470bef6fa05c`.

The package supports numerical reproduction from measured features. Original local raw texts, provider generation logs, cached source responses and historical intermediate snapshots are not part of this release. Text extraction and full source-audit commands require those inputs. The protocols describe the complete original workflow, including its retrospective and post hoc stages.

Source-index matches do not authenticate every publisher record or authorship label. Intervals condition on the recorded labels and fitted-model predictions. Original per-output generation history and distribution terms for the local raw corpus remain unresolved. No new license for third-party text is asserted.
