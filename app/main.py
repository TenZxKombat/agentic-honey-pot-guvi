from fastapi import FastAPI, Depends
from threading import Thread
from copy import deepcopy

from app.security import verify_api_key
from app.schemas import IncomingRequest, AgentResponse
from app.memory import get_session, add_message
from app.detector import detect_scam_intent
from app.intent import detect_intent
from app.agent import generate_agent_reply          # fast fallback
from app.llm_agent import generate_llm_reply         # background LLM
from app.extractor import extract_intelligence       # Phase 8A

app = FastAPI(title="Agentic Honey-Pot API")


# ─────────────────────────────────────────────
# Health Check
# ─────────────────────────────────────────────
@app.get("/health", dependencies=[Depends(verify_api_key)])
def health():
    return {"status": "ok"}


# ─────────────────────────────────────────────
# Background LLM Task (NON-BLOCKING)
# ─────────────────────────────────────────────
def run_llm_in_background(session_snapshot: dict):
    llm_reply = generate_llm_reply(
        conversation_history=session_snapshot["messages"],
        intelligence=session_snapshot["intelligence"]
    )
    if llm_reply:
        session_snapshot["pendingLLMReply"] = llm_reply


# ─────────────────────────────────────────────
# Main Honeypot Endpoint
# ─────────────────────────────────────────────
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

    # ─────────────────────────────────────────────
    # Phase 8A: Intelligence Extraction (INSTANT)
    # ─────────────────────────────────────────────
    extract_intelligence(
        request.message.text,
        session["intelligence"]
    )

    # ─────────────────────────────────────────────
    # Phase 5: Scam Detection (FAST)
    # ─────────────────────────────────────────────
    detection = detect_scam_intent(request.message.text)
    session["lastDetection"] = detection

    if detection["is_scam"]:
        session["scamDetected"] = True

    # ─────────────────────────────────────────────
    # Phase 8: Low-Latency Conversation
    # ─────────────────────────────────────────────

    # Use prepared LLM reply if available
    if "pendingLLMReply" in session:
        reply_text = session.pop("pendingLLMReply")

    else:
        # Immediate fallback reply (<200ms)
        intent = detect_intent(request.message.text)
        reply_text = generate_agent_reply(session, intent)

        # Fire LLM asynchronously for NEXT turn
        session_snapshot = deepcopy(session)

        Thread(
            target=run_llm_in_background,
            args=(session_snapshot,),
            daemon=True
        ).start()

    # 4. Store agent reply
    add_message(
        session=session,
        sender="user",
        text=reply_text,
        timestamp="now"
    )

    # 5. Return response immediately
    return {
        "status": "success",
        "reply": reply_text
    }


# ─────────────────────────────────────────────
# DEBUG ENDPOINT (FOR LOCAL TESTING ONLY)
# ❌ REMOVE BEFORE FINAL SUBMISSION
# ─────────────────────────────────────────────
@app.get(
    "/debug/session/{session_id}",
    dependencies=[Depends(verify_api_key)]
)
def debug_session(session_id: str):
    session = get_session(session_id)
    return {
        "messages": session["messages"],
        "intelligence": session["intelligence"],
        "scamDetected": session["scamDetected"]
    }
