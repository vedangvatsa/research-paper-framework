# Reviewer-objection analysis plan

## Status

This plan follows the completed source audit and revision 4 evaluation. Internal accuracy of 95.99% and external accuracy of 53.89% were already known. The additional analyses below are post hoc diagnostics, not preregistered confirmation or a new untouched test. Their definitions are recorded before computing their new results. Original predictions and result files remain unchanged.

The intended paper is **High Accuracy, Poor Transfer: A Case Study of AI-Generated Abstract Detection**. Its primary quantity is the performance of specified frozen procedures under the recorded labels in two corpora. It does not estimate the prevalence of AI writing, the best achievable detector, or a causal effect of model generation.

## Questions and fixed checks

| ID | Reviewer question | Check and rationale | Limits and possible outcome |
| --- | --- | --- | --- |
| D1 | Is the external failure only an arbitrary threshold choice? | Preserve 0.5. Also choose thresholds using the source out-of-fold scores only: maximum balanced accuracy and at most 1% or 5% empirical false positives. Apply each threshold to the existing external scores. | Out-of-fold threshold selection is a source-based diagnostic, not independent calibration of the final fitted model. Target error rates are not guaranteed. Improvement or lack of improvement is reported. |
| D2 | Could a different threshold recover the internal score? | Calculate the best balanced accuracy over all thresholds on the observed external scores. | This uses external labels and is an optimistic, test-label oracle within a threshold-rule family. It is not a deployment score, population bound or validated selection procedure. |
| D3 | Is logistic regression better only because it tolerates more false alarms? | Report paired differences in accuracy, recall, false-positive rate and ROC AUC on the same external texts; add empirical ROC recall at FPR no more than 1% and 5%. | Matched-FPR points use test labels and describe the score curves. They are not independently calibrated operating thresholds. |
| D4 | Does the result depend on one random seed? | Refit the eight-feature forest on identical local predictors with seeds 7, 42 and 2026. Reproduce seed 42 against saved external scores, then report every seed. | These are repeated fits on the same corpora, not independent dataset replications. No best seed is selected. |
| D5 | Would better source records restore transfer? | Fit the same forest and logistic regression to all 56,355 source-consistent pairs and score the original eligible external set. | The source filter is the earlier fixed rule. It does not authenticate labels or isolate a causal effect of source quality. These are exploratory retraining checks. |
| D6 | Is the gap only due to very different lengths? | Evaluate the existing full-procedure predictions within paired 150-250-word and 100-500-word restrictions, separately in each corpus. | This restricts support but does not exactly match distributions. It differs from the earlier common-length model refitted only within that range. |
| D7 | Are external observations duplicated or dependent? | Apply the same 128-permutation, seed-42 five-gram MinHash candidate search with 0.8 candidate and 0.85 exact-Jaccard thresholds within all retained external texts. Merge connected source-pair groups. | Candidate search is not exhaustive. Labels and frozen scores do not change. Any new groups are used for supplementary uncertainty estimates. |

## Uncertainty and comparisons

Use 1,000 source-group bootstrap draws with seed 42. For paired comparisons, resample the same external groups for both models. Report percentile intervals conditional on the recorded labels and fixed predictions. For the internal accuracy comparison, use the repaired revision 4 groups. Do not infer statistical equality from overlapping intervals, and do not describe a point estimate near 50% as equivalence to chance. The balanced constant-class baseline is exactly 50% accuracy under these class counts.

Class 1 remains the dataset's generated label. Predictions use score strictly greater than the threshold. Ties therefore receive class 0. Threshold searches include the all-negative and all-positive rules and keep tied scores together. If several rules tie, choose the largest threshold. A source-FPR threshold is the higher empirical quantile of source class-0 scores; strict comparison keeps the source empirical FPR within the target.

## Claim discipline

The analysis can support statements about fixed-rule transfer, ranking differences, specified length ranges, random-seed variation, and the selected source-consistency filter. It cannot establish that all detectors fail, that a generator version caused the gap, that lexical variety is a property unique to machine writing, or that a flagged author violated a rule.

Missing request logs, unresolved source records and the absence of a public local-data release remain explicit. No wording change is treated as a substitute for those records. The contribution is an auditable case study and its controls, not discovery that distributional generalization is a new problem.

## Outputs

Save new evidence under `results/defensibility_20261006/`. Preserve the current manuscript, PDF and status documents before editing. Store all new scores, thresholds, subsets, group assignments, input hashes and package versions. Include a reviewer-question record linking each answer to a section and artifact. Only completed results enter the manuscript.
