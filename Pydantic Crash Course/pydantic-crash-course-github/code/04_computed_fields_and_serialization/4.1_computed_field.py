"""
4.1 — @computed_field: VALUES THAT ARE ALWAYS FRESH, NEVER STORED
=============================================================
Some values shouldn't be stored — they should be derived, live, every
time, from other fields.
"""

from pydantic import BaseModel, computed_field


class Customer(BaseModel):
    name: str
    total_orders: int

    # @computed_field + @property, stacked in that order. Becomes a
    # read-only attribute — accessible like a normal field, but never
    # settable through the constructor.
    @computed_field
    @property
    def loyalty_tier(self) -> str:
        if self.total_orders < 5:
            return "bronze"
        elif self.total_orders < 20:
            return "silver"
        return "gold"


customer = Customer(name="Aditi Sharma", total_orders=12)
print("Accessed like a normal attribute:", customer.loyalty_tier)

print("\nmodel_dump() includes it automatically:")
print(customer.model_dump())

# Always fresh — never stored, so it can never go stale.
print(f"\nStarting tier: {customer.loyalty_tier} (total_orders={customer.total_orders})")
customer.total_orders = 25   # Pydantic models are mutable by default
print(f"After updating total_orders to 25: {customer.loyalty_tier}")


# A second example — a numeric computation
class OrderLineItem(BaseModel):
    product_name: str
    quantity: int
    unit_price: float

    @computed_field
    @property
    def line_total(self) -> float:
        return round(self.quantity * self.unit_price, 2)


item = OrderLineItem(product_name="Wireless Mouse", quantity=3, unit_price=799.00)
print(f"\n{item.product_name}: {item.quantity} x {item.unit_price} = {item.line_total}")
