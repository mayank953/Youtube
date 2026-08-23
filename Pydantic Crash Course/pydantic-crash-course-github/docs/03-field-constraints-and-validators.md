# 03 — Field Constraints & Custom Validators

`age: int` accepts `-50` just as happily as `28`. Real rules need `Field()`:

```python
from pydantic import BaseModel, Field

class Customer(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=0, le=120)   # ge = >=, le = <=
```

> **Analogy — the ATM PIN pad.** A bank ATM's PIN pad enforces exactly 4–6 digits, numeric only. `str` alone is an ATM that accepts anything you type. `Field()` constraints are the actual PIN pad rules.

The `Annotated` style is the more modern, composable equivalent: `name: Annotated[str, Field(min_length=2, max_length=100)]`. Both behave identically; prefer `Annotated` in production code.

## Built-in special types

`EmailStr` (needs `pip install pydantic[email]`), `HttpUrl`/`AnyUrl`, and `SecretStr` (masks sensitive values in logs/prints by default) cover extremely common needs out of the box.

## field_validator — one field, custom logic

```python
from pydantic import field_validator

class Customer(BaseModel):
    name: str

    @field_validator("name", mode="after")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("name cannot be empty")
        return cleaned.title()
```

`mode='after'` (default) runs once the value is already the correct type. `mode='before'` runs on the raw input — useful for cleaning up messy text before Pydantic tries to interpret it.

> **Analogy — airport immigration, checkpoint one.** Each passenger's own passport gets checked individually. That's `field_validator` — one field, its own rules, no visibility into any other field.

## model_validator — rules across fields

```python
from pydantic import model_validator

class CustomerSignup(BaseModel):
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def passwords_must_match(self):
        if self.password != self.confirm_password:
            raise ValueError("passwords do not match")
        return self
```

> **Analogy — airport immigration, checkpoint two.** The family gets checked as a group — "3 children, only 1 accompanying adult." `model_validator` always runs *after* every `field_validator` has already cleared its own passenger.

**Code for this part:** [`code/03_field_constraints_and_validators/`](../code/03_field_constraints_and_validators/)
