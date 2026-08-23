# 06 — Pydantic Settings

Every value from `os.getenv()` is a string — or `None` — always. `MAX_CONNECTIONS` arrives as `"200"`, not `200`. Writing `if debug_mode:` against the raw string `"false"` evaluates to `True`, since any non-empty string is truthy — a genuinely common bug.

> **Analogy — raw sensor wires vs. a dashboard.** A car's raw sensor wires carry unlabeled voltage — whether it means "speed" or "fuel level" is anywhere. The dashboard turns those signals into a trustworthy, typed gauge. `os.getenv()` gives raw wires. `BaseSettings` is the dashboard.

```python
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    api_key: SecretStr
    max_connections: int = Field(default=100, ge=1, le=1000)
    debug: bool = False

settings = AppSettings()   # reads from .env / environment automatically
```

A settings class is defined exactly like a `BaseModel` — `BaseSettings` (from the separate `pydantic-settings` package) extends it directly. Field names map to environment variable names automatically, uppercased. Every `Field()` constraint from Part 3 applies identically. `SecretStr` keeps API keys out of logs.

**Code for this part:** [`code/06_pydantic_settings/`](../code/06_pydantic_settings/)
