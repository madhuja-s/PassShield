from zxcvbn import zxcvbn

from entropy_checker import calculate_entropy_strength
from rule_checker import rule_based_score


def zxcvbn_only_score(password):
    """
    Standalone zxcvbn result, kept separate from the blended
    score in strength_checker.py, so it can sit side by side
    with the other two algorithms in the comparison view.
    """

    result = zxcvbn(password)

    score = result["score"]

    categories = {
        0: "Very Weak",
        1: "Weak",
        2: "Moderate",
        3: "Strong",
        4: "Very Strong"
    }

    return {
        "algorithm": "zxcvbn",
        "score": score,
        "category": categories.get(score, "Unknown"),
        "crack_time_display":
            result["crack_times_display"]["offline_slow_hashing_1e4_per_second"]
    }


def calculate_agreement_score(scores):
    """
    Simple agreement metric: how close the three algorithm
    scores are to each other, expressed as a 0-100 percentage.

    Spread of 0 (all algorithms agree exactly) = 100% agreement.
    Max possible spread on a 0-4 scale is 4, so we scale against
    that.
    """

    spread = max(scores) - min(scores)

    agreement_percent = round((1 - (spread / 4)) * 100)

    return max(agreement_percent, 0)


def compare_algorithms(password):
    """
    Runs all three password-strength algorithms and returns a
    single structured result for the comparison view:

    1. zxcvbn          - pattern/dictionary-aware guessability
    2. Shannon entropy - naive randomness-based baseline
    3. Rule-based/NIST - composition/policy-based scoring
    """

    zxcvbn_result = zxcvbn_only_score(password)
    entropy_result = calculate_entropy_strength(password)
    rule_result = rule_based_score(password)

    scores = [
        zxcvbn_result["score"],
        entropy_result["score"],
        rule_result["score"]
    ]

    agreement = calculate_agreement_score(scores)

    # Flag if the algorithms substantially disagree
    disagreement_flag = agreement < 60

    return {
        "zxcvbn": zxcvbn_result,
        "entropy": entropy_result,
        "rule_based": rule_result,
        "agreement_score": agreement,
        "disagreement_flag": disagreement_flag
    }


# Run only when this file is executed directly
if __name__ == "__main__":

    password = input("Enter a password to test: ")

    result = compare_algorithms(password)

    print("\n--- PassShield Algorithm Comparison ---\n")

    print("zxcvbn:      ", result["zxcvbn"]["score"], "/ 4  -", result["zxcvbn"]["category"])
    print("Entropy:     ", result["entropy"]["score"], "/ 4  -", result["entropy"]["category"])
    print("Rule-based:  ", result["rule_based"]["score"], "/ 4  -", result["rule_based"]["category"])

    print("\nAgreement score:", result["agreement_score"], "%")

    if result["disagreement_flag"]:
        print("The algorithms disagree significantly on this password.")
    else:
        print("The algorithms are broadly in agreement.")