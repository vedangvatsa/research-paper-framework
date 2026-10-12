"""Offline diagnostics for every retained text and approximate duplicate checks."""

import argparse
import hashlib
import importlib.metadata
import json
import re
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd
from datasketch import MinHash, MinHashLSH
from langid.langid import LanguageIdentifier, model as language_model
from threadpoolctl import threadpool_limits

from audit_recovered_data import sha256
from corrected_analysis import normalize


PAPER = Path(__file__).resolve().parents[1]
OUT = PAPER / "results/full_verification_20261005"
LANGUAGE = None
LIMITER = None


def shingles(text):
    words = normalize(text).split()
    return {" ".join(words[i:i+5]) for i in range(max(0, len(words)-4))}


def signature(text):
    pieces = shingles(text)
    sketch = MinHash(num_perm=128, seed=42)
    if pieces:
        sketch.update_batch([piece.encode() for piece in sorted(pieces)])
    return sketch.hashvalues, len(pieces)


def init_language():
    global LANGUAGE, LIMITER
    LIMITER = threadpool_limits(limits=1)
    LANGUAGE = LanguageIdentifier.from_modelstring(language_model, norm_probs=True)


def language_check(record):
    oid, label, text = record
    language, score = LANGUAGE.classify(text)
    letters = [c for c in text if c.isalpha()]
    return {"pair_id": oid, "label": label, "langid_language": language,
            "langid_normalized_score": float(score),
            "has_html_tag": bool(re.search(r"</?[A-Za-z][^>]*>", text)),
            "has_url": bool(re.search(r"https?://|www\.", text)),
            "has_replacement_character": "\ufffd" in text,
            "non_ascii_letter_share": sum(not c.isascii() for c in letters)/len(letters) if letters else 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    source = PAPER / "data/metadata/synthetic_abstracts_openai.csv"
    pairs = pd.read_csv(source, keep_default_na=False)
    frame = pd.read_csv(PAPER / "results/correction_20261005/revision2/features.csv.gz")
    retained = set(frame.pair_id)
    ids = pairs.openalex_id.tolist()
    published = pairs.human_abstract.tolist()
    generated = pairs.ai_abstract.tolist()
    all_texts = published + generated
    OUT.mkdir(exist_ok=True)
    sig_path = OUT / "local_minhash_signatures.npz"
    manifest_path = OUT / "minhash_manifest.json"
    if sig_path.exists():
        manifest = json.loads(manifest_path.read_text())
        assert manifest["input_sha256"] == sha256(source)
        assert manifest["signature_sha256"] == sha256(sig_path)
        with np.load(sig_path, allow_pickle=False) as saved:
            signatures, shingle_counts = saved["signatures"], saved["shingle_counts"]
    else:
        signatures = np.empty((len(all_texts), 128), dtype=np.uint64)
        shingle_counts = np.empty(len(all_texts), dtype=np.int32)
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            for i, (values, count) in enumerate(executor.map(signature, all_texts, chunksize=100)):
                signatures[i], shingle_counts[i] = values, count
                if (i+1) % 25000 == 0:
                    print(f"MinHash signatures: {i+1:,}/{len(all_texts):,}", flush=True)
        np.savez_compressed(sig_path, signatures=signatures, shingle_counts=shingle_counts)
        manifest = {"input_sha256": sha256(source), "signature_sha256": sha256(sig_path),
                    "order": "All published rows, then all generated rows, in original paired-file order",
                    "texts": len(all_texts), "num_perm": 128, "seed": 42, "shingle_words": 5,
                    "candidate_threshold": .8, "exact_jaccard_threshold": .85,
                    "datasketch_version": importlib.metadata.version("datasketch")}
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    lsh = MinHashLSH(threshold=.8, num_perm=128)
    fold_map = frame.drop_duplicates("pair_id").set_index("pair_id").fold.to_dict()
    matches = []
    for i, text in enumerate(all_texts):
        oid = ids[i % len(ids)]
        if oid not in retained or shingle_counts[i] == 0:
            continue
        sketch = MinHash(num_perm=128, seed=42, hashvalues=signatures[i])
        candidates = lsh.query(sketch)
        if candidates:
            left = shingles(text)
            for j in candidates:
                right = shingles(all_texts[j])
                score = len(left & right)/len(left | right)
                if score >= .85:
                    right_id = ids[j % len(ids)]
                    matches.append({"left_id": oid, "right_id": right_id,
                                    "left_label": i // len(ids), "right_label": j // len(ids), "jaccard": score,
                                    "left_fold": fold_map[oid], "right_fold": fold_map[right_id],
                                    "crosses_original_folds": fold_map[oid] != fold_map[right_id],
                                    "within_pair": oid == right_id})
        lsh.insert(i, sketch)
    duplicate_table = pd.DataFrame(matches, columns=["left_id", "right_id", "left_label", "right_label", "jaccard", "left_fold", "right_fold", "crosses_original_folds", "within_pair"])
    duplicate_table.to_csv(OUT / "near_duplicates_all_labels.csv", index=False)

    language_path = OUT / "text_quality.csv.gz"
    if language_path.exists():
        quality = pd.read_csv(language_path)
    else:
        tasks = [(oid, label, texts[i]) for label, texts in ((0, published), (1, generated))
                 for i, oid in enumerate(ids) if oid in retained]
        quality_rows = []
        with ProcessPoolExecutor(max_workers=args.workers, initializer=init_language) as executor:
            for i, row in enumerate(executor.map(language_check, tasks, chunksize=100), 1):
                quality_rows.append(row)
                if i % 25000 == 0:
                    print(f"Language/quality checks: {i:,}/{len(tasks):,}", flush=True)
        quality = pd.DataFrame(quality_rows)
        quality.to_csv(language_path, index=False, compression={"method": "gzip", "mtime": 0})
    assert len(quality) == len(frame)
    summary = {"retained_texts_checked": len(quality), "near_duplicate_pairs": len(matches),
               "near_duplicate_scope": "All retained published and generated texts, including cross-class candidates",
               "within_source_pair_matches": int(duplicate_table.within_pair.sum()),
               "near_duplicate_pairs_crossing_folds": int(duplicate_table.crosses_original_folds.sum()),
               "near_duplicate_source_ids": len({r[k] for r in matches for k in ("left_id", "right_id")}),
               "near_duplicate_search": manifest,
               "language_model": "langid 1.1.6 pretrained classifier; normalized scores are not verified correctness probabilities",
               "limits": "Approximate candidate search is not exhaustive. Language labels are diagnostic, not author-background labels or independently certified languages."}
    for label, name in ((0, "published"), (1, "generated")):
        subset = quality[quality.label == label]
        summary[name] = {"texts": len(subset), "language_counts": subset.langid_language.value_counts().to_dict(),
                         "non_english_score_at_least_0_9": int((subset.langid_language.ne("en") & subset.langid_normalized_score.ge(.9)).sum()),
                         "html_tags": int(subset.has_html_tag.sum()), "urls": int(subset.has_url.sum()),
                         "replacement_characters": int(subset.has_replacement_character.sum())}
    (OUT / "text_quality_all_labels_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
