import os
import requests
import zipfile
import io

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_workflow_logs(repo: str, run_id: int) -> str:
    """
    Downloads GitHub Actions logs and returns them as plain text
    """
    url = f"https://api.github.com/repos/{repo}/actions/runs/{run_id}/logs"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch logs: {response.text}")

    log_text = ""

    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        for name in z.namelist():
            with z.open(name) as f:
                log_text += f.read().decode(errors="ignore") + "\n"

    return log_text
