from zxcvbn import zxcvbn


# Plain-language labels for each attack scenario, ordered from
# the slowest/easiest-to-defend-against attacker to the
# fastest/hardest-to-defend-against attacker
SCENARIO_LABELS = {
    "online_throttling_100_per_hour":
        "Someone guessing on a login page (with limits on tries)",

    "online_no_throttling_10_per_second":
        "Someone guessing on a login page (no limits on tries)",

    "offline_slow_hashing_1e4_per_second":
        "Your password file gets stolen (well protected)",

    "offline_fast_hashing_1e10_per_second":
        "Your password file gets stolen (poorly protected)"
}


def estimate_crack_times(password):
    """
    Return crack-time estimates across multiple attacker scenarios,
    from a rate-limited online attacker up to a well-resourced
    offline attacker with fast hardware.

    zxcvbn already computes these under the hood; this module just
    reshapes them into a scenario-by-scenario view for the results
    page instead of showing a single number.
    """

    result = zxcvbn(password)

    display_times = result["crack_times_display"]
    raw_seconds = result["crack_times_seconds"]

    scenarios = []

    for key, label in SCENARIO_LABELS.items():

        scenarios.append({
            "scenario": label,
            "display_time": display_times[key],
            "seconds": float(raw_seconds[key])
        })

    return {
        "scenarios": scenarios,
        "fastest_crack_display": scenarios[-1]["display_time"],
        "slowest_crack_display": scenarios[0]["display_time"]
    }


# Run only when this file is executed directly
if __name__ == "__main__":

    password = input("Enter a password to test: ")

    result = estimate_crack_times(password)

    print("\n--- Multi-Scenario Crack-Time Estimate ---\n")

    for scenario in result["scenarios"]:

        print(scenario["scenario"])
        print("  Estimated time to crack:", scenario["display_time"])
        print()