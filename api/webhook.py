from fastapi import FastAPI, Request, BackgroundTasks
from core.agent_loop import agentic_heal
from utils.github_logs import fetch_workflow_logs
import os

app = FastAPI()

processed_runs = set()
REPO = os.getenv("GITHUB_REPO")

def process_failure(run_id: int):
    if run_id in processed_runs:
        print(f"Skipping duplicate run {run_id}")
        return

    processed_runs.add(run_id)

    print(f"📥 Fetching logs for run {run_id}")
    logs = fetch_workflow_logs(REPO, run_id)

    agentic_heal(logs)

@app.post("/github/webhook")
async def github_webhook(req: Request, background_tasks: BackgroundTasks):
    payload = await req.json()

    action = payload.get("action")
    run = payload.get("workflow_run", {})

    if action == "completed" and run.get("conclusion") == "failure":
        run_id = run.get("id")
        background_tasks.add_task(process_failure, run_id)

    return {"status": "received"}
