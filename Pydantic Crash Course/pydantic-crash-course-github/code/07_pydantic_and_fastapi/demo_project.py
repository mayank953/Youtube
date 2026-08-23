"""
DEMO — Customer Signup API, Fully Wired
=============================================================
Install first: pip install fastapi uvicorn
Run: uvicorn demo_project:app --reload
Then open: http://127.0.0.1:8000/docs and try POST /signup live.
"""

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field, computed_field

app = FastAPI(title="Customer Signup API — Part 7 Demo")


class Address(BaseModel):
    city: str
    state: str
    pin_code: str = Field(pattern=r"^\d{6}$")


class PastOrder(BaseModel):
    item: str
    amount: float = Field(ge=0)


class CustomerSignupRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    address: Address
    past_orders: list[PastOrder]


class CustomerReceipt(BaseModel):
    name: str
    city: str
    total_spent: float

    @computed_field
    @property
    def loyalty_tier(self) -> str:
        if self.total_spent < 1000:
            return "bronze"
        elif self.total_spent < 5000:
            return "silver"
        return "gold"


@app.post("/signup", response_model=CustomerReceipt)
def signup_customer(payload: CustomerSignupRequest) -> CustomerReceipt:
    total_spent = sum(order.amount for order in payload.past_orders)
    return CustomerReceipt(
        name=payload.name,
        city=payload.address.city,
        total_spent=total_spent,
    )


@app.get("/")
def root():
    return {"info": "POST a customer signup to /signup — try it via /docs"}
