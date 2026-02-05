import requests

GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"


def send_final_result(session: dict, session_id: str):
    """
    Sends final extracted intelligence to GUVI evaluation endpoint.
    """

    payload = {
        "sessionId": session_id,
        "scamDetected": session.get("scamDetected", False),
        "totalMessagesExchanged": len(session.get("messages", [])),
        "extractedIntelligence": session.get("intelligence", {}),
        "agentNotes": generate_agent_notes(session)
    }

    try:
        response = requests.post(
            GUVI_CALLBACK_URL,
            json=payload,
            timeout=5
        )
        print("GUVI CALLBACK STATUS:", response.status_code)
    except Exception as e:
        print("GUVI CALLBACK FAILED:", str(e))


def generate_agent_notes(session: dict) -> str:
    """
    Human-readable summary of scammer behavior.
    """
    keywords = session["intelligence"].get("suspiciousKeywords", [])

    if "upi" in keywords:
        return "Scammer attempted UPI-based payment fraud"
    if "lottery" in keywords or "prize" in keywords:
        return "Scammer used lottery or reward-based scam"
    if "blocked" in keywords or "verify" in keywords:
        return "Scammer used urgency and account threat tactics"

    return "Suspicious scam behavior detected"
