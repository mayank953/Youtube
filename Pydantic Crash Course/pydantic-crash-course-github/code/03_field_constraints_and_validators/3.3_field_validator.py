"""
3.3 — CUSTOM VALIDATORS: @field_validator
=============================================================
Built-in constraints cover most cases. For real business logic, write
a validator function with @field_validator, which operates on exactly
one field at a time.
"""

from pydantic import BaseModel, field_validator, ValidationError


class Customer(BaseModel):
    name: str
    email: str
    years_as_member: int

    # mode='after' (the default): runs AFTER Pydantic's normal type
    # validation. `value` is guaranteed to already be the correct type.
    @field_validator("name", mode="after")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        cleaned = value.strip()
        if len(cleaned) == 0:
            raise ValueError("name cannot be empty or only whitespace")
        return cleaned.title()

    @field_validator("email", mode="after")
    @classmethod
    def reject_disposable_domains(cls, value: str) -> str:
        blocked_domains = {"mailinator.com", "tempmail.com"}
        domain = value.split("@")[-1].lower()
        if domain in blocked_domains:
            raise ValueError(f"disposable email domains are not accepted ({domain})")
        return value.lower()

    # mode='before': runs BEFORE Pydantic tries to coerce the type.
    # `value` could be anything the caller passed — useful for cleaning
    # up messy raw input before Pydantic attempts to interpret it.
    @field_validator("years_as_member", mode="before")
    @classmethod
    def strip_years_suffix(cls, value):
        if isinstance(value, str):
            digits_only = "".join(ch for ch in value if ch.isdigit())
            return int(digits_only) if digits_only else value
        return value


customer = Customer(
    name="  rohan mehta  ",
    email="ROHAN@Example.COM",
    years_as_member="5 years",
)
print("Input was messy. Output is clean:")
print(customer, "\n")

try:
    Customer(name="Test", email="fake@mailinator.com", years_as_member=3)
except ValidationError as e:
    print("Blocked domain rejected:")
    print(e, "\n")

try:
    Customer(name="   ", email="test@example.com", years_as_member=3)
except ValidationError as e:
    print("Whitespace-only name rejected:")
    print(e)
