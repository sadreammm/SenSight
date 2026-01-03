import subprocess
import tempfile
import json
import os
from typing import List, Dict

class CodeAnalysisService:
    @staticmethod
    def static_analysis(code: str) -> List[Dict]:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
            temp_file.write(code.encode())
            file_path = temp_file.name

        security_issues = CodeAnalysisService._security_analysis(file_path)
        quality_issues = CodeAnalysisService._quality_analysis(file_path)
        issues = security_issues + quality_issues
        os.unlink(file_path)
        return issues
    
    @staticmethod
    def _security_analysis(file_path: str) -> List[Dict]:
        result = subprocess.run(
            ['bandit', '-f', 'json', file_path],
            capture_output=True,
            text=True
        )

        if result.stdout:
            results = json.loads(result.stdout)['results']
            return [
                {
                    'type': "security_issue",
                    'message': r["issue_text"],
                    'severity': r["issue_severity"],
                    'line': r["line_number"]
                }
                for r in results
            ]
        return []
    
    @staticmethod
    def _quality_analysis(file_path: str) -> List[Dict]:
        result = subprocess.run(
            ['pylint', file_path, "--output-format=json"],
            capture_output=True,
            text=True
        )

        if result.stdout:
            results = json.loads(result.stdout)
            return [
                {
                    'type': "code_quality_issue",
                    'message': r["message"],
                    'severity': r["type"],
                    'line': r["line"]
                }
                for r in results
            ]
        return []