def generate_agent_reply(session: dict) -> str:
    stage = session.get("agentStage", 0)

    if stage == 0:
        reply = "What do you mean? Why will my account be blocked?"
    elif stage == 1:
        reply = "Which bank are you talking about?"
    elif stage == 2:
        reply = "Okay… what do I need to do to fix this?"
    else:
        reply = "I’m a bit busy right now. Can I do this later?"

    session["agentStage"] = stage + 1
    return reply
