from fastapi import FastAPI

app = FastAPI(
    title="Agentic Honeypot API",
    description="Agentic Honey-Pot for Scam Detection & Intelligence Extraction",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    return {"status": "ok"}
