from core.agent_loop import agentic_heal

with open("test_logs.txt") as f:
    logs = f.read()

result = agentic_heal(logs)
print(result)
