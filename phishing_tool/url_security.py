"""URL and domain security analysis module."""
import socket
import re
from datetime import datetime

try:
    from . import report
except ImportError:  # pragma: no cover - support direct script execution
    import report

# Known legitimate company domains and their real IPs (examples)
# Note: Real-time DNS lookups will verify current IPs; this is a reference database
KNOWN_DOMAINS = {
    "google.com": ["142.250.80.46", "142.250.80.78", "142.250.185.46", "216.58.198.46"],
    "gmail.com": ["142.251.41.229", "142.250.185.46"],
    "github.com": ["140.82.113.3", "140.82.113.4"],
    "amazon.com": ["54.239.28.30", "205.251.242.103", "176.32.98.166"],
    "microsoft.com": ["13.107.42.14", "13.107.42.15"],
    "office.com": ["13.107.42.14"],
    "outlook.com": ["13.107.42.14", "13.107.42.15"],
    "apple.com": ["17.142.160.59", "17.142.160.60"],
    "icloud.com": ["17.142.160.59"],
    "facebook.com": ["31.13.64.35", "31.13.64.36"],
    "meta.com": ["31.13.64.35"],
    "twitter.com": ["104.244.42.1", "104.244.42.129"],
    "x.com": ["104.244.42.1"],
    "linkedin.com": ["108.174.10.10"],
    "paypal.com": ["66.211.169.66"],
    "stripe.com": ["54.187.174.169"],
    "bank.com": ["205.178.104.10"],
}

# Special characters that indicate high risk
RISKY_CHARACTERS = {
    "0": "O",  # zero vs letter O
    "1": "l",  # one vs lowercase L
    "1": "I",  # one vs uppercase I
    "ℓ": "l",  # script L
    "Ⅰ": "I",  # Roman numeral
}


def extract_domain(url: str) -> str:
    """Extract domain from URL. Handles both URLs and plain domains."""
    url = url.strip()
    # Remove protocol if present
    if "://" in url:
        url = url.split("://")[1]
    # Remove path if present
    url = url.split("/")[0]
    # Remove port if present
    url = url.split(":")[0]
    return url.lower()


def has_special_characters(domain: str) -> tuple:
    """Check for homoglyphs and suspicious character patterns.

    Returns: (has_risk, risk_details)
    """
    risky_patterns = []

    # Check for consecutive repeated characters (unusual for legit domains)
    if re.search(r'(.)\1{2,}', domain):
        risky_patterns.append("Multiple consecutive repeated characters")

    # Check for non-ASCII characters (homoglyphs)
    try:
        domain.encode('ascii')
    except UnicodeEncodeError:
        risky_patterns.append("Non-ASCII characters detected (homoglyph risk)")

    # Check for suspicious patterns like dash-O combinations
    if re.search(r'(0{2,}|l{2,}|1{2,})', domain):
        risky_patterns.append(
            "Possible look-alike character pattern (0/O, 1/l/I)")

    # Check for dashes at suspicious positions
    if domain.startswith('-') or domain.endswith('-'):
        risky_patterns.append("Domain starts or ends with dash")

    # Check for unusual TLD patterns
    if domain.count('.') > 2:
        risky_patterns.append("Multiple dots (subdomain suspicious)")

    return len(risky_patterns) > 0, risky_patterns


def perform_dns_lookup(domain: str) -> tuple:
    """Perform DNS lookup and return resolved IPs.

    Returns: (success, ip_addresses, error_message)
    """
    try:
        ips = socket.gethostbyname_ex(domain)
        return True, ips[2], None  # Return list of IPs
    except socket.gaierror as e:
        return False, [], f"DNS resolution failed: {str(e)}"
    except Exception as e:
        return False, [], f"Lookup error: {str(e)}"


def get_base_domain(domain: str) -> str:
    """Return the base domain portion of a hostname."""
    parts = domain.split('.')
    return '.'.join(parts[-2:]) if len(parts) >= 2 else domain


def check_against_known_domains(domain: str, resolved_ips: list, has_special: bool = False) -> tuple:
    """Check if domain and IPs match known legitimate company domains.

    Returns: (is_verified, verification_details, known_base_domain)
    """
    base_domain = get_base_domain(domain)

    if base_domain not in KNOWN_DOMAINS:
        return False, (
            f"Domain '{base_domain}' is not in the static known domain list. "
            "DNS resolution succeeded, but this site is not part of the sample database."
        ), False

    known_ips = KNOWN_DOMAINS[base_domain]
    matching_ips = [ip for ip in resolved_ips if ip in known_ips]

    if matching_ips:
        return True, f"✓ Verified: Domain resolves to known legitimate IP(s): {', '.join(matching_ips)}", True

    if has_special:
        return False, (
            f"⚠ Domain is a known base domain ({base_domain}) but contains suspicious character patterns. "
            f"Resolved IPs: {resolved_ips}"
        ), True

    return False, (
        f"Domain is a known base domain ({base_domain}) and DNS resolved successfully, but the resolved IPs differ from the sample list. "
        "Large services often use dynamic IP ranges or CDN endpoints."
    ), True


