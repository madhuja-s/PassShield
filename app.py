from flask import Flask, request, render_template

from strength_checker import calculate_strength
from breach_checker import check_password_breach
from data_store import save_password_result


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "GET":
        return render_template("index.html")

    password = request.form.get("password")

    if not password:
        return render_template("index.html")

    # Check password strength
    strength_result = calculate_strength(password)

    # Check password breach exposure
    breach_result = check_password_breach(password)

    # Save privacy-preserving results
    save_password_result(
    strength_result,
    breach_result
)

    # Display results
    return render_template(
        "result.html",
        strength=strength_result,
        breach=breach_result
    )


if __name__ == "__main__":
    app.run(debug=True)