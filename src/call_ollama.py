# The code was developed with assistance from ChatGPT.
# call_ollama.py
"""
Send structured chat requests to Ollama (Qwen 0.5B Instruct).
- Uses /api/chat endpoint for better JSON reliability.
- Applies few-shot context built by build_inputs.py.
- Validates and normalizes the JSON output.
"""

import os
import json
import re
import requests
from typing import Dict, Any
from build_inputs import build_context_from_payload, build_messages


# Environment defaults
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen2.5:0.5b-instruct")

# Generation settings (balance between speed and quality)
GEN_OPTIONS = {
    "temperature": 0.2,
    "repeat_penalty": 1.1,
    "top_p": 0.9,
    "num_predict": 80,
    "num_ctx": 192,
    "seed": 7,
}
STOP_TOKENS = ["}\n", "}\r", "}\r\n"]

# Default fallback response in case of failure
FALLBACK = {
    "category": "Focus",
    "summary": "Keep tasks small today.",
    "steps": ["Hydrate now", "Walk 10 minutes", "Focus 25 minutes"],
    "cautions": ["Avoid late caffeine"],
}


def _clip(s: str, max_words: int = 6) -> str:
    """Trim a string to N words and remove leading bullets or numbering."""
    s = re.sub(r"^[\-\*\d\.\)\(]+\s*", "", str(s).strip())
    return " ".join(s.split()[:max_words])


def _extract_json_block(text: str) -> Dict[str, Any]:
    """Extract the first {...} JSON block from a string and parse it."""
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        raise ValueError("No JSON object found in response.")
    return json.loads(match.group(0))


def _validate_and_fix(data: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure the returned JSON strictly matches the required structure."""
    result = {
        "category": (data.get("category") or FALLBACK["category"]).strip(),
        "summary": (data.get("summary") or FALLBACK["summary"]).strip(),
        "steps": data.get("steps") or [],
        "cautions": data.get("cautions") or [],
    }

    # Normalize types
    if not isinstance(result["steps"], list):
        result["steps"] = []
    if not isinstance(result["cautions"], list):
        result["cautions"] = []

    # Clip words and fill missing items
    result["steps"] = [_clip(s) for s in result["steps"] if isinstance(s, str)][:3]
    while len(result["steps"]) < 3:
        result["steps"].append(FALLBACK["steps"][len(result["steps"])])

    result["cautions"] = [_clip(result["cautions"][0])] if result["cautions"] else [FALLBACK["cautions"][0]]

    return result


def infer_from_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Main entry: takes frontend JSON input, sends to Ollama, returns validated JSON."""
    context = build_context_from_payload(payload)
    messages = build_messages(context)

    body = {
        "model": MODEL_NAME,
        "format": "json",
        "messages": messages,
        "options": GEN_OPTIONS,
        "stop": STOP_TOKENS,
        "stream": False,
    }

    try:
        r = requests.post(f"{OLLAMA_HOST}/api/chat", json=body, timeout=60)
        r.raise_for_status()
        res = r.json()
        content = res.get("message", {}).get("content", "") or res.get("response", "")
        parsed = _extract_json_block(content)
        return _validate_and_fix(parsed)
    except Exception as e:
        print(f"[WARN] Inference failed: {e}")
        return FALLBACK.copy()


# Local test
if __name__ == "__main__":
    sample = {
        "locale": "en",
        "version": "v1",
        "choices": {
            "mood": "low",
            "energy": "low",
            "sleep_quality": "poor",
            "stress": "high",
            "goal": "focus",
            "symptoms": ["headache"],
            "time_slot": "10-15m",
        },
        "free_text": "Exam week; slept badly.",
    }

    print(json.dumps(infer_from_payload(sample), indent=2))