"""Check DOI/canonical-ID clusters and identify usable fallback lookup targets."""

import json
import re
from pathlib import Path

import pandas as pd

PAPER = Path(__file__).resolve().parents[1]
ROOT = PAPER / "results/full_verification_20261005"


def valid_doi_identity(value):
    return re.fullmatch(r"https://doi\.org/10\.\d{4,9}/\S+", str(value).strip().lower()) is not None


def main():
    source = pd.read_csv(ROOT / "source_checks_resolved.csv.gz", low_memory=False)
    frame = pd.read_csv(ROOT / "revision3/features.csv.gz").drop_duplicates("pair_id")
    original = pd.read_csv(PAPER / "data/metadata/openalex_human_abstracts.csv", keep_default_na=False)
    joined = frame[["pair_id", "fold", "group_id"]].merge(source, left_on="pair_id", right_on="source_id", validate="one_to_one")
    conflicts, edges = [], []
    summary = {"reference_split": "revision3, before the final shared-identifier repair"}
    for key in ["stored_doi", "current_id", "current_doi"]:
        valid = joined[joined[key].notna() & joined[key].astype(str).str.strip().ne("")].copy()
        valid["identity"] = valid[key].str.strip().str.lower()
        if key.endswith("doi"):
            valid = valid[valid.identity.map(valid_doi_identity)]
        groups = valid.groupby("identity")
        duplicated = groups.size()[lambda counts: counts > 1]
        crossing = groups.fold.nunique()[lambda counts: counts > 1]
        summary[key] = {"duplicate_identity_groups": len(duplicated), "identity_groups_crossing_folds": len(crossing)}
        for identity in duplicated.index:
            members = sorted(valid.loc[valid.identity.eq(identity), "pair_id"])
            edges.extend({"left_id": members[0], "right_id": member, "identity_type": key, "identity": identity}
                         for member in members[1:])
        for identity in crossing.index:
            members = valid[valid.identity.eq(identity)]
            conflicts.append({"key": key, "identity": identity, "pairs": members.pair_id.tolist(), "folds": members.fold.tolist()})
    unresolved = source[source.source_status.eq("unresolved")].source_id
    missing = original[original.openalex_id.isin(unresolved)]
    summary["unresolved_ids"] = len(missing)
    summary["unresolved_with_doi"] = int(missing.doi.astype(str).str.startswith("https://doi.org/10.").sum())
    summary["conflicts"] = conflicts
    (ROOT / "source_identity_checks.json").write_text(json.dumps(summary, indent=2) + "\n")
    pd.DataFrame(edges, columns=["left_id", "right_id", "identity_type", "identity"]).to_csv(ROOT / "source_identity_edges.csv", index=False)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
