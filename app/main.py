from fastapi import FastAPI, Depends
from app.security import verify_api_key
from app.schemas import IncomingRequest, AgentResponse
from app.memory import get_session, add_message
from app.detector import detect_scam_intent

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

    # 3. Store incoming message
    add_message(
        session=session,
        sender=request.message.sender,
        text=request.message.text,
        timestamp=request.message.timestamp
    )

    # 4. Detect scam intent for CURRENT message
    detection = detect_scam_intent(request.message.text)
    session["lastDetection"] = detection

    # 5. Update intelligence store
    session["intelligence"]["suspiciousKeywords"].extend(
        detection["matched_keywords"]
    )

    # 6. Mark session as scam if detected
    if detection["is_scam"]:
        session["scamDetected"] = True

    # 7. Phase 5 reply logic (NO agent yet)
    if detection["is_scam"]:
        reply_text = "I’m not sure what this means. Can you explain?"
    else:
        reply_text = "Hello, how can I help you?"

    # 8. Store reply
    add_message(
        session=session,
        sender="user",
        text=reply_text,
        timestamp="now"
    )

    # 9. Return response
    return {
        "status": "success",
        "reply": reply_text
    }
