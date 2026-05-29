# backend/security/prompt_guard.py

import re

INJECTION_PATTERNS = [
    r"ignore (previous|all|above) instructions",
    r"you are now",
    r"jailbreak",
    r"act as (DAN|an AI without|a different)",
    r"forget your (rules|training|guidelines|instructions)",
    r"pretend you (are|have no|don't have)",
    r"do anything now",
    r"no restrictions",
    r"bypass",
    r"ignore your programming",
]

PII_PATTERNS = {
    "phone":   r"\b[6-9]\d{9}\b",
    "aadhaar": r"\b\d{4}\s\d{4}\s\d{4}\b",
    "email":   r"\b[\w.+-]+@[\w-]+\.\w+\b",
    "pan":     r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
}

SAFE_RESPONSES = {
    "INJECTION_DETECTED": (
        "Main sirf mahilaon ki suraksha aur kanoon se related sawaalon mein "
        "madad kar sakti hoon. Koi aur sawaal ho toh zaroor poochein."
    ),
}

def check_injection(text: str) -> bool:
    text_lower = text.lower()
    return any(re.search(p, text_lower) for p in INJECTION_PATTERNS)

def mask_pii(text: str) -> tuple:
    masked = text
    found = {}
    for label, pattern in PII_PATTERNS.items():
        matches = re.findall(pattern, text)
        if matches:
            found[label] = matches
            masked = re.sub(pattern, f"[{label.upper()}_REDACTED]", masked)
    return masked, found

def guard(text: str) -> tuple:
    """
    Returns (safe_text, threat_type_or_None)
    threat_type is None if input is clean
    """
    if not text or not text.strip():
        return text, "EMPTY_INPUT"

    if check_injection(text):
        return text, "INJECTION_DETECTED"

    safe_text, pii_found = mask_pii(text)

    if pii_found:
        print(f"[Security] PII masked: {list(pii_found.keys())}")

    return safe_text, None

def get_safe_response(threat_type: str) -> str:
    return SAFE_RESPONSES.get(
        threat_type,
        "Yeh request process nahi ho sakti. Kripya dobara try karein."
    )