import hashlib
import requests


HIBP_API_URL = "https://api.pwnedpasswords.com/range/"


def check_password_breach(password):
    """
    Check whether a password has appeared in known data breaches.

    Uses the Have I Been Pwned k-anonymity model:
    - The password is hashed locally using SHA-1.
    - Only the first 5 characters of the hash are sent to HIBP.
    - The complete password and complete hash are never sent.
    """

    # Step 1: Create SHA-1 hash locally
    sha1_hash = hashlib.sha1(
        password.encode("utf-8")
    ).hexdigest().upper()

    # Step 2: Split the hash
    first_5_characters = sha1_hash[:5]
    remaining_hash = sha1_hash[5:]

    # Step 3: Send only the first 5 characters to HIBP
    url = HIBP_API_URL + first_5_characters

    try:

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

    except requests.RequestException as error:

        return {
            "success": False,
            "breached": False,
            "breach_count": 0,
            "error": str(error)
        }

    # Step 4: Search the returned hashes
    for line in response.text.splitlines():

        hash_suffix, count = line.split(":")

        if hash_suffix == remaining_hash:

            return {
                "success": True,
                "breached": True,
                "breach_count": int(count),
                "error": None
            }

    # Password was not found
    return {
        "success": True,
        "breached": False,
        "breach_count": 0,
        "error": None
    }


if __name__ == "__main__":

    password = input("Enter a password to check for breaches: ")

    result = check_password_breach(password)

    print("\n--- PassShield Breach Check ---")

    if not result["success"]:

        print("Unable to complete breach check.")
        print("Error:", result["error"])

    elif result["breached"]:

        print("WARNING: Password found in known breaches.")
        print("Times seen:", result["breach_count"])

    else:

        print("Good news: Password was not found in known breaches.The password is good to go!")