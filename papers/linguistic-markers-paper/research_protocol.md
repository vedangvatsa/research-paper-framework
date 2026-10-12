# Research protocol: Language Patterns in AI vs Human Scientific Abstracts

## 1. Status and scope

This record follows [the research methodology guide](../../RESEARCH_METHODOLOGY.md). It records a retrospective correction of an existing study. It is not a preregistration.

This was the initial correction plan. The broader source audit, duplicate repair and external transfer test are documented in `full_verification_protocol.md`. `RESEARCH_STATUS.md` describes the final revision; the revision 2 audit below is retained as history.

- Responsible researcher listed in the manuscript is Vedang Ratan Vatsa.
- Protocol version is 1, dated 5 October 2026.
- Manuscript is `linguistic_markers_paper.md`.
- Study type is a descriptive corpus comparison with an exploratory classification evaluation. This design measures differences in a recovered dataset. It does not identify the causes of writing style or establish misconduct.
- Prior exposure includes the complete existing manuscript, reported group summaries, accuracy of 95.69%, reported feature importance, and existing analysis scripts. The original feature choices were already known before this correction.
- The initial public-repository review used commit `4681f29ae80006ca659e9f706c7148e98f537122`. The local working tree contains additional data and scripts that were not in that release.
- No registration or independent replication is claimed.

The primary question is whether eight defined text features distinguish the recovered published and generated abstracts when related source papers stay in one evaluation group. A prior question is whether the recovered files support the original corpus description and reported statistics.

The intended contribution is a traceable, corrected measurement in a specified corpus. Any claim about a particular generator depends on the available generation evidence. All claims about other models, prompts, fields, edited text, and current submissions require additional evidence.

## 2. Literature and gap record

The earlier review checked the cited primary papers and followed the relevant scientific-writing comparison literature on 5 October 2026. This is a targeted search, not a systematic review.

