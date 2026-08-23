"""
FINAL PROJECT — settings.py
=============================================================
Reuses the BaseSettings pattern from Part 6, extended to support three
possible AI providers so the project runs regardless of which key(s)
are available.
"""

from functools import lru_cache
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    anthropic_api_key: SecretStr | None = None
    openai_api_key: SecretStr | None = None
    openrouter_api_key: SecretStr | None = None

    anthropic_model: str = "claude-sonnet-4-6"
    openai_model: str = "gpt-4o"
    openrouter_free_model: str = "meta-llama/llama-3.1-8b-instruct:free"

    max_tokens: int = Field(default=1024, ge=1, le=8192)
    debug: bool = False

    def active_provider(self) -> str:
        if self.anthropic_api_key:
            return "anthropic"
        if self.openai_api_key:
            return "openai"
        if self.openrouter_api_key:
            return "openrouter"
        raise RuntimeError(
            "No AI provider key configured. Set ANTHROPIC_API_KEY, "
            "OPENAI_API_KEY, or OPENROUTER_API_KEY in your .env file "
            "(copy .env.example to get started — OpenRouter has a free tier)."
        )


@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()
