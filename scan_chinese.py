import os, re

def contains_chinese(text):
    return bool(re.search(r'[\u4e00-\u9fff]', text))

for root, _, files in os.walk('.'):
    if '.git' in root or '.agent' in root or '__pycache__' in root or 'node_modules' in root:
        continue
    for file in files:
        if not file.endswith(('.py', '.md', '.txt', '.yaml', '.yml', '.env.example', '.json')):
            continue
        filepath = os.path.join(root, file)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                if contains_chinese(content):
                    print(filepath)
        except Exception:
            pass
