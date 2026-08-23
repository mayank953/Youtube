# 10 — Final Project: AI Support Ticket Triage

A FastAPI backend exposing one endpoint, `POST /triage`. It accepts a raw, messy support message, sends it to an LLM (Anthropic, OpenAI, or a free OpenRouter model — whichever key is configured) with a guaranteed structured-output schema, and returns a fully validated, typed result: category, priority, sentiment, a computed SLA deadline, and redacted customer info.

Every concept from this course appears somewhere in this project:

| Concept | Where it appears |
|---|---|
| `BaseModel` + type hints | `IncomingTicket`, `TriagedTicket` |
| `Field` constraints | `message: str = Field(min_length=5, max_length=2000)` |
| `field_validator` | Redacts emails out of the raw message (`mode='before'`) |
| `model_validator` | `priority='high'` can't pair with `category='general_question'` |
| `computed_field` | `sla_hours`, derived live from `priority` |
| Nested models | `TriagedTicket.customer: CustomerInfo` |
| Serialization control | `TriageResponse` — a deliberately narrower public shape |
| `BaseSettings` | Multi-provider API key config with a free fallback |
| FastAPI integration | `IncomingTicket` as the `/triage` request body type |
| Structured LLM output | `client.messages.parse(output_format=TriagedTicket)` |

## Running it

```bash
cd code/10_final_project_ticket_triage
pip install -r ../../requirements.txt
cp .env.example .env   # add at least one API key — OpenRouter's free tier works
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000` for the plain-HTML front end, or `http://127.0.0.1:8000/docs` for the interactive API docs.

**Code for this part:** [`code/10_final_project_ticket_triage/`](../code/10_final_project_ticket_triage/)
