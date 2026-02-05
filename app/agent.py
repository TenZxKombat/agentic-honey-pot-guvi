def generate_agent_reply(session: dict, intent: str) -> str:
    """
    Rule-based fallback agent.
    Must be fast, neutral, and non-assumptive.
    """

    # Track stage per intent (not global)
    stages = session.setdefault("agentStages", {})
    stage = stages.get(intent, 0)

    if intent == "bank_threat":
        replies = [
            # ALWAYS start neutral
            "What do you mean? Why will my account be blocked?",
            "Blocked because of what exactly?",
            "I didn’t get any alert from the bank. What happened?",
            "Okay… what do I need to do to fix this?"
        ]

    elif intent == "upi_request":
        replies = [
            "Why do you need my UPI ID?",
            "I don’t usually share UPI like this. Is it necessary?",
            "Where exactly do I find my UPI ID?",
            "Let me check and get back to you."
        ]

    elif intent == "otp_request":
        replies = [
            "I haven’t received any OTP yet.",
            "How long does it usually take?",
            "It’s still not coming.",
            "Maybe I’ll try again later."
        ]

    elif intent == "phishing_link":
        replies = [
            "What is this link for?",
            "Is this the official website?",
            "It’s not opening properly for me.",
            "I’ll check it later."
        ]

    else:  # generic / unknown
        replies = [
            "Can you explain what this is about?",
            "I’m not sure I understand.",
            "Why is this happening?",
            "Let me look into it later."
        ]

    # Select reply safely
    reply = replies[min(stage, len(replies) - 1)]

    # Increment stage for this intent only
    stages[intent] = stage + 1
    session["agentStages"] = stages

    return reply
