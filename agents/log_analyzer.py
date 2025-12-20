def extract_error(logs: str) -> str:
    lines = logs.splitlines()
    error_lines = []

    for line in lines:
        if "ERROR" in line or "ModuleNotFoundError" in line or "Traceback" in line:
            error_lines.append(line)

    return "\n".join(error_lines[-20:])
