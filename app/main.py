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
    
    session = get_session(request.sessionId)

    if session["metadata"] is None:
        session["metadata"] = request.metadata

    add_message(
        session=session,
        sender=request.message.sender,
        text=request.message.text,
        timestamp=request.message.timestamp
    )

    detection = detect_scam_intent(request.message.text)

    session["intelligence"]["suspiciousKeywords"].extend(
        detection["matched_keywords"]
    )

    if detection["is_scam"]:
        session["scamDetected"] = True

    if session["scamDetected"]:
        reply_text = "I’m confused. Why would my account be blocked?"
    else:
        reply_text = "Hello, how can I help you?"

    add_message(
        session=session,
        sender="user",
        text=reply_text,
        timestamp="now"
    )

    return {
        "status": "success",
        "reply": reply_text
    }

