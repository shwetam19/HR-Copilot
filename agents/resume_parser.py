import json
import pdfplumber
import google.generativeai as genai
from pydantic import BaseModel
import os
from typing import List, Dict

class ResumeParseResult(BaseModel):
    name: str
    email: str
    phone: str
    skills: List[str]
    education: List[str]
    experience: List[Dict]
    projects: List[Dict]

class ResumeParser:
    def __init__(self, config: dict):
        genai.configure(api_key=config["gemini_key"])
        self.model = genai.GenerativeModel('gemini-2.5-pro')

    def _extract_pdf_text(self, pdf_path: str) -> str:
        text_content = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text_content.append(page.extract_text() or "")
        return "\n".join(text_content)

    def _build_prompt(self, text: str) -> str:
        return f"""
You are a resume parser AI. Extract the following from the resume text:

1. Full Name
2. Email
3. Phone Number
4. Skills (technical skills only)
5. Education details
6. Work experience (company, role, duration)
7. Projects (list title and a 1-line description for each project)

Return ONLY valid JSON:

{{
  "name": "...",
  "email": "...",
  "phone": "...",
  "skills": ["..."],
  "education": ["..."],
  "experience": [
    {{"company": "...", "role": "...", "duration": "..."}}
  ],
  "projects": [
    {{"title": "...", "description": "..."}}
  ]
}}

RESUME TEXT:
{text}
"""

    def parse(self, pdf_path: str) -> ResumeParseResult:
        resume_text = self._extract_pdf_text(pdf_path)
        prompt = self._build_prompt(resume_text)

        response = self.model.generate_content(prompt)
        text = response.text.strip()

        try:
            data = json.loads(text)
        except Exception:
            clean_text = text[text.find("{"): text.rfind("}") + 1]
            data = json.loads(clean_text)

        return ResumeParseResult(**data)
    

