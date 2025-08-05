import json
import google.generativeai as genai
from pydantic import BaseModel
import re

class CandidateScoreResult(BaseModel):
    score: int
    summary: str

class CandidateRanker:
    def __init__(self, config: dict):
        genai.configure(api_key=config["gemini_key"])
        self.model = genai.GenerativeModel('gemini-2.5-pro')

    def _build_prompt(self, jd: dict, resume: dict) -> str:
        """
        Builds a highly constrained prompt to force the model to output a single, valid JSON object.
        """
        return f"""
You are a hiring evaluator AI. Your task is to analyze a candidate's resume against a job description.

**Instructions:**
1.  Assign a suitability score out of 100, where 100 is a perfect match.
2.  Provide a 3-4 sentence explanation for the score. The explanation should be a concise summary of the key matching and non-matching points.
3.  Focus your analysis on: skills, relevant projects, experience, and education.
4.  **Crucially, return ONLY a single JSON object. Do not include any other text, conversation, or markdown wrappers like ```json```.**

**Job Description (JD):**
{json.dumps(jd, indent=2)}

**Candidate Resume:**
{json.dumps(resume, indent=2)}

**Output Format (STRICTLY):**
{{
  "score": 0,
  "summary": "Your detailed explanation here."
}}
"""

    def rank(self, jd_data: dict, resume_data: dict) -> CandidateScoreResult:
        prompt = self._build_prompt(jd_data, resume_data)
        
        try:
            # The safety settings are added to potentially reduce the model's
            # tendency to add extra text or conversational elements.
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json"
                ),
                safety_settings={
                    'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
                    'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
                    'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE',
                    'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
                }
            )
            text = response.text.strip()
            
            # Use regex to find and extract the JSON object robustly
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                clean_text = json_match.group(0)
            else:
                raise ValueError("Could not find a JSON object in the model's response.")
                
            data = json.loads(clean_text)
            return CandidateScoreResult(**data)
            
        except Exception as e:
            print(f"An error occurred during ranking: {e}")
            # Return a default error result or re-raise the exception
            return CandidateScoreResult(score=0, summary="Error processing model response.")