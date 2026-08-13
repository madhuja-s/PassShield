import json
import os
from datetime import datetime


LOG_FILE = "password_logs.json"


def save_password_result(strength_result, breach_result):
    """
    Save privacy-preserving password analysis results.

    IMPORTANT:
    The original password is NEVER stored.
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

    save_password_result(
        test_strength,
        test_breach
    )

    print("Test log saved successfully.")