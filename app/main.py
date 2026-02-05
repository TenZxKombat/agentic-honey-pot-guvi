from fastapi import FastAPI, Depends
from threading import Thread
from copy import deepcopy

from app.security import verify_api_key
from app.schemas import IncomingRequest, AgentResponse
from app.memory import get_session, add_message
from app.detector import detect_scam_intent
from app.intent import detect_intent
from app.agent import generate_agent_reply          # FAST fallback
from app.llm_agent import generate_llm_reply         # SLOW but smart

app = FastAPI(title="Agentic Honey-Pot API")


@app.get("/health", dependencies=[Depends(verify_api_key)])
def health():
    return {"status": "ok"}


def run_llm_in_background(session_snapshot: dict):
    """
    Runs LLM without blocking API response.
    Stores reply for NEXT turn.
    """
    llm_reply = generate_llm_reply(
        conversation_history=session_snapshot["messages"],
        intelligence=session_snapshot["intelligence"]
    )
    if llm_reply:
        session_snapshot["pendingLLMReply"] = llm_reply


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
    # Phase 5: Scam detection (fast, parallel)
    # ─────────────────────────────────────────────
    detection = detect_scam_intent(request.message.text)
    session["lastDetection"] = detection

    if detection["is_scam"]:
        session["scamDetected"] = True

    session["intelligence"]["suspiciousKeywords"].extend(
        detection.get("matched_keywords", [])
    )

    # ─────────────────────────────────────────────
    # Phase 8: NON-BLOCKING conversation
    # ─────────────────────────────────────────────

    # If LLM already prepared a reply earlier → use it NOW
    if "pendingLLMReply" in session:
        reply_text = session.pop("pendingLLMReply")

    else:
        # FAST immediate reply (always <200ms)
        intent = detect_intent(request.message.text)
        reply_text = generate_agent_reply(session, intent)

        # Fire-and-forget LLM for next turn
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

    # 5. Return response (IMMEDIATE)
    return {
        "status": "success",
        "reply": reply_text
    }
