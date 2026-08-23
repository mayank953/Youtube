"""
1.1 — THE DYNAMIC TYPING PROBLEM
=============================================================
Python will not stop you from shipping bad data. This file proves it,
using the exact scenario every real app runs into: a new customer
signing up through a web form.
"""

# A single variable can hold ANY type, at ANY time — Python never complains.
age = 25
print("age is:", age, "| type:", type(age))

age = "twenty-five"
print("age is now:", age, "| type:", type(age))


# A typical "register a new customer" function. It looks correct.
def register_customer(name, email, age):
    joined_year = 2026
    birth_year = joined_year - age   # assumes age is a number — nothing enforces that
    print(f"Registered {name} ({email}), born approx. {birth_year}")


# Works fine with clean data:
good_signup = {"name": "Aditi Sharma", "email": "aditi@example.com", "age": 28}
register_customer(**good_signup)

# Real-world data rarely stays clean. HTML forms send everything as text,
# spreadsheets export numbers as strings, and APIs occasionally send
# "unknown" instead of a number:
bad_signup = {"name": "Rohan Mehta", "email": "rohan@example.com", "age": "unknown"}

try:
    register_customer(**bad_signup)
except TypeError as e:
    print(f"\nCrashed: {e}")
    print("Notice WHERE it crashed — deep inside the calculation, not at")
    print("the moment the bad data actually entered the program.")

# The bug was never in the calculation. Nothing checked the incoming
# data at the door. That's the problem Pydantic solves — but first, the
# foundation it's built on: type hints. See 1.2_type_hints_basics.py
