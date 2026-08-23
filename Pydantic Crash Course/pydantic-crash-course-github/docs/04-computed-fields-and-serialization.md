# 04 — Computed Fields & Serialization Control

Some values shouldn't be stored — they should be derived, live, every time, from other fields.

```python
from pydantic import BaseModel, computed_field

class Customer(BaseModel):
    name: str
    total_orders: int

    @computed_field
    @property
    def loyalty_tier(self) -> str:
        if self.total_orders < 5:
            return "bronze"
        elif self.total_orders < 20:
            return "silver"
        return "gold"
```

`loyalty_tier` behaves like a normal read-only attribute, appears automatically in `model_dump()`, and is never settable through the constructor.

> **Analogy — the grocery receipt total.** A receipt doesn't store "total" as a fact someone typed in — it's calculated live from item prices at checkout. `@computed_field` is the register doing that math for you, every time, instead of a value drifting out of sync with reality.

This matters especially with AI-generated data: LLMs are unreliable at consistent arithmetic. Calculate derived values yourself from fields the model *did* classify, rather than asking it to compute and return them.

## Serialization control

```python
customer.model_dump(exclude={"password"})     # remove specific fields
customer.model_dump(include={"name"})          # ONLY these fields
customer.model_dump(exclude_unset=True)        # only fields the caller actually SET
customer.model_dump(exclude_none=True)         # drop fields currently None
```

`exclude_unset=True` is the single most useful flag for PATCH-style partial updates — default values that were never explicitly provided disappear from the output instead of silently overwriting other data.

**Code for this part:** [`code/04_computed_fields_and_serialization/`](../code/04_computed_fields_and_serialization/)
