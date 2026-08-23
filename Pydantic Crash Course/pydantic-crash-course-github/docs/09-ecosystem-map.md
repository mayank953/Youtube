# 09 — Where Pydantic Goes From Here

This course covers core Pydantic — `BaseModel`, `Field`, validators, `computed_field`, nested models, serialization control, `pydantic-settings`, and using those models directly with the OpenAI and Anthropic SDKs for structured output. That is the full scope.

**One layer up:** libraries like **Instructor** patch an existing LLM client to automatically validate its response against a Pydantic model and retry on failure — an automated version of the retry loop from Part 8.

**Two layers up:** full agent frameworks — **PydanticAI** (built by the Pydantic team), **LangChain**, **CrewAI** — all use Pydantic models as their validation layer under the hood, for tool schemas and structured agent outputs. What they add on top is orchestration: deciding *when* to call a tool, managing multi-turn state, chaining several LLM calls together. None of that orchestration is Pydantic's job — Pydantic's job, inside every one of these frameworks, is still exactly what this course taught: validate this piece of data against this schema.

**Deliberately out of scope:** PydanticAI, LangChain, CrewAI, and Instructor are not taught here. Everything covered is the foundation all four are built on, and transfers directly whenever you're ready to explore them.

**Code for this part:** [`code/09_ecosystem_map/`](../code/09_ecosystem_map/)
