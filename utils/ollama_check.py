"""
Smiling Critters — Ollama Setup Checker
Run directly to diagnose connection issues:
    python utils/ollama_check.py
"""

import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()


def check_ollama(url: str = None, model: str = None) -> dict:
    """Check Ollama connectivity and model availability."""
    url   = (url   or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")).rstrip("/")
    model = model or os.getenv("OLLAMA_MODEL", "llama3:latest")

    result = {
        "url":        url,
        "model":      model,
        "reachable":  False,
        "models":     [],
        "model_found": False,
        "error":      None,
    }

    try:
        r = requests.get(f"{url}/api/tags", timeout=3)
        if r.status_code == 200:
            result["reachable"] = True
            result["models"]    = [m["name"] for m in r.json().get("models", [])]
            result["model_found"] = any(
                m == model or m.startswith(model.split(":")[0])
                for m in result["models"]
            )
        else:
            result["error"] = f"HTTP {r.status_code}"
    except requests.exceptions.ConnectionError:
        result["error"] = "Connection refused — Ollama is not running"
    except requests.exceptions.Timeout:
        result["error"] = "Timeout — Ollama unreachable at this URL"
    except Exception as e:
        result["error"] = str(e)

    return result


def print_report(result: dict):
    print("\n🐾 Smiling Critters — Ollama Connection Report")
    print("=" * 52)
    print(f"  URL:   {result['url']}")
    print(f"  Model: {result['model']}")
    print()

    if result["reachable"]:
        print("  ✅ Ollama is running and reachable")
        if result["models"]:
            print(f"  📦 Models available: {', '.join(result['models'])}")
        else:
            print("  ⚠️  No models pulled yet")

        if result["model_found"]:
            print(f"  ✅ Model '{result['model']}' is ready")
        else:
            print(f"  ❌ Model '{result['model']}' not found")
            print(f"\n  Fix: ollama pull {result['model']}")
    else:
        print(f"  ❌ Cannot reach Ollama: {result['error']}")
        print()
        print("  Fixes:")
        print("  1. Start Ollama:         ollama serve")
        print(f"  2. Check URL in .env:    OLLAMA_BASE_URL={result['url']}")
        print("  3. If on another machine: use that machine's IP, e.g.")
        print("     OLLAMA_BASE_URL=http://192.168.1.X:11434")
        print()
        print("  Then run this check again.")

    print()


if __name__ == "__main__":
    # Optional: pass URL as argument
    url   = sys.argv[1] if len(sys.argv) > 1 else None
    model = sys.argv[2] if len(sys.argv) > 2 else None
    result = check_ollama(url, model)
    print_report(result)
    sys.exit(0 if result["reachable"] and result["model_found"] else 1)
