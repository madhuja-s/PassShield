from flask import Flask, request, render_template, session, jsonify

from strength_checker import calculate_strength
from breach_checker import check_password_breach
from comparison import compare_algorithms
from crack_time import estimate_crack_times
from passphrase_generator import suggest_passphrases
from reuse_detector import check_reuse
from leakage_checker import check_personal_info_leakage
from ab_experiment import assign_variant, get_nudge_message, track_improvement
from data_store import save_password_result
from analytics import compute_dashboard_stats


app = Flask(__name__)

# Required for Flask sessions (used by reuse_detector.py to
# remember hashed passwords checked earlier in this session).
# For a class/portfolio project this is fine; for a real
# deployment this should come from an environment variable
# instead of being hardcoded.
app.secret_key = "passshield-dev-secret-key-change-if-deploying"


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "GET":
        return render_template("index.html")

    password = request.form.get("password")

    if not password:
        return render_template("index.html")

    # Check password strength (existing blended zxcvbn + rules score)
    strength_result = calculate_strength(password)

    # Run all three algorithms side by side for the comparison view
    comparison_result = compare_algorithms(password)

    # Multi-scenario crack-time estimate
    crack_time_result = estimate_crack_times(password)

    # Check whether this password (or a close variation of it)
    # was already checked earlier in this browser session
    reuse_result = check_reuse(password, session)

    # Optional personal-info leakage check -- only runs if the
    # user filled in the optional name/birth-year fields
    name_input = request.form.get("name")
    birth_year_input = request.form.get("birth_year")

    leakage_result = check_personal_info_leakage(
        password,
        name=name_input or None,
        birth_year=birth_year_input or None
    )

    # Check password breach exposure
    breach_result = check_password_breach(password)

    # Offer passphrase alternatives whenever the password is weak
    # OR it's "risky" for reasons the raw score can't see -- a
    # breached password, or one that leaks personal information
    passphrase_suggestions = None

    is_risky = (
        strength_result["score"] < 2
        or breach_result.get("breached")
        or leakage_result["has_leakage"]
    )

    if is_risky:
        passphrase_suggestions = suggest_passphrases()

    # A/B nudge experiment: assign (or reuse) this session's
    # variant, track whether this check improved on the last one,
    # and build the nudge message -- shown only to Variant B
    ab_variant = assign_variant(session)

    improvement_result = track_improvement(session, strength_result["score"])

    nudge_message = None

    if ab_variant == "B":
        nudge_message = get_nudge_message(strength_result["score"])

    # Save privacy-preserving results, including the new-feature outcomes
    save_password_result(
        strength_result,
        breach_result,
        comparison_result,
        crack_time_result=crack_time_result,
        reuse_result=reuse_result,
        leakage_result=leakage_result,
        passphrase_offered=passphrase_suggestions is not None,
        ab_variant=ab_variant,
        improvement_result=improvement_result
    )

    # Display results
    return render_template(
        "result.html",
        strength=strength_result,
        comparison=comparison_result,
        crack_time=crack_time_result,
        passphrase_suggestions=passphrase_suggestions,
        reuse=reuse_result,
        leakage=leakage_result,
        breach=breach_result,
        nudge_message=nudge_message
    )


@app.route("/dashboard")
def dashboard():
    """
    Live analytics page. The page itself just loads once; the
    numbers and charts on it refresh automatically by polling
    /dashboard-data every few seconds (see dashboard.html).
    """

    return render_template("dashboard.html")


@app.route("/dashboard-data")
def dashboard_data():
    """
    JSON endpoint the dashboard page polls. Recomputes stats
    fresh from password_logs.json on every call, so the numbers
    are always current as of the moment they're requested.
    """

    return jsonify(compute_dashboard_stats())


if __name__ == "__main__":
    app.run(debug=True)