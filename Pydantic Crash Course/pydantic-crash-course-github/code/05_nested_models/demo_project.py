"""
DEMO — Full Customer Record, Nested
=============================================================
A realistic, deeply-nested Customer record: nested Address, and a list
of nested PastOrder entries, parsed straight from a raw dict.
"""

from pydantic import BaseModel, EmailStr, Field, ValidationError


class Address(BaseModel):
    city: str
    state: str
    pin_code: str = Field(pattern=r"^\d{6}$")   # exactly 6 digits


class PastOrder(BaseModel):
    order_id: str
    item: str
    amount: float = Field(ge=0)


class Customer(BaseModel):
    name: str
    email: EmailStr
    address: Address


class CustomerRecord(BaseModel):
    customer: Customer
    past_orders: list[PastOrder]
    newsletter_url: str | None = None


incoming_record = {
    "customer": {
        "name": "Aditi Sharma",
        "email": "aditi@example.com",
        "address": {"city": "Bengaluru", "state": "Karnataka", "pin_code": "560001"},
    },
    "past_orders": [
        {"order_id": "ORD-001", "item": "Wireless Mouse", "amount": 799.00},
        {"order_id": "ORD-002", "item": "USB-C Hub", "amount": 1499.00},
    ],
    "newsletter_url": "https://example.com/newsletter/aditi",
}

record = CustomerRecord.model_validate(incoming_record)

print(f"Customer: {record.customer.name}")
print(f"Location: {record.customer.address.city}, {record.customer.address.state}")
print(f"Total spent: ₹{sum(o.amount for o in record.past_orders)}")
for order in record.past_orders:
    print(f"   - {order.item} (₹{order.amount})")

print("\n--- Now with a broken PIN code (only 3 digits) ---")
broken_record = dict(incoming_record)
broken_record["customer"] = dict(incoming_record["customer"])
broken_record["customer"]["address"] = {"city": "Delhi", "state": "Delhi", "pin_code": "110"}

try:
    CustomerRecord.model_validate(broken_record)
except ValidationError as e:
    print("Rejected, with a precise nested error path:")
    print(e)
