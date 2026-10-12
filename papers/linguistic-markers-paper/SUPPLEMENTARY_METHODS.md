# Supplementary Methods for High Accuracy, Poor Transfer

## S1. Text processing

The feature extractor decodes HTML entities, applies Unicode NFKC normalization and collapses whitespace. It uses the following Python Unicode token pattern.

```text
[^\W\d_]+(?:['\u2019][^\W\d_]+)*
```

The pattern excludes decimal digits and underscores, retains internal straight or curly apostrophes, and splits hyphenated terms. Some Unicode numeric characters outside the decimal-digit class can match. Word counts therefore refer to this operational rule. Duplicate normalization applies case folding before extracting and joining these tokens. Source-file joins instead require exact stored published-text agreement, cleaned-title agreement and matching numeric years.

Sentence boundaries use the four English parameter tables from NLTK's `punkt_tab.zip`. Segments with no word tokens are omitted. The archive comes from `nltk/nltk_data`, revision

```text
550b6625bcef1f2abff2ff770a5a0d272c9c6b2a
```

Its SHA-256 is

```text
e57f64187974277726a3417ca6f181ec5403676c717672eef6a748a7b20e0106
```

MTLD uses `lexicalrichness` 0.4.1 with threshold 0.72. The input is the case-folded token sequence, with no additional library preprocessing. Forward and reverse passes are averaged, including partial factors for unfinished sequences. Failed, nonfinite or nonpositive values are rejected.

## S2. Word lists

These are the complete fixed dictionaries used by the extractor. Matches are counted per 1,000 word tokens. Connector matching scans within sentences and takes the longest available phrase once.

**Hedges.** `may`, `might`, `possibly`, `suggest`, `suggests`, `suggested`, `suggesting`, `appear`, `appears`, `appeared`, `appearing`, `seem`, `seems`, `seemed`, `seeming`, `maybe`, `perhaps`, `probable`, `probably`, `likely`, `unlikely`, `plausible`, `plausibly`, `tentative`, `tentatively`, `indicate`, `indicates`, `indicated`, `indicating`.

**Boosters.** `clearly`, `obviously`, `demonstrate`, `demonstrates`, `demonstrated`, `demonstrating`, `prove`, `proves`, `proved`, `proving`, `establish`, `establishes`, `established`, `establishing`, `definitely`, `show`, `shows`, `showed`, `showing`, `certainly`, `certain`, `undeniably`, `undeniable`, `always`, `never`, `evident`, `evidently`, `indeed`.

**Self-mentions.** `i`, `we`, `our`, `my`, `us`, `me`, `ours`.

Self-mention counting excludes all-uppercase tokens except `I`. Other dictionary matches use case-folded tokens.

**Connectors.** `however`, `nevertheless`, `nonetheless`, `conversely`, `instead`, `contrastingly`, `therefore`, `consequently`, `thus`, `hence`, `accordingly`, `as a result`, `furthermore`, `moreover`, `in addition`, `additionally`, `besides`, `also`.

The opener ratio counts sentences whose first counted tokens match a connector. Leading punctuation and decimal digits do not contribute word tokens.

## S3. Fold assignment and decision rules

Connected source records share a group identifier. Each group enters one of five folds using the following rule.

```python
from hashlib import sha256
key = sha256(("42:" + group_id).encode()).hexdigest()
fold = int(key[:16], 16) % 5
```

The fixed decision rule assigns the generated label when the model score is strictly greater than 0.5. Ties receive the published label. Source FPR-cap thresholds use NumPy's `higher` quantile method on published-class out-of-fold scores, at quantiles 0.99 and 0.95. These give empirical source caps under the strict comparison rule. The external oracle evaluates every distinct single-threshold decision, including constant predictions, using external labels.

## S4. Configured generation prompts

The archived OpenAI scripts specify `gpt-4o-mini`, temperature 0.7 and a maximum output of 400 tokens. The following strings document their two prompt variants. Title placeholders vary by source record. The paired files do not identify which variant produced each output.

### Variant A

**System message**

> You are a scientific researcher writing an academic abstract.

**User message**

> Write a realistic academic abstract (150-250 words) for a research paper titled: '[title]'. Write only the abstract text, no preamble.

### Variant B

**System message**

> You are an expert academic writer who writes clear, concise abstracts for scientific papers.

**User message**

> Write an academic abstract for the following research paper title. The abstract should be approximately 200-300 words, written in a formal academic style, and include the key elements: background, methods, results, and conclusion.
>
> Title: [title]
>
> Abstract:

These are configured inputs from code. Per-output provider responses, dates, model snapshots, prompt assignments and finish reasons are unavailable.

## S5. Versions and artifact locations

The external corpus is `NicolaiSivesind/ChatGPT-Research-Abstracts` at revision

```text
07857e2a97571ab553421ed645ef470bef6fa05c
```

The primary internal features, group assignments, predictions and summaries are in `results/full_verification_20261005/revision4/`. The frozen external files are in `results/full_verification_20261005/external/`. Source-consistent internal fits are in `results/full_verification_20261005/source_consistency_final/`. Post hoc thresholds, seed and length checks are in `results/defensibility_20261006/`; its `same_model/` directory contains the identical-fitted-model comparisons.

The external models were fitted using revision 3 features before the final local DOI-group repair. Revision 4 retains the same predictors and labels. The repair changes internal group/fold assignments, not the frozen external scores.

The numerical environment uses Python 3.13 and the versions in `requirements-corrected.txt`. The reproduction package includes a checker for all 22 saved prediction sets and an optional full-source forest refit. Prediction CSVs use round-trip float parsing to preserve score ties. The original fitting scripts' default feature parsing is retained when refitting. Original text extraction and provenance checks require the local source files and cached records beyond the feature/score package.
