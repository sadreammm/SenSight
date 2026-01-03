import requests
from typing import Optional, Dict
from config.settings import settings

class GitHubService:
    def __init__(self):
        self.headers = {
            'Authorization': f'token {settings.ACCESS_TOKEN}',
            'Accept': 'application/vnd.github.v3+json'
        }
    
    def get_issue_details(self, repo_url: str, issue_number: str) -> Optional[Dict]:
        issue_url = f"{repo_url}/issues/{issue_number}"
        response = requests.get(issue_url, headers=self.headers)
        
        if response.status_code == 200:
            issue = response.json()
            return {
                "number": issue.get('number'),
                "title": issue.get('title'),
                "body": issue.get('body'),
                "labels": [label['name'] for label in issue.get('labels', [])]
            }
        return None
    
    def get_diff(self, url: str) -> str:
        diff_headers = {
            'Authorization': f'Token {settings.ACCESS_TOKEN}',
            'Accept': 'application/vnd.github.v3.diff'
        }
        response = requests.get(url, headers=diff_headers)
        return response.text
    
    def get_full_file(self, repo_url: str, branch: str, file_path: str) -> str:
        raw_headers = {
            'Authorization': f'token {settings.ACCESS_TOKEN}',
            'Accept': 'application/vnd.github.v3.raw'
        }
        contents_url = f"{repo_url}/contents/{file_path}?ref={branch}"
        response = requests.get(contents_url, headers=raw_headers)
        
        if response.status_code == 200:
            return response.text
        return ""
    
    def post_comment(self, pr_url: str, comment: str) -> int:
        comments_url = f"{pr_url}/comments"
        headers = {
            'Authorization': f'token {settings.ACCESS_TOKEN}',
            'Accept': 'application/vnd.github.v3+json'
        }
        data = {"body": comment}
        response = requests.post(comments_url, json=data, headers=headers)
        return response.status_code