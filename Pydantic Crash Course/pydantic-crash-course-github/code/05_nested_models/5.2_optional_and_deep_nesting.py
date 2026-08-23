"""
5.2 — OPTIONAL NESTED MODELS AND DEEP NESTING
=============================================================
An entire nested model can be optional, and nesting can go several
levels deep with no extra ceremony.
"""

from pydantic import BaseModel


# An entire nested model that's optional
class Discount(BaseModel):
    code: str
    percent_off: float


class Order(BaseModel):
    order_id: str
    total: float
    discount: Discount | None = None   # the WHOLE nested object may be absent


order_without_discount = Order(order_id="ORD-001", total=1499.00)
print("No discount applied:", order_without_discount.discount)   # None

order_with_discount = Order(
    order_id="ORD-002",
    total=1499.00,
    discount={"code": "FESTIVE20", "percent_off": 20.0},   # dict auto-converts to Discount
)
print("Discount applied:", order_with_discount.discount.code, order_with_discount.discount.percent_off)


# Deep nesting — as many levels as you actually need
class Address(BaseModel):
    city: str
    state: str


class Customer(BaseModel):
    name: str
    billing_address: Address
    shipping_address: Address | None = None   # optional nested model, again


class OrderItem(BaseModel):
    product_name: str
    quantity: int
    unit_price: float


class FullOrder(BaseModel):
    order_id: str
    customer: Customer               # level 1 nesting
    items: list[OrderItem]           # level 1 nesting, as a list


deep_data = {
    "order_id": "ORD-123",
    "customer": {
        "name": "Aditi Sharma",
        "billing_address": {"city": "Bengaluru", "state": "Karnataka"},
        # shipping_address omitted — falls back to None
    },
    "items": [
        {"product_name": "Wireless Mouse", "quantity": 2, "unit_price": 799.00},
        {"product_name": "USB-C Hub", "quantity": 1, "unit_price": 1499.00},
    ],
}

full_order = FullOrder.model_validate(deep_data)
print("\nDeep access chain:", full_order.customer.billing_address.city)
print("Shipping address (never provided):", full_order.customer.shipping_address)

order_total = sum(item.quantity * item.unit_price for item in full_order.items)
print(f"Calculated order total: {order_total}")
