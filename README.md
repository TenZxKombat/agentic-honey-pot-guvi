# Agentic Honeypot for Scam Detection

This project is built for the GUVI x HCL National Hackathon.

Phase 1:
- FastAPI project bootstrap
- Health check endpoint

Phase 2:
- API security layer using x-api-key
- Unauthorized requests blocked with 401 response
- Centralized security dependency in FastAPI
- API key managed via environment variables
- Ensures only authorized clients can access the API

Phase 3:
- Request and response schema validation using Pydantic
- Strict adherence to GUVI-defined input and output formats
- Validation of conversationHistory structure
- Prevents malformed or unexpected requests
- Ensures compatibility with automated evaluation

Phase 4: Session Memory & Multi-Turn Conversation Handling
- In-memory session management using unique sessionId
- Persistent conversation state across multiple API calls
- Support for multi-turn scam conversations
- Automatic grouping of messages by session
- Agent responses appended to conversation history
- Schema-safe handling of optional metadata
- Foundation for agent reasoning and intelligence extraction
