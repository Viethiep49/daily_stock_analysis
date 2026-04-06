import os
import re

pattern = re.compile(r'[\u4e00-\u9fff]')
results = []

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for i, line in enumerate(lines, 1):
                        if pattern.search(line):
                            results.append(f'{filepath} -> {i}: {line.rstrip()}')
            except:
                pass

with open('chinese_chars_in_python.txt', 'w', encoding='utf-8') as out:
    out.write('\n'.join(results))
print(f'Total matches: {len(results)}')
unique_files = len(set(r.split(' -> ')[0] for r in results))
print(f'Unique files: {unique_files}')
