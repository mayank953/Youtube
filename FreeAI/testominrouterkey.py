"""
Test an OmniRoute API key.

OmniRoute (https://github.com/pitbaden/omniroute) is a self-hosted, OpenAI-compatible
AI gateway. It has no dedicated "check key" endpoint, so this script verifies the key
by calling the standard OpenAI-compatible routes:

    1. GET  /v1/models             -> gateway reachable, key accepted, lists models
    2. POST /v1/chat/completions   -> a real (tiny) completion actually works

Usage:
    export OMNIROUTE_API_KEY="your-key"
    # optional, defaults to http://localhost:20128/v1
    export OMNIROUTE_BASE_URL="http://localhost:20128/v1"
    python testominrouterkey.py

    # or pass them directly:
    python testominrouterkey.py <api_key> [base_url] [model]
"""

import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_BASE_URL = "http://localhost:20128/v1"
# Override with a model your gateway actually has configured (see /v1/models output).
DEFAULT_MODEL = "cc/claude-opus-4-6"


def _request(base_url, path, api_key, method="GET", payload=None):
    url = f"{base_url.rstrip('/')}{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            body = json.loads(body)
        except ValueError:
            pass
        return e.code, body
    except urllib.error.URLError as e:
        return None, f"Connection error: {e.reason}"


def check_key(api_key, base_url, model):
    print(f"1. Listing models ({base_url}/models) ...")
    status, body = _request(base_url, "/models", api_key)
    if status == 200 and isinstance(body, dict):
        models = body.get("data", [])
        print(f"   OK - key accepted, {len(models)} models available")
        for m in models[:10]:
            print(f"      - {m.get('id')}")
        if len(models) > 10:
            print(f"      ... and {len(models) - 10} more")
    elif status in (401, 403):
        print(f"   FAILED - key rejected (HTTP {status}): {body}")
        return False
    elif status is None:
        print(f"   FAILED - {body}")
        print("   Is the OmniRoute gateway running and is OMNIROUTE_BASE_URL correct?")
        return False
    else:
        print(f"   WARNING (HTTP {status}): {body}")

    print(f"\n2. Live completion with '{model}' ...")
    status, body = _request(
        base_url,
        "/chat/completions",
        api_key,
        method="POST",
        payload={
            "model": model,
            "messages": [{"role": "user", "content": "Reply with exactly: pong"}],
            "max_tokens": 10,
        },
    )
    if status == 200 and isinstance(body, dict):
        reply = body["choices"][0]["message"]["content"]
        print(f"   OK - model replied: {reply!r}")
        usage = body.get("usage")
        if usage:
            print(f"      usage: {usage}")
        return True
    if status in (401, 403):
        print(f"   FAILED - key rejected (HTTP {status}): {body}")
    else:
        print(f"   FAILED (HTTP {status}): {body}")
        print("   The key may be valid but this model isn't configured - "
              "try one from the list above.")
    return False


def main():
    args = sys.argv[1:]
    api_key = args[0] if len(args) > 0 else os.environ.get("OMNIROUTE_API_KEY")
    base_url = (
        args[1] if len(args) > 1
        else os.environ.get("OMNIROUTE_BASE_URL", DEFAULT_BASE_URL)
    )
    model = args[2] if len(args) > 2 else os.environ.get("OMNIROUTE_MODEL", DEFAULT_MODEL)

    if not api_key:
        print("No API key. Set OMNIROUTE_API_KEY or pass it as the first argument.")
        sys.exit(1)

    shown = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "(short key)"
    print(f"Testing OmniRoute key: {shown}")
    print(f"Base URL: {base_url}\n")

    ok = check_key(api_key, base_url, model)
    print("\nKey works." if ok else "\nKey test failed.")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
