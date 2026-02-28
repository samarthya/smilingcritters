"""
Smiling Critters — LLM Router
Tries Ollama (local) first, falls back to Gemini (cloud).
All calls are sanitised before sending to remove identifying info.
"""

import os
import requests
import json
import time
import streamlit as st
from typing import Generator


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL    = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
GEMINI_API_KEY  = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL    = "gemini-1.5-flash"


def _sanitise_messages(messages: list[dict]) -> list[dict]:
    """Strip any accidental PII patterns before sending to cloud LLM."""
    import re
    safe = []
    for m in messages:
        content = m.get("content", "")
        # Remove email-like patterns
        content = re.sub(r'\b[\w.+-]+@[\w-]+\.\w+\b', '[email removed]', content)
        # Remove phone-like patterns
        content = re.sub(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', '[phone removed]', content)
        safe.append({**m, "content": content})
    return safe


def _ollama_available() -> bool:
    try:
        r = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=2)
        return r.status_code == 200
    except Exception:
        return False


def _call_ollama(system_prompt: str, messages: list[dict]) -> Generator[str, None, None]:
    """Stream response from Ollama."""
    payload = {
        "model": OLLAMA_MODEL,
        "stream": True,
        "messages": [{"role": "system", "content": system_prompt}] + messages,
        "options": {
            "temperature": 0.7,
            "num_predict": 300,
        }
    }
    with requests.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        json=payload,
        stream=True,
        timeout=60
    ) as resp:
        for line in resp.iter_lines():
            if line:
                try:
                    data = json.loads(line)
                    token = data.get("message", {}).get("content", "")
                    if token:
                        yield token
                    if data.get("done"):
                        break
                except json.JSONDecodeError:
                    continue


def _call_gemini(system_prompt: str, messages: list[dict]) -> Generator[str, None, None]:
    """Stream response from Gemini Flash."""
    if not GEMINI_API_KEY:
        yield "Hmm, I'm having a little trouble connecting right now! Can you try again in a moment? 🌟"
        return

    # Build Gemini message format
    gemini_messages = []
    for m in messages:
        role = "user" if m["role"] == "user" else "model"
        gemini_messages.append({
            "role": role,
            "parts": [{"text": m["content"]}]
        })

    payload = {
        "system_instruction": {"parts": [{"text": system_prompt}]},
        "contents": gemini_messages,
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 300,
        }
    }

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:streamGenerateContent?alt=sse&key={GEMINI_API_KEY}"
    )

    with requests.post(url, json=payload, stream=True, timeout=60) as resp:
        for line in resp.iter_lines():
            if line:
                line_str = line.decode("utf-8") if isinstance(line, bytes) else line
                if line_str.startswith("data: "):
                    try:
                        data = json.loads(line_str[6:])
                        parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
                        for part in parts:
                            token = part.get("text", "")
                            if token:
                                yield token
                    except (json.JSONDecodeError, IndexError, KeyError):
                        continue


def get_llm_response(
    system_prompt: str,
    messages: list[dict],
    use_local: bool = True,
) -> Generator[str, None, None]:
    """
    Main entry point. Returns a streaming generator of tokens.
    Tries Ollama first if use_local=True, falls back to Gemini.
    """
    safe_messages = _sanitise_messages(messages)

    if use_local and _ollama_available():
        source = "🏠 Local AI"
        try:
            yield from _call_ollama(system_prompt, safe_messages)
            return
        except Exception as e:
            # Fall through to Gemini
            pass

    # Gemini fallback
    yield from _call_gemini(system_prompt, safe_messages)


def check_llm_status() -> dict:
    """Return status of both LLM backends for the parent dashboard."""
    ollama_ok = _ollama_available()
    gemini_ok = bool(GEMINI_API_KEY)
    return {
        "ollama": {
            "available": ollama_ok,
            "model": OLLAMA_MODEL,
            "url": OLLAMA_BASE_URL,
            "label": "🏠 Local (Ollama)",
        },
        "gemini": {
            "available": gemini_ok,
            "model": GEMINI_MODEL,
            "label": "☁️ Cloud (Gemini)",
        },
        "active": "ollama" if ollama_ok else ("gemini" if gemini_ok else "none"),
    }
