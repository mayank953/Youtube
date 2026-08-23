# Pydantic — Complete Crash Course

A complete, hands-on course covering Pydantic (data validation in Python) from first principles through to using it as the foundation for reliable AI applications — structured LLM outputs, FastAPI integration, and a full working final project.

One consistent example — a `Customer` — runs through the entire course, evolving from a simple signup form into a full AI-powered support ticket triage system by the final project.

## Structure

| Part | Topic | Docs | Code |
|---|---|---|---|
| 01 | Why Pydantic Exists + Type Hints | [docs/01](docs/01-why-pydantic-and-type-hints.md) | [code/01](code/01_why_pydantic_and_type_hints/) |
| 02 | Your First Model | [docs/02](docs/02-your-first-model.md) | [code/02](code/02_your_first_model/) |
| 03 | Field Constraints & Custom Validators | [docs/03](docs/03-field-constraints-and-validators.md) | [code/03](code/03_field_constraints_and_validators/) |
| 04 | Computed Fields & Serialization | [docs/04](docs/04-computed-fields-and-serialization.md) | [code/04](code/04_computed_fields_and_serialization/) |
| 05 | Nested Models | [docs/05](docs/05-nested-models.md) | [code/05](code/05_nested_models/) |
| 06 | Pydantic Settings | [docs/06](docs/06-pydantic-settings.md) | [code/06](code/06_pydantic_settings/) |
| 07 | Pydantic + FastAPI | [docs/07](docs/07-pydantic-and-fastapi.md) | [code/07](code/07_pydantic_and_fastapi/) |
| 08 | The AI Bridge: Structured LLM Outputs | [docs/08](docs/08-ai-bridge-structured-outputs.md) | [code/08](code/08_ai_bridge_structured_outputs/) |
| 09 | Where Pydantic Goes From Here | [docs/09](docs/09-ecosystem-map.md) | [code/09](code/09_ecosystem_map/) |
| 10 | Final Project — AI Support Ticket Triage | [docs/10](docs/10-final-project.md) | [code/10](code/10_final_project_ticket_triage/) |

## Scope

This course teaches **core Pydantic** — `BaseModel`, `Field`, validators, `computed_field`, nested models, serialization, `pydantic-settings`, and using Pydantic models directly with the OpenAI and Anthropic SDKs for structured output.

It does **not** teach any agent framework. PydanticAI, LangChain, CrewAI, and Instructor are mentioned in Part 09 for context only — see [docs/09](docs/09-ecosystem-map.md) for an honest map of where they sit relative to what's covered here.

## Getting started

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Each part's folder under `code/` is self-contained and runnable on its own — files are numbered in the order they're meant to be read (`1.1`, `1.2`, `1.3`, then `demo_project.py`). Parts 01–07 need no API key. Parts 08 and 10 need at least one of: an Anthropic key, an OpenAI key, or a free OpenRouter key (see `.env.example` in those folders).

## Requirements

- Python 3.11+
- See `requirements.txt` for the full dependency list
