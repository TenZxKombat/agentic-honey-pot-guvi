from app.memory import get_session, add_message
from app.schemas import IncomingRequest, AgentResponse
from app.security import verify_api_key
from fastapi import FastAPI, Depends

app = FastAPI(
    title="Agentic Honeypot API",
    description="Agentic Honey-Pot for Scam Detection & Intelligence Extraction",
    version="1.0.0"
)

@app.get("/health", dependencies=[Depends(verify_api_key)])
def health_check():
    return {"status": "ok"}


@app.post(
    "/honeypot/message",
    response_model=AgentResponse,
    dependencies=[Depends(verify_api_key)]
)
def honeypot_message(request: IncomingRequest):

    session = get_session(request.sessionId)

    # Save metadata once
    if session["metadata"] is None:
        session["metadata"] = request.metadata

    # Store incoming message
    add_message(
        session,
        sender=request.message.sender,
        text=request.message.text,
        timestamp=request.message.timestamp
    )

    reply_text = "Can you explain this more clearly?"

    add_message(
        session,
        sender="agent",
        text=reply_text,
        timestamp="now"
    )

    return {
        "status": "success",
        "reply": reply_text
    }
