def rule_based_checks(password):
    """
    NIST-style composition checks. These mirror the checks in
    strength_checker.py so the rule-based algorithm can be
    scored on its own, independent of zxcvbn.
    """

    checks = {
        "minimum_length": len(password) >= 8,
        "good_length": len(password) >= 12,
        "has_uppercase": any(char.isupper() for char in password),
        "has_lowercase": any(char.islower() for char in password),
        "has_digit": any(char.isdigit() for char in password),
        "has_special_character": any(
            not char.isalnum() for char in password
        )
    }

    return checks


def score_to_category(score):

    if score < 1:
        return "Very Weak"

    elif score < 2:
        return "Weak"

    elif score < 3:
        return "Moderate"

    elif score < 4:
        return "Strong"

    else:
        return "Very Strong"


def rule_based_score(password):
    """
    Standalone rule-based / NIST composition score, expressed
    on the same 0-4 scale as zxcvbn and the entropy algorithm.
    """

    checks = rule_based_checks(password)

    rules_passed = sum(checks.values())

    total_rules = len(checks)

    # Scale rules passed onto a 0-4 range
    score = round((rules_passed / total_rules) * 4, 2)

    return {
        "algorithm": "Rule-Based (NIST-style)",
        "score": score,
        "category": score_to_category(score),
        "checks": checks,
        "rules_passed": rules_passed,
        "total_rules": total_rules
    }


# Run only when this file is executed directly
if __name__ == "__main__":

    password = input("Enter a password to test: ")

    result = rule_based_score(password)

    print("\n--- Rule-Based (NIST-style) Analysis ---")

    print("Score:", result["score"], "/ 4")
    print("Category:", result["category"])

    print("\nChecks:")

    for check, passed in result["checks"].items():

        status = "PASS" if passed else "FAIL"

        print(check, ":", status)