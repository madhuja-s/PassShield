import secrets


def assign_variant(session):
    """
    Assign this browser session to Variant A (control, plain meter)
    or Variant B (meter + behavioral nudge), 50/50, and keep it
    fixed for the rest of the session so a user doesn't flip
    between variants on repeated checks.
    """

    if "ab_variant" not in session:
        session["ab_variant"] = secrets.choice(["A", "B"])

    return session["ab_variant"]


def get_nudge_message(score):
    """
    Behavioral nudge shown only to Variant B, only when the
    password isn't already strong. Messages are deliberately
    concrete and action-oriented rather than a generic "try
    harder" -- that's the whole point being tested.
    """

    if score < 2:

        return (
            "Weak passwords are the single biggest cause of account "
            "takeovers. Switching to one of the suggestions below "
            "takes under 10 seconds and removes most of that risk."
        )

    elif score <= 3:

        return (
            "You're close to a strong password. A few extra "
            "characters or a passphrase instead would make it "
            "far harder to crack."
        )

    # Already strong -- no nudge needed
    return None


def track_improvement(session, current_score):
    """
    Compare this check's score against the score from this
    session's previous check, to see whether the user's next
    password choice actually got stronger.

    Only the numeric score is kept in the session (no password,
    no hash needed here) -- reuse_detector.py already handles
    the hash-based reuse tracking separately.
    """

    previous_score = session.get("ab_last_score")

    is_first_check = previous_score is None

    improved = None

    if not is_first_check:
        improved = current_score > previous_score

    # Update the session with this check's score for next time
    session["ab_last_score"] = current_score

    return {
        "is_first_check": is_first_check,
        "previous_score": previous_score,
        "current_score": current_score,
        "improved": improved
    }


# Simple standalone test using a plain dict in place of a Flask session
if __name__ == "__main__":

    fake_session = {}

    variant = assign_variant(fake_session)

    print("Assigned variant:", variant)

    for score in [1.0, 1.0, 2.5, 3.6]:

        result = track_improvement(fake_session, score)

        nudge = get_nudge_message(score) if variant == "B" else None

        print("\nScore:", score)
        print("  ", result)

        if nudge:
            print("  Nudge shown:", nudge)