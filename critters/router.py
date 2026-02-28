"""
Smiling Critters — LLM Router
Tries Ollama (local) first, falls back to Gemini (cloud).

Known design constraints
------------------------
- Ollama availability is cached for OLLAMA_CACHE_TTL seconds so the status
  badge and pre-call reachability check share one network round-trip.
- PII sanitisation only runs before Gemini (cloud) calls — Ollama is local.
- If Ollama starts streaming but fails mid-response, we do NOT fall through to
  Gemini (that would produce a garbled double-response).  Instead we append a
  small reconnect nudge and return.
- check_llm_status() reports Gemini as available only when a key is configured;
  detecting an invalid/expired key would require a live test call.
"""

import os
import json
import time
import requests
from requests.exceptions import HTTPError
from dotenv import load_dotenv
from typing import Dict, Generator, List, Optional

load_dotenv()  # safety net — also called in app.py

GEMINI_MODEL = "gemini-2.0-flash"

# ── Ollama availability cache ─────────────────────────────────────────────────
# Re-check at most once per TTL window so the status badge + pre-call check
# share a single HTTP round-trip instead of blocking every render.
OLLAMA_CACHE_TTL = 5.0   # seconds
_ollama_cache: Dict = {"available": False, "checked_at": 0.0, "url": ""}

# ── Gemini rate-limit backoff ─────────────────────────────────────────────────
# When a 429 is received, skip Gemini for GEMINI_BACKOFF_S seconds so
# subsequent messages don't hammer the rate-limit endpoint.
GEMINI_BACKOFF_S = 60.0  # seconds to wait after a 429 before retrying
GEMINI_MAX_RETRIES = 3   # attempts before giving up
_gemini_backoff_until: float = 0.0


def _get_config() -> Dict[str, str]:
    """Read config fresh on every call — DB overrides env."""
    try:
        from db.queries import get_setting
        ollama_url   = get_setting("ollama_url")   or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        ollama_model = get_setting("ollama_model") or os.getenv("OLLAMA_MODEL", "llama3.1:8b")
        db_key       = get_setting("gemini_key")   or ""
        gemini_key   = db_key if (db_key and db_key != "your_gemini_api_key_here") else os.getenv("GEMINI_API_KEY", "")
    except Exception:
        ollama_url   = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        ollama_model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
        gemini_key   = os.getenv("GEMINI_API_KEY", "")
    return {
        "ollama_url":   ollama_url.rstrip("/"),
        "ollama_model": ollama_model,
        "gemini_key":   gemini_key,
    }


def _sanitise_for_cloud(messages: List[Dict]) -> List[Dict]:
    """Strip PII before sending messages to a cloud API. Not needed for Ollama."""
    import re
    safe = []
    for m in messages:
        content = m.get("content", "")
        content = re.sub(r'\b[\w.+-]+@[\w-]+\.\w+\b', '[email removed]', content)
        content = re.sub(r'\b\d{3}[-.\ s]?\d{3}[-.\ s]?\d{4}\b', '[phone removed]', content)
        safe.append({**m, "content": content})
    return safe


def _ollama_available(url: str) -> bool:
    """Cached reachability check — hits the network at most once per OLLAMA_CACHE_TTL."""
    now = time.monotonic()
    if (
        _ollama_cache["url"] == url
        and now - _ollama_cache["checked_at"] < OLLAMA_CACHE_TTL
    ):
        return _ollama_cache["available"]
    try:
        r = requests.get(f"{url}/api/tags", timeout=2)
        result = r.status_code == 200
    except Exception:
        result = False
    _ollama_cache.update({"available": result, "checked_at": now, "url": url})
    return result


def _call_ollama(system_prompt: str, messages: List[Dict], url: str, model: str) -> Generator[str, None, None]:
    payload = {
        "model": model,
        "stream": True,
        "messages": [{"role": "system", "content": system_prompt}] + messages,
        "options": {"temperature": 0.7, "num_predict": 300},
    }
    with requests.post(f"{url}/api/chat", json=payload, stream=True, timeout=60) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines():
            if not line:
                continue
            try:
                data  = json.loads(line)
                token = data.get("message", {}).get("content", "")
                if token:
                    yield token
                if data.get("done"):
                    break
            except json.JSONDecodeError:
                continue


