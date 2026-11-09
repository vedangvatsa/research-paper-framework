"""Figures for the agentic-readiness paper. All values recomputed from
results-gentle.jsonl. No titles inside chart images; captions live in text.
"""
import csv
import json
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).parent
DATA = BASE / "data"
FIG = BASE / "figures"
FIG.mkdir(exist_ok=True)

tiers = {r["domain"]: r["tier"] for r in csv.DictReader(open(DATA / "sample.csv"))}
sc = [json.loads(l) for l in open(DATA / "results-gentle.jsonl") if l.strip()]
N = len(sc)

plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})

# Figure 1: score histogram
scores = [r["score"] for r in sc]
fig, ax = plt.subplots(figsize=(6.5, 3.2))
ax.hist(scores, bins=range(0, 101, 5), color="#4f6fb5", edgecolor="white", linewidth=0.4)
ax.axvline(sum(scores) / N, color="#c0392b", linestyle="--", linewidth=1.2, label=f"mean {sum(scores)/N:.1f}")
ax.set_xlabel("Stored checklist score (0 to 100)")
ax.set_ylabel("Hostname records")
ax.legend(frameon=False)
fig.tight_layout(pad=1.2)
fig.savefig(FIG / "fig2_score_hist.png", dpi=150)
plt.close(fig)

# Tier comparison of stored scores and bot-user-agent status predicates.
order = ["tier1_top10k", "tier2_10k_100k", "tier3_100k_1m"]
labels = ["Ranks 1-10k", "Ranks 10,001-100k", "Ranks 100,001-1M"]
means, no_bot_success = [], []
for t in order:
    s = [r for r in sc if tiers.get(r["domain"]) == t]
    means.append(sum(r["score"] for r in s) / len(s))
    no_bot_success.append(sum(1 for r in s if r["checks"].get("bot-ua-access") == "fail") / len(s) * 100)
x = range(3)
fig, ax1 = plt.subplots(figsize=(6.5, 3.2))
b1 = ax1.bar([i - 0.2 for i in x], means, width=0.4, color="#4f6fb5", label="Mean checklist score")
ax1.set_ylabel("Mean checklist score")
ax1.set_xticks(list(x))
ax1.set_xticklabels(labels)
ax2 = ax1.twinx()
b2 = ax2.bar([i + 0.2 for i in x], no_bot_success, width=0.4, color="#d98a3d", label="Neither bot-UA request classified as HTTP 200")
ax2.set_ylabel("Neither bot-UA request HTTP 200 (%)")
ax2.set_ylim(0, 100)
for i, (m, r) in enumerate(zip(means, no_bot_success)):
    ax1.text(i - 0.2, m + 0.4, f"{m:.1f}", ha="center", fontsize=8)
    ax2.text(i + 0.2, r + 1, f"{r:.1f}%", ha="center", fontsize=8)
fig.tight_layout(pad=1.2)
fig.savefig(FIG / "fig3_tier_compare.png", dpi=150)
plt.close(fig)

# Reported predicate pass shares, not validated feature-adoption rates.
checks = [
    ("robots-ai-policy", "robots.txt rule check"),
    ("llms-txt", "llms.txt check"),
    ("markdown-negotiation", "Markdown-like response"),
    ("bot-ua-access", "HTTP 200 for both test requests"),
    ("mcp-server-live", "MCP response marker"),
    ("openapi-spec", "OpenAPI version marker"),
    ("security-txt", "security.txt contact marker"),
    ("json-ld", "JSON-LD script check"),
    ("sitemap-xml", "Sitemap + robots.txt markers"),
    ("markdown-twins", "index.md body check"),
    ("agent-payments", "Payment-related markers"),
]
shares = [sum(1 for r in sc if r["checks"].get(c) == "pass") / N * 100 for c, _ in checks]
order_idx = sorted(range(len(checks)), key=lambda i: shares[i])
fig, ax = plt.subplots(figsize=(6.5, 4.0))
ax.barh([checks[i][1] for i in order_idx], [shares[i] for i in order_idx], color="#4f6fb5", height=0.6)
ax.set_xlabel("Recorded pass share of 50,000 hostnames (%)")
for i, v in enumerate([shares[i] for i in order_idx]):
    ax.text(v + 0.4, i, f"{v:.2f}%", va="center", fontsize=8)
ax.set_xlim(0, max(shares) * 1.35)
fig.tight_layout(pad=1.2)
fig.savefig(FIG / "fig1_adoption.png", dpi=150)
plt.close(fig)

print("wrote", sorted(p.name for p in FIG.glob("fig*.png")))

