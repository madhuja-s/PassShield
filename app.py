from flask import Flask, request

from strength_checker import calculate_strength
from breach_checker import check_password_breach


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    result = None

    if request.method == "POST":

        password = request.form.get("password")

        if password:

            # Check password strength
            strength_result = calculate_strength(password)

            # Check password breach exposure
            breach_result = check_password_breach(password)

            # Combine both results
            result = {
                "strength": strength_result,
                "breach": breach_result
            }

    return f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>PassShield</title>

    </head>

    <body>

        <h1>PassShield</h1>

        <h2>Password Security Checker</h2>

        <form method="POST">

            <label>
                Enter your password:
            </label>

            <input
                type="password"
                name="password"
                required
            >

            <button type="submit">
                Check Password
            </button>

        </form>

        {
            f'''
            <hr>

            <h2>Security Results</h2>

            <h3>
                Password Strength:
                {result["strength"]["strength"]}
            </h3>

            <p>
                Strength Score:
                {result["strength"]["score"]}/4
            </p>

            <h3>Custom Checks</h3>

            <ul>
                {
                    "".join(
                        f"<li>{check}: {'PASS' if passed else 'FAIL'}</li>"
                        for check, passed
                        in result["strength"]["custom_checks"].items()
                    )
                }
            </ul>

            <h3>Breach Check</h3>

            {
                f'''
                <p>
                    WARNING: This password has appeared in
                    {result["breach"]["breach_count"]} known breaches.
                </p>
                '''
                if result["breach"]["breached"]
                else
                '''
                <p>
                    Good news: This password was not found
                    in known breaches.
                </p>
                '''
                if result["breach"]["success"]
                else
                f'''
                <p>
                    Breach check could not be completed.
                </p>
                <p>
                    Error: {result["breach"]["error"]}
                </p>
                '''
            }

            '''
            if result
            else ""
        }

    </body>

    </html>
    """


if __name__ == "__main__":

    app.run(debug=True)