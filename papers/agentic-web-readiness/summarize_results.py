"""Summarize scan results and design-weighted sensitivity estimates.

The 10k/20k/20k sample deliberately over-represents high-ranked domains.
Ordinary counts describe that constructed sample. Design-weighted estimates
target the dated Tranco top-1M frame and include sampling error only, not
scanner, network, threshold, or selective-recheck error.
"""
import csv, json, math
from datetime import datetime
from pathlib import Path
from collections import Counter, defaultdict
from statistics import median

BASE = Path(__file__).parent
DATA = BASE / "data"

CHECKS = ["robots-ai-policy", "llms-txt", "markdown-negotiation", "bot-ua-access",
          "mcp-server-live", "openapi-spec", "security-txt", "json-ld",
          "sitemap-xml", "markdown-twins", "agent-payments"]

FRAME_N = {
    "tier1_top10k": 10_000,
    "tier2_10k_100k": 90_000,
    "tier3_100k_1m": 900_000,
}
REFRESH_SCORE_CUTOFF = 10


def load_rows(path: Path) -> list[dict]:
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def validate_rows(rows: list[dict], sample_domains: set[str], label: str) -> None:
    domains = [row.get("domain") for row in rows]
    if len(domains) != len(set(domains)):
        raise ValueError(f"{label} contains duplicate domains")
    if set(domains) != sample_domains:
        missing = len(sample_domains - set(domains))
        unexpected = len(set(domains) - sample_domains)
        raise ValueError(f"{label} domain set mismatch: {missing} missing, {unexpected} unexpected")
    if any("score" not in row or "checks" not in row for row in rows):
        raise ValueError(f"{label} contains an unscored row")
    check_counts = {len(row["checks"]) for row in rows}
    if check_counts != {61}:
        raise ValueError(f"{label} does not contain exactly 61 check statuses per row: {check_counts}")


def status_pass_summary(rows: list[dict]) -> dict:
    return {
        check: {
            "status_pass": sum(1 for row in rows if row["checks"].get(check) == "pass"),
            "n": len(rows),
            "share": round(
                sum(1 for row in rows if row["checks"].get(check) == "pass") / len(rows), 4
            ) if rows else 0.0,
        }
        for check in CHECKS
    }


def full_status_counts(rows: list[dict]) -> dict:
    """Return every saved status count so the paper need not print a 61-row table."""
    checks = sorted(rows[0]["checks"])
    statuses = ("pass", "warning", "fail", "na")
    return {
        check: {
            status: sum(1 for row in rows if row["checks"].get(check) == status)
            for status in statuses
        }
        for check in checks
    }


def crux_summary(rows: list[dict], crux_labels: dict[str, bool]) -> dict:
    groups = {}
    for label, wanted in (("listed", True), ("unlisted", False)):
        subset = [row for row in rows if crux_labels[row["domain"]] is wanted]
        groups[label] = {
            "n": len(subset),
            "mean_score": round(sum(row["score"] for row in subset) / len(subset), 1),
            "status_passes": status_pass_summary(subset),
        }
    return groups


def compare_waves(initial_rows: list[dict], final_rows: list[dict], tiers: dict[str, str]) -> dict:
    initial = {row["domain"]: row for row in initial_rows}
    final = {row["domain"]: row for row in final_rows}
    changed = [domain for domain in initial if initial[domain]["scannedAt"] != final[domain]["scannedAt"]]
    low_score_domains = {
        domain for domain, row in initial.items() if row["score"] <= REFRESH_SCORE_CUTOFF
    }
    by_tier = {}
    for tier in FRAME_N:
        domains = [domain for domain in initial if tiers[domain] == tier]
        changed_in_tier = [domain for domain in changed if tiers[domain] == tier]
        by_tier[tier] = {
            "n": len(domains),
            "newer_row_n": len(changed_in_tier),
            "newer_row_share": round(len(changed_in_tier) / len(domains), 4),
            "initial_mean_score": round(sum(initial[domain]["score"] for domain in domains) / len(domains), 4),
            "final_mean_score": round(sum(final[domain]["score"] for domain in domains) / len(domains), 4),
            "mean_score_change_newer_rows": round(
                sum(final[domain]["score"] - initial[domain]["score"] for domain in changed_in_tier)
                / len(changed_in_tier),
                4,
            ),
        }
    return {
        "initial_mean_score": round(sum(row["score"] for row in initial_rows) / len(initial_rows), 4),
        "final_mean_score": round(sum(row["score"] for row in final_rows) / len(final_rows), 4),
        "initial_no_bot_ua_http_200_success_share": round(
            sum(row["checks"]["bot-ua-access"] == "fail" for row in initial_rows) / len(initial_rows),
            4,
        ),
        "final_no_bot_ua_http_200_success_share": round(
            sum(row["checks"]["bot-ua-access"] == "fail" for row in final_rows) / len(final_rows),
            4,
        ),
        "newer_row_n": len(changed),
        "newer_row_share": round(len(changed) / len(initial), 4),
        "refresh_score_cutoff": REFRESH_SCORE_CUTOFF,
        "initial_score_at_or_below_cutoff_n": len(low_score_domains),
        "newer_row_score_at_or_below_cutoff_n": len(set(changed) & low_score_domains),
        "unchanged_score_at_or_below_cutoff_n": len(low_score_domains - set(changed)),
        "by_tier": by_tier,
    }


