"""Generate educational phishing templates."""


def generate_template(tactic: str) -> str:
    """Return a plain-text educational template for the given tactic.

    Args:
        tactic (str): One of 'spoofing', 'typosquatting', 'urgency', 'social_engineering'

    Returns:
        str: Formatted template or error message for unknown tactic.

    Examples:
        generate_template('spoofing')
    """
    t = (tactic or "").lower()
    if t == "spoofing":
        return (
            "EDUCATIONAL TEMPLATE: Email Spoofing\n"
            "--------------------------------------------------\n"
            "From: CEO <ceo@companny.com>\n"
            "Subject: Urgent: Wire transfer required\n"
            "\n"
            "Example:\n"
            "From: "
            "\n"
            "A malicious actor forges the From header so the email appears to come from a trusted executive.\n"
            "Why it works: Attackers spoof display names and subtle domain typos to exploit trust.\n"
            "Defense: Verify sender email addresses, check full headers, call the sender via known numbers.\n"
        )
    if t == "typosquatting":
        return (
            "EDUCATIONAL TEMPLATE: Typosquatting\n"
            "--------------------------------------------------\n"
            "Examples:\n"
            "  goog1e.com  (vs google.com)\n"
            "  amaz0n.com  (vs amazon.com)\n"
            "\n"
            "Explanation: Single-character substitutions or homoglyphs look similar in the UI.\n"
            "Defense: Check domain carefully, hover links, use bookmarks for critical sites.\n"
        )
    if t == "urgency":
        return (
            "EDUCATIONAL TEMPLATE: Urgency-Based Attack\n"
            "--------------------------------------------------\n"
            "Subject: URGENT: Verify Your Account Immediately\n"
            "Body: Your account will be REVOKED in 24 hours unless you verify immediately.\n"
            "\n"
            "Explanation: Attacker pressures the user to bypass normal verification steps.\n"
            "Defense: Legitimate organizations do not force immediate action by email; verify independently.\n"
        )
    if t == "social_engineering":
        return (
            "EDUCATIONAL TEMPLATE: Social Engineering\n"
            "--------------------------------------------------\n"
            "Example fake form:\n"
            "  Please enter your email and password here to re-activate your account:\n"
            "  [Email]\n"
            "  [Password]\n"
            "\n"
            "Explanation: Attackers create urgency and authority to collect credentials.\n"
            "Defense: Never provide passwords via email; use official channels and MFA.\n"
        )
    return f"Error: Unknown template type '{tactic}'. Supported: spoofing, typosquatting, urgency, social_engineering"
