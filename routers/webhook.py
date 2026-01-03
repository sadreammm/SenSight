from fastapi import APIRouter, Request
import json
from typing import Dict
from services.github_service import GitHubService
from services.context_service import ContextService
from services.code_analysis_service import CodeAnalysisService
from services.ai_service import AIService
from utils.diff_parser import extract_diff_code
from utils.code_inspector import detect_context_gaps

router = APIRouter()

github_service = GitHubService()
context_service = ContextService(github_service)
analysis_service = CodeAnalysisService()
ai_service = AIService()

@router.post("/webhook/github")
async def github_webhook(request: Request):
    payload = await request.body()
    event = json.loads(payload)
    
    pr_data = extract_pr_data(event)
    task_context = context_service.extract_task_context(pr_data)
    
    diff_text = github_service.get_diff(pr_data.get('diff_url'))
    files = extract_diff_code(diff_text)
    
    analyzed_files = analyze_files(files, pr_data)
    all_issues = collect_issues(analyzed_files)
    ai_review = ai_service.review_code(analyzed_files, task_context, all_issues, pr_data)
    post_status = github_service.post_comment(pr_data.get('url', ''), ai_review)
    if post_status != 201:
        ai_review += "\n\n*Note: Failed to post comment on GitHub.*"
        return {"status": "failed_to_post_comment", "ai_review": ai_review}
    return {
        "status": "received",
        "pr_data": pr_data,
        "task_context": task_context,
        "files_analyzed": len(analyzed_files),
        "context_decisions": {f['file']: f['context_type'] for f in analyzed_files},
        "ai_review": ai_review
    }

def extract_pr_data(event: Dict) -> Dict:
    pr_data = {}
    if event.get('action') in ['opened', 'synchronize']:
        pr = event.get('pull_request', {})
        pr_data = {
            "author": pr.get('user', {}).get('login'),
            "number": pr.get('number'),
            "url": pr.get('url'),
            "diff_url": pr.get('diff_url'),
            "repo_url": pr.get('base', {}).get('repo', {}).get('url'),
            "branch": pr.get('head', {}).get('ref'),
            "title": pr.get('title', ''),
            "body": pr.get('body', '')
        }
    return pr_data

def analyze_files(files, pr_data: Dict):
    analyzed_files = []
    for file_diff in files:
        need_full_context = detect_context_gaps(file_diff['added_code'])
        if need_full_context:
            file_content = github_service.get_full_file(
                pr_data.get('repo_url', ''),
                pr_data.get('branch', 'main'),
                file_diff.get('file', '')
            )
            file_diff['full_content'] = file_content
            file_diff['context_type'] = 'full'
        else:
            file_diff['context_type'] = 'diff'
        analyzed_files.append(file_diff)
    return analyzed_files

def collect_issues(analyzed_files):
    all_issues = []
    for file_diff in analyzed_files:
        code = file_diff.get('full_content') or file_diff.get('added_code', '')
        if code:
            issues = analysis_service.static_analysis(code)
            all_issues.extend(issues)
    return all_issues