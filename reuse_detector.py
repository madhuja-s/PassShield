import hashlib


# Cap how many past checks we remember per session, so the
# session data doesn't grow without bound during a long session
MAX_HISTORY = 20


def hash_value(value):
    """
    SHA-256 hash of a string, returned as hex. Used for both
    the exact-match hash and the skeleton hash below -- neither
    can be reversed back into the original password.
    """

    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def get_skeleton(password):
    """
    Strip a password down to just its lowercase letters.

    This intentionally collapses common password *variations*
    onto the same skeleton, e.g. "Password1", "password2!",
    and "PASSWORD!!" all reduce to "password". Hashing that
    skeleton lets us detect "this is a tweak of something you
    already checked" without ever storing anything close to
    the original password.
    """

    letters_only = [char.lower() for char in password if char.isalpha()]

    return "".join(letters_only)


def check_reuse(password, session):
    """
    Compare the current password against this session's history
    of previously checked passwords (stored as hashes only).

    session is expected to be Flask's session object (or any
    dict-like object) -- this function reads and writes
    session["password_history"].

    Returns a result dict, and also updates the session history
    as a side effect.
    """

    exact_hash = hash_value(password)
    skeleton_hash = hash_value(get_skeleton(password))

    history = session.get("password_history", [])

    is_exact_repeat = any(
        entry["exact_hash"] == exact_hash for entry in history
    )

    is_similar_variation = any(
        entry["skeleton_hash"] == skeleton_hash
        and entry["exact_hash"] != exact_hash
        for entry in history
    )

    # Record this check for future comparisons in the session
    history.append({
        "exact_hash": exact_hash,
        "skeleton_hash": skeleton_hash
    })

    # Keep only the most recent MAX_HISTORY entries
    session["password_history"] = history[-MAX_HISTORY:]

    return {
        "is_exact_repeat": is_exact_repeat,
        "is_similar_variation": is_similar_variation,
        "checks_this_session": len(session["password_history"])
    }


# Simple standalone test using a plain dict in place of a Flask session
if __name__ == "__main__":

    fake_session = {}

    while True:

        password = input("Enter a password to test (blank to stop): ")

        if not password:
            break

        result = check_reuse(password, fake_session)

        print("\n--- Reuse Check ---")

        if result["is_exact_repeat"]:
            print("You checked this exact password already this session.")

        elif result["is_similar_variation"]:
            print("This looks like a variation of a password you already checked.")

        else:
            print("This is a new password pattern for this session.")

        print("Checks so far:", result["checks_this_session"], "\n")