# 05 — Nested Models

A customer has an address. A customer has a list of past orders. Using one model as a field type inside another just works, and validation cascades automatically.

```python
class Address(BaseModel):
    city: str
    state: str
    pin_code: str

class Customer(BaseModel):
    name: str
    email: EmailStr
    address: Address        # a whole model, used as a field type
```

Parsing straight from a nested dictionary — exactly what happens with real JSON from an API, a form, or an LLM response:

```python
incoming = {
    "name": "Rohan Mehta",
    "email": "rohan@example.com",
    "address": {"city": "Pune", "state": "Maharashtra", "pin_code": "411001"},
}
customer = Customer.model_validate(incoming)
customer.address.city   # "Pune" — dot-chain access, fully typed
```

> **Analogy — the org chart.** An org chart isn't one flat list of names — it's a person, who belongs to a team, which belongs to a department. A `Company` model containing `list[Department]`, each containing `list[Employee]`, validates every layer automatically when the top-level model validates.

When something fails deep inside a nested structure, the error pinpoints the exact path (`address.state`, `address.pin_code`) no matter how many layers deep.

**Coercion isn't symmetric.** Pydantic turns the string `"25"` into the int `25` safely, but will *not* turn the int `12345` into the string `"12345"` for a `str` field — that direction is too lossy to do silently.

## Optional nested models

```python
class Order(BaseModel):
    order_id: str
    discount: Discount | None = None   # the WHOLE nested object may be absent
```

Nesting has no practical depth limit — model inside model inside list of models works exactly as expected.

**Code for this part:** [`code/05_nested_models/`](../code/05_nested_models/)
