"""
3.2 — BUILT-IN SPECIAL TYPES
=============================================================
Pydantic ships pre-built types for extremely common validation needs.

Install first: pip install pydantic[email]
"""

from pydantic import BaseModel, EmailStr, HttpUrl, SecretStr, ValidationError


# EmailStr — real email format validation
class Customer(BaseModel):
    name: str
    email: EmailStr


try:
    Customer(name="Rohan", email="not-an-email-at-all")
except ValidationError as e:
    print("EmailStr rejects malformed emails:")
    print(e, "\n")

print("Valid:", Customer(name="Rohan", email="rohan@example.com"), "\n")


# HttpUrl — URL format validation
class CustomerProfile(BaseModel):
    website: HttpUrl


try:
    CustomerProfile(website="not a url")
except ValidationError as e:
    print("HttpUrl rejects non-URL strings:")
    print(e, "\n")

print("Valid profile:", CustomerProfile(website="https://rohan.dev"), "\n")


# SecretStr — values that should never leak into logs or prints
class CustomerAccount(BaseModel):
    email: str
    password: SecretStr


account = CustomerAccount(email="rohan@example.com", password="super-secret-123")
print("Printing the account directly:", account)
print("Real value, accessed on purpose:", account.password.get_secret_value())
