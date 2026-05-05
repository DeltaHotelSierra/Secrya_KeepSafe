import re


def _extract_header(email_text: str, header_name: str) -> str:
    """Return the value of the first occurrence of a header in the email text.

    Example:
        _extract_header(text, 'From') -> 'Bank Support <support@your-bank.com>'
    """
    try:
        pattern = rf"^{header_name}:\s*(.*)$"
        m = re.search(pattern, email_text, re.IGNORECASE | re.MULTILINE)
        return m.group(1).strip() if m else ""
    except Exception:
        return ""


def check_sender_spoofing(email_text: str) -> dict:
    """Detect common typosquatting/spoofing patterns in the From: header.

    Returns a dict with keys: detected (bool), risk_score (0-10), details (str).
    """
    if not email_text:
        return {"detected": False, "risk_score": 0, "details": "Could not parse"}
    try:
        sender = _extract_header(email_text, "From")
        lowered = sender.lower()
        patterns = {
            "goog1e.com": "google.com",
            "amaz0n.com": "amazon.com",
            "m1crosoft.com": "microsoft.com",
            "paypol.com": "paypal.com",
        }
        for p in patterns:
            if p in lowered:
                return {
                    "detected": True,
                    "risk_score": 9,
                    "details": f"Sender domain contains suspicious pattern '{p}' (looks like {patterns[p]})",
                }
        return {"detected": False, "risk_score": 1, "details": "No common spoofing patterns detected"}
    except Exception:
        return {"detected": False, "risk_score": 0, "details": "Could not parse"}


def check_urgency_language(email_text: str) -> dict:
    """Look for urgency keywords and assign a risk score.

    Returns dict with detected_keywords (list) and risk_score.
    """
    if not email_text:
        return {"detected_keywords": [], "risk_score": 0}
    keywords = ["immediately", "urgent",
                "now", "24 hours", "verify", "revoked"]
    found = []
    lowered = email_text.lower()
    for k in keywords:
        if k.lower() in lowered:
            found.append(k)
    if not found:
        score = 0
    elif len(found) <= 2:
        score = 5
    else:
        score = 8
    return {"detected_keywords": found, "risk_score": score}


def _extract_urls(email_text: str) -> list:
    """Return list of URLs found in the email text."""
    if not email_text:
        return []
    urls = re.findall(r"https?://[\w\-._~:/?#[\]@!$&'()*+,;=%]+", email_text)
    return urls


def _domain_from_email_address(address: str) -> str:
    """Extract domain from an email address if possible."""
    m = re.search(r"@([\w.-]+)", address)
    return m.group(1).lower() if m else ""


def _domain_from_url(url: str) -> str:
    """Extract domain part from URL."""
    m = re.search(r"https?://([^/]+)", url)
    return m.group(1).lower() if m else ""


def check_link_mismatch(email_text: str) -> dict:
    """Check whether visible links mismatch the sender domain.

    Returns dict with mismatch_detected (bool), risk_score, details.
    """
    if not email_text:
        return {"mismatch_detected": False, "risk_score": 0, "details": "Empty email"}
    sender = _extract_header(email_text, "From")
    sender_domain = _domain_from_email_address(sender)
    urls = _extract_urls(email_text)
    if not urls:
        return {"mismatch_detected": False, "risk_score": 0, "details": "No URLs found"}
    # Check first URL for mismatch
    url_domain = _domain_from_url(urls[0])
    if sender_domain and url_domain and (sender_domain not in url_domain):
        return {
            "mismatch_detected": True,
            "risk_score": 9,
            "details": f"Sender domain '{sender_domain}' does not match URL domain '{url_domain}'",
        }
    return {"mismatch_detected": False, "risk_score": 1, "details": "URL domain matches sender domain"}


def analyze_email(email_text: str) -> dict:
    """Aggregate checks and return a full analysis dict.

    Example:
        result = analyze_email(open('test_data/phishing_example.txt').read())
    """
    if not email_text:
        return {"risk_level": "UNKNOWN", "risk_score": 0, "indicators": [], "details": "Empty email"}
    try:
        spoof = check_sender_spoofing(email_text)
        urgency = check_urgency_language(email_text)
        link = check_link_mismatch(email_text)
        scores = [float(spoof.get("risk_score", 0)), float(
            urgency.get("risk_score", 0)), float(link.get("risk_score", 0))]
        avg = sum(scores) / len(scores) if scores else 0.0
        if avg >= 7:
            level = "HIGH"
        elif avg >= 4:
            level = "MEDIUM"
        else:
            level = "LOW"
        indicators = []
        explanations = []
        if spoof.get("detected"):
            indicators.append("Sender spoofing")
            explanations.append(spoof.get("details"))
        if urgency.get("detected_keywords"):
            indicators.append("Urgency language")
            explanations.append("Urgency keywords: " +
                                ", ".join(urgency.get("detected_keywords")))
        if link.get("mismatch_detected"):
            indicators.append("Link mismatch")
            explanations.append(link.get("details"))
        return {
            "risk_level": level,
            "risk_score": round(avg, 2),
            "indicators": indicators,
            "explanations": explanations,
            "details": {"spoofing": spoof, "urgency": urgency, "link_mismatch": link},
        }
    except Exception:
        return {"risk_level": "UNKNOWN", "risk_score": 0, "indicators": [], "details": "Error during analysis"}