def derived_results(rows: list[dict], tiers: dict[str, str]) -> dict:
    by_tier = {
        tier: [row for row in rows if tiers[row["domain"]] == tier]
        for tier in FRAME_N
    }
    readable = [row for row in rows if row["checks"]["access-js-hydration"] == "pass"]
    bot_status = Counter(row["checks"]["bot-ua-access"] for row in rows)
    fails = Counter(
        check
        for row in rows
        for check, status in row["checks"].items()
        if status in ("fail", "warning")
    )
    fail_warning_total = sum(fails.values())
    top15 = fails.most_common(15)

    return {
        "readable_root_screen": {
            "definition": "access-js-hydration status pass: more than 300 regex-extracted characters",
            "n": len(readable),
            "share": round(len(readable) / len(rows), 4),
            "mean_score": round(sum(row["score"] for row in readable) / len(readable), 1),
            "bot_ua_status_counts": dict(Counter(row["checks"]["bot-ua-access"] for row in readable)),
            "tracked_status_passes": status_pass_summary(readable),
        },
        "bot_ua_status_counts": dict(bot_status),
        "grade_counts": dict(Counter(row["grade"] for row in rows)),
        "tier_results": {
            tier: {
                "n": len(subset),
                "mean_score": round(sum(row["score"] for row in subset) / len(subset), 1),
                "median_score": median(row["score"] for row in subset),
                "no_bot_ua_http_200_success_share": round(
                    sum(row["checks"]["bot-ua-access"] == "fail" for row in subset) / len(subset),
                    4,
                ),
            }
            for tier, subset in by_tier.items()
        },
        "layer_means": {
            layer: round(sum(row["layers"][layer] for row in rows) / len(rows), 1)
            for layer in ("discovery", "access", "usability", "security", "seo", "payments")
        },
        "mcp_screen": {
            "basic_status_pass_n": sum(
                row["checks"]["mcp-server-live"] == "pass" for row in rows
            ),
            "capabilities_status_pass_n": sum(
                row["checks"]["mcp-schema-handshake"] == "pass" for row in rows
            ),
        },
        "fail_warning_concentration": {
            "instances": fail_warning_total,
            "top15_instances": sum(count for _, count in top15),
            "top15_share": round(sum(count for _, count in top15) / fail_warning_total, 4),
            "top15": [{"check": check, "n": count} for check, count in top15],
        },
    }


def reverify_comparison(initial_rows: list[dict], reverify_rows: list[dict]) -> dict:
    initial = {row["domain"]: row for row in initial_rows}
    domains = [row.get("domain") for row in reverify_rows]
    if len(domains) != len(set(domains)) or not set(domains) <= set(initial):
        raise ValueError("reverify rows do not form a unique subset of the initial corpus")
    deltas = [row["score"] - initial[row["domain"]]["score"] for row in reverify_rows]
    return {
        "n": len(reverify_rows),
        "mean_score_change": round(sum(deltas) / len(deltas), 4),
        "up_20_or_more_n": sum(delta >= 20 for delta in deltas),
        "down_20_or_more_n": sum(delta <= -20 for delta in deltas),
    }


def design_estimate(rows: list[dict], tiers: dict[str, str], value) -> dict:
    """Stratified mean with finite-population sampling error only."""
    total_population = sum(FRAME_N.values())
    estimate = 0.0
    variance = 0.0
    strata = {}

    for tier, population_n in FRAME_N.items():
        values = [value(row) for row in rows if tiers.get(row["domain"]) == tier]
        sample_n = len(values)
        if sample_n == 0:
            raise ValueError(f"No rows found for {tier}")
        mean = sum(values) / sample_n
        sample_variance = (
            sum((item - mean) ** 2 for item in values) / (sample_n - 1)
            if sample_n > 1 else 0.0
        )
        share = population_n / total_population
        sampling_fraction = sample_n / population_n
        estimate += share * mean
        variance += (share ** 2) * (1 - sampling_fraction) * sample_variance / sample_n
        strata[tier] = {
            "population_n": population_n,
            "sample_n": sample_n,
            "mean": mean,
            "sampling_fraction": sampling_fraction,
        }

    standard_error = math.sqrt(max(0.0, variance))
    return {
        "estimate": estimate,
        "sampling_se": standard_error,
        "sampling_ci95": [estimate - 1.96 * standard_error, estimate + 1.96 * standard_error],
        "strata": strata,
    }


