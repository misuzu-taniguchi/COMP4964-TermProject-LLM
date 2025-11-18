# The code was developed with assistance from ChatGPT.
# build_inputs.py
"""
Builds structured input messages for Ollama's /api/chat endpoint (Qwen 0.5B Instruct).
- Reads system behavior rules from prompts/system.txt.
- Injects one few-shot example for stability.
- Builds a concise English context summary from frontend payload.
"""

from pathlib import Path
from typing import Dict, List, Any


def read_system_prompt() -> str:
    """Load the system instructions from prompts/system.txt"""
    return Path("prompts/system.txt").read_text()


def _join(values: List[str]) -> str:
    """Join a list of short descriptors into a single comma-separated phrase."""
    return ", ".join([v for v in values if v])


def build_context_from_payload(payload: Dict[str, Any]) -> str:
    """
    Convert frontend payload into a concise English context description.
    Example: 'Mood low, energy low, slept badly, goal focus, symptom headache.'
    """
    ch = payload.get("choices", {}) if isinstance(payload, dict) else {}
    parts = []
    if ch.get("mood"): parts.append(f"mood {ch['mood']}")
    if ch.get("energy"): parts.append(f"energy {ch['energy']}")
    if ch.get("sleep_quality"): parts.append(f"sleep {ch['sleep_quality']}")
    if ch.get("stress"): parts.append(f"stress {ch['stress']}")
    if ch.get("goal"): parts.append(f"goal {ch['goal']}")
    if ch.get("symptoms"): parts.append(f"symptoms {_join(ch['symptoms'])}")
    if ch.get("time_slot"): parts.append(f"time {ch['time_slot']}")
    if payload.get("free_text"): parts.append(f"note {payload['free_text']}")
    context = ", ".join(parts) if parts else "tired, can't focus, exam week, slept badly"
    return f"Context: {context}."


def build_messages(context: str) -> List[Dict[str, str]]:
    """
    Build the /api/chat 'messages' array for Qwen instruct.
    Includes one few-shot example to stabilize structure.
    """
    system = read_system_prompt()

    fewshot_user = "Example context: low energy."
    fewshot_assistant = (
        '{"category":"Energy","summary":"Gentle boost with small actions.",'
        '"steps":["Hydrate now","Stand and stretch","Short fresh-air walk"],'
        '"cautions":["Avoid late caffeine"]}'
    )

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": fewshot_user},
        {"role": "assistant", "content": fewshot_assistant},
        {"role": "user", "content": context},
    ]