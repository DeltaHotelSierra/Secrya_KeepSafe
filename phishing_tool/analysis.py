from email import policy
from email.parser import BytesParser, Parser
import ipaddress
import re
from urllib.parse import urlparse


def _extract_header(email_text: str, header_name: str) -> str:
    """Return the value of the first occurrence of a header in the email text."""
    parsed_header = _extract_parsed_header(email_text, header_name)
    if parsed_header:
        return parsed_header
    try:
        pattern = rf"^{header_name}:\s*(.*)$"
        match = re.search(pattern, email_text, re.IGNORECASE | re.MULTILINE)
        return match.group(1).strip() if match else ""
    except Exception:
        return ""


def _parse_email(email_text: str):
    """Parse email text into a message object when possible."""
    if not email_text:
        return None

    try:
        raw_bytes = email_text.encode("utf-8", errors="replace")
        return BytesParser(policy=policy.default).parsebytes(raw_bytes)
    except Exception:
        try:
            return Parser(policy=policy.default).parsestr(email_text)
        except Exception:
            return None


def _extract_parsed_header(email_text: str, header_name: str) -> str:
    """Extract a header value using Python's email parser first."""
    message = _parse_email(email_text)
    if not message:
        return ""
    try:
        value = message.get(header_name)
        return str(value).strip() if value else ""
    except Exception:
        return ""


def _extract_body_text(email_text: str) -> str:
    """Return the text body extracted from a raw email when available."""
    message = _parse_email(email_text)
    if not message:
        return email_text

    try:
        if message.is_multipart():
            parts = []
            for part in message.walk():
                if part.get_content_maintype() == "multipart":
                    continue
                if part.get_content_type() != "text/plain":
                    continue
                payload = part.get_content()
                if isinstance(payload, str):
                    parts.append(payload)
            return "\n".join(parts).strip() or email_text

        payload = message.get_content()
        if isinstance(payload, str):
            return payload.strip() or email_text
        return email_text
    except Exception:
        return email_text


def _extract_urls(email_text: str) -> list:
    """Return the list of URLs found in the email text."""
    if not email_text:
        return []
    body = _extract_body_text(email_text)
    return re.findall(r"https?://[\w\-._~:/?#[\]@!$&'()*+,;=%]+", body)


def _domain_from_email_address(address: str) -> str:
    """Extract the domain from an email address if possible."""
    match = re.search(r"@([\w.-]+)", address)
    return match.group(1).lower() if match else ""


def _domain_from_url(url: str) -> str:
    """Extract the host part from a URL."""
    parsed = urlparse(url)
    return parsed.netloc.lower()


def check_sender_spoofing(email_text: str) -> dict:
    """Detect common spoofing and typosquatting patterns in the From header."""
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
        for pattern, intended_brand in patterns.items():
            if pattern in lowered:
                return {
                    "detected": True,
                    "risk_score": 9,
                    "details": (
                        f"Sender domain contains suspicious pattern '{pattern}' "
                        f"(looks like {intended_brand})"
                    ),
                }
        return {
            "detected": False,
            "risk_score": 1,
            "details": "No common spoofing patterns detected",
        }
    except Exception:
        return {"detected": False, "risk_score": 0, "details": "Could not parse"}


def check_urgency_language(email_text: str) -> dict:
    """Look for urgency keywords and assign a risk score."""
    if not email_text:
        return {"detected_keywords": [], "risk_score": 0}

    keywords = ["immediately", "urgent",
                "now", "24 hours", "verify", "revoked"]
    lowered = _extract_body_text(email_text).lower()
    found = [keyword for keyword in keywords if keyword in lowered]

    if not found:
        score = 0
    elif len(found) <= 2:
        score = 5
    else:
        score = 8
    return {"detected_keywords": found, "risk_score": score}


def check_link_mismatch(email_text: str) -> dict:
    """Check whether a link domain is different from the sender domain."""
    if not email_text:
        return {"mismatch_detected": False, "risk_score": 0, "details": "Empty email"}

    sender = _extract_header(email_text, "From")
    sender_domain = _domain_from_email_address(sender)
    urls = _extract_urls(email_text)
    if not urls:
        return {"mismatch_detected": False, "risk_score": 0, "details": "No URLs found"}

    url_domain = _domain_from_url(urls[0])
    if sender_domain and url_domain and sender_domain not in url_domain:
        return {
            "mismatch_detected": True,
            "risk_score": 9,
            "details": f"Sender domain '{sender_domain}' does not match URL domain '{url_domain}'",
        }
    return {
        "mismatch_detected": False,
        "risk_score": 1,
        "details": "URL domain matches sender domain",
    }


