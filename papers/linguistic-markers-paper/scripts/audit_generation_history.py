"""Inspect original script/schema evidence without executing APIs or printing secrets."""

import ast
import hashlib
import json
from pathlib import Path

import pandas as pd

from audit_recovered_data import sha256


PAPER = Path(__file__).resolve().parents[1]
OUTPUT = PAPER / "results/full_verification_20261005/generation_history.json"
RESPONSE_FIELDS = {"request_id", "response_id", "id", "created", "created_at", "timestamp",
                   "model", "model_version", "finish_reason", "prompt", "prompt_id", "system_fingerprint"}


def main():
    script_records = []
    for path in sorted((PAPER / "scripts").glob("generate*.py")):
        tree = ast.parse(path.read_text())
        output_dicts, model_names, fields = [], set(), set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                if node.value.startswith(("gpt-", "llama-", "command-r", "minimaxai/")):
                    model_names.add(node.value)
            if isinstance(node, ast.Dict):
                keys = {key.value for key in node.keys if isinstance(key, ast.Constant) and isinstance(key.value, str)}
                if "ai_abstract" in keys and "human_abstract" in keys:
                    output_dicts.append(sorted(keys))
                    fields.update(keys & RESPONSE_FIELDS)
        if output_dicts or model_names:
            script_records.append({"path": str(path.relative_to(PAPER)), "sha256": sha256(path),
                                   "configured_model_names": sorted(model_names),
                                   "paired_output_dictionary_keys": output_dicts,
                                   "request_metadata_in_paired_output": sorted(fields)})
    final_path = PAPER / "data/metadata/synthetic_abstracts_openai.csv"
    final = pd.read_csv(final_path, keep_default_na=False)
    final_by_id = final.set_index("openalex_id")
    schemas = []
    for path in sorted((PAPER / "data/metadata").glob("*.csv")):
        frame = pd.read_csv(path, keep_default_na=False)
        item = {"path": str(path.relative_to(PAPER)), "sha256": sha256(path), "rows": len(frame),
                "columns": list(frame.columns), "request_metadata_columns": sorted(set(frame.columns) & RESPONSE_FIELDS)}
        if "ai_abstract" in frame and "openalex_id" in frame:
            unique = frame.drop_duplicates("openalex_id").set_index("openalex_id")
            shared = unique.index.intersection(final_by_id.index)
            item["ids_in_final"] = len(shared)
            item["same_generated_text_as_final"] = int(unique.loc[shared, "ai_abstract"].eq(final_by_id.loc[shared, "ai_abstract"]).sum())
        schemas.append(item)
    # Scope is deliberately limited to the study directory. Build/audit logs are
    # not historical generation evidence, and unrelated account stores are not searched.
    original_logs = [str(p.relative_to(PAPER)) for folder in (PAPER, PAPER / "data", PAPER / "scripts")
                     for p in folder.glob("*.log")]
    result = {"script_evidence": script_records, "file_schemas": schemas,
              "generation_log_candidates_in_study_locations": original_logs,
              "per_output_request_history_recoverable_from_these_files": False,
              "conclusion": "Configured model names are observable. Original response IDs, timestamps, model snapshots, prompt assignments and finish reasons are not retained in the paired CSVs. Backup text equality does not authenticate a generation date or provider."}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
