"""
8.3 — CLAUDE (ANTHROPIC) STRUCTURED OUTPUTS WITH PYDANTIC
=============================================================
Install first: pip install anthropic python-dotenv
Requires an ANTHROPIC_API_KEY in a .env file in this folder (copy
.env.example and fill it in).
"""

from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


class CustomerMessage(BaseModel):
    # extra="forbid" adds "additionalProperties": false to the generated
    # JSON schema — tightens the contract so the model can't add
    # surprise extra keys we didn't ask for.
    model_config = ConfigDict(extra="forbid")

    customer_name: str
    topic: Literal["billing", "shipping", "technical", "general"]
    is_urgent: bool


client = Anthropic()

# Pattern A — the higher-level .parse() method, direct equivalent of
# OpenAI's responses.parse.
response = client.messages.parse(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Extract: Rohan says his order hasn't shipped yet and he's quite annoyed about it.",
        }
    ],
    output_format=CustomerMessage,
)

message: CustomerMessage = response.parsed_output
print("Fully parsed, typed, validated result (via Claude):")
print(f"  customer_name: {message.customer_name}")
print(f"  topic:         {message.topic}")
print(f"  is_urgent:     {message.is_urgent}")


# Pattern B — the underlying "strict tool use" mechanism, for cases
# needing finer control. Same idea, different name.
class SpamCheck(BaseModel):
    model_config = ConfigDict(extra="forbid")
    is_spam: bool = Field(description="True if the message is spam")
    reason: str = Field(description="Brief reason for the determination")


tool_response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system="Determine if the following customer message is spam.",
    messages=[
        {"role": "user", "content": "Congratulations! You've won $1000! Click now to claim!!!"}
    ],
    tools=[
        {
            "name": "spam_check",
            "description": "Return the spam detection result",
            "input_schema": SpamCheck.model_json_schema(),
        }
    ],
    tool_choice={"type": "tool", "name": "spam_check"},
)

tool_use_block = next(block for block in tool_response.content if block.type == "tool_use")
spam_result = SpamCheck.model_validate(tool_use_block.input)
print(f"\nSpam check result: is_spam={spam_result.is_spam}, reason={spam_result.reason!r}")
