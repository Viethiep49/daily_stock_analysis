import os
import re
import sys

pattern = re.compile(r'[\u4e00-\u9fff]')

def check_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines, 1):
                if pattern.search(line):
                    print(f"{filepath} -> {i}: {line.rstrip()}")
    except Exception as e:
        pass

def main():
    for root, dirs, files in os.walk('.'):
        # Exclude node_modules and .git
        dirs[:] = [d for d in dirs if d not in ['node_modules', '.git']]
        for file in files:
            if file.endswith(('.js', '.ts', '.tsx', '.jsx')):
                filepath = os.path.join(root, file)
                check_file(filepath)

if __name__ == '__main__':
    main()
