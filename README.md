# PassShield

**An Integrated Password Security and Behavioral Risk Analytics System**

PassShield is a Flask web application that evaluates password strength using three independent algorithms, checks for breach exposure via a privacy-preserving API, layers on four behavioral security features, and runs an A/B experiment to test whether behavioral nudges actually improve password choices — all backed by a Power BI dashboard and a live in-app analytics page.

---

## Features

- **Three-algorithm strength comparison** — zxcvbn (pattern/dictionary-based), Shannon entropy (randomness-based), and rule-based/NIST composition checking, run side by side with an agreement/disagreement score
- **Privacy-preserving breach detection** — checks HaveIBeenPwned via the k-anonymity model; only the first 5 characters of a SHA-1 hash ever leave the device
- **Reused/similar-password detection** — flags exact repeats and pattern variations within a browser session using hashed "skeletons," never raw passwords
- **Multi-scenario crack-time estimate** — shows how drastically crack time changes across four attacker capability levels
- **Passphrase suggestion generator** — offline Diceware-style generator (2048-word list) for weak or risky passwords
- **Personal-info leakage check** — optional, never-stored check for whether a password contains the user's name or birth year
- **A/B nudge experiment** — randomly assigns each session to a control or nudge-message variant, tracking whether within-session password choices improve
- **Dual analytics dashboards** — a Power BI dashboard for formal reporting, and a live in-app dashboard (`/dashboard`) that auto-refreshes every 5 seconds

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript, Chart.js |
| Strength algorithms | zxcvbn, custom Shannon entropy, custom rule-based checker |
| Breach detection | HaveIBeenPwned API (k-anonymity) |
| Analytics | Power BI, custom Flask live dashboard |
| Data storage | JSON (anonymized, no raw passwords) |

---

## Project Structure

```
PassShield/
├── app.py                    # Flask routes and request handling
├── strength_checker.py       # Base strength score (zxcvbn + rule blend)
├── entropy_checker.py        # Shannon entropy algorithm
├── rule_checker.py           # Rule-based/NIST composition algorithm
├── comparison.py             # Runs all 3 algorithms, computes agreement score
├── breach_checker.py         # HaveIBeenPwned k-anonymity breach check
├── crack_time.py             # Multi-scenario crack-time estimator
├── passphrase_generator.py   # Diceware-style passphrase suggestions
├── reuse_detector.py         # Session-based reused/similar password detection
├── leakage_checker.py        # Optional personal-info leakage check
├── ab_experiment.py          # A/B nudge experiment logic
├── analytics.py              # Computes stats for the live dashboard
├── data_store.py             # Anonymized JSON logging
├── templates/
│   ├── index.html            # Password input form
│   ├── result.html           # Full results page
│   └── dashboard.html        # Live analytics dashboard
└── static/
    └── style.css
```

---

## Setup

1. Clone the repository and create a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\Activate.ps1        # Windows PowerShell
   ```

2. Install dependencies:
   ```
   pip install flask zxcvbn requests
   ```

3. Run the app:
   ```
   python app.py
   ```

4. Open in your browser:
   - Main app: `http://127.0.0.1:5000/`
   - Live dashboard: `http://127.0.0.1:5000/dashboard`

---

## How the Algorithm Comparison Works

Most password checkers rely on a single scoring method. PassShield runs three independent algorithms on every password and computes an **agreement score** — the closer the three scores are to each other, the higher the agreement. When they diverge significantly, the result page flags it explicitly. This surfaces real cases where a password satisfies every composition rule (uppercase, digit, symbol) but is still highly guessable by pattern-based analysis, or vice versa.

## How the A/B Experiment Works

Each browser session is randomly and persistently assigned to:
- **Variant A (control)** — standard results page, no additional messaging
- **Variant B (nudge)** — same results page, plus a contextual behavioral message when the password isn't already strong

Within-session improvement is tracked by comparing each check's score against the same session's previous check, logged per variant. This is a **within-session** test (comparing a user's successive checks in one sitting), not a cross-user longitudinal study, since the app has no persistent accounts.

## Privacy Design

- Raw passwords are never stored, logged, or transmitted in full at any point
- Breach checking uses k-anonymity — only a 5-character hash prefix is sent externally
- Reuse detection compares hashed "skeletons" of passwords, never the passwords themselves
- Personal-info leakage checking is entirely optional and the input is never persisted
- Only derived, non-identifying attributes (scores, categories, boolean flags, timestamps) are written to `password_logs.json`

---

## Known Limitations

- The A/B experiment is session-scoped, not a true cross-user longitudinal study
- Live dashboard statistics are aggregate averages; a single new check has limited visible effect on them once enough historical data exists
- `app.secret_key` in `app.py` is a hardcoded placeholder suitable for local development only — a real deployment should load this from an environment variable

---

## Future Enhancements

- Cross-session/account-based tracking for a true longitudinal A/B test
- Machine-learning-based strength classifier as a fourth comparison algorithm
- Real-time push to Power BI via streaming datasets (currently requires manual/scheduled refresh)