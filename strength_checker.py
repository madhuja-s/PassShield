from zxcvbn import zxcvbn


def custom_password_checks(password):
    """
    Perform additional rule-based checks.
    """

    checks = {
        "minimum_length": len(password) >= 8,
        "has_uppercase": any(char.isupper() for char in password),
        "has_lowercase": any(char.islower() for char in password),
        "has_digit": any(char.isdigit() for char in password),
        "has_special_character": any(
            not char.isalnum() for char in password
        )
    }

    return checks


def calculate_strength(password):
    """
    Calculate password strength using:
    1. zxcvbn
    2. Custom rule-based checks
    """

    # Analyze password using zxcvbn
    zxcvbn_result = zxcvbn(password)

    # zxcvbn gives a score from 0 to 4
    zxcvbn_score = zxcvbn_result["score"]

    # Run our custom checks
    custom_checks = custom_password_checks(password)

    # Count the rules that passed
    rules_passed = sum(custom_checks.values())

    # Convert custom rules to a 0-4 score
    rule_score = (
        rules_passed / len(custom_checks)
    ) * 4

    # Combine both scores
    final_score = round(
        (zxcvbn_score + rule_score) / 2,
        2
    )

    # Convert score into a readable category
    if final_score < 1:
        strength = "Very Weak"

    elif final_score < 2:
        strength = "Weak"

    elif final_score < 3:
        strength = "Moderate"

    elif final_score < 4:
        strength = "Strong"

    else:
        strength = "Very Strong"

    return {
        "strength": strength,
        "score": final_score,
        "zxcvbn_score": zxcvbn_score,
        "custom_checks": custom_checks,
        "feedback": zxcvbn_result["feedback"]
    }


# Run only when this file is executed directly
if __name__ == "__main__":

    password = input("Enter a password to test: ")

    result = calculate_strength(password)

    print("\n--- PassShield Password Analysis ---")

    print("Strength:", result["strength"])

    print("Score:", result["score"], "/ 4")

    print(
        "zxcvbn Score:",
        result["zxcvbn_score"],
        "/ 4"
    )

    print("\nCustom Checks:")

    for check, passed in result["custom_checks"].items():

        if passed:
            status = "PASS"
        else:
            status = "FAIL"

        print(check, ":", status)

    print("\nFeedback:")

    warning = result["feedback"]["warning"]

    if warning:
        print("Warning:", warning)

    suggestions = result["feedback"]["suggestions"]

    for suggestion in suggestions:
        print("-", suggestion)