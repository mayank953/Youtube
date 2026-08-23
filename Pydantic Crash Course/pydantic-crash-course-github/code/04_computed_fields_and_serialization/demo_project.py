"""
DEMO — Public vs Internal Customer Feed
=============================================================
Serializing the same Customer model two different ways for two
different audiences.
"""

from pydantic import BaseModel, EmailStr, computed_field


class Customer(BaseModel):
    name: str
    total_orders: int
    email: EmailStr

    @computed_field
    @property
    def loyalty_tier(self) -> str:
        if self.total_orders < 5:
            return "bronze"
        elif self.total_orders < 20:
            return "silver"
        return "gold"


customers = [
    Customer(name="Aditi Sharma", total_orders=22, email="aditi@example.com"),
    Customer(name="Rohan Mehta", total_orders=2, email="rohan@example.com"),
    Customer(name="Meera Iyer", total_orders=15, email="meera@example.com"),
]

print("=== INTERNAL DUMP (our own database — everything included) ===")
for c in customers:
    print(c.model_dump())

print("\n=== PUBLIC 'TOP CUSTOMERS' LEADERBOARD (email redacted) ===")
for c in customers:
    print(c.model_dump(exclude={"email"}))

print("\nloyalty_tier appears in BOTH dumps automatically — it's a")
print("computed_field, so it can never drift out of sync with total_orders.")
