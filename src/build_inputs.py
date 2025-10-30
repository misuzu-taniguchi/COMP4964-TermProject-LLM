from pathlib import Path

def build_inputs(selected_option: str, free_text: str) -> str:
    system = Path("prompts/system.txt").read_text()
    return (
        f"SYSTEM:\n{system}\n\n"
        "SCHEMA (verbal): category,risk_level,summary,steps[],cautions,disclaimer\n\n"
        "USER:\n"
        f"Option: {selected_option}\n"
        f"Note: {free_text}\n"
        "Return JSON ONLY."
    )
