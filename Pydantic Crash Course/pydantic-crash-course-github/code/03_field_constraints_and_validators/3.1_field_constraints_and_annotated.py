"""
3.1 — FIELD CONSTRAINTS: Field() and the Annotated pattern
=============================================================
Types alone aren't enough — age: int accepts -50 just as happily as 28.
Field() enforces real business rules: minimum lengths, numeric ranges,
regex patterns.
"""

from typing import Annotated
from pydantic import BaseModel, Field, ValidationError


# Direct style
class CustomerV1(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=0, le=120)                # ge = >=, le = <=
    referral_code: str = Field(pattern=r"^[A-Z]{3}\d{4}$")


# Numeric constraints: gt (>), ge (>=), lt (<), le (<=)
# String constraints: min_length, max_length, pattern (a regex)

try:
    CustomerV1(name="A", age=25, referral_code="ABC1234")
except ValidationError as e:
    print("name='A' is too short (min_length=2):")
    print(e, "\n")

valid_customer = CustomerV1(name="Rohan Mehta", age=25, referral_code="ABC1234")
print("Valid customer:", valid_customer, "\n")


# Annotated style — the more modern, composable pattern. Behaves
# identically; separates "the type" from "the metadata about the type."
class CustomerV2(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=100)]
    age: Annotated[int, Field(ge=0, le=120)]
    email: Annotated[
        str,
        Field(description="Customer's contact email", examples=["rohan@example.com"]),
    ]


customer_v2 = CustomerV2(name="Rohan Mehta", age=25, email="rohan@example.com")
print("Annotated-style model:", customer_v2)
print("Both styles behave identically — prefer Annotated in production code.\n")


# Defaults combined with constraints — useful for app configuration too.
class LoyaltyConfig(BaseModel):
    points_per_purchase: int = Field(default=10, ge=1, le=1000)
    tier_threshold: int = Field(default=100, ge=0)


print("Config with defaults applied:", LoyaltyConfig())
