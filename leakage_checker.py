def build_context_fragments(name=None, birth_year=None):
    """
    Turn optional user-supplied context into a set of lowercase
    fragments to search for inside the password.

    Both inputs are optional -- if neither is provided, this
    check is simply skipped (see check_personal_info_leakage).
    Nothing here is ever stored; it only exists for the length
    of this one request.
    """

    fragments = {}

    if name:

        clean_name = name.strip().lower()

        if len(clean_name) >= 3:

            fragments["name"] = clean_name
            fragments["name_reversed"] = clean_name[::-1]

    if birth_year:

        birth_year = str(birth_year).strip()

        if len(birth_year) == 4 and birth_year.isdigit():

            fragments["birth_year_full"] = birth_year
            # Common shorthand: last two digits, e.g. 2005 -> "05"
            fragments["birth_year_short"] = birth_year[-2:]

    return fragments


def check_personal_info_leakage(password, name=None, birth_year=None):
    """
    Check whether the password contains fragments of optional,
    user-supplied personal context (name, birth year).

    This is entirely opt-in: if the user leaves both fields
    blank, the check is skipped and nothing is evaluated.
    """

    fragments = build_context_fragments(name, birth_year)

    if not fragments:

        return {
            "checked": False,
            "has_leakage": False,
            "leaks_found": []
        }

    password_lower = password.lower()

    leaks_found = []

    labels = {
        "name": "your name",
        "name_reversed": "your name spelled backwards",
        "birth_year_full": "your birth year",
        "birth_year_short": "your birth year (shortened)"
    }

    for key, fragment in fragments.items():

        if fragment and fragment in password_lower:
            leaks_found.append(labels[key])

    return {
        "checked": True,
        "has_leakage": len(leaks_found) > 0,
        "leaks_found": leaks_found
    }


# Run only when this file is executed directly
if __name__ == "__main__":

    password = input("Enter a password to test: ")
    name = input("Your name (optional, press Enter to skip): ")
    birth_year = input("Your birth year (optional, press Enter to skip): ")

    result = check_personal_info_leakage(
        password,
        name=name or None,
        birth_year=birth_year or None
    )

    print("\n--- Personal-Info Leakage Check ---")

    if not result["checked"]:
        print("No context provided -- check skipped.")

    elif result["has_leakage"]:
        print("This password appears to contain:")

        for leak in result["leaks_found"]:
            print(" -", leak)

    else:
        print("No personal-info leakage detected.")