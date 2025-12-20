import os
import json
import re
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found")

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-2.5-flash"


def _extract_json(text: str) -> dict:
    """
    Extract JSON from Gemini output.
    Handles markdown fences and extra text safely.
    """
    # Remove ```json ``` or ``` ```
    cleaned = re.sub(r"```(?:json)?", "", text)
    cleaned = cleaned.replace("```", "").strip()

    # Extract first JSON object
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if not match:
        raise RuntimeError(f"No JSON found in Gemini output:\n{text}")

    return json.loads(match.group())


def diagnose(error_log: str) -> dict:
    prompt = f"""
You are an autonomous CI/CD self-healing agent.

CI FAILURE LOG:
{error_log}

Identify the root cause and suggest a minimal fix.

Respond ONLY with valid JSON (no explanations).

Schema:
{{
  "category": "dependency_error | syntax_error | test_failure",
  "confidence": 0.0,
  "fix": {{
    "file": "",
    "action": "add | replace",
    "content": ""
  }}
}}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    raw_text = response.text.strip()

    return _extract_json(raw_text)
