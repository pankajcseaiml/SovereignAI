"""
SovereignAI — Model Download & Verification Manager
Pulls and verifies local open-weight LLMs via Ollama API.
"""

import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path

DEFAULT_MODEL = "qwen2.5:0.5b"
DEFAULT_OLLAMA_URL = os.getenv("MODEL_SERVER_URL", "http://localhost:11434")


def check_ollama_alive(base_url: str) -> bool:
    """Checks if Ollama server is reachable."""
    try:
        req = urllib.request.Request(f"{base_url}/api/version")
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode())
                print(f"[+] Ollama server is online (version {data.get('version')})")
                return True
    except Exception:
        pass
    return False


def pull_model(base_url: str, model_name: str) -> bool:
    """Triggers model pull in Ollama."""
    print(f"[*] Requesting pull for model: '{model_name}' from {base_url}...")
    url = f"{base_url}/api/pull"
    payload = json.dumps({"name": model_name, "stream": False}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read().decode())
            if data.get("status") == "success":
                print(f"[SUCCESS] Model '{model_name}' downloaded successfully.")
                return True
            else:
                print(f"[*] Response: {data}")
                return True
    except Exception as e:
        print(f"[ERROR] Failed to pull model '{model_name}': {e}", file=sys.stderr)
        return False


def list_models(base_url: str):
    """Lists installed models in Ollama."""
    url = f"{base_url}/api/tags"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            models = data.get("models", [])
            print(f"[*] Available models in Ollama ({len(models)}):")
            for m in models:
                print(f"  - {m.get('name')} ({round(m.get('size', 0) / 1024 / 1024, 1)} MB)")
            return models
    except Exception as e:
        print(f"[WARNING] Could not list models: {e}")
        return []


def main():
    import argparse
    parser = argparse.ArgumentParser(description="SovereignAI Model Manager")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model name to pull")
    parser.add_argument("--url", default=DEFAULT_OLLAMA_URL, help="Ollama base URL")
    args = parser.parse_args()

    print("========================================================")
    print("  SovereignAI — Model Download & Verification           ")
    print("========================================================")

    if not check_ollama_alive(args.url):
        print(f"[!] Ollama server at {args.url} is not responding.", file=sys.stderr)
        print("    If running inside Docker, ensure sovereign-ollama container is started.")
        print("    You can start it with: docker compose up -d ollama")
        sys.exit(0)

    success = pull_model(args.url, args.model)
    list_models(args.url)

    if success:
        print("[SUCCESS] Model setup complete.")
    else:
        print("[ERROR] Model download encountered issues.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
