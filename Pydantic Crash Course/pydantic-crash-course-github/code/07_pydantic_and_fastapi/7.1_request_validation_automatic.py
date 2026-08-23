"""
7.1 — AUTOMATIC REQUEST VALIDATION
=============================================================
Install first: pip install fastapi uvicorn
Run: uvicorn "7.1_request_validation_automatic:app" --reload
Then open: http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title="Part 7.1 — Automatic Request Validation")


class Address(BaseModel):
    city: str
    state: str


class Customer(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=120)
    address: Address


@app.post("/signup")
def signup_customer(customer: Customer):
    """
    `customer: Customer` is the entire validation logic. By the time
    this function body runs, FastAPI has already parsed the request
    body, validated every field, coerced compatible types, and
    rejected the request with a detailed error if anything failed.
    """
    return {
        "message": f"Welcome, {customer.name}!",
        "location": f"{customer.address.city}, {customer.address.state}",
    }


@app.get("/")
def root():
    return {"info": "Open /docs in your browser to try this live and interactively."}
