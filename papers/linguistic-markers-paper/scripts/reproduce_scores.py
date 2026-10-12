"""Verify a score-level reproduction package; optionally refit the main forest."""

import argparse
import hashlib
import io
import json
import zipfile
from pathlib import Path, PurePosixPath

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, average_precision_score, confusion_matrix,
                             f1_score, precision_score, recall_score, roc_auc_score)


FEATURES = ["mean_sent_len", "sent_len_cv", "hedge_density", "booster_density",
            "self_mention_density", "connector_density", "lexical_diversity_mtld",
            "first_word_connector_ratio"]


def read_scores(content, compression=None):
    # Ranking metrics depend on ties. Preserve the writer's complete float
    # representation rather than collapsing nearby values in the CSV parser.
    return pd.read_csv(io.BytesIO(content), compression=compression, float_precision="round_trip")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path, help="ZIP package or extracted package directory")
    parser.add_argument("--refit", action="store_true", help="Refit the 100-tree source forest and reproduce external scores")
    args = parser.parse_args()
    archive = zipfile.ZipFile(args.package) if args.package.is_file() else None

    def read(name):
        path = PurePosixPath(name)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError("Invalid package path")
        return archive.read(name) if archive else (args.package / name).read_bytes()

    manifest = json.loads(read("package_manifest.json"))
    for name, expected in manifest["files"].items():
        assert hashlib.sha256(read(name)).hexdigest() == expected, name
    checked = 0
    for case in manifest["prediction_sets"]:
        expected = case["metrics"]
        frame = read_scores(read(case["path"]), compression="gzip")
        y, p, prediction = frame.label.to_numpy(), frame.probability.to_numpy(), frame.prediction.to_numpy()
        assert np.array_equal(prediction, (p > .5).astype(int))
        cm = confusion_matrix(y, prediction, labels=[0, 1])
        observed = {"accuracy": accuracy_score(y, prediction), "precision": precision_score(y, prediction),
                    "recall": recall_score(y, prediction), "f1": f1_score(y, prediction),
                    "false_positive_rate": cm[0, 1]/cm[0].sum(), "specificity": cm[0, 0]/cm[0].sum(),
                    "roc_auc": roc_auc_score(y, p), "average_precision": average_precision_score(y, p)}
        assert cm.tolist() == expected["confusion_matrix"], case["path"]
        for metric, value in observed.items():
            assert np.isclose(value, expected[metric], rtol=0, atol=1e-11), (case["path"], metric)
        print(f"Verified {case['name']}: accuracy={observed['accuracy']:.8f}")
        checked += 1
    if args.refit:
        source = pd.read_csv(io.BytesIO(read(manifest["refit"]["source_features"])), compression="gzip")
        test = pd.read_csv(io.BytesIO(read(manifest["refit"]["external_features"])), compression="gzip")
        saved = read_scores(read(manifest["refit"]["external_predictions"]), compression="gzip")
        saved = test[["pair_id", "label"]].merge(saved, on=["pair_id", "label"], validate="one_to_one", how="left")
        forest = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=8)
        forest.fit(source[FEATURES].to_numpy(), source.label.to_numpy())
        p = forest.predict_proba(test[FEATURES].to_numpy())[:, 1]
        maximum_error = float(np.max(np.abs(p-saved.probability.to_numpy())))
        assert maximum_error < 1e-12, maximum_error
        print(f"Fresh forest fit reproduces external scores; maximum error={maximum_error}")
    print(f"All {checked} prediction sets verified. This checks numerical reproduction, not label authenticity.")
    if archive:
        archive.close()


if __name__ == "__main__":
    main()
