"""
2.2 — CREATING INSTANCES, COERCION, REQUIRED vs OPTIONAL
=============================================================
"""

from pydantic import BaseModel, ValidationError


class Customer(BaseModel):
    name: str
    email: str
    age: int
    newsletter_opt_in: bool = False   # has a default -> OPTIONAL


# Two equivalent ways to create an instance from a dictionary.
incoming_data = {"name": "Aditi Sharma", "email": "aditi@example.com", "age": 28}

customer_a = Customer(**incoming_data)
customer_b = Customer.model_validate(incoming_data)
print("customer_a:", customer_a)
print("customer_b:", customer_b)

# Fields with no default are REQUIRED. Fields with a default are optional.
customer_no_newsletter = Customer(name="Rohan", email="rohan@example.com", age=25)
print("\nMissing newsletter_opt_in falls back to its default:", customer_no_newsletter.newsletter_opt_in)

try:
    Customer(name="Incomplete Customer")   # missing email AND age
except ValidationError as e:
    print("\nMissing REQUIRED fields raises ValidationError, naming every problem at once:")
    print(e)

# Automatic type coercion, and where Pydantic draws the line.
coerced = Customer(name="Test", email="test@example.com", age="28")   # string age
print(f"\nage='28' (string) became age={coerced.age!r} (type: {type(coerced.age).__name__})")

try:
    Customer(name="Test", email="test@example.com", age="twenty-eight")
except ValidationError as e:
    print("\n'twenty-eight' can't be safely converted to an int, so it's rejected:")
    print(e)
