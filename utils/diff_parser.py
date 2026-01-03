from typing import Dict, List
import re

def extract_diff_code(diff_text: str) -> List[Dict]:
    current_file = None
    added_lines = []
    removed_lines = []
    files = []
    
    for line in diff_text.splitlines():
        if line.startswith('diff --git'):
            if current_file:
                files.append({
                    'file': current_file,
                    'added_code': '\n'.join(added_lines),
                    'removed_code': '\n'.join(removed_lines)
                })
                added_lines = []
                removed_lines = []
        elif line.startswith('+++'):
            current_file = line.split('b/')[-1]
        elif line.startswith('+') and not line.startswith('+++'):
            added_lines.append(line[1:])
        elif line.startswith('-') and not line.startswith('---'):
            removed_lines.append(line[1:])
    
    if current_file:
        files.append({
            'file': current_file,
            'added_code': '\n'.join(added_lines),
            'removed_code': '\n'.join(removed_lines)
        })
    
    return files