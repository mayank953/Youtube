"""
2.1 — YOUR FIRST MODEL: BaseModel vs dataclass vs plain class
=============================================================
Three ways to define "the shape of a customer" in Python. They look
almost identical. They behave very differently.

Install first: pip install pydantic
"""

from dataclasses import dataclass
from pydantic import BaseModel


# Option 1 — a plain class with type-hinted attributes only.
class CustomerPlainClass:
    name: str
    email: str
    age: int


try:
    # A plain class with only annotations has no real __init__, so it
    # doesn't even accept constructor arguments.
    customer = CustomerPlainClass(name="Aditi", email="aditi@example.com", age="not a number")
except TypeError as e:
    print("Plain class fails immediately, but for a confusing reason:")
    print(f"   {e}\n")


# Option 2 — a dataclass. Clean syntax, ZERO validation.
@dataclass
class CustomerDataclass:
    name: str
    email: str
    age: int


customer_dc = CustomerDataclass(name="Aditi", email="aditi@example.com", age="not a number")
print("dataclass accepts the bad data with no complaint:")
print(f"   age = {customer_dc.age!r} (type: {type(customer_dc.age).__name__})\n")


# Option 3 — a Pydantic BaseModel. Looks the same. Actually validates.
class Customer(BaseModel):
    name: str
    email: str
    age: int


print("BaseModel actually inspects the data:")
try:
    Customer(name="Aditi", email="aditi@example.com", age="not a number")
except Exception as e:
    print(f"   Rejected immediately:\n   {e}\n")

# A numeric STRING, on the other hand, is safely coerced:
customer = Customer(name="Aditi", email="aditi@example.com", age="30")
print(f"   age='30' (string) became age={customer.age!r} (type: {type(customer.age).__name__})")
print("   Pydantic safely converts compatible types, but refuses anything")
print("   that can't be converted without ambiguity.")
