import os, requests, json
from build_inputs import build_inputs

LLM_ENDPOINT = os.getenv("LLM_ENDPOINT", "http://localhost:8080")

def infer_tgi(option: str, text: str):
    payload = {
        "inputs": build_inputs(option, text),
        "parameters": {
            "max_new_tokens": 256,
            "temperature": 0.3,
            "top_p": 0.9,
            "repetition_penalty": 1.05,
            "stop": ["```"]
        }
    }
    r = requests.post(f"{LLM_ENDPOINT}/generate", json=payload, timeout=10)
    r.raise_for_status()
    out = r.json()
    # TGI returns {"generated_text": "..."} or a list depending on version; normalize:
    if isinstance(out, list) and out and "generated_text" in out[0]:
        txt = out[0]["generated_text"]
    elif "generated_text" in out:
        txt = out["generated_text"]
    else:
        txt = out
    # 最低限のJSON整形（失敗時はそのまま返す）
    try:
        return json.loads(txt)
    except Exception:
        return {"_raw": txt}

if __name__ == "__main__":
    print(infer_tgi("Reduce stress", "Busy week and irregular sleep."))
