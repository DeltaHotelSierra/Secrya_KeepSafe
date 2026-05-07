"""URL and domain security analysis module."""
import socket
import re
from datetime import datetime

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
        risky_patterns.append("Possible look-alike character pattern (0/O, 1/l/I)")
    
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


def check_against_known_domains(domain: str, resolved_ips: list) -> tuple:
    """Check if domain and IPs match known legitimate company domains.
    
    Returns: (is_verified, verification_details)
    """
    # Extract base domain (e.g., mail.google.com -> google.com)
    parts = domain.split('.')
    base_domain = '.'.join(parts[-2:]) if len(parts) >= 2 else domain
    
    if base_domain not in KNOWN_DOMAINS:
        return False, f"Domain '{base_domain}' not in known legitimate domains database"
    
    known_ips = KNOWN_DOMAINS[base_domain]
    matching_ips = [ip for ip in resolved_ips if ip in known_ips]
    
    if matching_ips:
        return True, f"✓ Verified: Domain resolves to known legitimate IP(s): {', '.join(matching_ips)}"
    else:
        return False, f"⚠ Domain exists but IP mismatch. Expected: {known_ips}, Got: {resolved_ips}"


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
    if dns_resolved:
        is_verified, verification_status = check_against_known_domains(domain, resolved_ips)
    
    # Determine risk level
    risk_indicators = []
    if has_special:
        risk_indicators.extend(char_risks)
    
    if not dns_resolved:
        risk_indicators.append(f"DNS resolution failed: {dns_error}")
    
    if dns_resolved and not is_verified:
        risk_indicators.append("Domain resolves but IP not verified against known legitimate IPs")
    
    if has_special and dns_resolved:
        risk_level = "HIGH"
    elif not dns_resolved:
        risk_level = "HIGH"
    elif has_special or (dns_resolved and not is_verified):
        risk_level = "MEDIUM"
    elif is_verified:
        risk_level = "LOW"
    else:
        risk_level = "MEDIUM"
    
    recommendations = []
    if not dns_resolved:
        recommendations.append("Domain cannot be resolved - likely fake or typo")
        recommendations.append("Do not visit this URL")
    elif has_special:
        recommendations.append("Domain contains suspicious character patterns")
        recommendations.append("Verify the correct spelling with official sources")
    elif not is_verified and dns_resolved:
        recommendations.append("Domain resolves but not in known legitimate domains database")
        recommendations.append("Verify through official company channels before clicking")
    else:
        recommendations.append("Domain appears legitimate")
        recommendations.append("Still exercise caution with personal information")
    
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
        "risk_level": risk_level,
        "risk_indicators": risk_indicators,
        "recommendations": recommendations,
    }
