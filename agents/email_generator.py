import json
import google.generativeai as genai
from pydantic import BaseModel

class EmailResult(BaseModel):
    subject: str
    body: str
    type: str  # "invite" or "rejection"

class EmailGenerator:
    def __init__(self, config: dict):
        genai.configure(api_key=config["gemini_key"])
        self.model = genai.GenerativeModel('gemini-2.5-pro')

    def _build_prompt(self, candidate: dict, jd: dict, ranking: dict) -> str:
        decision = "invite" if ranking["score"] >= 75 else "rejection"

        return f"""
You are an assistant generating professional emails for recruiters.

Create an email for a candidate based on this data:

CANDIDATE:
{json.dumps(candidate, indent=2)}

JOB ROLE:
{jd.get('role', 'N/A')}

SCORE: {ranking['score']}
DECISION: {decision}

Guidelines:
- If decision is "invite", write a polite interview invitation email.
- If decision is "rejection", write a polite rejection email.
- Keep tone formal and concise.
- Output JSON ONLY in this format:

{{
  "subject": "...",
  "body": "...",
  "type": "{decision}"
}}
"""

    def generate(self, candidate: dict, jd: dict, ranking: dict) -> EmailResult:
        prompt = self._build_prompt(candidate, jd, ranking)

        response = self.model.generate_content(prompt)
        text = response.text.strip()

        try:
            data = json.loads(text)
        except Exception:
            clean_text = text[text.find("{"): text.rfind("}") + 1]
            data = json.loads(clean_text)

        return EmailResult(**data)
