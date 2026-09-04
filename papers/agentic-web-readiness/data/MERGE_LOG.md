# Corpus merge log (append-only; newest at bottom)

## 2026-09-04 — R3 low-band refresh merged (latest-wins by scannedAt)
- Inputs: results-gentle.jsonl (50,000 rows, mean 22.7) + results-r3-shard{0..3}.jsonl
  (21,247 rows) + results-reverify.jsonl (300 rows)
- Changed rows: 21,547 of 50,000. Mean delta among changed rows: +7.0.
  Rows up >=20 points: 3,430. Rows down >=20 points: 0.
- Output: results-gentle.jsonl (50,000 rows, mean 25.7, 0 missing).
- Pre-merge backup: data/checkpoints/ckpt-pre-r3merge/results-gentle.jsonl
- Verification: all 61 appendix rows and all headline shares recomputed
  from the merged file match the paper with zero mismatches.
