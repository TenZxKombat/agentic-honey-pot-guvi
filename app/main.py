from fastapi import FastAPI, Depends
from app.security import verify_api_key
from app.schemas import IncomingRequest, AgentResponse

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
    # For now, just a dummy reply to confirm the endpoint works
    return {
        "status": "success",
        "reply": "Hello, how can I help you?"
    }
