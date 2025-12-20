def apply_fix(fix: dict):
    file = fix["file"]
    action = fix["action"]
    content = fix["content"]

    if action == "add":
        with open(file, "a") as f:
            f.write("\n" + content)

    elif action == "replace":
        with open(file, "w") as f:
            f.write(content)
