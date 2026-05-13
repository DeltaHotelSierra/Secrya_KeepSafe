"""Generate educational phishing templates.

This module provides simple, human-readable templates for training and testing.
The main function `generate_template` can optionally save the generated template
to `phishing_tool/GENERATED_EMAILS/` so it can be analyzed later by the tool.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional


GENERATED_DIR = Path(__file__).resolve().parent / "GENERATED_EMAILS"


def _ensure_generated_dir() -> Path:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    return GENERATED_DIR


def _slugify(value: str) -> str:
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in value).strip("_.-") or "template"


def generate_template(tactic: str, *, save: bool = False, name: Optional[str] = None) -> str:
    """Return a plain-text educational template for the given tactic.

    Args:
        tactic: One of 'spoofing', 'typosquatting', 'urgency', 'social_engineering'
        save: If True, write the generated template to `phishing_tool/GENERATED_EMAILS/`.
        name: Optional filename prefix for the saved file.

    Returns:
        str: Formatted template text. If `save=True` the returned string will have a
        final line indicating the saved file path.
    """
    t = (tactic or "").lower()
    if t == "spoofing":
        text = (
            "EDUCATIONAL TEMPLATE: Email Spoofing\n"
            "--------------------------------------------------\n"
            "From: CEO <ceo@company.com>\n"
            "Subject: Urgent: Wire transfer required\n"
            "\n"
            "Example:\n"
            "From: Jane Doe <jane.doe@company.com>\n"
            "To: finance@company.com\n"
            "Subject: Urgent: approve wire transfer\n"
            "\n"
            "A malicious actor forges the From header so the email appears to come from a trusted executive.\n"
            "Why it works: Attackers spoof display names and use subtle domain typos to exploit trust.\n"
            "Defense: Verify sender email addresses, inspect full headers, and call known contacts on their published numbers.\n"
        )
    elif t == "typosquatting":
        text = (
            "EDUCATIONAL TEMPLATE: Typosquatting\n"
            "--------------------------------------------------\n"
            "Examples:\n"
            "  goog1e.com  (vs google.com)\n"
            "  amaz0n.com  (vs amazon.com)\n"
            "\n"
            "Explanation: Single-character substitutions or homoglyphs look similar in the UI.\n"
            "Defense: Check domain carefully, hover links, and use bookmarks for critical sites.\n"
        )
    elif t == "urgency":
        text = (
            "EDUCATIONAL TEMPLATE: Urgency-Based Attack\n"
            "--------------------------------------------------\n"
            "Subject: URGENT: Verify Your Account Immediately\n"
            "Body: Your account will be REVOKED in 24 hours unless you verify immediately.\n"
            "\n"
            "Explanation: Attacker pressures the user to bypass normal verification steps.\n"
            "Defense: Legitimate organizations do not force immediate action by email; verify independently.\n"
        )
    elif t == "social_engineering":
        text = (
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
    else:
        return f"Error: Unknown template type '{tactic}'. Supported: spoofing, typosquatting, urgency, social_engineering"

    if save:
        d = _ensure_generated_dir()
        prefix = (name or tactic or "template").strip()
        stem = _slugify(prefix)
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        fname = f"{stem}_{ts}.txt"
        path = d / fname
        path.write_text(text, encoding="utf-8")
        return text + f"\n\nSaved to: {str(path)}"

    return text

