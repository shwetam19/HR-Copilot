import json
import google.generativeai as genai
from pydantic import BaseModel

class JDAnalysisResult(BaseModel):
    role: str
    skills: list
    tools: list
    experience_years: int
    soft_skills: list

class JDAnalyzer:
    def __init__(self, config: dict):
        """
        Initialize JD Analyzer with Gemini Pro configuration.
        """
        genai.configure(api_key=config["gemini_key"])
        
        self.model = genai.GenerativeModel('gemini-2.5-pro')

    def _build_prompt(self, jd_text: str) -> str:
        return f"""
You are an expert at analyzing job descriptions.
Given the job description text below, extract:

1. Role/Position
2. Top 10 hard skills
3. Tools/Frameworks/Technologies
4. Minimum years of experience (if mentioned, else estimate)
5. Soft skills (teamwork, communication, leadership, etc.)

Return ONLY valid JSON in this format:

{{
  "role": "...",
  "skills": ["skill1", "skill2"],
  "tools": ["tool1", "tool2"],
  "experience_years": 0,
  "soft_skills": ["soft1", "soft2"]
}}

JOB DESCRIPTION:
{jd_text}
"""

    def analyze(self, jd_text: str) -> JDAnalysisResult:
        """
        Analyze job description and return structured result.
        """
        prompt = self._build_prompt(jd_text)

        # Generate content using the Gemini 2.5 Pro model
        response = self.model.generate_content(prompt)
        text = response.text.strip()

        # Parse the JSON output
        try:
            data = json.loads(text)
        except Exception:
            # Fallback if model returns extra explanation
            clean_text = text[text.find("{"): text.rfind("}") + 1]
            data = json.loads(clean_text)

        return JDAnalysisResult(**data)
