"""
7.2 — RESPONSE MODELS AND AUTO-GENERATED DOCS
=============================================================
Run: uvicorn "7.2_response_models_and_docs:app" --reload
Then open: http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field, computed_field

app = FastAPI(title="Part 7.2 — Response Models")


class Customer(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    total_orders: int = Field(ge=0)


# A SEPARATE model for what we send back — deliberately not the same
# shape as the request model.
class CustomerReceipt(BaseModel):
    name: str
    total_orders: int

    @computed_field
    @property
    def loyalty_tier(self) -> str:
        return "gold" if self.total_orders >= 20 else "standard"


@app.post("/signup", response_model=CustomerReceipt)
def signup_customer(customer: Customer) -> CustomerReceipt:
    return CustomerReceipt(name=customer.name, total_orders=customer.total_orders)


if __name__ == "__main__":
    import json
    print("This is the JSON Schema FastAPI generates from our Customer model")
    print("(this is what powers the /docs page's request schema):\n")
    print(json.dumps(Customer.model_json_schema(), indent=2))
