"""Create a whitelisted feature/score package without collecting new data."""

import argparse
import hashlib
import json
import zipfile
from pathlib import Path


PAPER = Path(__file__).resolve().parents[1]
BASE = PAPER / "results/full_verification_20261005"
DIAGNOSTICS = PAPER / "results/defensibility_20261006"
OUTPUT = DIAGNOSTICS / "high_accuracy_poor_transfer_reproduction.zip"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-existing", action="store_true")
    args = parser.parse_args()
    if OUTPUT.exists():
        if not args.archive_existing:
            raise ValueError("Reproduction package already exists; preserve it before rebuilding")
        archive_dir = DIAGNOSTICS / "previous_packages"
        archive_dir.mkdir(exist_ok=True)
        fingerprint = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()[:16]
        destination = archive_dir / f"{OUTPUT.stem}-{fingerprint}.zip"
        if destination.exists():
            raise ValueError("An identical archive already exists; inspect before rebuilding")
        OUTPUT.rename(destination)
    files = set()
    cases = []

    def add(path):
        path = path.resolve()
        path.relative_to(PAPER)
        if not path.is_file():
            raise FileNotFoundError(path)
        files.add(path)

    for name in ("linguistic_markers_paper.md", "linguistic_markers_paper.pdf",
                 "SUPPLEMENTARY_METHODS.md", "supplementary_methods.pdf",
                 "research_protocol.md", "full_verification_protocol.md",
                 "defensibility_protocol.md", "same_model_protocol.md", "requirements-corrected.txt"):
        add(PAPER / name)
    for name in ("reproduce_scores.py", "corrected_analysis.py", "audit_recovered_data.py",
                 "prepare_corrected_results.py", "evaluate_external_corpus.py",
                 "audit_text_quality.py", "regroup_confirmed_duplicates.py", "defensibility_checks.py",
                "same_model_transfer.py", "prepare_defensibility_results.py", "verify_defensibility.py",
                 "test_corrected_analysis.py", "test_defensibility_checks.py", "test_score_precision.py"):
        add(PAPER / "scripts" / name)
    for folder in (BASE / "revision4", BASE / "source_consistency_final", BASE / "external"):
        evaluation = json.loads((folder / "evaluation.json").read_text())
        add(folder / "evaluation.json")
        add(folder / "features.csv.gz")
        for model in evaluation["models"]:
            pred = folder / f"predictions_{model['name']}.csv.gz"
            add(pred)
            cases.append({"name": model["name"], "path": str(pred.relative_to(PAPER)), "metrics": model})
    diagnostics = json.loads((DIAGNOSTICS / "diagnostics.json").read_text())
    add(DIAGNOSTICS / "diagnostics.json")
    for result in diagnostics["forest_seed_checks"] + diagnostics["source_consistent_training"]:
        path = DIAGNOSTICS / f"predictions_{result['name']}.csv.gz"
        add(path)
        cases.append({"name": result["name"], "path": str(path.relative_to(PAPER)), "metrics": result})
    same_model = json.loads((DIAGNOSTICS / "same_model/evaluation.json").read_text())
    add(DIAGNOSTICS / "same_model/evaluation.json")
    for result in same_model["rows"]:
        path = DIAGNOSTICS / f"same_model/predictions_fold_{result['fold']}.csv.gz"
        add(path)
        cases.append({"name": f"same_model_fold_{result['fold']}", "path": str(path.relative_to(PAPER)), "metrics": result["external"]})
    for path in (BASE / "revision4/manifest.json", BASE / "revision4/feature_comparisons.csv",
                 BASE / "revision4/exclusions.csv", BASE / "source_checks_resolved.csv.gz",
                 BASE / "source_summary_resolved.json", BASE / "near_duplicates_all_labels.csv",
                  BASE / "source_identity_edges.csv", BASE / "external/eligibility.json",
                  BASE / "external/exclusions.csv", BASE / "external/download_manifest.json",
                  BASE / "revision4/length_summary.json", BASE / "generation_history.json",
                  BASE / "text_quality.csv.gz", BASE / "text_quality_all_labels_summary.json",
                  DIAGNOSTICS / "external_groups.csv", DIAGNOSTICS / "external_near_duplicates.csv"):
        add(path)
    for name in ("fig1_lengths.png", "fig2_comparisons.png", "fig3_curves.png", "fig4_confusion.png"):
        add(BASE / "revision4/figures" / name)
    readme = """# Score-level reproduction package

This package accompanies the local research draft. It has not been published to
a public archive. It contains measured features, split/group identifiers, saved
scores, analysis code and evidence records. It does not authenticate authorship
labels, supply missing generation logs, or reproduce original text collection.

After extraction, install the recorded environment and verify:

    python -m pip install -r requirements-corrected.txt
    python scripts/reproduce_scores.py .
    python scripts/reproduce_scores.py . --refit
    python scripts/verify_defensibility.py

The first check independently recalculates the classification metrics for all
22 saved prediction sets. The optional refit trains the main source forest from
the supplied features and compares its external scores with the frozen scores.
Prediction CSVs are read with round-trip float parsing so that nearby scores do
not become artificial ties in ranking metrics.
The diagnostic checker also verifies the threshold searches, length restrictions,
paired point differences and same-fitted-model comparisons. The included code
describes the other fits and bootstrap calculations.

Feature-level reproduction is different from checking features against original
text. That further check needs access to the local raw corpus and the pinned
external text files. Public raw-data access and release terms remain author
requirements. This package assigns no new license to third-party material.

The SHA-256 manifest detects changes to packaged files; it does not establish
the truth of their source labels. The manuscript and SUPPLEMENTARY_METHODS.md
state the interpretation, dictionaries, prompt templates and resource versions.
The supplement is also supplied as supplementary_methods.pdf.

The package includes source-comparison rows, the sanitized generation-history
inventory, and saved language/formatting diagnostics. Original text extraction,
live-source checks and the full paper-build workflow need the complete local
workspace and raw inputs. The three checker commands above run from this package.
"""
    manifest = {"scope": "Feature- and score-level numerical reproduction; original labels not authenticated",
                "files": {}, "prediction_sets": cases,
                "refit": {"source_features": str((BASE / "revision4/features.csv.gz").relative_to(PAPER)),
                          "external_features": str((BASE / "external/features.csv.gz").relative_to(PAPER)),
                          "external_predictions": str((BASE / "external/predictions_forest_eight_external.csv.gz").relative_to(PAPER))}}
    with zipfile.ZipFile(OUTPUT, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in sorted(files):
            content = path.read_bytes()
            name = str(path.relative_to(PAPER))
            manifest["files"][name] = hashlib.sha256(content).hexdigest()
            archive.writestr(name, content)
        encoded = readme.encode()
        archive.writestr("README_REPRODUCTION.md", encoded)
        manifest["files"]["README_REPRODUCTION.md"] = hashlib.sha256(encoded).hexdigest()
        archive.writestr("package_manifest.json", json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"package": str(OUTPUT), "bytes": OUTPUT.stat().st_size,
                      "files": len(files)+2, "prediction_sets": len(cases),
                      "sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest()}, indent=2))


if __name__ == "__main__":
    main()
