"""Fetch the explicitly selected, revision-pinned external corpus and its card."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd


PAPER = Path(__file__).resolve().parents[1]
DEST = PAPER / "results/full_verification_20261005/external"
REVISION = "07857e2a97571ab553421ed645ef470bef6fa05c"
BASE = f"https://huggingface.co/datasets/NicolaiSivesind/ChatGPT-Research-Abstracts/resolve/{REVISION}/"
FILES = {"README.md": "010d3e5fa7be392ec7e58fcae468dd65a00caec4",
         "research_abstracts-final.csv": "1219a4c67edd5e41f92439a97715e5ec61878111"}


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    manifest = {"dataset": "NicolaiSivesind/ChatGPT-Research-Abstracts", "revision": REVISION,
                "retrieved_utc": datetime.now(timezone.utc).isoformat(), "files": {}}
    for name, expected_blob in FILES.items():
        path = DEST / name
        if path.exists():
            data = path.read_bytes()
        else:
            with urlopen(Request(BASE + name, headers={"User-Agent": "Corpus-transfer-audit/1.0"}), timeout=120) as response:
                data = response.read()
        git_blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if git_blob != expected_blob:
            raise ValueError(f"External artifact does not match its pinned Git blob: {name}")
        if not path.exists():
            path.write_bytes(data)
        manifest["files"][name] = {"url": BASE + name, "git_blob": git_blob,
                                    "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
    frame = pd.read_csv(DEST / "research_abstracts-final.csv", keep_default_na=False)
    manifest["rows"] = len(frame)
    manifest["columns"] = list(frame.columns)
    manifest["empty_cells"] = {col: int(frame[col].astype(str).str.strip().eq("").sum()) for col in frame.columns}
    manifest["source_scope"] = "Independent dataset author's declared labels and GPT-3.5-turbo-0301 configuration; not independently authenticated generation logs"
    (DEST / "download_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
