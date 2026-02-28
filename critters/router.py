"""
Smiling Critters — LLM Router
Tries Ollama (local) first, falls back to Gemini (cloud).

Config priority (highest → lowest):
  1. DB settings (parent dashboard → overrides everything at runtime)
  2. Environment variables / .env file
  3. Hard-coded defaults
"""

import os
import requests
import json
from typing import Dict, Generator, List, Optional

from dotenv import load_dotenv
load_dotenv()  # Load .env file — must happen before any os.getenv() calls

# Defaults from env (can be overridden by DB settings at call time)
_DEFAULT_OLLAMA_URL   = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
_DEFAULT_OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
_DEFAULT_GEMINI_KEY   = os.getenv("GEMINI_API_KEY", "")

GEMINI_MODEL = "gemini-1.5-flash"


def _get_config() -> Dict[str, str]:
    """
    Read live config from DB (parent dashboard settings), falling back to env vars.
    Called fresh on every LLM request so dashboard changes take effect immediately.
    """
    try:
        from db.queries import get_setting
        ollama_url   = get_setting("ollama_url")   or _DEFAULT_OLLAMA_URL
        ollama_model = get_setting("ollama_model") or _DEFAULT_OLLAMA_MODEL
        gemini_key   = get_setting("gemini_key")   or _DEFAULT_GEMINI_KEY
    except Exception:
        # DB not ready yet (e.g. first run before init_db) — fall back to env
        ollama_url   = _DEFAULT_OLLAMA_URL
        ollama_model = _DEFAULT_OLLAMA_MODEL
        gemini_key   = _DEFAULT_GEMINI_KEY

    return {
        "ollama_url":   ollama_url.rstrip("/"),
        "ollama_model": ollama_model,
        "gemini_key":   gemini_key,
    }


def _sanitise_messages(messages: List[Dict]) -> List[Dict]:
    """Strip accidental PII patterns before sending to any LLM."""
    import re
    safe = []
    for m in messages:
        content = m.get("content", "")
        content = re.sub(r'\b[\w.+-]+@[\w-]+\.\w+\b', '[email removed]', content)
        content = re.sub(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', '[phone removed]', content)
        safe.append({**m, "content": content})
    return safe


def _ollama_available(url: str) -> bool:
    try:
        r = requests.get(f"{url}/api/tags", timeout=2)
        return r.status_code == 200
    except Exception:
        return False


def _call_ollama(
    system_prompt: str,
    messages: List[Dict],
    url: str,
    model: str,
) -> Generator[str, None, None]:
    """Stream response from Ollama."""
    payload = {
        "model": model,
        "stream": True,
        "messages": [{"role": "system", "content": system_prompt}] + messages,
        "options": {
            "temperature": 0.7,
            "num_predict": 300,
        },
    }
    with requests.post(f"{url}/api/chat", json=payload, stream=True, timeout=60) as resp:
        for line in resp.iter_lines():
            if line:
                try:
                    data  = json.loads(line)
                    token = data.get("message", {}).get("content", "")
                    if token:
                        yield token
                    if data.get("done"):
                        break
                except json.JSONDecodeError:
                    continue


def _call_gemini(
    system_prompt: str,
    messages: List[Dict],
    api_key: str,
) -> Generator[str, None, None]:
    """Stream response from Gemini Flash."""
    if not api_key:
        yield "Hmm, I'm having a little trouble connecting right now! Can you try again in a moment? 🌟"
        return

    gemini_messages = []
    for m in messages:
        role = "user" if m["role"] == "user" else "model"
        gemini_messages.append({"role": role, "parts": [{"text": m["content"]}]})

    payload = {
        "system_instruction": {"parts": [{"text": system_prompt}]},
        "contents": gemini_messages,
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 300},
    }
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:streamGenerateContent?alt=sse&key={api_key}"
    )

    with requests.post(url, json=payload, stream=True, timeout=60) as resp:
        for line in resp.iter_lines():
            if line:
                line_str = line.decode("utf-8") if isinstance(line, bytes) else line
                if line_str.startswith("data: "):
                    try:
                        data  = json.loads(line_str[6:])
                        parts = (data.get("candidates", [{}])[0]
                                     .get("content", {})
                                     .get("parts", []))
                        for part in parts:
                            token = part.get("text", "")
                            if token:
                                yield token
                    except (json.JSONDecodeError, IndexError, KeyError):
                        continue


def get_llm_response(
    system_prompt: str,
    messages: List[Dict],
    use_local: bool = True,
) -> Generator[str, None, None]:
    """
    Main entry point. Returns a streaming token generator.
    Reads live config so dashboard changes take effect without restart.
    """
    cfg           = _get_config()
    safe_messages = _sanitise_messages(messages)

    if use_local and _ollama_available(cfg["ollama_url"]):
        try:
            yield from _call_ollama(system_prompt, safe_messages,
                                    cfg["ollama_url"], cfg["ollama_model"])
            return
        except Exception:
            pass  # Fall through to Gemini

    yield from _call_gemini(system_prompt, safe_messages, cfg["gemini_key"])


def check_llm_status() -> Dict:
    """Return live status of both backends. Used by UI and parent dashboard."""
    cfg       = _get_config()
    ollama_ok = _ollama_available(cfg["ollama_url"])
    gemini_ok = bool(cfg["gemini_key"])

    return {
        "ollama": {
            "available": ollama_ok,
            "model":     cfg["ollama_model"],
            "url":       cfg["ollama_url"],
            "label":     "🏠 Local (Ollama)",
        },
        "gemini": {
            "available": gemini_ok,
            "model":     GEMINI_MODEL,
            "label":     "☁️ Cloud (Gemini)",
        },
        "active": "ollama" if ollama_ok else ("gemini" if gemini_ok else "none"),
    }
