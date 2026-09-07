import json
import os
from collections import Counter, defaultdict
from datetime import datetime


LOG_FILE = "password_logs.json"


def load_logs():
    """
    Load all logged results. Returns an empty list if the log
    file doesn't exist yet (e.g. before anyone has checked a
    password) so the dashboard can still render safely.
    """

    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE, "r", encoding="utf-8") as file:

        try:
            return json.load(file)

        except json.JSONDecodeError:
            return []


def safe_average(values):
    """Average a list of numbers, returning 0 if the list is empty."""

    values = [v for v in values if v is not None]

    if not values:
        return 0

    return round(sum(values) / len(values), 2)


def compute_dashboard_stats():
    """
    Read every logged password check and turn it into the
    summary numbers the live dashboard page needs.

    Every log entry might not have every field -- older entries
    from before we added a feature won't have that feature's
    data -- so every lookup here uses .get() and skips entries
    that don't have what's needed for that particular stat.
    """

    logs = load_logs()

    total_checks = len(logs)

    # --- Strength + breach basics ---

    avg_strength_score = safe_average(
        [entry.get("strength_score") for entry in logs]
    )

    breach_count = sum(1 for entry in logs if entry.get("breached"))

    breach_rate = round(
        (breach_count / total_checks) * 100, 1
    ) if total_checks else 0

    strength_category_counts = Counter(
        entry.get("strength_category", "Unknown") for entry in logs
    )

    # --- Algorithm comparison ---

    comparison_entries = [
        entry["comparison"] for entry in logs if "comparison" in entry
    ]

    avg_algorithm_scores = {
        "zxcvbn": safe_average(
            [c.get("zxcvbn_score") for c in comparison_entries]
        ),
        "entropy": safe_average(
            [c.get("entropy_score") for c in comparison_entries]
        ),
        "rule_based": safe_average(
            [c.get("rule_based_score") for c in comparison_entries]
        )
    }

    avg_agreement_score = safe_average(
        [c.get("agreement_score") for c in comparison_entries]
    )

    disagreement_count = sum(
        1 for c in comparison_entries if c.get("disagreement_flag")
    )

    disagreement_rate = round(
        (disagreement_count / len(comparison_entries)) * 100, 1
    ) if comparison_entries else 0

    # --- Reuse + leakage rates ---

    reuse_entries = [entry["reuse"] for entry in logs if "reuse" in entry]

    reused_count = sum(
        1 for r in reuse_entries
        if r.get("is_exact_repeat") or r.get("is_similar_variation")
    )

    reuse_rate = round(
        (reused_count / len(reuse_entries)) * 100, 1
    ) if reuse_entries else 0

    leakage_entries = [
        entry["leakage"] for entry in logs
        if "leakage" in entry and entry["leakage"].get("checked")
    ]

    leaked_count = sum(
        1 for l in leakage_entries if l.get("has_leakage")
    )

    leakage_rate = round(
        (leaked_count / len(leakage_entries)) * 100, 1
    ) if leakage_entries else 0

    # --- A/B nudge experiment ---

    variant_counts = Counter(
        entry.get("ab_variant") for entry in logs if entry.get("ab_variant")
    )

    improvement_by_variant = {}

    for variant in ["A", "B"]:

        variant_entries = [
            entry for entry in logs
            if entry.get("ab_variant") == variant
            and "ab_improved_since_last_check" in entry
        ]

        improved_count = sum(
            1 for entry in variant_entries
            if entry["ab_improved_since_last_check"]
        )

        improvement_by_variant[variant] = round(
            (improved_count / len(variant_entries)) * 100, 1
        ) if variant_entries else 0

    # --- Checks over time (by day) ---

    checks_by_day = defaultdict(int)

    for entry in logs:

        timestamp = entry.get("timestamp")

        if timestamp:

            day = timestamp[:10]  # "YYYY-MM-DD" prefix of the ISO timestamp
            checks_by_day[day] += 1

    checks_over_time = [
        {"date": day, "count": count}
        for day, count in sorted(checks_by_day.items())
    ]

    return {
        "total_checks": total_checks,
        "avg_strength_score": avg_strength_score,
        "breach_count": breach_count,
        "breach_rate": breach_rate,
        "strength_category_counts": dict(strength_category_counts),
        "avg_algorithm_scores": avg_algorithm_scores,
        "avg_agreement_score": avg_agreement_score,
        "disagreement_rate": disagreement_rate,
        "reuse_rate": reuse_rate,
        "leakage_rate": leakage_rate,
        "variant_counts": dict(variant_counts),
        "improvement_by_variant": improvement_by_variant,
        "checks_over_time": checks_over_time,
        "last_updated": datetime.now().strftime("%H:%M:%S")
    }


# Run only when this file is executed directly
if __name__ == "__main__":

    import pprint

    pprint.pprint(compute_dashboard_stats())