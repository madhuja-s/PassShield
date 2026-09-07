import json
import os
from datetime import datetime


LOG_FILE = "password_logs.json"


def save_password_result(
    strength_result,
    breach_result,
    comparison_result=None,
    crack_time_result=None,
    reuse_result=None,
    leakage_result=None,
    passphrase_offered=False,
    ab_variant=None,
    improvement_result=None
):
    """
    Save privacy-preserving password analysis results.

    IMPORTANT:
    The original password is NEVER stored.

    All the new-feature arguments are optional, so this still
    works anywhere the older call (with fewer arguments) is used.
    """

    # Create a log entry using only derived information
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "password_length": strength_result.get("password_length"),
        "strength_score": strength_result.get("score"),
        "zxcvbn_score": strength_result.get("zxcvbn_score"),
        "strength_category": strength_result.get("strength"),
        "custom_checks": strength_result.get("custom_checks"),
        "breached": breach_result.get("breached"),
        "breach_count": breach_result.get("breach_count")
    }

    # Multi-algorithm comparison fields
    if comparison_result:

        log_entry["comparison"] = {
            "zxcvbn_score": comparison_result["zxcvbn"]["score"],
            "entropy_score": comparison_result["entropy"]["score"],
            "entropy_bits": comparison_result["entropy"]["total_entropy_bits"],
            "rule_based_score": comparison_result["rule_based"]["score"],
            "agreement_score": comparison_result["agreement_score"],
            "disagreement_flag": comparison_result["disagreement_flag"]
        }

    # Crack-time fields -- only the fastest and slowest scenario
    # are logged, since the full breakdown is only needed on the
    # results page itself, not for dashboard-level analytics
    if crack_time_result:

        log_entry["crack_time"] = {
            "fastest_scenario_display": crack_time_result["fastest_crack_display"],
            "slowest_scenario_display": crack_time_result["slowest_crack_display"]
        }

    # Reuse/similar-password detection fields
    if reuse_result:

        log_entry["reuse"] = {
            "is_exact_repeat": reuse_result["is_exact_repeat"],
            "is_similar_variation": reuse_result["is_similar_variation"]
        }

    # Personal-info leakage fields -- only whether it was checked
    # and whether anything leaked; the actual name/birth year are
    # never logged, only the yes/no outcome
    if leakage_result:

        log_entry["leakage"] = {
            "checked": leakage_result["checked"],
            "has_leakage": leakage_result["has_leakage"]
        }

    # Whether a passphrase alternative was offered for this password
    log_entry["passphrase_offered"] = passphrase_offered

    # A/B nudge experiment fields -- which variant this session saw,
    # and whether this check scored higher than this session's
    # previous check (the actual behavioral outcome being measured)
    if ab_variant:

        log_entry["ab_variant"] = ab_variant

        if improvement_result and not improvement_result["is_first_check"]:

            log_entry["ab_improved_since_last_check"] = improvement_result["improved"]

    # Read existing logs
    if os.path.exists(LOG_FILE):

        with open(LOG_FILE, "r", encoding="utf-8") as file:

            try:
                logs = json.load(file)

            except json.JSONDecodeError:
                logs = []

    else:
        logs = []

    # Add the new result
    logs.append(log_entry)

    # Save the updated logs
    with open(LOG_FILE, "w", encoding="utf-8") as file:

        json.dump(
            logs,
            file,
            indent=4
        )


# Test the data storage system
if __name__ == "__main__":

    test_strength = {
        "password_length": 16,
        "score": 4,
        "zxcvbn_score": 4,
        "strength": "Very Strong",
        "custom_checks": {
            "minimum_length": True,
            "has_uppercase": True,
            "has_lowercase": True,
            "has_digit": True,
            "has_special_character": True
        }
    }

    test_breach = {
        "success": True,
        "breached": False,
        "breach_count": 0
    }

    test_comparison = {
        "zxcvbn": {"score": 4},
        "entropy": {"score": 3, "total_entropy_bits": 72.5},
        "rule_based": {"score": 4.0},
        "agreement_score": 83,
        "disagreement_flag": False
    }

    save_password_result(
        test_strength,
        test_breach,
        test_comparison
    )

    print("Test log saved successfully.")