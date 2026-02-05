from fastapi import FastAPI, Depends
from app.security import verify_api_key
from app.schemas import IncomingRequest, AgentResponse
from app.memory import get_session, add_message
from app.detector import detect_scam_intent
from app.intent import detect_intent
from app.agent import generate_agent_reply
from app.extractor import extract_intelligence
from app.callback import send_final_result

app = FastAPI(title="Agentic Honey-Pot API")


# ─────────────────────────────────────────────
# Health Check (KEEP IN PROD)
# ─────────────────────────────────────────────
@app.get("/health", dependencies=[Depends(verify_api_key)])
def health():
    return {"status": "ok"}


# ─────────────────────────────────────────────
# Honeypot Endpoint
# ─────────────────────────────────────────────
@app.post(
    "/honeypot/message",
    response_model=AgentResponse,
    dependencies=[Depends(verify_api_key)]
)
def honeypot_message(request: IncomingRequest):

    # 1️⃣ Get or create session
    session = get_session(request.sessionId)

    # 2️⃣ Store metadata once
    if session["metadata"] is None:
        session["metadata"] = request.metadata

    # 3️⃣ Store incoming scammer message
    add_message(
        session=session,
        sender=request.message.sender,
        text=request.message.text,
        timestamp=request.message.timestamp
    )

    # 4️⃣ Phase 8A — Intelligence extraction
    extract_intelligence(
        request.message.text,
        session["intelligence"]
    )

    # 5️⃣ Phase 5 — Scam detection
    detection = detect_scam_intent(request.message.text)
    if detection["is_scam"]:
        session["scamDetected"] = True

    # 6️⃣ Agent reply (fast, deterministic)
    intent = detect_intent(request.message.text)
    reply_text = generate_agent_reply(session, intent)

    # 7️⃣ Store agent reply
    add_message(
        session=session,
        sender="user",
        text=reply_text,
        timestamp="now"
    )

    # ─────────────────────────────────────────────
    # Phase 9 — GUVI Final Callback (CORRECTED)
    # Fires AFTER 6 scammer messages
    # ─────────────────────────────────────────────
    scammer_message_count = sum(
        1 for m in session["messages"] if m["sender"] == "scammer"
    )

    has_intelligence = any(
        len(v) > 0 for v in session["intelligence"].values()
    )

    if (
        session.get("scamDetected") is True
        and session.get("completed") is not True
        and scammer_message_count >= 6   # ✅ FIXED CONDITION
        and has_intelligence
    ):
        send_final_result(session, request.sessionId)
        session["completed"] = True

    # 8️⃣ Return response
    return {
        "status": "success",
        "reply": reply_text
    }
