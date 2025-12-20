from agents.log_analyzer import extract_error
from agents.reasoner import diagnose
from agents.fixer import apply_fix
from agents.verifier import is_confident

def agentic_heal(logs: str):
    for attempt in range(3):
        error_log = extract_error(logs)
        diagnosis = diagnose(error_log)

        if not is_confident(diagnosis):
            return "Low confidence. Manual review needed."

        apply_fix(diagnosis["fix"])

        # Assume CI will rerun automatically
        return "Fix applied. Awaiting CI rerun."

    return "Healing failed after retries."
