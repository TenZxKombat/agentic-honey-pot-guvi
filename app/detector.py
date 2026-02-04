import re

SCAM_KEYWORDS = {
    "bank": 0.25,
    "blocked": 0.3,
    "verify": 0.25,
    "upi": 0.6,
    "otp": 0.4,
    "urgent": 0.3,
    "act": 0.2,
    "now": 0.2,
    "account": 0.2,
    "immediately": 0.2,
    "details": 0.15,
    "click": 0.2,
    "link": 0.2,
    "kyc": 0.25,
    "share": 0.2,
    "suspended": 0.2,
}

SCAM_THRESHOLD = 0.6


def detect_scam_intent(text: str) -> dict:
    text_lower = text.lower()
    confidence = 0.0
    matched = []

    for keyword, weight in SCAM_KEYWORDS.items():
        # FIX: allow punctuation after words
        if re.search(rf"\b{keyword}\b", text_lower):
            confidence += weight
            matched.append(keyword)

    confidence = min(confidence, 1.0)

    return {
        "is_scam": confidence >= SCAM_THRESHOLD,
        "confidence": round(confidence, 2),
        "matched_keywords": matched
    }