def analyze_url_security(url: str) -> dict:
    """Comprehensive URL security analysis.

    Returns dict with:
    - url: original input
    - domain: extracted domain
    - dns_resolved: whether DNS lookup succeeded
    - resolved_ips: list of resolved IP addresses
    - special_chars_risk: whether special characters detected
    - char_risks: list of character risk details
    - is_verified: whether domain matches known legitimate domain
    - verification_status: detailed verification message
    - risk_level: HIGH/MEDIUM/LOW
    - risk_indicators: list of detected risks
    - recommendations: list of recommendations
    """
    domain = extract_domain(url)

    # Check for special characters
    has_special, char_risks = has_special_characters(domain)

    # Perform DNS lookup
    dns_resolved, resolved_ips, dns_error = perform_dns_lookup(domain)

    # Check against known domains
    is_verified = False
    verification_status = ""
    known_base_domain = False
    if dns_resolved:
        is_verified, verification_status, known_base_domain = check_against_known_domains(
            domain, resolved_ips, has_special)

    # Determine risk score and level
    risk_indicators = []
    if has_special:
        risk_indicators.extend(char_risks)

    if not dns_resolved:
        risk_indicators.append(f"DNS resolution failed: {dns_error}")

    if dns_resolved and not is_verified:
        if known_base_domain:
            risk_indicators.append(
                "Domain resolves successfully but resolved IPs differ from the sample list")
        else:
            risk_indicators.append(
                "Domain resolves successfully but is not in the static known domain list")

    risk_score = 0
    if not dns_resolved:
        risk_score = 10
    else:
        risk_score = 1 if is_verified else 4
        if has_special:
            risk_score += 4
        if dns_resolved and not is_verified:
            risk_score += 2
        risk_score = min(risk_score, 10)

    if risk_score >= 7:
        risk_level = "HIGH"
    elif risk_score >= 3:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    recommendations = []
    if not dns_resolved:
        recommendations.append(
            "Domain cannot be resolved - likely fake or typo")
        recommendations.append("Do not visit this URL")
    elif has_special:
        recommendations.append("Domain contains suspicious character patterns")
        recommendations.append(
            "Verify the correct spelling with official sources")
    elif not is_verified and dns_resolved:
        if known_base_domain:
            recommendations.append(
                "Domain resolves successfully, but resolved IPs differ from the sample list")
            recommendations.append(
                "Verify through official company channels before clicking if unsure")
        else:
            recommendations.append(
                "Domain resolves successfully, but this website is not in the static known domain list")
            recommendations.append(
                "Verify the URL carefully if the source is unfamiliar")
    else:
        recommendations.append("Domain appears legitimate")
        recommendations.append(
            "Still exercise caution with personal information")

    return {
        "url": url,
        "domain": domain,
        "dns_resolved": dns_resolved,
        "resolved_ips": resolved_ips,
        "dns_error": dns_error,
        "special_chars_risk": has_special,
        "char_risks": char_risks,
        "is_verified": is_verified,
        "verification_status": verification_status,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_indicators": risk_indicators,
        "recommendations": recommendations,
    }


def generate_url_security_report(analysis_result: dict, url: str = None) -> str:
    """Format URL security results into a printable report string."""
    if not analysis_result or not isinstance(analysis_result, dict):
        return "Error: Invalid analysis result format"

    source_url = url or analysis_result.get("url", "")
    lines = [
        "URL PHISHING ANALYSIS REPORT",
        "========================",
        f"URL Analyzed: {analysis_result.get('url', source_url)}",
        f"Domain: {analysis_result.get('domain', '')}",
        f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "SECURITY CHECK RESULTS:",
        "------------------------",
        "",
        "DNS Resolution:",
        f"  Status: {'✓ Resolved' if analysis_result.get('dns_resolved') else '✗ Failed to resolve'}",
        f"  Error: {analysis_result.get('dns_error') if analysis_result.get('dns_error') else 'None'}",
        f"  Resolved IPs: {', '.join(analysis_result.get('resolved_ips', [])) if analysis_result.get('resolved_ips') else 'N/A'}",
        "",
        "Domain Verification:",
        f"  Status: {'✓ Verified Legitimate' if analysis_result.get('is_verified') else '✗ Not Verified'}",
        f"  Details: {analysis_result.get('verification_status', '')}",
        "",
        "Character Analysis:",
        f"  Suspicious Patterns: {'Yes' if analysis_result.get('special_chars_risk') else 'No'}",
        f"  Details: {chr(10).join(['  - ' + risk for risk in analysis_result.get('char_risks', [])]) if analysis_result.get('char_risks') else '  None detected'}",
        "",
        "RISK ASSESSMENT:",
        "------------------------",
        report.format_risk_line(analysis_result.get(
            'risk_level'), analysis_result.get('risk_score')),
        "",
        "Detected Indicators:",
        f"{chr(10).join(['  - ' + indicator for indicator in analysis_result.get('risk_indicators', [])]) if analysis_result.get('risk_indicators') else '  None detected'}",
        "",
        "RECOMMENDATIONS:",
        "------------------------",
        *[f"  - {rec}" for rec in analysis_result.get('recommendations', [])],
        "",
        "COPY-PASTE READY:",
        "------------------------",
        f"Real Domain: {analysis_result.get('domain', '')}",
        f"Real IP(s): {', '.join(analysis_result.get('resolved_ips', [])) if analysis_result.get('resolved_ips') else 'Unable to resolve'}",
        f"Visit: https://{analysis_result.get('domain', '')}",
    ]
    return "\n".join(lines)
