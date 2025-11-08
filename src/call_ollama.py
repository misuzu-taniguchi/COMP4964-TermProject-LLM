from dotenv import load_dotenv
load_dotenv()

import os, requests, json
from build_inputs import build_inputs

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL = os.getenv("OLLAMA_MODEL", "tinyllama:1.1b")

def infer_ollama(option: str, text: str):
    payload = {
        "model": MODEL,
        "prompt": build_inputs(option, text),
        "options": {
            "temperature": 0.3, 
            "num_predict": 128,
            "num_ctx": 256,
            }
    }
    r = requests.post(f"{OLLAMA_HOST}/api/generate", json=payload, timeout=30)
    r.raise_for_status()
    # Ollama streams; for simplicity, concatenate
    txt = ""
    for chunk in r.iter_lines():
        if not chunk: continue
        j = json.loads(chunk.decode())
        txt += j.get("response", "")
        if j.get("done"): break
    try:
        return json.loads(txt)
    except Exception:
        return {"_raw": txt}

if __name__ == "__main__":
    print(infer_ollama("Improve sleep", "Coffee at 5pm, can't sleep."))
