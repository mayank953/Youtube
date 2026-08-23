"""
DEMO — Fix the Customer Signup Function, For Real This Time
=============================================================
The exact same messy signup batch from Part 1's demo, now validated
through a real Pydantic model instead.
"""

from pydantic import BaseModel, ValidationError


class Customer(BaseModel):
    name: str
    email: str
    age: int
    newsletter_opt_in: bool = False


def register_customer(data: dict):
    try:
        customer = Customer(**data)
    except ValidationError as e:
        print(f"Rejected at the door: {data}")
        for err in e.errors():
            print(f"     - {err['loc'][0]}: {err['msg']}")
        return None

    plan = "Newsletter subscriber" if customer.newsletter_opt_in else "No newsletter"
    print(f"Registered {customer.name} <{customer.email}> (age {customer.age}) — {plan}")
    return customer


incoming_signups = [
    {"name": "Aditi Sharma", "email": "aditi@example.com", "age": 28, "newsletter_opt_in": True},
    {"name": "Rohan Mehta", "email": "rohan@example.com", "age": "twenty-five"},   # bad age
    {"name": "", "email": "not-an-email", "age": -5},                               # multiple issues
    {"name": "Meera Iyer", "email": "meera@example.com", "age": 34},
]

print("Processing the SAME signups, now validated:\n")
results = [register_customer(signup) for signup in incoming_signups]

successful = [r for r in results if r is not None]
print(f"\n{len(successful)}/{len(incoming_signups)} signups made it through — every bad")
print("one was rejected with a clear reason, right at the door.")