| Source and discovery route | Relevant evidence | Role in this study |
| --- | --- | --- |
| [Desaire et al., 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10328544/), related scientific-writing study | Small linguistic feature set, including sentence-length variation, with ordinary classifiers and document-level evaluation | Establishes that simple-feature detection of scientific writing is prior work. This study cannot claim that general idea as new. |
| [Gao et al., 2023](https://www.nature.com/articles/s41746-023-00819-6), scientific-abstract comparison | Title-based generated abstracts, detector tests, and blinded reviewer errors | Clarifies the narrower writing task and the need to report false alarms. |
| [Guo et al., 2023](https://arxiv.org/abs/2301.07597), existing reference | Question-answer corpus and linguistic comparisons | Background on corpus-specific differences, not evidence for an abstract-level MTLD result. |
| [McCarthy and Jarvis, 2010](https://link.springer.com/article/10.3758/BRM.42.2.381), existing reference | Validation of lexical-diversity measures in tested corpora | Supports MTLD as a text measure, not a universal guarantee against length effects. |
| [Liang et al., 2023](https://arxiv.org/abs/2304.02819), writer-background evaluation | Detection errors affecting non-native English writing | Motivates narrow use claims. No writer-language labels are available here. |

This correction is not intended to claim a new detector architecture. Review-specific screening and meta-analysis are not applicable because the paper reports an original corpus analysis.

## 3. Claims and evidence

| ID | Question and target quantity | Required evidence | Main rival explanation | Permitted scope |
| --- | --- | --- | --- | --- |
| C1 | What files, source records, and generation settings underlie the corpus? | File hashes, row counts, source-ID joins, exact script settings, available generation metadata | Early scripts or replaced metadata may not describe the final run | Distinguish what files establish from undocumented run history. |
| C2 | Which features differ within source-paper pairs? | Fresh feature extraction, paired differences, uncertainty, stated exclusions | Length, content, segmentation, or field differences | Descriptive differences in included records only. |
| C3 | How well do the features classify records from new source groups within this corpus? | Grouped evaluation, saved predictions, simple baselines, metrics and uncertainty | Related-text leakage and easy length cues | Retrospective internal evaluation, not independent replication. |
| C4 | How sensitive are results to length and feature choices? | Length-only and single-feature baselines, feature-removal conditions, common-length subset | Corpus construction explains most discrimination | Report the observed sensitivity, including weaker results. |

An unresolved generator identity or collection history limits C1 and any model-specific interpretation of C2-C4. Correct classification alone cannot resolve provenance.

## 4. Definitions and assumptions

The comparison unit is a source-paper pair. The source label describes the recorded text origin, not its factual quality. A pre-2022 publication date is a proxy for presumed-human writing, not direct verification of authorship. MTLD measures diversity in a text, not the size of an author's vocabulary. Word-list counts measure matches, not validated psychological traits.

The classifier receives only the specified numeric features. Source IDs, titles, labels, fold assignments, and publication years are excluded from predictors.

| Assumption | Check | Consequence if unresolved |
| --- | --- | --- |
| The paired records match real source papers | Join by authentic work ID, compare titles, years and source text, inspect records | State the source as recorded rather than independently certified. |
| The recorded generated class came from the stated process | Inspect final scripts and any request-level logs; do not infer execution from a filename | Attribute settings to the script; do not invent a generation date or version. |
| Segmentation measures the intended feature | Test abbreviations, decimals, multiword connectors, and sample real texts | Describe measurement errors and avoid mechanism claims. |
| Related records do not cross evaluation groups | Assert disjoint IDs and normalized title/text groups | Correct groups before reporting metrics. |

There is no formal or causal claim requiring a mathematical proof. The data cannot identify cognitive mechanisms, training objectives, or effects of human-feedback training.

## 5. Decision log before corrected analysis

| Decision | Rationale and alternatives | Sensitivity or revision rule |
| --- | --- | --- |
| Preserve all original data and write corrected outputs separately | Raw evidence and earlier results must remain inspectable | Never overwrite source CSVs or silently replace historical summaries. |
| Audit the recovered files before using the old headline figures | Public files were incomplete and cannot settle provenance | Withdraw or qualify claims that do not trace to recovered records. |
| Retain the eight feature concepts | Avoid selecting new features after seeing a favorable result | Compare simpler subsets and length-only features. |
| Use at least 100 counted words in each included text | Implements the stated eligibility rule and limits extremely short-text instability | Record exclusions and compare lengths; no claim that this threshold removes length effects. |
| Use a documented sentence tokenizer that handles common abbreviations and decimals | The historical punctuation split can fragment scientific numbers | Test against explicit examples and inspect real-text cases. |
| Preserve pairs and group repeated source IDs, normalized titles and exact text matches | Row-level stratification is insufficient for new-source claims | Fail the evaluation if an exact related-text group crosses folds. Near-duplicate limits remain explicit. |
| Fix splits and classifier settings before inspecting corrected scores | Avoid tuning to corrected evaluation outcomes | Any later change is recorded as exploratory. |
| Compare random forest with logistic regression, MTLD-only, sentence-variation-only and length-only models | Tests whether the complete feature set adds useful information | Report all comparisons, even if simpler models perform as well. |
| Use pair-level uncertainty for descriptive differences | Texts in a pair are related observations | State the resampling unit and assumptions; do not treat fold SD as a confidence interval. |

The existing sample size is a recovered-data constraint, not a prospective power calculation. No new paid generation or large-scale collection is part of this correction.

## 6. Design and analysis plan

E1 audits raw files and recreates the historical eligibility rule solely to test whether the saved summaries can be traced to the recovered data. It records row counts, duplicates, year ranges, missing values, title and ID matches, hashes, and the content of relevant configuration fields. It does not execute collection or generation scripts.

E2 extracts corrected features from eligible pairs. Sentence boundaries use the English Punkt parameter tables from NLTK data revision `550b6625bcef1f2abff2ff770a5a0d272c9c6b2a`. The archive hash is recorded. Unicode letter sequences, with internal apostrophes, define words. Full processing details, package versions, dictionaries, and failure counts are written with the outputs. Phrase matches use complete token sequences. Uppercase abbreviations are not treated as personal pronouns, except `I`, whose contextual ambiguity remains. Feature failures are reported, not encoded as valid zeros. Texts with fewer than two recognized sentences are excluded from the primary eight-feature comparison and counted.

E3 uses five fixed source-group folds, a 100-tree random forest with seed 42, and prespecified simpler baselines. A group's fold is the first 16 hexadecimal digits of SHA-256 applied to `42:` followed by its group ID, converted to an integer modulo five. Every evaluated text receives one out-of-fold prediction. The analysis records group overlap assertions. These folds are a retrospective internal check because the original data and results have already been examined; none is called an untouched confirmatory test set.

E4 examines length effects using the length-only baseline and a common-length restriction of 150-250 counted words in both texts of a pair. The restricted model is trained and evaluated within that subset using the same group assignments. The eight-feature forest is also compared with a forest omitting MTLD. These choices were fixed before reading corrected performance. Any additional diagnostics are marked exploratory. Testing new prompts, new generators, edited text, or prospective submissions is outside the available dataset.

## 7. Outcomes and recording

Primary descriptive outcomes are within-pair feature differences with 95% intervals. Report both class summaries and paired differences. Multiple feature tests, if reported, use Holm adjustment across the eight features. Practical interpretation relies on effect sizes and intervals rather than a small p-value alone.

Classification outcomes include accuracy, AI-class precision, recall, F1, ROC AUC, average precision, human false-positive rate, specificity, and the confusion matrix. The default decision threshold is fixed at 0.5 and its tie convention is recorded. Uncertainty refers to the specified resampling procedure, not to unknown deployment settings. Report fold spread as fold spread.

Artifacts retain source/group IDs, text hashes, labels, features, fold assignments, predictions, model settings, package versions, timestamps, exclusions, and input hashes. Raw text stays local unless a documented distribution route is established. No monetary value is attached to these outcomes.

## 8. Reproducibility and validity

Analysis code and exact commands are recorded in the paper-specific README and result manifest. Known-answer tests cover feature extraction, grouping, exclusions, and metric arithmetic. Historical summary reproduction is kept separate from scientific validity. Validity limits include unknown sampling history, title-only generation, unrecorded model snapshots, unmeasured field effects, possible training-data exposure, and author-background differences.

## 9. Deviations and open questions

The initial recovered-file audit preceded corrected feature extraction. It verified 100,000 source rows, 100,000 paired rows and 200,000 stored feature rows, with all 32 reported class means and SDs matching the stored feature table to four decimal places. It also found 10 short source IDs, 19 missing source titles, 37 unequal stored titles, 23,856 published texts shorter than 100 words under the historical ASCII word rule, and 557 zero MTLD values. These are audit observations, not corrected-model results.

Eligibility was clarified after this audit but before corrected prediction scores were calculated. Exclude invalid IDs, missing source titles, title/text/year disagreement across the paired and source files, normalized duplicates and cross-class exact copies. One observed source record, `W1979290264`, pairs the title of Braun and Clarke's 2006 methods paper with an abstract about an Indigenous language-learning study. Exclude that record and record the reason. The audit cannot establish that every remaining source abstract matches its publisher record. No universal source-quality claim is made.

The recovered generation code contains at least two prompt variants, including explicit requested lengths and academic-style instructions. Per-output prompt assignments and response dates are not retained. The earlier single-neutral-prompt and October 2024 claims cannot be retained as verified facts.

An implementation error in the first correction run treated work IDs with fewer than seven digits as invalid. Direct checks of `https://api.openalex.org/works/W852874` and `https://api.openalex.org/works/W226145` on 5 October 2026 show that short numeric IDs can be real OpenAlex records. Remove the minimum-digit assumption. The first corrected scores had been seen at this point. This revision is required by identifier validity, not by model performance. Preserve that run as an audit trail and use only `results/correction_20261005/revision2/` for the revised manuscript. Regenerate the file audit as `source_audit_v2.json`. Identifier syntax still does not verify every source's content or language.

| ID | Open question | Consequence and next step |
| --- | --- | --- |
| Q1 | Which source-collection scripts produced the final records? | Inspect source files and recover logs; avoid a representative-random-sample claim without support. |
| Q2 | Can the generator, model snapshot, and dates be verified per output? | Inspect records; qualify or remove unsupported version/date statements. |
| Q3 | Do the recovered features and raw texts reproduce the historical tables? | Run a read-only audit before replacing any result. |
| Q4 | Does discrimination persist after grouped evaluation and length controls? | Run E2-E4 and report the outcome without retaining old headline figures by assumption. |
| Q5 | Can the corpus be shared or reconstructed under its source terms? | Document a data-access route before a reproducibility claim. |

## 10. Evidence audit at revision 2, retained as history

| Claim | Actual finding | Evidence | Permitted interpretation |
| --- | --- | --- | --- |
| C1 | 100,000 recovered pairs and 200,000 historical feature rows; all reported means and SDs reproduced from the historical feature file | `results/correction_20261005/source_audit_v2.json` | File consistency is supported. Sampling history and per-output generation attribution remain incomplete. |
| C2 | Corrected eligibility retains 74,513 pairs in 74,105 groups. MTLD differs by 42.20 units, with a group-bootstrap interval of 41.93 to 42.45. Sentence CV differs by -0.189, with an interval of -0.191 to -0.188. | `revision2/features.csv.gz`, `feature_comparisons.csv`, `exclusions.csv`, and input hashes | Descriptive differences in stored labels and the stated subset, not causes of writing style. |
| C3 | Eight-feature forest accuracy is 95.98%, with conditional interval 95.88%-96.08%; false-positive rate is 3.60%. Seven model conditions completed. | `revision2/evaluation.json`, saved per-text predictions and `verification.json` | Retrospective internal performance. No independent prospective or external validation. |
| C4 | Length-only accuracy is 90.37%. The 150-250-word subset contains 34,873 pairs and has 94.82% accuracy. | `revision2/metrics_forest_length.json`, `metrics_forest_common_length.json` | Construction choices provide predictive information. The restricted-range comparison is not exact length matching or a causal decomposition. |

`revision2/` in this table is relative to `results/correction_20261005/`. Source hashes are unchanged. Group assignments and all seven sets of predictions were checked against the manifest. Descriptive summaries and manuscript tables were independently recalculated. The intervals resample fixed predictions, not newly trained models. No inferential p-values are reported; feature intervals are marginal descriptive intervals rather than simultaneous coverage.

The strongest remaining objection is that the recovered labels, source fields and generation conditions are not independently verified in full. The manuscript therefore uses a presumed-human published class and limits every result to this corpus. Unknown sampling, language labels, near-duplicates, source errors, training-data exposure and prompt assignment remain possible explanations. A public data-access route is also missing.

The argument now connects the source audit, explicit questions, eligibility, paired measurements, source-group evaluation, length controls, and a bounded conclusion. `RESEARCH_STATUS.md` records the review findings and publication blockers. Automated checks are aids to that argument, not evidence of universal correctness.

## 11. Final follow-up outcome

Revision 4 retains 74,513 pairs and joins confirmed near-duplicates and shared identifiers into 73,886 groups. Its internal forest accuracy is 95.99%, with a conditional interval of 95.89%-96.09%, and its false-positive rate is 3.60%. Length-only accuracy is 90.38%.

All 100,000 original IDs were checked. DOI fallback brought current-record retrieval to 98,907, leaving 1,093 unresolved. The source-consistent sensitivity uses 56,355 pairs and gives 95.92% forest accuracy. These are same-index consistency checks, not independent authentication of every publisher or author.

The external test retains 8,319 pairs after overlap and eligibility checks. The frozen forest reaches 53.89% accuracy, 11.73% generated-text recall and AUC 0.7296. Logistic regression reaches 68.91% accuracy. The external predictions were not retuned after inspection. Their predictors and training labels are unchanged by the final internal grouping repair.

The conclusion is now a bounded negative transfer result alongside high internal discrimination. The original claim of general reliable authorship detection is not supported. Generation logs, complete source authenticity, sampling probabilities and public release of the local corpus remain unresolved. The final evidence is under `results/full_verification_20261005/`, with `revision4/` as the main internal run.
