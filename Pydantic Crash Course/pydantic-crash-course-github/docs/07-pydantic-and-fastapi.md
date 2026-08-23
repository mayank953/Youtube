# 07 — Pydantic in Production: FastAPI

A FastAPI endpoint can take a Pydantic model directly as a parameter type:

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()

class Customer(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr

@app.post("/signup")
def signup_customer(customer: Customer):
    return {"message": f"Welcome, {customer.name}!"}
```

FastAPI parses the incoming JSON body, validates every field, coerces compatible types, and rejects malformed requests with a detailed error — all before the function body runs. No manual `if` checks.

> **Analogy — one scanner at the terminal entrance.** Airport security used to mean every gate built its own metal detector. FastAPI installs one scanner at the entrance everyone walks through — and that scanner *is* your Pydantic model.

## Response models

```python
@app.post("/signup", response_model=CustomerReceipt)
def signup_customer(customer: Customer) -> CustomerReceipt:
    return CustomerReceipt(name=customer.name, total_orders=customer.total_orders)
```

`response_model=` isn't just documentation — FastAPI actively filters the returned object to that exact shape, as a safety net against leaking extra fields. `model_json_schema()` is the mechanism underneath the auto-generated `/docs` page: every `Field()` constraint is translated automatically into documented API constraints.

**Code for this part:** [`code/07_pydantic_and_fastapi/`](../code/07_pydantic_and_fastapi/)
