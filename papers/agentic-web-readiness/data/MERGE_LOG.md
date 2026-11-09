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

## 2026-09-10 — Audit note on low-band selection
- The preserved pre-merge backup has 22,344 rows with score 11 or below.
  The R3 shard files contain 21,247 of those rows; the 300 re-check rows are
  also in that low-score set and do not overlap the R3 shards. The 21,547
  merged newer rows therefore leave 797 pre-merge low-score rows unchanged.
- The available artifacts do not explain why the shard list did not include
  those 797 rows. The earlier statement that every score-11-or-below row was
  refreshed is not supported by the preserved files.

## 2026-09-10 — Correction to low-band audit note
- The selection rule is score 10 or below, not score 11 or below. The initial
  backup contains exactly 21,547 rows at or below 10, and those are exactly
  the 21,547 rows replaced by a newer result. The 797 unchanged rows above
  are all score-11 rows and were not in the refresh target.
- This supersedes the claimed unexplained selection gap in the preceding note.