def analyze_email(email_text: str) -> dict:
    """Aggregate email checks and return a full analysis dictionary."""
    if not email_text:
        return {"risk_level": "UNKNOWN", "risk_score": 0, "indicators": [], "details": "Empty email"}

    try:
        spoof = check_sender_spoofing(email_text)
        urgency = check_urgency_language(email_text)
        link = check_link_mismatch(email_text)
        scores = [
            float(spoof.get("risk_score", 0)),
            float(urgency.get("risk_score", 0)),
            float(link.get("risk_score", 0)),
        ]
        average = sum(scores) / len(scores) if scores else 0.0
        if average >= 7:
            level = "HIGH"
        elif average >= 4:
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
            detected_keywords = urgency.get("detected_keywords") or []
            explanations.append("Urgency keywords: " +
                                ", ".join(detected_keywords))
        if link.get("mismatch_detected"):
            indicators.append("Link mismatch")
            explanations.append(link.get("details"))

        return {
            "risk_level": level,
            "risk_score": round(average, 2),
            "indicators": indicators,
            "explanations": explanations,
            "details": {"spoofing": spoof, "urgency": urgency, "link_mismatch": link},
        }
    except Exception:
        return {
            "risk_level": "UNKNOWN",
            "risk_score": 0,
            "indicators": [],
            "details": "Error during analysis",
        }


def _normalize_url(url: str) -> str:
    """Return a URL with a scheme so urlparse can inspect it reliably."""
    if not url:
        return ""
    stripped = url.strip()
    if re.match(r"^https?://", stripped, re.IGNORECASE):
        return stripped
    return f"https://{stripped}"


def _host_looks_like_ip(host: str) -> bool:
    """Return True if the host is an IP address."""
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def analyze_url(url: str) -> dict:
    """Score a URL for common phishing and scam indicators."""
    if not url or not isinstance(url, str):
        return {"risk_level": "UNKNOWN", "risk_score": 0, "indicators": [], "details": "Empty URL"}

    normalized = _normalize_url(url)
    parsed = urlparse(normalized)
    host = (parsed.netloc or "").lower()
    path = (parsed.path or "").lower()
    query = (parsed.query or "").lower()
    indicators = []
    explanations = []
    score = 0

    if not parsed.scheme or not host:
        return {"risk_level": "UNKNOWN", "risk_score": 0, "indicators": [], "details": "Malformed URL"}

    if parsed.scheme != "https":
        indicators.append("No HTTPS")
        explanations.append("The URL does not use HTTPS.")
        score += 3

    if _host_looks_like_ip(host):
        indicators.append("IP address host")
        explanations.append(
            "The host is an IP address instead of a normal domain name.")
        score += 5

    if host.startswith("xn--") or ".xn--" in host:
        indicators.append("Punycode domain")
        explanations.append(
            "The domain uses punycode, which is often used for lookalike domains.")
        score += 4

    if host.count("-") >= 2:
        indicators.append("Multiple hyphens")
        explanations.append(
            "The host contains several hyphens, which is common in impersonation domains.")
        score += 2

    if host.count(".") >= 3:
        indicators.append("Many subdomains")
        explanations.append(
            "The host uses many subdomains, which can be used to hide the real domain.")
        score += 2

    suspicious_terms = ["login", "verify", "account", "secure", "update",
                        "wallet", "bank", "password", "signin", "confirm", "auth"]
    if any(term in host for term in suspicious_terms) or any(term in path for term in suspicious_terms) or any(term in query for term in suspicious_terms):
        indicators.append("Credential bait")
        explanations.append(
            "The URL includes account or login language commonly used in scams.")
        score += 3

    if any(term in path for term in ["download", "invoice", "payment", "document", "verify"]):
        indicators.append("Action bait")
        explanations.append(
            "The path contains action-oriented terms often used to pressure users.")
        score += 2

    if score >= 8:
        level = "HIGH"
    elif score >= 4:
        level = "MEDIUM"
    else:
        level = "LOW"

    if not indicators:
        explanations.append("No strong scam indicators were detected.")

    return {
        "risk_level": level,
        "risk_score": min(round(score, 2), 10),
        "indicators": indicators,
        "explanations": explanations,
        "details": {"url": normalized, "host": host, "path": path},
    }
