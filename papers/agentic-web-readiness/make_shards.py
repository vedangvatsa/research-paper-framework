"""Shard remaining (not-yet-scanned) domains across K workers for parallel scan."""
import json
import sys

BASE = "/Users/vedang/ZCodeProject/research-paper-framework/papers/agentic-web-readiness/data"
K = int(sys.argv[1]) if len(sys.argv) > 1 else 4

domains = [l.strip() for l in open(f"{BASE}/domains.txt") if l.strip()]
done = set()
try:
    for line in open(f"{BASE}/results.jsonl"):
        line = line.strip()
        if line:
            try:
                done.add(json.loads(line).get("domain"))
            except Exception:
                pass
except FileNotFoundError:
    pass

remaining = [d for d in domains if d not in done]
shards = [[] for _ in range(K)]
for i, d in enumerate(remaining):
    shards[i % K].append(d)
for k, s in enumerate(shards):
    with open(f"{BASE}/shard{k}.txt", "w") as f:
        f.write("\n".join(s) + "\n")
print(f"total={len(domains)} done={len(done)} remaining={len(remaining)} shards={[len(s) for s in shards]}")