def rounded_estimate(result: dict, decimals: int = 4) -> dict:
    return {
        "estimate": round(result["estimate"], decimals),
        "sampling_se": round(result["sampling_se"], decimals),
        "sampling_ci95": [round(value, decimals) for value in result["sampling_ci95"]],
        "strata": {
            tier: {
                **values,
                "mean": round(values["mean"], decimals),
                "sampling_fraction": round(values["sampling_fraction"], decimals),
            }
            for tier, values in result["strata"].items()
        },
    }

def main() -> None:
    tiers = {}
    crux_labels = {}
    with open(DATA / "sample.csv") as f:
        for row in csv.DictReader(f):
            if row["domain"] in tiers:
                raise ValueError(f"sample.csv contains duplicate domain {row['domain']}")
            tiers[row["domain"]] = row["tier"]
            crux_labels[row["domain"]] = row["crux_overlap"] == "1"
    if set(tiers.values()) != set(FRAME_N):
        raise ValueError("sample.csv does not contain the expected three sampling tiers")
    gentle = DATA / "results-gentle.jsonl"
    src = gentle if gentle.exists() else DATA / "results.jsonl"
    rows = load_rows(src)
    validate_rows(rows, set(tiers), "final corpus")
    scored = rows
    errors = []
    by_tier = defaultdict(list)
    for r in scored:
        by_tier[tiers.get(r["domain"], "unknown")].append(r["score"])
    adoption = status_pass_summary(scored)
    status_counts = Counter("completed" for _ in rows)
    scan_times = [datetime.fromisoformat(row["scannedAt"].replace("Z", "+00:00")) for row in scored]
    summary = {
        "attempted_domains": len(rows),
        "completed": len(scored),
        "errors": len(errors),
        "status_counts": dict(status_counts),
        "mean_score": round(sum(r["score"] for r in scored) / len(scored), 1) if scored else None,
        "scan_timing": {
            "earliest": min(scan_times).isoformat(),
            "latest": max(scan_times).isoformat(),
            "span_hours": round((max(scan_times) - min(scan_times)).total_seconds() / 3600, 2),
        },
        "tier_means": {t: round(sum(v) / len(v), 1) for t, v in by_tier.items() if v},
        "tier_n": {t: len(v) for t, v in by_tier.items()},
        "tracked_status_passes": adoption,
        "full_status_counts": full_status_counts(scored),
        "crux_overlap": {
            "normalization": "leading www. removed on both Tranco and CrUX hostnames",
            "listed_n": sum(crux_labels.values()),
            "unlisted_n": len(crux_labels) - sum(crux_labels.values()),
            "groups": crux_summary(scored, crux_labels),
        },
        "derived_results": derived_results(scored, tiers),
    }

    premerge = DATA / "checkpoints" / "ckpt-pre-r3merge" / "results-gentle.jsonl"
    waves = {"final_latest_wins": scored}
    if premerge.exists():
        initial_rows = load_rows(premerge)
        validate_rows(initial_rows, set(tiers), "initial gentle corpus")
        waves["initial_gentle"] = initial_rows
        reverify_path = DATA / "results-reverify.jsonl"
        if reverify_path.exists():
            summary["reverify_comparison"] = reverify_comparison(
                initial_rows, load_rows(reverify_path)
            )

    design_summary = {
        "estimand": "First 1M entries of Tranco list ZJQ6G, generated 2026-09-02; recorded download 2026-09-03",
        "caveat": (
            "Intervals include stratified sampling error only. They do not include "
            "scanner, network, threshold, selective-recheck, or measurement error."
        ),
        "waves": {},
    }
    for wave_name, wave_rows in waves.items():
        measures = {
            "checklist_score": design_estimate(wave_rows, tiers, lambda row: float(row["score"])),
            "no_bot_ua_http_200_success": design_estimate(
                wave_rows,
                tiers,
                lambda row: 1.0 if row.get("checks", {}).get("bot-ua-access") == "fail" else 0.0,
            ),
        }
        for check in CHECKS:
            measures[f"status_pass_{check}"] = design_estimate(
                wave_rows,
                tiers,
                lambda row, check=check: 1.0 if row.get("checks", {}).get(check) == "pass" else 0.0,
            )
        design_summary["waves"][wave_name] = {
            key: rounded_estimate(value) for key, value in measures.items()
        }
    if "initial_gentle" in waves:
        design_summary["two_wave_comparison"] = compare_waves(
            waves["initial_gentle"], waves["final_latest_wins"], tiers
        )

    with open(DATA / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    with open(DATA / "design_weighted_summary.json", "w") as f:
        json.dump(design_summary, f, indent=2)
    print(json.dumps({
        "summary_file": str(DATA / "summary.json"),
        "design_weighted_file": str(DATA / "design_weighted_summary.json"),
        "completed": summary["completed"],
        "mean_score": summary["mean_score"],
        "crux_listed_n": summary["crux_overlap"]["listed_n"],
        "weighted_waves": list(design_summary["waves"]),
    }, indent=2))

if __name__ == "__main__":
    main()
