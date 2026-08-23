"""
6.2 — BaseSettings, .env FILES, AND SecretStr
=============================================================
Install first: pip install pydantic-settings

To run with a real .env file: copy .env.example to .env in this folder
and edit the values, then: python "6.2_basesettings_and_env_files.py"
"""

import os
from functools import lru_cache
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Field name -> env var name mapping is automatic uppercase:
    # api_key -> API_KEY, max_connections -> MAX_CONNECTIONS
    api_key: SecretStr = Field(default=SecretStr("demo-key-not-set"))
    max_connections: int = Field(default=100, ge=1, le=1000)
    debug: bool = False


# So this file runs standalone even without a real .env present:
os.environ.setdefault("API_KEY", "sk-demo-key-12345")
os.environ.setdefault("MAX_CONNECTIONS", "200")
os.environ.setdefault("DEBUG", "true")

settings = AppSettings()

print("settings.api_key:", settings.api_key, "(masked automatically — SecretStr)")
print("settings.max_connections:", settings.max_connections, "| type:", type(settings.max_connections).__name__)
print("settings.debug:", settings.debug, "| type:", type(settings.debug).__name__)
print("\nCompare to 6.1: max_connections is now a REAL int, debug a REAL bool.")
print("A bad MAX_CONNECTIONS value would raise a clear error at startup.")

print("\nAccessing the real secret value on purpose:")
print("  settings.api_key.get_secret_value() ->", settings.api_key.get_secret_value())


# Singleton pattern: load settings once, reuse everywhere.
@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()


print("\nCached settings instance:", get_settings().max_connections)
