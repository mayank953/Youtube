"""
FINAL PROJECT — llm_client.py
=============================================================
Reuses Part 8's structured-output patterns (OpenAI, Anthropic,
OpenRouter free fallback), consolidated into one function the FastAPI
endpoint calls without needing to know which provider is active.
"""

import json
from anthropic import Anthropic
from openai import OpenAI

from models import IncomingTicket, TriagedTicket
from settings import get_settings


def triage_ticket(ticket: IncomingTicket) -> TriagedTicket:
    settings = get_settings()
    provider = settings.active_provider()

    prompt = (
        f"Classify this customer support ticket.\n\n"
        f"Message: {ticket.message}\n"
        f"Customer name (if known): {ticket.customer_name or 'unknown'}\n\n"
        f"If an order number is mentioned anywhere in the message, extract it "
        f"as customer.order_id."
    )

    if provider == "anthropic":
        return _triage_with_anthropic(prompt, settings)
    elif provider == "openai":
        return _triage_with_openai(prompt, settings)
    else:
        return _triage_with_openrouter_free(prompt, settings)


def _triage_with_anthropic(prompt: str, settings) -> TriagedTicket:
    client = Anthropic(api_key=settings.anthropic_api_key.get_secret_value())
    response = client.messages.parse(
        model=settings.anthropic_model,
        max_tokens=settings.max_tokens,
        messages=[{"role": "user", "content": prompt}],
        output_format=TriagedTicket,
    )
    return response.parsed_output


def _triage_with_openai(prompt: str, settings) -> TriagedTicket:
    client = OpenAI(api_key=settings.openai_api_key.get_secret_value())
    response = client.responses.parse(
        model=settings.openai_model,
        input=prompt,
        text_format=TriagedTicket,
    )
    return response.output_parsed


def _triage_with_openrouter_free(prompt: str, settings, max_retries: int = 3) -> TriagedTicket:
    client = OpenAI(
        api_key=settings.openrouter_api_key.get_secret_value(),
        base_url="https://openrouter.ai/api/v1",
    )
    schema = json.dumps(TriagedTicket.model_json_schema())
    system_prompt = (
        "You are a support ticket classifier. Respond with ONLY raw JSON "
        f"matching this exact schema, no markdown fences, no extra text:\n{schema}"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]

    last_error = None
    for attempt in range(1, max_retries + 1):
        if last_error:
            messages.append(
                {
                    "role": "user",
                    "content": f"Your previous response was invalid: {last_error}\nRespond with corrected valid JSON only.",
                }
            )

        completion = client.chat.completions.create(
            model=settings.openrouter_free_model,
            messages=messages,
        )
        raw = completion.choices[0].message.content.strip()
        cleaned = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

        try:
            data = json.loads(cleaned)
            return TriagedTicket.model_validate(data)
        except Exception as e:
            last_error = str(e)

    raise RuntimeError(f"Failed to get a valid triage result after {max_retries} attempts: {last_error}")
