"""
4.2 — SERIALIZATION CONTROL: exclude, include, exclude_unset
=============================================================
model_dump() returns every field by default. Real applications almost
always need to hide something, or send only part of a model.
"""

from pydantic import BaseModel, SecretStr


class CustomerAccount(BaseModel):
    name: str
    email: str
    password: SecretStr
    bio: str = "No bio yet."


customer = CustomerAccount(name="Rohan Mehta", email="rohan@example.com", password="hunter2")

# exclude: remove specific fields from the output
public_profile = customer.model_dump(exclude={"password"})
print("Public-facing dump (password removed):")
print(public_profile, "\n")

# include: the inverse — ONLY these fields, nothing else
name_only = customer.model_dump(include={"name"})
print("include={'name'} ->", name_only, "\n")

# exclude_unset: only serialize fields the CALLER explicitly set — the
# single most useful flag for PATCH-style partial updates.
print("Full dump (bio used its default, wasn't explicitly set):")
print(customer.model_dump())

print("\nSame object, exclude_unset=True:")
print(customer.model_dump(exclude_unset=True))
print("-> 'bio' disappears — it was never explicitly provided, it just")
print("   fell back to its default. Useful for PATCH requests: update")
print("   only the fields the client actually sent.\n")

# exclude_none: drop fields that are currently None
class CustomerContact(BaseModel):
    name: str
    phone: str | None = None
    fax: str | None = None


contact = CustomerContact(name="Aditi Sharma", phone="+91-98765-43210")
print("With exclude_none=True:")
print(contact.model_dump(exclude_none=True))
