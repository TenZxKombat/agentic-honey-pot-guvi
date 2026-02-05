from openai import OpenAI
from app.config import OPENAI_API_KEY

# Fail fast if key is missing
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not loaded")

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are a normal Indian user talking to someone who contacted you first.

You do NOT know it is a scam.
You are confused and cautious.
If the message is vague (e.g. "account will be blocked"),
you ask WHY and WHAT happened.

You do NOT assume bank names, companies, or prizes.
You do NOT invent details.

Keep replies short, natural, and questioning.
"""

def generate_llm_reply(conversation_history, intelligence):
    """
    Generate a human-like reply using LLM.
    IMPORTANT: Only scammer messages are fed to the LLM.
    """

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Only include scammer messages (critical fix)
    for msg in conversation_history:
        if msg.get("sender") == "scammer":
            messages.append({
                "role": "user",
                "content": msg.get("text", "")
            })

    try:
        response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages[-4:],   # system + last 3 scammer msgs
        max_tokens=40,
        temperature=0.6,
        timeout=2
         )

        
        return response.choices[0].message.content.strip()

    except Exception as e:
        print("LLM ERROR:", str(e))
        return None
