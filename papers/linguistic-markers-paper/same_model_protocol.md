# Same-fitted-model transfer check

This is an additional post hoc check after the primary external results and the D1-D7 diagnostics were known. It addresses a separate question about comparability. The primary report compares source cross-validation with a final model fitted to all source data. That is a validation-to-use workflow, not an isolated effect of changing only the evaluation corpus.

For each existing source fold, refit exactly the original 100-tree forest with seed 42 on the other four folds. Check that its source-held-out scores reproduce the saved scores. Evaluate that same fitted forest on the unchanged external feature table at threshold 0.5. Report all five source/external pairs of results, with training and test counts, accuracy, recall, false-positive rate and ROC AUC. Do not select a best fold or alter any threshold.

These five fits share training records and use the same external corpus. They are not five independent dataset replications. A persistent gap would show that the full-source refit is not necessary for the observed failure under these procedures. It would not identify the cause of the cross-corpus difference.

Keep the original predictions and the first diagnostic plan unchanged. Save this check under `results/defensibility_20261006/same_model/` with input and code hashes.
