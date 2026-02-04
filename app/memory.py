from typing import Dict

# In-memory session store
SESSIONS: Dict[str, dict] = {}

def get_session(session_id: str) -> dict:
    """
    Returns existing session or creates a new one.
    """
    if session_id not in SESSIONS:
        SESSIONS[session_id] = {
            "messages": [],       
            "metadata": None,   
            "intelligence": {        # later
                "bankAccounts": [],
                "upiIds": [],
                "phishingLinks": [],
                "phoneNumbers": [],
                "suspiciousKeywords": []
            },
            "scamDetected": False,
            "completed": False
        }
    return SESSIONS[session_id]

def add_message(session: dict, sender: str, text: str, timestamp: str):
    session["messages"].append({
        "sender": sender,
        "text": text,
        "timestamp": timestamp
    })

