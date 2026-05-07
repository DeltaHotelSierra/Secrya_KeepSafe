"""Format and persist phishing analysis reports."""

from datetime import datetime
from pathlib import Path
import re


REPORTS_DIR = Path(__file__).resolve().parent / "reports"

RESET_COLOR = "\033[0m"
RED_COLOR = "\033[31m"
ORANGE_COLOR = "\033[38;2;255;165;0m"
YELLOW_COLOR = "\033[33m"
BLUE_COLOR = "\033[34m"
GREEN_COLOR = "\033[32m"


def _ensure_analysis_result(analysis_result: dict) -> bool:
    """Return True when the analysis payload looks like a report result."""
    return isinstance(analysis_result, dict) and "risk_level" in analysis_result


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
        return RED_COLOR
    if score <= 4:
        return ORANGE_COLOR
    if score <= 6:
        return YELLOW_COLOR
    if score <= 8:
        return BLUE_COLOR
    return GREEN_COLOR


def format_risk_line(risk_level: str, risk_score) -> str:
    """Format the risk line with color based on the numeric score."""
    color = _risk_color_for_score(risk_score)
    score_text = "?" if risk_score is None else risk_score
    line = f"Risk Level: {risk_level} ({score_text}/10)"
    return f"{color}{line}{RESET_COLOR}" if color else line


def _build_report_lines(title: str, analysis_result: dict, source_label: str = None) -> list:
    """Build the shared report body for email and URL analysis."""
    lines = [title, "=" * len(title)]
    if source_label:
        lines.append(source_label)
    lines.append(format_risk_line(analysis_result.get(
        'risk_level'), analysis_result.get('risk_score')))
    lines.append("")
    lines.append("DETECTED INDICATORS:")
    if analysis_result.get("indicators"):
        lines.extend(
            f"- {indicator}" for indicator in analysis_result.get("indicators"))
    else:
        lines.append("- None detected")
    lines.append("")
    lines.append("WHY THIS MATTERS:")
    if analysis_result.get("explanations"):
        lines.extend(
            f"- {explanation}" for explanation in analysis_result.get("explanations"))
    else:
        lines.append("- No specific explanations")
    lines.append("")
    lines.append("RECOMMENDATIONS:")
    lines.extend(_recommendations_for_level(analysis_result.get("risk_level")))
    return lines


def format_report(analysis_result: dict, email_file: str = None) -> str:
    """Format email analysis results into a printable report string."""
    if not _ensure_analysis_result(analysis_result):
        return "Error: Invalid analysis result format"
    source_label = f"File: {email_file}" if email_file else None
    return "\n".join(_build_report_lines("PHISHING ANALYSIS REPORT", analysis_result, source_label))


def format_url_report(analysis_result: dict, url: str = None) -> str:
    """Format URL analysis results into a printable report string."""
    if not _ensure_analysis_result(analysis_result):
        return "Error: Invalid analysis result format"
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
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
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