def _call_gemini(system_prompt: str, messages: List[Dict], api_key: str) -> Generator[str, None, None]:
    global _gemini_backoff_until

    # Honour backoff window — don't even attempt if we're in cooldown
    wait = _gemini_backoff_until - time.monotonic()
    if wait > 0:
        raise RuntimeError(
            f"RATE_LIMITED:{wait:.0f}"
        )

    gemini_messages = []
    for m in messages:
        role = "user" if m["role"] == "user" else "model"
        gemini_messages.append({"role": role, "parts": [{"text": m["content"]}]})

    payload = {
        "system_instruction": {"parts": [{"text": system_prompt}]},
        "contents": gemini_messages,
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 300},
    }
    endpoint = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:streamGenerateContent?alt=sse&key={api_key}"
    )

    for attempt in range(1, GEMINI_MAX_RETRIES + 1):
        try:
            with requests.post(endpoint, json=payload, stream=True, timeout=60) as resp:
                if resp.status_code == 429:
                    # Parse Retry-After header if present, else use default backoff
                    retry_after = float(resp.headers.get("Retry-After", GEMINI_BACKOFF_S))
                    _gemini_backoff_until = time.monotonic() + retry_after
                    if attempt < GEMINI_MAX_RETRIES:
                        time.sleep(min(retry_after, 4.0 * attempt))  # short sleep then retry
                        continue
                    raise RuntimeError(f"RATE_LIMITED:{retry_after:.0f}")
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if not line:
                        continue
                    line_str = line.decode("utf-8") if isinstance(line, bytes) else line
                    if not line_str.startswith("data: "):
                        continue
                    try:
                        data  = json.loads(line_str[6:])
                        parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
                        for part in parts:
                            token = part.get("text", "")
                            if token:
                                yield token
                    except (json.JSONDecodeError, IndexError, KeyError):
                        continue
                return  # success — exit retry loop
        except RuntimeError:
            raise  # propagate RATE_LIMITED sentinel
        except Exception as e:
            if attempt == GEMINI_MAX_RETRIES:
                raise
            time.sleep(2.0 * attempt)


def get_llm_response(
    system_prompt: str,
    messages: List[Dict],
    use_local: bool = True,
) -> Generator[str, None, None]:
    """
    Main entry point. Always yields at least one token — never silently empty.

    Fallback rules
    --------------
    1. Ollama available → stream Ollama.  If it fails *before* any token is
       yielded, fall through to Gemini.  If it fails *mid-stream*, append a
       reconnect nudge and return — do NOT start a Gemini response on top of
       a partial Ollama one.
    2. Gemini key set → stream Gemini (with PII sanitisation).
    3. Both unavailable → friendly error message.
    """
    cfg = _get_config()

    # Try Ollama first (no PII sanitisation needed — fully local)
    if use_local and _ollama_available(cfg["ollama_url"]):
        yielded = False
        try:
            for token in _call_ollama(system_prompt, messages, cfg["ollama_url"], cfg["ollama_model"]):
                yielded = True
                yield token
            if yielded:
                return
        except Exception:
            if yielded:
                # Mid-stream failure: don't fall through — a partial Ollama response
                # followed by a full Gemini response would be garbled and confusing.
                yield "\n\n*(Oops, my connection went a bit wobbly! Could you ask me that again? 🌟)*"
                return
            # No tokens emitted yet → fall through to Gemini

    # Try Gemini (sanitise PII before sending to cloud)
    if cfg["gemini_key"]:
        cloud_msgs = _sanitise_for_cloud(messages)
        try:
            yielded = False
            for token in _call_gemini(system_prompt, cloud_msgs, cfg["gemini_key"]):
                yielded = True
                yield token
            if yielded:
                return
        except RuntimeError as e:
            # RATE_LIMITED sentinel from _call_gemini
            if str(e).startswith("RATE_LIMITED:"):
                secs = str(e).split(":", 1)[1]
                yield (
                    f"Hmm, my cloud brain is a little tired right now 😴 "
                    f"It needs about {secs} seconds to rest! "
                    f"Could you try again in a moment? 🌟"
                )
                return
            yield f"Oops, I had a hiccup connecting to my brain! (Error: {str(e)[:80]}) 🌟"
            return
        except Exception as e:
            yield f"Oops, I had a hiccup connecting to my brain! (Error: {str(e)[:80]}) 🌟"
            return

    # Both unavailable
    yield (
        "Oh no, I can't think right now! 🌟 "
        "Ask a grown-up to check the AI settings — "
        "Ollama needs to be running, or a Gemini key needs to be added in Parent Dashboard."
    )


def check_llm_status() -> Dict:
    cfg            = _get_config()
    ollama_ok      = _ollama_available(cfg["ollama_url"])
    gemini_has_key = bool(cfg["gemini_key"]) and cfg["gemini_key"] != "your_gemini_api_key_here"
    gemini_backoff = time.monotonic() < _gemini_backoff_until
    gemini_ok      = gemini_has_key and not gemini_backoff

    if ollama_ok:
        active = "ollama"
    elif gemini_ok:
        active = "gemini"
    elif gemini_has_key and gemini_backoff:
        active = "rate_limited"
    else:
        active = "none"

    backoff_secs = max(0.0, _gemini_backoff_until - time.monotonic())
    return {
        "ollama": {"available": ollama_ok, "model": cfg["ollama_model"], "url": cfg["ollama_url"]},
        "gemini": {"available": gemini_ok, "has_key": gemini_has_key,
                   "rate_limited": gemini_backoff, "backoff_secs": round(backoff_secs),
                   "model": GEMINI_MODEL},
        "active": active,
    }
