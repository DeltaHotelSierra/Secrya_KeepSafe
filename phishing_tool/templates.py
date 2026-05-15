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
    """Ensure the GENERATED_EMAILS directory exists and return its Path.

    Creates the directory (including parents) if it does not already exist.

    Returns:
        pathlib.Path: Absolute path to the directory used for generated emails.
    """
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    return GENERATED_DIR


def _slugify(value: str) -> str:
    """Create a filesystem-safe slug from an arbitrary string.

    Non-alphanumeric characters are replaced with underscores except for
    dot, underscore and dash which are allowed. Leading/trailing dots,
    underscores and dashes are stripped. If the resulting slug is empty,
    the literal string "template" is returned.

    Args:
        value (str): Input string to convert into a slug.

    Returns:
        str: A safe filename-friendly slug.
    """
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in value).strip("_.-") or "template"


def generate_template(tactic: str, *, save: bool = False, name: Optional[str] = None) -> str:
    """Return a plain-text educational template for the given tactic.

    Args:
        tactic (str): One of 'spoofing', 'typosquatting', 'urgency', or
            'social_engineering' (case-insensitive). Required.
        save (bool): If True, write the generated template to
            `phishing_tool/GENERATED_EMAILS/`. Defaults to False.
        name (Optional[str]): Optional filename prefix to use when saving the
            generated template. If omitted the tactic name is used.

    Returns:
        str: Formatted template text. If ``save=True`` the returned string
        includes a final line indicating the saved file path.

    Raises:
        ValueError: If ``tactic`` is None or not a supported tactic.
    """
    if tactic is None:
        raise ValueError("tactic must be provided (supported: " + ", ".join(get_supported_tactics()) + ")")
    # Normalize input
    t = str(tactic).strip().lower()
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
    elif t == "pretexting":
        text = (
            "EDUCATIONAL TEMPLATE: Pretexting\n"
            "--------------------------------------------------\n"
            "Example pretext:\n"
            "  Caller: IT Support <it-support@company.com>\n"
            "  Message: We detected abnormal activity on your account; please provide your login to verify.\n"
            "\n"
            "Explanation: The attacker invents a believable scenario (the pretext) to obtain information or access.\n"
            "Defense: Verify the request through independent channels, do not share credentials, and escalate suspicious calls.\n"
        )
    elif t == "vishing":
        text = (
            "EDUCATIONAL TEMPLATE: Vishing (Voice Phishing)\n"
            "--------------------------------------------------\n"
            "Example voicemail/call script:\n"
            "  Caller: Bank Security\n"
            "  Message: We need to confirm recent transactions; please call back and verify your card number.\n"
            "\n"
            "Explanation: Attackers use phone calls to impersonate trusted organizations and extract sensitive information.\n"
            "Defense: Do not provide sensitive data over unsolicited calls; hang up and call the official number from your account statement.\n"
        )
    elif t == "smishing":
        text = (
            "EDUCATIONAL TEMPLATE: Smishing (SMS Phishing)\n"
            "--------------------------------------------------\n"
            "Example SMS:\n"
            "  From: +1-800-555-0123\n"
            "  Message: Urgent: Your package delivery failed. Click http://track.example to reschedule.\n"
            "\n"
            "Explanation: Phishing via SMS attempts to trick users into clicking links or sharing info via mobile messages.\n"
            "Defense: Avoid clicking links in unexpected SMS, verify with the sender through official channels, and report suspicious texts.\n"
        )
    else:
        supported = ", ".join(get_supported_tactics())
        raise ValueError(f"Unknown template type '{tactic}'. Supported: {supported}")

    # At this point a `text` variable has been assigned for a known tactic.
    # Optionally save to disk and return a note about the saved path.
    if save:
        d = _ensure_generated_dir()
        prefix = (name or tactic or "template").strip()
        stem = _slugify(prefix)
        # Use local time for filenames per user's request
        ts_local = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"{stem}_{ts_local}.txt"
        path = d / fname
        # Avoid collisions by appending a counter suffix if the file exists
        if path.exists():
            counter = 1
            while True:
                candidate = d / f"{stem}_{ts_local}_{counter}.txt"
                if not candidate.exists():
                    path = candidate
                    break
                counter += 1
        path.write_text(text, encoding="utf-8")
        return text + f"\n\nSaved to: {str(path)}"

    return text


def get_supported_tactics() -> list:
    """Return the list of supported tactic names.

    Returns:
        list[str]: Supported tactic names as lowercase strings.
    """
    return [
        "spoofing",
        "typosquatting",
        "urgency",
        "social_engineering",
        "pretexting",
        "vishing",
        "smishing",
    ]


def list_generated_templates() -> list:
    """Scan the GENERATED_EMAILS directory and return saved templates with timestamps.

    The function inspects files in the `GENERATED_EMAILS` directory and returns
    a list of dictionaries with the filename and the creation timestamp. Where
    the platform exposes a birth/creation time this is preferred; otherwise the
    file modification time is used. Timestamps are presented as local-time ISO
    8601 strings including the timezone offset (e.g. ``2026-05-14T10:19:11+02:00``).

    Returns:
        list[dict]: Each dict has keys ``name`` and ``created_iso``. The list is
        sorted newest-first by the chosen creation timestamp.
    """
    d = GENERATED_DIR
    if not d.exists():
        return []
    files = [p for p in d.iterdir() if p.is_file()]

    def _created_ts(path: Path) -> float:
        """Return the best available creation timestamp for ``path`` as POSIX float."""
        st = path.stat()
        if hasattr(st, "st_birthtime"):
            return float(st.st_birthtime)
        return float(st.st_mtime)

    files.sort(key=_created_ts, reverse=True)
    out: list[dict] = []
    for p in files:
        ts = _created_ts(p)
        # Convert to local timezone ISO 8601 with offset
        created_iso = datetime.fromtimestamp(ts).astimezone().isoformat(timespec="seconds")
        out.append({"name": p.name, "created_iso": created_iso})
    return out

