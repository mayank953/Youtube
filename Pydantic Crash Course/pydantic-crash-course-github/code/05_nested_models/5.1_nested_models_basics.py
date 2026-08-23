"""
5.1 — NESTED MODELS: real data is never flat
=============================================================
A customer has an address. A customer has a list of past orders. Using
one model as a field type inside another just works, and validation
cascades automatically.
"""

from pydantic import BaseModel, EmailStr, ValidationError


# One model used as a field type inside another
class Address(BaseModel):
    city: str
    state: str
    pin_code: str


class Customer(BaseModel):
    name: str
    email: EmailStr
    address: Address    # a whole model, used as a field type


customer_a = Customer(
    name="Aditi Sharma",
    email="aditi@example.com",
    address=Address(city="Bengaluru", state="Karnataka", pin_code="560001"),
)
print("Created with a real Address instance:", customer_a.address.city, "\n")


# The real power: parsing straight from a nested dictionary — exactly
# what happens with real JSON from an API, form, or (later) an LLM.
incoming_data = {
    "name": "Rohan Mehta",
    "email": "rohan@example.com",
    "address": {"city": "Pune", "state": "Maharashtra", "pin_code": "411001"},
}
customer_b = Customer.model_validate(incoming_data)
print("Parsed from a raw nested dict:", customer_b.address.city, customer_b.address.state)
print("Full chain access ->", customer_b.address.pin_code, "\n")


# Coercion is NOT symmetric. Pydantic happily turns the string "25"
# into the int 25, but will NOT turn the int 12345 into the string
# "12345" for a str field — going the other direction is too lossy to
# do silently.
almost_right_data = {
    "name": "Karan Verma",
    "email": "karan@example.com",
    "address": {"city": "Delhi", "state": "Delhi", "pin_code": 12345},   # int, NOT a str
}
try:
    Customer.model_validate(almost_right_data)
except ValidationError as e:
    print("An int pin_code is rejected for a str field:")
    print(e, "\n")

worse_data = {
    "name": "Meera Iyer",
    "email": "meera@example.com",
    "address": {"city": "Chennai"},   # missing state and pin_code
}
try:
    Customer.model_validate(worse_data)
except ValidationError as e:
    print("The error path shows exactly which NESTED field failed:")
    print(e)


# Lists of nested models
class PastOrder(BaseModel):
    order_id: str
    item: str
    amount: float


class CustomerWithHistory(BaseModel):
    customer: Customer
    past_orders: list[PastOrder]   # a LIST of nested models


history_data = {
    "customer": {
        "name": "Aditi Sharma",
        "email": "aditi@example.com",
        "address": {"city": "Bengaluru", "state": "Karnataka", "pin_code": "560001"},
    },
    "past_orders": [
        {"order_id": "ORD-001", "item": "Wireless Mouse", "amount": 799.00},
        {"order_id": "ORD-002", "item": "USB-C Hub", "amount": 1499.00},
    ],
}

record = CustomerWithHistory.model_validate(history_data)
print(f"\n{record.customer.name} has {len(record.past_orders)} past orders:")
for order in record.past_orders:
    print(f"   - {order.item} (₹{order.amount})")
