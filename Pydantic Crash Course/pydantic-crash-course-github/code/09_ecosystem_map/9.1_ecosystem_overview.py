"""
9.1 — WHERE PYDANTIC GOES FROM HERE
=============================================================
A short, honest map of the ecosystem. This course teaches core Pydantic
— the validation foundation. It does not teach any agent framework.
Here's where everything else sits on top of what you now know.
"""

# THE FOUNDATION — what this course covered, start to finish:
#
#   pydantic (core)
#     -> BaseModel, Field, validators, computed_field, nested models,
#        serialization control
#   pydantic-settings
#     -> BaseSettings, typed config from environment variables
#   Structured LLM output (Part 8)
#     -> using YOUR Pydantic models directly with the OpenAI SDK
#        (client.responses.parse) and the Anthropic SDK
#        (client.messages.parse) — no extra framework, no agent loop


# ONE LAYER UP — libraries that use Pydantic to solve a narrower
# problem than a full agent (structured extraction from one LLM call):
#
#   Instructor
#     - Patches an existing LLM client (OpenAI, Anthropic, etc.) to
#       automatically validate its response against a Pydantic model,
#       and automatically retries with the validation error fed back on
#       failure. This is, almost exactly, an automated version of the
#       manual retry loop built by hand in 8.4.
#
#   Illustrative pseudocode of the pattern (not installed or taught here):
#     # import instructor
#     # client = instructor.from_provider("openai/gpt-4o-mini")
#     # result = client.chat.completions.create(
#     #     response_model=TicketClassification,
#     #     messages=[...],
#     #     max_retries=3,
#     # )


# TWO LAYERS UP — full agent frameworks, out of scope for this course,
# that also use Pydantic models as their validation layer under the hood:
#
#   PydanticAI    -> built by the Pydantic team; agents, tools, typed
#                    dependency injection, multi-step reasoning loops
#   LangChain     -> the largest general agent + RAG ecosystem
#   CrewAI        -> multi-agent orchestration
#
# All three let you define a Pydantic model as an agent's output schema
# or a tool's input schema — the exact same BaseModel skill covered in
# this course. What they add on top is orchestration: deciding when to
# call a tool, managing multi-turn state, chaining several LLM calls
# together. None of that orchestration is Pydantic's job — Pydantic's
# job, inside every one of these frameworks, is still exactly what this
# course taught: validate this piece of data against this schema.

print(__doc__)
