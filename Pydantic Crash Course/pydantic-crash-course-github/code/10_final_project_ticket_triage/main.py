"""
FINAL PROJECT — main.py
=============================================================
Every concept from Parts 1-8 in one running system.

Install first:
    pip install fastapi uvicorn anthropic openai python-dotenv pydantic-settings

Run:
    1. Copy .env.example to .env and add at least ONE API key
       (OpenRouter's free tier works if you don't have a paid key)
    2. uvicorn main:app --reload
    3. Open http://127.0.0.1:8000  -> the plain-HTML front end
       Open http://127.0.0.1:8000/docs -> the auto-generated API docs
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import ValidationError

from models import IncomingTicket, TriageResponse
from llm_client import triage_ticket
from settings import get_settings

app = FastAPI(title="AI Support Ticket Triage API")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")


@app.post("/triage", response_model=TriageResponse)
def triage(incoming: IncomingTicket) -> TriageResponse:
    """
    1. FastAPI + `incoming: IncomingTicket` already validated the
       request body before this line runs (Part 7) — including the
       email-redaction field_validator firing automatically.
    2. triage_ticket() calls whichever AI provider is configured
       (Part 8) and returns an already-validated TriagedTicket,
       including its computed sla_hours (Part 4) and its
       model_validator safety-net rule (Part 3).
    3. Reshaped into the smaller public TriageResponse (Part 4's
       serialization-control lesson, applied structurally).
    """
    try:
        result = triage_ticket(incoming)
    except ValidationError as e:
        raise HTTPException(status_code=502, detail=f"AI response failed validation: {e}")
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))

    return TriageResponse.from_triaged_ticket(result)


@app.get("/health")
def health_check():
    settings = get_settings()
    try:
        provider = settings.active_provider()
        return {"status": "ok", "active_provider": provider}
    except RuntimeError as e:
        return {"status": "not_configured", "detail": str(e)}
