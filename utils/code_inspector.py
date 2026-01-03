from typing import Set
import re

def extract_definitions(code: str) -> Set[str]:
    return set(re.findall(r"^\s*(?:def|class)\s+([a-zA-Z_]\w*)", code, re.MULTILINE))

def extract_calls(code: str) -> Set[str]:
    return set(re.findall(r"\b([a-zA-Z_]\w*)\s*\(", code))

def extract_imports(code: str) -> Set[str]:
    imports = set()
    for match in re.findall(r'^\s*from\s+\S+\s+import\s+(.+)', code, re.MULTILINE):
        names = match.replace('(', '').replace(')', '').split(',')
        for n in names:
            imports.add(n.strip().split(' as ')[0])

    for match in re.findall(r'^\s*import\s+(\S+)', code, re.MULTILINE):
        imports.add(match.split(' as ')[0].split('.')[0])
    
    return imports

def detect_context_gaps(code: str) -> bool:
    defined = extract_definitions(code)
    calls = extract_calls(code)
    imports = extract_imports(code)
    
    BUILTINS = {
        "print", "len", "range", "str", "int", "float", "list", "dict", "set",
        "tuple", "open", "sum", "min", "max", "map", "filter", "zip", "enumerate"
    }

    gaps = {c for c in calls if c not in defined and c not in BUILTINS and c not in imports}

    if gaps:
        return True
    if re.search(r'^\s*@\w+', code, re.MULTILINE):
        return True
    if re.search(r'^\s*class\s+', code, re.MULTILINE):
        return True
    if len(code.splitlines()) > 100:
        return True
    
    return False