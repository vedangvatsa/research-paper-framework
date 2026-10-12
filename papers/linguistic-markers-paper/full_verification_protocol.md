# Full verification follow-up

## Status and prior exposure

Recorded on 5 October 2026 after the revision 2 internal results were known. This is a prospective plan for additional checks within a retrospective correction, not a preregistration. The earlier protocol and original files remain preserved.

The goal is to check the remaining source, generation-history, measurement and transfer claims. No finite check can establish every possible factual or causal claim. Each check below records coverage, failures and the narrower conclusion it supports.

## A. Source records

Attempt to retrieve all 100,000 original source IDs from the current OpenAlex API, prioritizing the 74,513 retained pairs. Save the request IDs, timestamps, selected response fields, response hashes and errors. Compare IDs, titles, DOIs, years and abstract text. Record current language, work type, source type, retraction status, subject and citation count. A current index match is not independent verification against every publisher or proof of human authorship.

Use documented batches of at most 100 IDs. Respect service limits and cache responses. Single-entity lookups are explicitly free under OpenAlex's published pricing and can resolve missing or merged IDs. No paid balance, embedded credential or alternate network identity is used. A refused request remains unresolved rather than being treated as a mismatch.

Report exact text agreement after Unicode, HTML and whitespace normalization separately from word-level similarity. Changes in a live index can reflect correction or record merging, so a difference is not automatically an error in the older file. Inspect examples before interpreting disagreement.

A source-consistent sensitivity set requires agreement on normalized title and year, an exactly matching normalized abstract, current English language, an article type and no recorded retraction. This is a conservative same-index consistency check. It does not authenticate every publisher record. Refit the unchanged eight-feature and length-only models using the original group folds on that subset, without retuning. Report all resulting scores.

## B. Generation provenance

Inspect all generation scripts and available study files for response identifiers, timestamps, returned model names, finish reasons, prompt assignments and preservation of full responses. Inventory schemas and record whether a fact is configured, observed per record, or unavailable. Compare backup/generated files to identify unchanged records where possible. Do not derive an API generation date from a filesystem modification date. Do not use credentials found in old scripts or rerun generation.

## C. Text quality and related records

Check every retained text for deterministic quality indicators, including markup, URLs, unusual length and script composition. Retrieve source-language labels through A. Apply a fixed language detector only as a diagnostic, not as certain ground truth.

Search for approximate duplicated published text with word five-gram MinHash, 128 permutations, an LSH candidate threshold of 0.8 and exact candidate Jaccard confirmation of at least 0.85. Record detection settings and the fact that this candidate search is not exhaustive. Identify any confirmed pairs whose original folds differ. Do not claim that filtering old predictions repairs their earlier training exposure.

The first published-text pass found 521 confirmed near-duplicate links, including 362 crossing revision 2 folds. This triggers a correction before the external test is scored. Extend the same fixed comparison rule to all retained texts in both classes, merge source groups connected by any confirmed link, and refit all seven internal model conditions. Keep every measured feature value and label unchanged. Store the repaired evaluation as `results/full_verification_20261005/revision3/`; preserve revision 2. Repeat the source-consistent sensitivity with these repaired groups. No threshold or feature is selected using the new scores.

## D. External transfer evaluation

Use the public `NicolaiSivesind/ChatGPT-Research-Abstracts` dataset, revision `07857e2a97571ab553421ed645ef470bef6fa05c`, if its paired CSV and labels are usable. Its author-supplied card describes 10,000 abstracts per class, GPT-3.5-turbo-0301 generation, title-based prompts and requested word counts equal to the source abstracts. The card does not establish every source's authenticity or a complete request log. Preserve that limit and do not redistribute the corpus under an invented license.

Freeze the existing feature extraction, eligibility, seed, model settings and decision threshold. Train the eight-feature forest, length-only forest and eight-feature logistic regression on the complete revision 2 training corpus. Do not tune any model on external results. Exclude entire external pairs with missing text, fewer than 100 counted words, fewer than two sentences, feature failures, normalized duplicate text, or title/text overlap with any original local pair. Check approximate text overlap as well when identifiers are absent. Save all exclusion reasons.

Score the remaining external pairs once. Report class counts, confusion matrices, accuracy, precision, recall, F1, false-positive rate, ROC AUC and average precision. Bootstrap external source groups for conditional intervals without refitting. Report the result even if performance is poor. This tests transfer to one independently assembled public corpus, not a prospective real-world deployment or proof of a universal marker.

## E. Final claim audit

Update the manuscript only from completed checks. Record which statements are verified within scope, contradicted, qualified or still unknown. Preserve revision 2 numbers as earlier internal results if new source audits narrow their interpretation. Publication readiness requires a defensible data-access route, truthful generation attribution and claims consistent with all completed tests. Missing records are not filled with assumptions presented as facts.

## Additional identifier resolution and final grouping

After the first source and external checks, all 85 unresolved source IDs with a usable stored DOI were queried through OpenAlex's documented DOI singleton endpoint. Ten additional records were recovered. The original ID-only audit is preserved separately from `source_checks_resolved.csv.gz` and `source_summary_resolved.json`.

A further identity check found one pair of source records sharing a valid DOI but crossing revision 3 folds. Bare resolver URLs such as `https://doi.org/` are not valid DOI identities and were excluded from this grouping check. All valid stored/current DOI and current canonical-ID links are added to the grouping graph, and all internal conditions are refitted in `revision4/`. This is a correction of a known dependence, not model tuning. The external predictions remain frozen. Their revision 3 training predictors and labels are identical to the final revision 4 predictors and labels; only internal group/fold metadata changes.

## Completed evidence audit

| Claim | Evidence obtained | Final scope |
| --- | --- | --- |
| Source records can be checked | All 100,000 attempted; 98,907 retrieved after DOI fallback; 1,093 unresolved | Current OpenAlex coverage and agreement, not complete publisher authentication |
| Local feature results persist with stricter grouping | All 521 confirmed near-duplicate links and five recorded identity links remain inside final folds; 95.99% forest accuracy | Internal evaluation of stored labels |
| A cleaner same-index subset supports local separation | 56,355 source-consistent pairs; forest accuracy 95.92%; length-only 90.26% | Sensitivity to the declared consistency rules |
| High internal accuracy transfers without tuning | External accuracy 53.89%, recall 11.73%, AUC 0.7296 for the forest | This proposed broad claim is contradicted in the tested external corpus |
| Simpler models have the same relative ranking externally | Logistic regression reaches 68.91%, above the forest's external score despite lower internal accuracy | The internal model ranking does not carry over to this test |
| Per-output generation details can be recovered | Five scripts and seven metadata files contain no saved request-level fields | Exact attribution and dates remain unestablished |

The recorded external exclusions total 1,681 pairs, leaving 8,319. Raw-to-feature text hashes verify the class mapping for all 16,638 evaluated texts. Conditional intervals resample the declared source groups with predictions fixed; they do not resolve uncertainty about labels, unknown sampling or other deployment conditions.

Known-answer tests, accounting checks, numerical reproduction, source-cache linkage, reference checks and PDF inspection support the narrower manuscript. They do not substitute for missing generation records, a public data-access route or independent human peer review.
