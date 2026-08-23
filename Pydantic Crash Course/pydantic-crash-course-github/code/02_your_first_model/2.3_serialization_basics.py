"""
2.3 — SERIALIZATION BASICS: model_dump() and model_dump_json()
=============================================================
Getting data back OUT of a model in a shape the rest of your system
can use: model -> dict, or model -> JSON string.
"""

from pydantic import BaseModel


class Customer(BaseModel):
    name: str
    email: str
    age: int
    newsletter_opt_in: bool = False


customer = Customer(name="Aditi Sharma", email="aditi@example.com", age=28, newsletter_opt_in=True)

# model_dump() -> plain Python dictionary
# Use for: inserting into a database, passing to another function
customer_dict = customer.model_dump()
print("model_dump() ->", customer_dict)
print("type:", type(customer_dict), "\n")

# model_dump_json() -> JSON string
# Use for: HTTP API responses, writing to a .json file
customer_json = customer.model_dump_json()
print("model_dump_json() ->", customer_json)
print("type:", type(customer_json), "\n")

# indent= for human-readable output
print("Pretty-printed:")
print(customer.model_dump_json(indent=2))
