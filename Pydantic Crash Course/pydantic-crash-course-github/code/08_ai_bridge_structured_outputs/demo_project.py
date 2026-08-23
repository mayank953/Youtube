"""
DEMO — Same Customer Message, Same Schema, Any Provider
=============================================================
Run the same messy customer message through OpenAI, Anthropic, or
OpenRouter — proving the Pydantic model definition is provider-agnostic.

Set up .env (copy .env.example) with at least ONE key, then:
    python demo_project.py
"""

import os
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict
from dotenv import load_dotenv

load_dotenv()

MESSY_MESSAGE = (
    "hey my order didnt come yet its been like 2 weeks!! order number "
    "maybe 4521?? im pretty annoyed ngl - Rohan"
)


class TicketClassification(BaseModel):
    model_config = ConfigDict(extra="forbid")
    customer_name: str | None = None
    category: Literal["billing", "shipping", "technical", "general_question"]
    priority: Literal["low", "medium", "high"]
    sentiment: Literal["positive", "negative", "neutral"]
    order_id: int | None = Field(default=None, description="Order number if mentioned")
    summary: str = Field(max_length=200)


def classify_with_anthropic(text: str) -> TicketClassification:
    from anthropic import Anthropic

    client = Anthropic()
    response = client.messages.parse(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": f"Classify this support ticket:\n\n{text}"}],
        output_format=TicketClassification,
    )
    return response.parsed_output


def classify_with_openai(text: str) -> TicketClassification:
    from openai import OpenAI

    client = OpenAI()
    response = client.responses.parse(
        model="gpt-4o",
        input=f"Classify this support ticket:\n\n{text}",
        text_format=TicketClassification,
    )
    return response.output_parsed


def classify_with_openrouter_free(text: str) -> TicketClassification:
    import json
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
    schema = json.dumps(TicketClassification.model_json_schema())
    completion = client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct:free",
        messages=[
            {
                "role": "system",
                "content": f"Respond with ONLY raw JSON matching this schema, no markdown fences:\n{schema}",
            },
            {"role": "user", "content": f"Classify this support ticket:\n\n{text}"},
        ],
    )
    raw = completion.choices[0].message.content.strip()
    cleaned = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return TicketClassification.model_validate(json.loads(cleaned))


if __name__ == "__main__":
    print(f"Message: {MESSY_MESSAGE}\n")

    if os.getenv("ANTHROPIC_API_KEY"):
        print("Using Anthropic (Claude)...")
        result = classify_with_anthropic(MESSY_MESSAGE)
    elif os.getenv("OPENAI_API_KEY"):
        print("Using OpenAI...")
        result = classify_with_openai(MESSY_MESSAGE)
    elif os.getenv("OPENROUTER_API_KEY"):
        print("Using OpenRouter (free model)...")
        result = classify_with_openrouter_free(MESSY_MESSAGE)
    else:
        raise SystemExit(
            "No API key found. Set ANTHROPIC_API_KEY, OPENAI_API_KEY, or "
            "OPENROUTER_API_KEY in your .env file (see .env.example)."
        )

    print("\nValidated result (identical shape, regardless of provider):")
    print(result.model_dump_json(indent=2))
