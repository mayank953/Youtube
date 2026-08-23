"""
DEMO — Break the Customer Signup Function
=============================================================
A batch of realistic signups, including messy data. No Pydantic yet —
this is the "before" picture. Part 2's demo is the fix, on the exact
same data.
"""


def register_customer(name: str, email: str, age: int):
    birth_year = 2026 - age
    print(f"Registered {name} <{email}> — born ~{birth_year}")


incoming_signups = [
    {"name": "Aditi Sharma", "email": "aditi@example.com", "age": 28},
    {"name": "Rohan Mehta", "email": "rohan@example.com", "age": "twenty-five"},  # bad age
    {"name": "", "email": "not-an-email", "age": -5},                              # multiple issues
    {"name": "Meera Iyer", "email": "meera@example.com", "age": 34},
]

print("Processing signups with ZERO validation:\n")

for signup in incoming_signups:
    try:
        register_customer(**signup)
    except TypeError as e:
        print(f"Crashed on {signup}: {e}")

print(
    "\nSignup #3 (empty name, garbage email, negative age) did NOT crash —"
    "\nit silently 'registered' garbage. That's arguably worse than a"
    "\ncrash: bad data is now sitting in the system undetected."
)
