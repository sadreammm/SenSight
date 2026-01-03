import google.generativeai as genai
import json
from typing import Dict, List
from config.settings import settings
from models.database import CodeReview, SessionLocal

genai.configure(api_key=settings.GEMINI_API_KEY)

class AIService:
    def __init__(self):
        self.model_name = "gemini-2.5-flash"
    
    def run_llm_review(self, prompt: str) -> str:
        model = genai.GenerativeModel(self.model_name)
        response = model.generate_content(prompt)
        return response.text
    
    def create_prompt(
        self,
        files_context: List[Dict],
        task_context: Dict,
        static_issues: List[Dict]
    ) -> str:
        prompt = f"""
        You are reviewing a GitHub Pull Request.

        ### Task Context
        {json.dumps(task_context, indent=2)}

        ### Code Changes
        {json.dumps(files_context, indent=2)}

        ### Static Analysis Findings
        {json.dumps(static_issues, indent=2)}

        ### Instructions
        - Identify bugs, security issues, and design problems
        - Check alignment with task requirements
        - Suggest concrete improvements
        - Be concise and professional
        """
        return prompt
    
    def save_review(
        self,
        pr_data: Dict,
        task_context: Dict,
        files_context: List[Dict],
        static_issues: List[Dict],
        ai_review: str
    ):
        session = SessionLocal()
        review = CodeReview(
            repo=pr_data.get('repo_url', ''),
            pr_number=pr_data.get('number', 0),
            pr_data={
                "pr_data": pr_data,
                "task_context": task_context,
                "files_context": files_context,
                "static_issues": static_issues,
                "ai_review": {
                    "model": self.model_name,
                    "version": "1.0",
                    "review_text": ai_review
                }
            }
        )
        session.add(review)
        session.commit()
        session.close()
    
    def review_code(
        self,
        files_context: List[Dict],
        task_context: Dict,
        static_issues: List[Dict],
        pr_data: Dict
    ) -> str:
        prompt = self.create_prompt(files_context, task_context, static_issues)
        ai_review = self.run_llm_review(prompt)
        self.save_review(pr_data, task_context, files_context, static_issues, ai_review)
        return ai_review