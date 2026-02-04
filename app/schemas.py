from pydantic import BaseModel
from typing import List, Optional


# Single message object
class Message(BaseModel):
    sender: str           # "scammer" or "user"
    text: str
    timestamp: str        # ISO-8601 string


# Metadata object
class Metadata(BaseModel):
    channel: Optional[str]
    language: Optional[str]
    locale: Optional[str]


# Incoming request from Mock Scammer API
class IncomingRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: List[Message] = []
    metadata: Optional[Metadata]


# Response we send back
class AgentResponse(BaseModel):
    status: str
    reply: str
