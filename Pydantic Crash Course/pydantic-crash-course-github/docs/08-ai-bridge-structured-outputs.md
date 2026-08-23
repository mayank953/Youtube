# 08 — The AI Bridge: Validating What LLMs Give You Back

An LLM asked to "extract customer info as JSON" might wrap the response in a markdown code fence, add a friendly preamble, or return a boolean as the string `"yes definitely"` instead of `true`. All are realistic outputs — only one survives a naive `json.loads()` unmodified.

> **Analogy — shouting an order vs. a printed slip.** An LLM shouting its answer across the room is exactly as unreliable as a customer shouting a restaurant order — half the words get lost. What you want is the LLM handing you the printed, checkbox order slip: a response guaranteed to match a schema you defined.

## OpenAI structured outputs

```python
from openai import OpenAI
client = OpenAI()

response = client.responses.parse(
    model="gpt-4o",
    input="Extract: Rohan says his order hasn't shipped yet.",
    text_format=CustomerMessage,   # pass the Pydantic MODEL directly
)
message = response.output_parsed   # already validated
```

## Claude (Anthropic) structured outputs

```python
from anthropic import Anthropic
client = Anthropic()

response = client.messages.parse(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Extract: Rohan says his order hasn't shipped yet."}],
    output_format=CustomerMessage,
)
message = response.parsed_output   # already validated
```

One Pydantic model, reused unchanged across both providers — the schema is provider-agnostic; only the SDK call around it changes.

## Literal + the retry pattern

`Literal["low", "medium", "high"]` (from Part 1) physically restricts what an AI classification can return. When a response fails validation, the `ValidationError` is the trigger for a self-correcting retry loop: feed the error back to the model and ask it to try again. This simple pattern — ask, validate, retry with the error — is the entire mechanism libraries like Instructor automate under a decorator.

> **Structured outputs guarantee shape, never correctness.** A perfectly-formatted, confidently wrong answer is still possible. Validation catches malformed data, not hallucinated facts.

**Code for this part:** [`code/08_ai_bridge_structured_outputs/`](../code/08_ai_bridge_structured_outputs/)
