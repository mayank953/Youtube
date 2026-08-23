"""
FINAL PROJECT — models.py
=============================================================
Every concept from Parts 1-5 appears here: BaseModel, Field
constraints, field_validator, model_validator, computed_field, nested
models, and Literal — applied to the same Customer thread this whole
course has followed, now handling an incoming support message.
"""

import re
from typing import Literal
from pydantic import BaseModel, Field, field_validator, model_validator, computed_field, ConfigDict


class IncomingTicket(BaseModel):
    """
    The raw, messy ticket text a customer submitted. Constraints here
    are a cost-control measure as much as a data-quality one: an empty
    or absurdly long message never reaches the LLM call at all.
    """

    message: str = Field(min_length=5, max_length=2000)
    customer_name: str | None = Field(default=None, max_length=100)

    @field_validator("message", mode="before")
    @classmethod
    def redact_emails(cls, value):
        if isinstance(value, str):
            return re.sub(r"[\w.-]+@[\w.-]+\.\w+", "[redacted-email]", value)
        return value


class CustomerInfo(BaseModel):
    name: str | None = None
    order_id: int | None = Field(default=None, description="Order number, if mentioned")


class TriagedTicket(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category: Literal["billing", "shipping", "technical", "general_question"]
    priority: Literal["low", "medium", "high"]
    sentiment: Literal["positive", "negative", "neutral"]
    summary: str = Field(max_length=200)
    customer: CustomerInfo = Field(default_factory=CustomerInfo)

    @computed_field
    @property
    def sla_hours(self) -> int:
        sla_map = {"high": 4, "medium": 24, "low": 72}
        return sla_map[self.priority]

    @model_validator(mode="after")
    def high_priority_needs_real_category(self):
        if self.priority == "high" and self.category == "general_question":
            raise ValueError(
                "priority='high' cannot pair with category='general_question' "
                "— a truly urgent issue should classify as billing/shipping/technical"
            )
        return self


class TriageResponse(BaseModel):
    category: str
    priority: str
    sentiment: str
    summary: str
    sla_hours: int
    customer: CustomerInfo

    @classmethod
    def from_triaged_ticket(cls, ticket: TriagedTicket) -> "TriageResponse":
        return cls(
            category=ticket.category,
            priority=ticket.priority,
            sentiment=ticket.sentiment,
            summary=ticket.summary,
            sla_hours=ticket.sla_hours,
            customer=ticket.customer,
        )
