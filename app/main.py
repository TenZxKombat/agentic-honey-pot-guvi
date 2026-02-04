from fastapi import FastAPI, Depends
from app.security import verify_api_key

app = FastAPI(
    title="Agentic Honeypot API",
    description="Agentic Honey-Pot for Scam Detection & Intelligence Extraction",
    version="1.0.0"
)

@app.get("/health", dependencies=[Depends(verify_api_key)])
def health_check():
    return {"status": "ok"}
