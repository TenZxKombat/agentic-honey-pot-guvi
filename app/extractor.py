import re

UPI_REGEX = re.compile(r"[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}")
PHONE_REGEX = re.compile(r"(?:\+91[\s\-]?)?[6-9]\d{9}")
URL_REGEX = re.compile(r"https?://[^\s]+")
BANK_ACC_REGEX = re.compile(r"\d{9,18}")

SUSPICIOUS_KEYWORDS = [
    "blocked", "verify", "verification", "urgent",
    "immediately", "suspended", "account", "otp",
    "upi", "call", "share", "now",
    "reward", "prize", "lottery", "claim",
    "final notice", "support", "executive", "act", "bank",
    "act",
    "details",
    "click",
    "link",
    "kyc",
]


def extract_intelligence(text: str, intelligence: dict):
    lower_text = text.lower()

    # 1️⃣ Phone numbers (FIXED)
    phones_found = PHONE_REGEX.findall(text)
    for phone in phones_found:
        phone_clean = phone.strip()
        if phone_clean not in intelligence["phoneNumbers"]:
            intelligence["phoneNumbers"].append(phone_clean)

    phone_digits = {re.sub(r"\D", "", p) for p in intelligence["phoneNumbers"]}

    # 2️⃣ UPI IDs
    for upi in UPI_REGEX.findall(text):
        if upi not in intelligence["upiIds"]:
            intelligence["upiIds"].append(upi)

    # 3️⃣ Links
    for url in URL_REGEX.findall(text):
        if url not in intelligence["phishingLinks"]:
            intelligence["phishingLinks"].append(url)

    # 4️⃣ Bank accounts (exclude phones)
    for acc in BANK_ACC_REGEX.findall(text):
        acc_digits = acc.lstrip("0")

        if acc_digits in phone_digits:
            continue
        if acc_digits.startswith("91") and len(acc_digits) <= 12:
            continue

        if acc not in intelligence["bankAccounts"]:
            intelligence["bankAccounts"].append(acc)

    # 5️⃣ Suspicious keywords
    for word in SUSPICIOUS_KEYWORDS:
        if word in lower_text and word not in intelligence["suspiciousKeywords"]:
            intelligence["suspiciousKeywords"].append(word)
