"""
1.3 — OPTIONAL AND LITERAL TYPES
=============================================================
Two more type-hint patterns that appear constantly once Pydantic enters
the picture, and become especially important later when constraining
what an AI model is allowed to return.
"""

from typing import Optional, Literal

# Optional — a value that might legitimately not exist yet.
# Both lines mean exactly the same thing; the pipe syntax is preferred
# in modern Python (3.10+).
phone_old_style: Optional[str] = None
phone: str | None = None
phone = "+91-98765-43210"   # also valid

# Literal — a strict multiple-choice constraint, not a free-form string.
customer_tier: Literal["bronze", "silver", "gold"] = "bronze"
ticket_priority: Literal["low", "medium", "high"] = "medium"

print("phone:", phone)
print("customer_tier:", customer_tier, "| ticket_priority:", ticket_priority)

# Still just documentation at this stage — Python allows this:
customer_tier = "this is not one of the allowed options"
print("Python let us set an invalid tier:", customer_tier)

# Why this matters later: when an AI model classifies a support
# message's priority, you don't want it returning "kinda urgent i
# guess." With Literal["low", "medium", "high"] enforced by Pydantic,
# the response is forced to be one of exactly those three values.
