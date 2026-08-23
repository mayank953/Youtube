# 02 — Your First Model

Three ways exist to define "the shape of a customer" in Python: a plain class, a `@dataclass`, and a Pydantic `BaseModel`. They look almost identical. They behave very differently.

```python
from dataclasses import dataclass
from pydantic import BaseModel

@dataclass
class CustomerDataclass:
    name: str
    email: str
    age: int

class Customer(BaseModel):
    name: str
    email: str
    age: int
```

A `@dataclass` generates a real `__init__` from the type hints, so it accepts arguments — but validates nothing. `CustomerDataclass(name="Alice", email="alice@example.com", age="not a number")` is accepted silently.

A `BaseModel` genuinely inspects the data: it validates types, coerces safely-compatible values, and raises a clear `ValidationError` the moment something doesn't fit.

> **Analogy — the customs declaration form.** An airport customs form isn't a suggestion — an officer reads it, checks your passport is real, rejects it if something's wrong. A dataclass is a form nobody reads. A BaseModel is the form with an officer standing behind it.

A numeric *string* like `"30"` is safely coerced to the int `30` — Pydantic's default "lax mode" converts compatible types but refuses anything ambiguous.

## Creating instances and required vs. optional

```python
customer = Customer(**{"name": "Aditi", "email": "aditi@example.com", "age": 28})
# or, equivalently:
customer = Customer.model_validate({"name": "Aditi", "email": "aditi@example.com", "age": 28})
```

Fields with no default are **required** — a missing one raises a `ValidationError` naming every problem at once. Fields with a default (`newsletter_opt_in: bool = False`) are **optional**.

## Getting data back out

```python
customer.model_dump()        # -> plain Python dict
customer.model_dump_json()   # -> JSON string
```

> **Analogy — the customs entry stamp.** Once customs approves your form, they issue a clean, standardized stamp every other department can read instantly. `model_dump()` is that stamp.

**Code for this part:** [`code/02_your_first_model/`](../code/02_your_first_model/)
