"""
3.4 — CUSTOM VALIDATORS: @model_validator (cross-field rules)
=============================================================
Some rules can't be checked one field at a time — they depend on the
relationship between two or more fields. That's model_validator.
"""

from pydantic import BaseModel, model_validator, field_validator, ValidationError


class CustomerSignup(BaseModel):
    email: str
    password: str
    confirm_password: str

    # mode='after': runs once EVERY field has individually passed. The
    # function receives the fully-built model instance.
    @model_validator(mode="after")
    def passwords_must_match(self):
        if self.password != self.confirm_password:
            raise ValueError("password and confirm_password do not match")
        return self


try:
    CustomerSignup(email="rohan@example.com", password="hunter2", confirm_password="hunter3")
except ValidationError as e:
    print("Mismatched passwords rejected:")
    print(e, "\n")

print("Matching passwords accepted:",
      CustomerSignup(email="rohan@example.com", password="hunter2", confirm_password="hunter2"), "\n")


# A second example — combining field_validator AND model_validator, and
# proving the execution order: field validators always run first.
class CustomerPreferences(BaseModel):
    name: str
    email_updates_only: bool
    sms_updates_only: bool

    @field_validator("name", mode="after")
    @classmethod
    def not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("name is required")
        print("   -> field_validator ran first (checking name alone)")
        return value

    @model_validator(mode="after")
    def check_contact_preference(self):
        print("   -> model_validator ran second (checking the whole model)")
        if self.email_updates_only and self.sms_updates_only:
            raise ValueError("cannot set both email_updates_only and sms_updates_only")
        return self


print("Watch the print order:")
try:
    CustomerPreferences(name="Meera Iyer", email_updates_only=True, sms_updates_only=True)
except ValidationError as e:
    print("\nRejected — contradictory preferences:")
    print(e)
