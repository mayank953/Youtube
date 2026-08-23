# 01 — Why Pydantic Exists

Python is dynamically typed. A single variable can hold an integer, then a string, then a list, with zero complaints from the language itself. This is genuinely useful for quick scripts — and genuinely dangerous the moment you're working with data that came from *outside* your own code: an API response, a form submission, an LLM.

A typical `register_customer()` function that calculates a birth year from an `age` field looks completely reasonable. It works — right up until `age` arrives as the string `"unknown"` instead of a number, and the program crashes deep inside a calculation, often several function calls away from where the bad data actually entered.

> **Analogy — the courier with no intake desk.** A courier company with no intake desk will happily load any package onto the truck — no address, no weight limit, wrong label, doesn't matter. The problem isn't discovered until the truck is three stops into its route. Pydantic is the intake desk: it inspects every package at the door and refuses the bad ones on the spot.

## Type hints — documentation, not enforcement

Type hints tell Python, and every developer reading the code, what type a variable is *supposed* to hold:

```python
name: str = "Aditi Sharma"
age: int = 28
account_balance: float = 499.99
is_active: bool = True
```

Python does not enforce these at runtime. This line runs without complaint: `age: int = "not a number at all"`. Type hints are read by humans, IDEs, and — critically — Pydantic. Plain Python ignores them completely.

> **Analogy — the recipe card on the wall.** A recipe card pinned to a shared kitchen wall says "2 cups flour." It's useful — everyone can read it. But nothing stops someone from dumping in 2 cups of salt instead. Type hints are the recipe card. Pydantic is what turns it into an actual lock.

Container types follow the same pattern — `list[str]`, `dict[str, int]` — using Python 3.9+'s lowercase built-ins directly.

## Optional and Literal

Two more patterns that matter constantly once Pydantic enters the picture:

```python
from typing import Optional, Literal

phone: str | None = None                                    # might not exist yet
customer_tier: Literal["bronze", "silver", "gold"] = "bronze"  # exact options only
```

`Literal` becomes especially useful later: when an AI model classifies a support message's priority, `Literal["low", "medium", "high"]` forces the response into exactly one of those three values — no "kinda urgent i guess."

**Code for this part:** [`code/01_why_pydantic_and_type_hints/`](../code/01_why_pydantic_and_type_hints/)
