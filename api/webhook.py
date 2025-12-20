from fastapi import FastAPI, Request
from core.agent_loop import agentic_heal

app = FastAPI()

@app.post("/github/webhook")
async def github_webhook(req: Request):
    payload = await req.json()

    if payload["workflow_run"]["conclusion"] == "failure":
        logs = "Mock CI logs for now"
        result = agentic_heal(logs)
        return {"status": result}

    return {"status": "ignored"}
