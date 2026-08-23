"""
DEMO — Full Customer Signup Validator
=============================================================
Combining Field() constraints, a built-in special type, a
field_validator, and a model_validator, all on one Customer model.
"""

from typing import Annotated
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator, ValidationError


class Customer(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=100)]
    age: Annotated[int, Field(ge=0, le=120)]
    email: EmailStr
    password: str
    confirm_password: str

    @field_validator("name", mode="after")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("name cannot be blank")
        return cleaned.title()

    @model_validator(mode="after")
    def passwords_must_match(self):
        if self.password != self.confirm_password:
            raise ValueError("password and confirm_password do not match")
        return self

    def age_group(self) -> str:
        if self.age < 18:
            return "Minor"
        elif self.age < 60:
            return "Adult"
        return "Senior"


incoming_signups = [
    {
        "name": "  aditi sharma  ",
        "age": 28,
        "email": "aditi@example.com",
        "password": "hunter2",
        "confirm_password": "hunter2",
    },
    {
        "name": "R",  # too short — min_length=2
        "age": 25,
        "email": "rohan@example.com",
        "password": "abc123",
        "confirm_password": "abc123",
    },
    {
        "name": "Meera Iyer",
        "age": 34,
        "email": "not-a-valid-email",   # EmailStr rejects this
        "password": "abc123",
        "confirm_password": "abc123",
    },
    {
        "name": "Karan Verma",
        "age": 40,
        "email": "karan@example.com",
        "password": "abc123",
        "confirm_password": "xyz789",   # mismatch — model_validator rejects
    },
]

print("Validating a batch of customer signups:\n")
for raw in incoming_signups:
    try:
        customer = Customer(**raw)
        print(f"Accepted: {customer.name} — {customer.age_group()} ({customer.age})")
    except ValidationError as e:
        print(f"Rejected: {raw.get('name', '???')!r}")
        for err in e.errors():
            field = ".".join(str(loc) for loc in err["loc"]) or "(whole model)"
            print(f"     - {field}: {err['msg']}")
    print()
