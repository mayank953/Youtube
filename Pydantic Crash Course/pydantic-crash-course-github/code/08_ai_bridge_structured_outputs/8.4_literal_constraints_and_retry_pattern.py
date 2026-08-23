"""
8.4 — Literal FOR CONSTRAINED AI OUTPUTS + THE RETRY PATTERN
=============================================================
Install first: pip install openai python-dotenv
Requires an OPENROUTER_API_KEY in your .env file — a free tier is
available at https://openrouter.ai/keys, so this file runs without a
paid OpenAI/Anthropic key.

Structured outputs guarantee SHAPE, never CORRECTNESS. A perfectly
formatted, confidently wrong answer is still possible — validation
catches malformed data, not hallucinated facts.
"""

import json
import os
from typing import Literal
from pydantic import BaseModel, Field, ValidationError
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class TicketClassification(BaseModel):
    category: Literal["billing", "shipping", "technical", "general_question"]
    priority: Literal["low", "medium", "high"]
    sentiment: Literal["positive", "negative", "neutral"]
    summary: str = Field(max_length=200)


openrouter_client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)
FREE_MODEL = "meta-llama/llama-3.1-8b-instruct:free"   # check openrouter.ai/models for current free options


def ask_llm_for_json(raw_ticket_text: str, previous_error: str | None = None) -> str:
    """
    Not every provider/model supports guaranteed structured outputs the
    way OpenAI's or Anthropic's .parse() do. Many free models only
    support plain prompting, so here we describe the schema in the
    prompt ourselves and validate the response after the fact.
    """
    schema_description = json.dumps(TicketClassification.model_json_schema(), indent=2)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a support ticket classifier. Respond with ONLY raw JSON "
                f"matching this exact schema, no markdown fences, no extra text:\n{schema_description}"
            ),
        },
        {"role": "user", "content": f"Classify this support ticket:\n\n{raw_ticket_text}"},
    ]

    if previous_error:
        messages.append(
            {
                "role": "user",
                "content": f"Your previous response was invalid: {previous_error}\nPlease correct it and respond with valid JSON only.",
            }
        )

    completion = openrouter_client.chat.completions.create(model=FREE_MODEL, messages=messages)
    return completion.choices[0].message.content


def classify_ticket_with_retry(raw_ticket_text: str, max_retries: int = 3) -> TicketClassification | None:
    """
    Ask the model, try to validate, and if it fails, feed the error back
    and ask again. This is the entire mechanism behind "self-correcting"
    structured extraction.
    """
    last_error: str | None = None

    for attempt in range(1, max_retries + 1):
        print(f"  Attempt {attempt}/{max_retries}...")
        raw_response = ask_llm_for_json(raw_ticket_text, previous_error=last_error)
        cleaned = raw_response.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()

        try:
            data = json.loads(cleaned)
            return TicketClassification.model_validate(data)
        except (json.JSONDecodeError, ValidationError) as e:
            last_error = str(e)
            print(f"     Failed: {last_error[:120]}...")

    print(f"  Gave up after {max_retries} attempts.")
    return None


if __name__ == "__main__":
    messy_ticket = (
        "hey my order didnt come yet its been like 2 weeks!! order number "
        "maybe 4521?? im pretty annoyed ngl"
    )

    print("Classifying a messy ticket with automatic retry-on-failure:\n")
    result = classify_ticket_with_retry(messy_ticket)

    if result:
        print("\nFinal validated result:")
        print(result.model_dump_json(indent=2))
    else:
        print("\nCould not get a valid classification within the retry budget.")
