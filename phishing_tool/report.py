"""Format analysis results into a plain-text report."""


def format_report(analysis_result: dict, email_file: str = None) -> str:
    """Format the analysis_result (from analyze_email) into a printable report string.

    Returns an error message if the input is invalid.
    """
    if not isinstance(analysis_result, dict) or "risk_level" not in analysis_result:
        return "Error: Invalid analysis result format"
    lines = []
    lines.append("PHISHING ANALYSIS REPORT")
    lines.append("========================")
    if email_file:
        lines.append(f"File: {email_file}")
    lines.append(
        f"Risk Level: {analysis_result.get('risk_level')} ({analysis_result.get('risk_score')}/10)")
    lines.append("")
    lines.append("DETECTED INDICATORS:")
    if analysis_result.get("indicators"):
        for ind in analysis_result.get("indicators"):
            lines.append(f"- {ind}")
    else:
        lines.append("- None detected")
    lines.append("")
    lines.append("WHY THIS MATTERS:")
    if analysis_result.get("explanations"):
        for ex in analysis_result.get("explanations"):
            lines.append(f"- {ex}")
    else:
        lines.append("- No specific explanations")
    lines.append("")
    lines.append("RECOMMENDATIONS:")
    rl = analysis_result.get("risk_level")
    if rl == "HIGH":
        lines.extend([
            "- Do not click links or download attachments",
            "- Report to security team immediately",
            "- Delete the email or forward to spam",
        ])
    elif rl == "MEDIUM":
        lines.extend([
            "- Verify through official channel before interacting",
            "- Check sender domain in email headers",
        ])
    elif rl == "LOW":
        lines.extend([
            "- Likely safe but exercise caution",
            "- Verify unexpected requests through official channels",
        ])
    else:
        lines.append("- Unable to determine recommendations")
    return "\n".join(lines)
