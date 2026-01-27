def extract_error(logs: str) -> str:
    """
    Extracts the most relevant error lines from CI logs
    """
    lines = logs.splitlines()

    error_keywords = [
        "ModuleNotFoundError",
        "ImportError",
        "Traceback",
        "ERROR",
        "Error:",
        "FAILED",
        "Exception"
    ]

    extracted = []

    for line in lines:
        for key in error_keywords:
            if key in line:
                extracted.append(line.strip())
                break

    # Limit size for LLM
    return "\n".join(extracted[-20:])
