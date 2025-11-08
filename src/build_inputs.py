from pathlib import Path

def build_inputs(selected_option: str, free_text: str) -> str:
    system = Path("prompts/system.txt").read_text()

    return (
        f"SYSTEM:\n{system}\n\n"
        "SCHEMA (verbal): category,risk_level,summary,steps[],cautions[],disclaimer\n"
        "FORMAT: Return JSON ONLY, minified or pretty is fine. Do NOT use markdown or code fences.\n"
        "CONSTRAINTS: 3 steps max, 1 caution, keep total output short.\n"
        "USER:\n"
        f"Option: {selected_option}\n"
        f"Note: {free_text}\n"
        "TASK: Produce a single JSON object following the schema.\n"
    )