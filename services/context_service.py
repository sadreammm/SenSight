from typing import Dict, List
import re
from services.github_service import GitHubService

class ContextService:
    def __init__(self, github_service: GitHubService):
        self.github_service = github_service
    
    def extract_task_context(self, pr_data: Dict) -> Dict:
        task_info = {
            "pr_title": pr_data.get('title', ''),
            "pr_description": pr_data.get('body', ''),
            "linked_issues": [],
            "task_type": None,
            "requirements": []
        }
        
        pr_body = pr_data.get('body', '')
        if pr_body:
            issue_pattern = r'(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#(\d+)'
            issues = re.findall(issue_pattern, pr_body, re.IGNORECASE)
            task_info['linked_issues'] = issues
            
            if issues and pr_data.get('repo_url'):
                for issue_num in issues:
                    issue_details = self.github_service.get_issue_details(
                        pr_data['repo_url'], issue_num
                    )
                    if issue_details:
                        task_info['requirements'].append(issue_details)
        
        title_lower = task_info['pr_title'].lower()
        if any(word in title_lower for word in ['fix', 'bug', 'resolve']):
            task_info['task_type'] = 'bugfix'
        elif any(word in title_lower for word in ['feature', 'add', 'implement']):
            task_info['task_type'] = 'feature'
        elif any(word in title_lower for word in ['refactor', 'improve', 'optimize']):
            task_info['task_type'] = 'refactor'
        
        return task_info