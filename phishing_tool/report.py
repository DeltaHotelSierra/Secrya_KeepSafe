"""Format and persist phishing analysis reports."""

from datetime import datetime, timezone
from pathlib import Path
import re


REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"

RESET_COLOR = "\033[0m"
RED_COLOR = "\033[38;2;255;0;0m"
ORANGE_COLOR = "\033[38;2;255;165;0m"
YELLOW_COLOR = "\033[38;2;255;255;0m"
BLUE_COLOR = "\033[38;2;0;102;255m"
GREEN_COLOR = "\033[38;2;0;200;0m"


def _ensure_analysis_result(analysis_result: dict) -> bool:
    """Return True when the analysis payload looks like a report result."""
    # Basic shape check
    if not isinstance(analysis_result, dict):
        return False, "analysis_result must be a dict"
    if "risk_level" not in analysis_result:
        return False, "missing required field: risk_level"

    # Validate risk_level
    rl = str(analysis_result.get("risk_level") or "").upper()
    if rl not in ("HIGH", "MEDIUM", "LOW"):
        return False, "risk_level must be one of: HIGH, MEDIUM, LOW"

    # Validate risk_score (None or number between 0 and 10)
    score = analysis_result.get("risk_score")
    if score is None:
        return True, None
    try:
        val = float(score)
    except (TypeError, ValueError):
        return False, "risk_score must be numeric or None"
    if val < 0 or val > 10:
        return False, "risk_score must be between 0 and 10"
    return True, None


def _recommendations_for_level(risk_level: str) -> list:
    """Return a list of recommendations for the given risk level."""
    if risk_level == "HIGH":
        return [
            "- Do not click links or download attachments",
            "- Report to security team immediately",
            "- Delete the message or move it to spam",
        ]
    if risk_level == "MEDIUM":
        return [
            "- Verify through an official channel before interacting",
            "- Check sender details and domain carefully",
        ]
    if risk_level == "LOW":
        return [
            "- Likely safe, but still verify unexpected requests",
            "- Use normal caution before opening links",
        ]
    return ["- Unable to determine recommendations"]


def _risk_color_for_score(risk_score) -> str:
    """Return an ANSI color code for the given risk score."""
    try:
        score = float(risk_score)
    except (TypeError, ValueError):
        return ""

    if score <= 2:
        return GREEN_COLOR
    if score <= 4:
        return BLUE_COLOR
    if score <= 6:
        return YELLOW_COLOR
    if score <= 8:
        return ORANGE_COLOR
    if score <= 10:
        return RED_COLOR
    return RED_COLOR


def format_risk_line(risk_level: str, risk_score) -> str:
    """Format the risk line with color based on the numeric score."""
    color = _risk_color_for_score(risk_score)
    score_text = "?" if risk_score is None else risk_score
    line = f"Risk Level: {risk_level} ({score_text}/10)"
    return f"{color}{line}{RESET_COLOR}" if color else line


def _build_report_lines(title: str, analysis_result: dict, source_label: str | None = None) -> list:
    """Build the shared report body for email and URL analysis."""
    risk_level = str(analysis_result.get("risk_level") or "UNKNOWN")
    risk_score = analysis_result.get("risk_score")
    indicators = analysis_result.get("indicators") or []
    explanations = analysis_result.get("explanations") or []

    lines = [title, "=" * len(title)]
    if source_label:
        lines.append(source_label)
    lines.append(format_risk_line(risk_level, risk_score))
    lines.append("")
    lines.append("DETECTED INDICATORS:")
    if indicators:
        lines.extend(f"- {indicator}" for indicator in indicators)
    else:
        lines.append("- None detected")
    lines.append("")
    lines.append("WHY THIS MATTERS:")
    if explanations:
        lines.extend(f"- {explanation}" for explanation in explanations)
    else:
        lines.append("- No specific explanations")
    lines.append("")
    lines.append("RECOMMENDATIONS:")
    lines.extend(_recommendations_for_level(risk_level))
    return lines


def format_report(analysis_result: dict, email_file: str | None = None) -> str:
    """Format email analysis results into a printable report string."""
    ok, err = _ensure_analysis_result(analysis_result)
    if not ok:
        return f"Error: {err}"
    source_label = f"File: {email_file}" if email_file else None
    return "\n".join(_build_report_lines("PHISHING ANALYSIS REPORT", analysis_result, source_label))


def format_url_report(analysis_result: dict, url: str | None = None) -> str:
    """Format URL analysis results into a printable report string."""
    ok, err = _ensure_analysis_result(analysis_result)
    if not ok:
        return f"Error: {err}"
    source_label = f"URL: {url}" if url else None
    return "\n".join(_build_report_lines("URL SCAM ANALYSIS REPORT", analysis_result, source_label))


def _slugify(value: str) -> str:
    """Return a filesystem-friendly slug for a report name."""
    slug = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
    slug = re.sub(r"_+", "_", slug).strip("_.")
    return slug or "report"


def save_report(report_text: str, report_name: str) -> Path:
    """Save a report to the reports folder and return the created path."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    stem = _slugify(report_name)
    filename = f"{stem}_{timestamp}.txt"
    report_path = REPORTS_DIR / filename
    report_path.write_text(report_text, encoding="utf-8")
    return report_path


def list_recent_reports(limit: int = 10) -> list:
    """Return report files sorted from newest to oldest."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_files = [path for path in REPORTS_DIR.iterdir() if path.is_file()]
    report_files.sort(key=lambda path: path.stat().st_mtime, reverse=True)
    return report_files[:limit]


def read_report(report_path: Path) -> str:
    """Read a report file from disk."""
    return Path(report_path).read_text(encoding="utf-8")
