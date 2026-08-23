"""
DEMO — Real Application Settings Class
=============================================================
A complete settings class for the customer-facing app used from Part 7
onward: typed fields, Field() constraints, SecretStr, and a .env file.
"""

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    anthropic_api_key: SecretStr = Field(default=SecretStr("not-set"))
    openai_api_key: SecretStr = Field(default=SecretStr("not-set"))
    openrouter_api_key: SecretStr = Field(default=SecretStr("not-set"))
    request_timeout_seconds: int = Field(default=30, ge=1, le=300)

    debug: bool = False
    log_level: str = "INFO"
    max_connections: int = Field(default=10, ge=1, le=100)

    @property
    def is_production(self) -> bool:
        return not self.debug


settings = AppSettings()

print("=== Application Settings Loaded ===")
print(f"Debug mode:         {settings.debug}")
print(f"Is production:      {settings.is_production}")
print(f"Log level:          {settings.log_level}")
print(f"Max connections:    {settings.max_connections}")
print(f"Request timeout:    {settings.request_timeout_seconds}s")
print(f"Anthropic key set?: {settings.anthropic_api_key.get_secret_value() != 'not-set'}")
print(f"OpenAI key set?:    {settings.openai_api_key.get_secret_value() != 'not-set'}")
print(f"OpenRouter key set?:{settings.openrouter_api_key.get_secret_value() != 'not-set'}")
