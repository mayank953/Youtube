"""
8.1 — WHY RAW LLM TEXT OUTPUT IS A LIABILITY
=============================================================
No API key needed for this file — realistic LLM output patterns are
simulated as plain strings, isolating the parsing problem itself.
"""

import json
from pydantic import BaseModel, ValidationError


class CustomerMessage(BaseModel):
    customer_name: str
    topic: str
    is_urgent: bool


# Four realistic things an LLM might return for "extract the customer
# message info as JSON," without any structured-output enforcement.
llm_response_1 = '{"customer_name": "Rohan", "topic": "shipping delay", "is_urgent": true}'

llm_response_2 = """```json
{"customer_name": "Rohan", "topic": "shipping delay", "is_urgent": true}
```"""   # wrapped in a markdown code fence — very common

llm_response_3 = (
    "Sure! Here's the extracted info: "
    '{"customer_name": "Rohan", "topic": "shipping delay", "is_urgent": true}'
    " Let me know if you need anything else!"
)   # chatty preamble/postamble mixed in with the JSON

llm_response_4 = '{"customer_name": "Rohan", "topic": "shipping delay", "is_urgent": "yes definitely"}'
# right SHAPE, wrong TYPE — is_urgent is a phrase, not a boolean

print("Attempting to parse each response with plain json.loads() + Pydantic:\n")

for i, raw in enumerate([llm_response_1, llm_response_2, llm_response_3, llm_response_4], start=1):
    print(f"--- Response #{i} ---")
    try:
        data = json.loads(raw)
        message = CustomerMessage.model_validate(data)
        print(f"Parsed successfully: {message}")
    except json.JSONDecodeError:
        print("Failed — the text wasn't valid JSON on its own")
        print("(markdown fences and chatty preambles break naive parsing)")
    except ValidationError as e:
        print(f"Valid JSON, but failed Pydantic validation:\n   {e}")
    print()

print(
    "Response #1 works. #2 and #3 need manual cleanup before they'll even"
    "\nparse. #4 parses fine but fails validation — right shape, wrong data."
    "\nThe fix: ask the provider to guarantee the shape, instead of hoping"
    "\nand cleaning up after the fact. That's 'structured outputs' — next."
)
