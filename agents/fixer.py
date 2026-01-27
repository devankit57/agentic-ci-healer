from utils.github_client import create_fix_pr

def apply_fix(fix):
    return create_fix_pr(
        fix["file"],
        fix["content"]
    )
