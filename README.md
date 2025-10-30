# COMP4964 Term Project – LLM Hosting (Ollama)

This repo hosts and tests the **LLM service** for our AI-powered API project.  
It contains prompts, schema, local runners, and deploy guides (DigitalOcean).  
Frontend/Backend live in a separate repository.

---

## What this provides
- **Prompt & schema**: `prompts/system.txt`, `prompts/fewshot.md`, `prompts/schema.json`
- **Client runners**: `src/call_ollama.py` (local/Ollama), `src/call_tgi.py` (TGI-ready)
- **Evaluation**: `evaluations/goldset.jsonl`, `evaluations/eval_smoke.py`
- **Deploy notes**: `deploy/DigitalOcean.md`, `deploy/docker-compose.tgi.yml`, `deploy/test_curl.sh`

Output is always **JSON** with this schema:
```json
{ "category":"stress|sleep|nutrition|activity|mood",
  "risk_level":"low|moderate|high",
  "summary":"...",
  "steps":[{"title":"...","how":"...","duration":"...","evidence_hint":"optional"}],
  "cautions":["..."],
  "disclaimer":"This is general wellness information, not medical advice."
}