# Figure 4: layer means by tier (grouped bars)
tier_ids = ["tier1_top10k", "tier2_10k_100k", "tier3_100k_1m"]
tier_labels = ["Ranks 1-10k", "Ranks 10,001-100k", "Ranks 100,001-1M"]
layer_ids = ["discovery", "access", "usability", "security", "seo", "payments"]
layer_labels = ["Discovery", "Access", "Interface", "Security", "SEO", "Payments"]
by_tier = {t: [r for r in sc if tiers.get(r["domain"]) == t] for t in tier_ids}
means = {L: [sum(r["layers"][L] for r in by_tier[t]) / len(by_tier[t]) for t in tier_ids] for L in layer_ids}
x = range(len(layer_labels))
w = 0.24
colors = ["#4f6fb5", "#d98a3d", "#5da86f"]
fig, ax = plt.subplots(figsize=(6.5, 3.4))
for i, t in enumerate(tier_ids):
    ax.bar([j + (i - 1) * w for j in x], [means[L][i] for L in layer_ids], width=w, color=colors[i], label=tier_labels[i])
ax.set_xticks(list(x))
ax.set_xticklabels(layer_labels, rotation=0)
ax.set_ylabel("Mean group score (0 to 100)")
ax.legend(frameon=False, fontsize=8)
ax.set_ylim(0, 50)
fig.tight_layout(pad=1.2)
fig.savefig(FIG / "fig5_layers_by_tier.png", dpi=150)
plt.close(fig)

# Recorded fail/warning labels; their causes are not independently observed.
fails = Counter()
for r in sc:
    for cid, st in r["checks"].items():
        if st in ("fail", "warning"):
            fails[cid] += 1
top15 = fails.most_common(15)
labels15 = [c for c, _ in top15][::-1]
vals15 = [fails[c] / N * 100 for c in labels15]
display_labels15 = ["mcp-jsonrpc-screen" if c == "mcp-server-live" else c for c in labels15]
fig, ax = plt.subplots(figsize=(6.5, 4.2))
ax.barh(display_labels15, vals15, color="#4f6fb5", height=0.6)
ax.set_xlabel("Recorded fail or warning share of hostnames (%)")
for i, v in enumerate(vals15):
    ax.text(v - 1, i, f"{v:.1f}%", va="center", ha="right", fontsize=8, color="white")
ax.set_xlim(0, 100)
fig.tight_layout(pad=1.2)
fig.savefig(FIG / "fig6_failure_pareto.png", dpi=150)
plt.close(fig)

# Figure 6: policy signal versus bot-UA request outcome
cats = ["pass", "warning", "fail"]
cat_labels = {
    "pass": "Robots heuristic pass",
    "warning": "Robots heuristic warning",
    "fail": "Robots heuristic fail",
}
bot_order = ["pass", "warning", "fail"]
bot_labels = ["Both classified HTTP 200", "One classified HTTP 200", "Neither classified HTTP 200"]
fig, ax = plt.subplots(figsize=(6.5, 3.4))
x = range(3)
w = 0.24
bcolors = ["#5da86f", "#d98a3d", "#c0392b"]
for i, b in enumerate(bot_order):
    vals = []
    for c in cats:
        sub = [r for r in sc if r["checks"].get("robots-ai-policy") == c]
        vals.append(sum(1 for r in sub if r["checks"].get("bot-ua-access") == b) / len(sub) * 100)
    ax.bar([j + (i - 1) * w for j in x], vals, width=w, color=bcolors[i], label=bot_labels[i])
ax.set_xticks(list(x))
ax.set_xticklabels([cat_labels[c] for c in cats])
ax.set_ylabel("Share of row group (%)")
ax.legend(frameon=False, fontsize=8)
fig.tight_layout(pad=1.2)
fig.savefig(FIG / "fig7_policy_behavior.png", dpi=150)
plt.close(fig)

# Figure 7: grade mix by tier (100% stacked bars)
grades = ["B", "C", "D", "F"]
gcolors = {"B": "#5da86f", "C": "#9bc53d", "D": "#d98a3d", "F": "#c0392b"}
fig, ax = plt.subplots(figsize=(6.5, 3.2))
bottoms = [0.0, 0.0, 0.0]
for g in grades:
    vals = []
    for t in tier_ids:
        s = by_tier[t]
        vals.append(sum(1 for r in s if r.get("grade") == g) / len(s) * 100)
    ax.bar(tier_labels, vals, bottom=list(bottoms), color=gcolors[g], label=f"Score band {g}")
    bottoms = [b + v for b, v in zip(bottoms, vals)]
ax.set_ylabel("Share of tier (%)")
ax.legend(frameon=False, fontsize=8, ncol=4, loc="lower center", bbox_to_anchor=(0.5, 1.01))
fig.tight_layout(pad=1.2)
fig.savefig(FIG / "fig4_grades_by_tier.png", dpi=150)
plt.close(fig)

print("wrote7", sorted(p.name for p in FIG.glob("fig*.png")))
