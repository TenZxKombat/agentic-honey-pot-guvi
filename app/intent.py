import re

INTENT_PATTERNS = {
    "bank_threat": [
        r"bank account",
        r"account will be blocked",
        r"account suspended"
    ],
    "upi_request": [
        r"\bupi\b",
        r"send money",
        r"payment"
    ],
    "otp_request": [
        r"\botp\b",
        r"one time password"
    ],
    "phishing_link": [
        r"http://",
        r"https://",
        r"click.*link"
    ]
}


def detect_intent(text: str) -> str:
    text = text.lower()

    for intent, patterns in INTENT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text):
                return intent

    return "generic_threat"
