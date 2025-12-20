def is_confident(diagnosis: dict) -> bool:
    return diagnosis.get("confidence", 0) >= 0.7
