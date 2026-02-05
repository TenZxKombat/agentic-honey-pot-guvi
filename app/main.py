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
# ROOT ENDPOINT (PUBLIC — FOR GUVI TESTER)
# Accepts GET, POST, HEAD
# ─────────────────────────────────────────────
@app.api_route("/", methods=["GET", "POST", "HEAD"])
def root():
    return {"status": "ok"}


# ─────────────────────────────────────────────
# HEALTH CHECK (PUBLIC)
# ─────────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok"}


# ─────────────────────────────────────────────
# HONEYPOT ENDPOINT (SECURED)
# ─────────────────────────────────────────────
@app.post(
    "/honeypot/message",
    response_model=AgentResponse,
    dependencies=[Depends(verify_api_key)]
)
def honeypot_message(request: IncomingRequest):

    session = get_session(request.sessionId)

    if session["metadata"] is None:
        session["metadata"] = request.metadata

    add_message(
        session=session,
        sender=request.message.sender,
        text=request.message.text,
        timestamp=request.message.timestamp
    )

    extract_intelligence(
        request.message.text,
        session["intelligence"]
    )

    detection = detect_scam_intent(request.message.text)
    if detection["is_scam"]:
        session["scamDetected"] = True

    intent = detect_intent(request.message.text)
    reply_text = generate_agent_reply(session, intent)

    add_message(
        session=session,
        sender="user",
        text=reply_text,
        timestamp="now"
    )

    scammer_message_count = sum(
        1 for m in session["messages"] if m["sender"] == "scammer"
    )

    has_intel = any(len(v) > 0 for v in session["intelligence"].values())

    if (
        session["scamDetected"]
        and not session["completed"]
        and scammer_message_count >= 6
        and has_intel
    ):
        send_final_result(session, request.sessionId)
        session["completed"] = True

    return {
        "status": "success",
        "reply": reply_text
    }
