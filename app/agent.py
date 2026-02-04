def generate_agent_reply(session: dict, intent: str) -> str:
    stage = session.get("agentStage", 0)

    if intent == "bank_threat":
        replies = [
            "What do you mean? Why will my account be blocked?",
            "Which bank are you talking about?",
            "Okay… what do I need to do to fix this?",
            "I’m a bit busy right now. Can I do this later?"
        ]

    elif intent == "upi_request":
        replies = [
            "I don’t use UPI much. What is it exactly?",
            "Where do I find my UPI ID?",
            "Is it safe to share UPI like this?",
            "I’ll check and get back to you later."
        ]

    elif intent == "otp_request":
        replies = [
            "I haven’t received any OTP yet.",
            "Should I wait for the message?",
            "It’s not coming. Can you resend it?",
            "Maybe I’ll try later."
        ]

    elif intent == "phishing_link":
        replies = [
            "The link isn’t opening for me.",
            "Is this the correct link?",
            "It says page not found.",
            "I’ll try again later."
        ]

    else:  # generic_threat
        replies = [
            "Can you explain what this is about?",
            "Why is this happening?",
            "What do I need to do?",
            "I’ll take care of it later."
        ]

    # Cap stage to last reply
    reply = replies[min(stage, len(replies) - 1)]
    session["agentStage"] = stage + 1
    return reply
