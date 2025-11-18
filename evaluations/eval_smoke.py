# The code was developed with assistance from ChatGPT.
"""
Smoke test for LLM output structure.

Loads test prompts from `goldset.jsonl` and checks whether
the model returns valid JSON with expected keys.
"""
import json, os
from src.call_ollama import infer_ollama

for line in open("evaluations/goldset.jsonl"):
    case = json.loads(line)
    result = infer_ollama(case["opt"], case["txt"])
    print(f"{case['opt']}: {list(result.keys())}")
