"""
8.2 — OPENAI STRUCTURED OUTPUTS WITH PYDANTIC
=============================================================
Install first: pip install openai python-dotenv
Requires an OPENAI_API_KEY in a .env file in this folder (copy
.env.example and fill it in).
"""

from typing import Literal
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class CustomerMessage(BaseModel):
    customer_name: str
    topic: Literal["billing", "shipping", "technical", "general"]
    is_urgent: bool


client = OpenAI()

response = client.responses.parse(
    model="gpt-4o",
    input="Extract: Rohan says his order hasn't shipped yet and he's quite annoyed about it.",
    text_format=CustomerMessage,   # pass the Pydantic MODEL, not a JSON schema dict
)

# response.output_parsed is ALREADY a validated CustomerMessage instance
message: CustomerMessage = response.output_parsed
print("Fully parsed, typed, validated result:")
print(f"  customer_name: {message.customer_name}")
print(f"  topic:         {message.topic}")
print(f"  is_urgent:     {message.is_urgent}")


# A richer example — nested models + Literal + a list, extracting a
# whole support call's structured summary from a messy paragraph.
class FollowUpAction(BaseModel):
    task: str
    priority: Literal["low", "medium", "high"] = "medium"


class SupportCallSummary(BaseModel):
    customer_name: str
    topics_discussed: list[str]
    summary: str = Field(max_length=300)
    follow_ups: list[FollowUpAction]


call_response = client.responses.parse(
    model="gpt-4o",
    input="""
    Call with Aditi Sharma. She asked about her recent order status and
    also wanted to update her shipping address. We need to update her
    address by Friday — that's high priority — and send her a tracking
    link, which is lower priority.
    """,
    text_format=SupportCallSummary,
)

summary = call_response.output_parsed
print(f"\nCustomer: {summary.customer_name}")
print(f"Topics: {', '.join(summary.topics_discussed)}")
for action in summary.follow_ups:
    print(f"  - [{action.priority}] {action.task}")
