"""
1.2 — TYPE HINTS: THE FOUNDATION PYDANTIC IS BUILT ON
=============================================================
Type hints are plain Python syntax — not Pydantic yet. Pydantic reads
these hints and enforces them; Python itself does not.
"""

# The four basic types
name: str = "Aditi Sharma"
age: int = 28
account_balance: float = 499.99
is_active: bool = True

# The critical gotcha — Python does not enforce type hints:
age: int = "not a number at all"
print("Did Python stop us? age =", age, "| type:", type(age))

# Container types — since Python 3.9+, use lowercase built-ins directly
past_purchases: list[str] = ["Wireless Mouse", "USB-C Hub"]
purchase_counts: dict[str, int] = {"Wireless Mouse": 2, "USB-C Hub": 1}

# Function signatures — the most valuable place to use hints
def format_balance(amount: float, currency: str = "USD") -> str:
    return f"{currency} {amount:.2f}"

print(format_balance(499.99))
print(format_balance(499.99, currency="INR"))

# Type hints give three real benefits even without Pydantic:
#   1. Documentation — code becomes self-explanatory
#   2. IDE support — autocomplete, error squiggles, refactoring
#   3. A foundation for validation tools (Pydantic) to build on
#
# See 1.3_optional_and_literal_types.py for two more patterns before
# Pydantic itself is introduced.
