import math
from collections import Counter


def calculate_shannon_entropy(password):
    """
    Calculate the Shannon entropy of a password based on
    the frequency of each character.

    Returns entropy in bits per character, and total entropy
    (bits per character * password length).
    """

    if not password:
        return {
            "entropy_per_char": 0,
            "total_entropy": 0
        }

    length = len(password)

    # Count how often each character appears
    frequencies = Counter(password)

    entropy_per_char = 0

    for count in frequencies.values():
        probability = count / length
        entropy_per_char -= probability * math.log2(probability)

    total_entropy = entropy_per_char * length

    return {
        "entropy_per_char": round(entropy_per_char, 3),
        "total_entropy": round(total_entropy, 3)
    }


def entropy_to_score(total_entropy):
    """
    Convert total entropy (bits) into a 0-4 score so it can be
    compared directly against zxcvbn and rule-based scores.

    These thresholds are the classical entropy-strength bands
    (roughly: <28 bits very weak ... 80+ bits very strong).
    """

    if total_entropy < 28:
        return 0

    elif total_entropy < 36:
        return 1

    elif total_entropy < 60:
        return 2

    elif total_entropy < 80:
        return 3

    else:
        return 4


def score_to_category(score):

    categories = {
        0: "Very Weak",
        1: "Weak",
        2: "Moderate",
        3: "Strong",
        4: "Very Strong"
    }

    return categories.get(score, "Unknown")


def calculate_entropy_strength(password):
    """
    Full entropy-based strength result, shaped to match the
    other algorithm modules (score, category, raw details) so
    comparison.py can treat all three algorithms the same way.
    """

    entropy_data = calculate_shannon_entropy(password)

    score = entropy_to_score(entropy_data["total_entropy"])

    return {
        "algorithm": "Shannon Entropy",
        "score": score,
        "category": score_to_category(score),
        "entropy_per_char": entropy_data["entropy_per_char"],
        "total_entropy_bits": entropy_data["total_entropy"]
    }


# Run only when this file is executed directly
if __name__ == "__main__":

    password = input("Enter a password to test: ")

    result = calculate_entropy_strength(password)

    print("\n--- Shannon Entropy Analysis ---")

    print("Entropy per character:", result["entropy_per_char"], "bits")
    print("Total entropy:", result["total_entropy_bits"], "bits")
    print("Score:", result["score"], "/ 4")
    print("Category:", result["category"])