import re

SCAM_KEYWORDS = {
    "urgent": 0.2,
    "immediately": 0.2,
    "blocked": 0.2,
    "suspended": 0.2,
    "verify": 0.15,
    "bank": 0.15,
    "upi": 0.25,
    "otp": 0.3,
    "click": 0.2,
    "link": 0.2,
    "kyc": 0.25
}

SCAM_THRESHOLD = 0.6


def detect_scam_intent(text: str) -> dict:
    text_lower = text.lower()
    confidence = 0.0
    matched_keywords = []

    for keyword, weight in SCAM_KEYWORDS.items():
        if re.search(rf"\b{keyword}\b", text_lower):
            confidence += weight
            matched_keywords.append(keyword)

    confidence = min(confidence, 1.0)

    return {
        "is_scam": confidence >= SCAM_THRESHOLD,
        "confidence": round(confidence, 2),
        "matched_keywords": matched_keywords
    }
