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
