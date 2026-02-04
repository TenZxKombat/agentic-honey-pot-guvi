from fastapi import FastAPI, Depends
from app.security import verify_api_key
from app.schemas import IncomingRequest, AgentResponse
from app.memory import get_session, add_message
from app.detector import detect_scam_intent
from app.intent import detect_intent
from app.agent import generate_agent_reply

app = FastAPI(title="Agentic Honey-Pot API")


@app.get("/health", dependencies=[Depends(verify_api_key)])
def health():
    return {"status": "ok"}


@app.post(
    "/honeypot/message",
    response_model=AgentResponse,
    dependencies=[Depends(verify_api_key)]
)
def honeypot_message(request: IncomingRequest):
    # 1. Get or create session
    session = get_session(request.sessionId)

    # 2. Store metadata once
    if session["metadata"] is None:
        session["metadata"] = request.metadata

    # 3. Store incoming scammer message
    add_message(
        session=session,
        sender=request.message.sender,
        text=request.message.text,
        timestamp=request.message.timestamp
    )

    # 4. Detect scam intent (Phase 5)
    detection = detect_scam_intent(request.message.text)
    session["lastDetection"] = detection

    # 5. Update intelligence keywords (for reporting later)
    session["intelligence"]["suspiciousKeywords"].extend(
        detection["matched_keywords"]
    )

    # 6. Mark session as scam if ever detected
    if detection["is_scam"]:
        session["scamDetected"] = True

    # 7. Phase 6B — semantic-aware agent response
    if detection["is_scam"] or session["scamDetected"]:
        intent = detect_intent(request.message.text)
        reply_text = generate_agent_reply(session, intent)
    else:
        reply_text = "Hello, how can I help you?"

    # 8. Store agent reply
    add_message(
        session=session,
        sender="user",
        text=reply_text,
        timestamp="now"
    )

    # 9. Return structured response
    return {
        "status": "success",
        "reply": reply_text
    }
