"""
6.1 — THE PROBLEM WITH os.getenv()
=============================================================
Every value from os.getenv() is a string — always, with no exceptions.
"""

import os

os.environ["API_KEY"] = "sk-demo-key-12345"
os.environ["MAX_CONNECTIONS"] = "200"
os.environ["DEBUG"] = "true"

api_key = os.getenv("API_KEY")
max_connections = os.getenv("MAX_CONNECTIONS")
debug_mode = os.getenv("DEBUG")

print("api_key:", repr(api_key), "| type:", type(api_key).__name__)
print("max_connections:", repr(max_connections), "| type:", type(max_connections).__name__)
print("debug_mode:", repr(debug_mode), "| type:", type(debug_mode).__name__)

print(
    "\nmax_connections is the STRING '200', not the number 200. "
    "debug_mode is the STRING 'true', not the boolean True. Writing "
    "`if debug_mode:` right now evaluates to True for ANY non-empty "
    "string — including the string 'false'."
)

# The manual boilerplate every project ends up writing by hand:
def get_max_connections_the_hard_way() -> int:
    raw = os.getenv("MAX_CONNECTIONS")
    if raw is None:
        return 100
    try:
        return int(raw)
    except ValueError:
        raise ValueError(f"MAX_CONNECTIONS must be a number, got: {raw!r}")


def get_debug_the_hard_way() -> bool:
    raw = os.getenv("DEBUG", "false").lower()
    return raw in ("true", "1", "yes", "on")


print("\nManually converted:")
print("  max_connections (int):", get_max_connections_the_hard_way())
print("  debug (bool):", get_debug_the_hard_way())
print("\nImagine writing this for every config value in a real app.")
