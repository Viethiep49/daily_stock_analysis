# -*- coding: utf-8 -*-
"""Replace Chinese in .py comments/docstrings/logs with English translations."""
import os
import re
import sys

RE_CN = re.compile(r'[\u4e00-\u9fff]')

SKIP_DIRS = {'.git', '__pycache__', 'node_modules', '.agent', 'venv', '.venv'}
PY_DIRS = ['src', 'bot', 'api', 'data_provider', 'tests', 'scripts']

def has_cn(s):
    return bool(RE_CN.search(s))

def is_comment(line):
    s = line.lstrip()
    return s.startswith('#')

def is_logger_or_print(line):
    s = line.strip()
    return bool(re.match(r'(logger|log)\.(info|warning|error|debug|critical)\(', s)) or s.startswith('print(')

def in_docstring_context(lines, idx):
    """Simple heuristic: check if line is likely inside a docstring."""
    # Check if line is triple-quoted
    line = lines[idx].strip()
    if line.startswith(('"""', "'''")):
        return True
    # Check if we're between two triple-quote markers
    count_before = 0
    for i in range(idx):
        count_before += lines[i].count('"""') + lines[i].count("'''")
    return count_before % 2 == 1

TRANSLATE = {
    # Common phrases found in this project (Chinese -> English)
    "\u914d\u7f6e": "config",
    "\u73af\u5883\u53d8\u91cf": "env var",
    "\u9ed8\u8ba4\u503c": "default",
    "\u5fc5\u586b": "required",
    "\u53ef\u9009": "optional",
    "\u542f\u7528": "enable",
    "\u7981\u7528": "disable",
    "\u83b7\u53d6\u6570\u636e": "fetch data",
    "\u6570\u636e\u6e90": "data source",
    "\u6570\u636e\u83b7\u53d6": "data fetch",
    "\u83b7\u53d6\u5931\u8d25": "fetch failed",
    "\u5206\u6790": "analysis",
    "\u5f00\u59cb\u5206\u6790": "start analysis",
    "\u5b8c\u6210\u5206\u6790": "analysis complete",
    "\u5206\u6790\u5b8c\u6210": "analysis done",
    "\u5206\u6790\u5931\u8d25": "analysis failed",
    "\u6b63\u5728\u5206\u6790": "analyzing",
    "\u8df3\u8fc7": "skip",
    "\u901a\u77e5": "notification",
    "\u63a8\u9001": "push",
    "\u53d1\u9001": "send",
    "\u53d1\u9001\u5931\u8d25": "send failed",
    "\u53d1\u9001\u6210\u529f": "send success",
    "\u6d88\u606f": "message",
    "\u80a1\u7968": "stock",
    "\u81ea\u9009\u80a1": "watchlist",
    "\u4ee3\u7801": "code",
    "\u540d\u79f0": "name",
    "\u884c\u60c5": "quote",
    "\u5b9e\u65f6\u884c\u60c5": "realtime quote",
    "\u5927\u76d8": "market",
    "\u5e02\u573a": "market",
    "\u677f\u5757": "sector",
    "\u6da8\u8dcc": "change",
    "\u6280\u672f\u6307\u6807": "technical indicator",
    "\u5747\u7ebf": "moving average",
    "\u6210\u4ea4\u91cf": "volume",
    "\u4ef7\u683c": "price",
    "\u62a5\u544a": "report",
    "\u751f\u6210\u62a5\u544a": "generate report",
    "\u9519\u8bef": "error",
    "\u5f02\u5e38": "exception",
    "\u5931\u8d25": "failed",
    "\u6210\u529f": "success",
    "\u91cd\u8bd5": "retry",
    "\u8d85\u65f6": "timeout",
    "\u5f00\u59cb": "start",
    "\u7ed3\u675f": "end",
    "\u5b8c\u6210": "complete",
    "\u521d\u59cb\u5316": "initialize",
    "\u52a0\u8f7d": "load",
    "\u89e3\u6790": "parse",
    "\u8fd4\u56de": "return",
    "\u672a\u627e\u5230": "not found",
    "\u4e0d\u652f\u6301": "not supported",
    "\u68c0\u67e5": "check",
    "\u9a8c\u8bc1": "validate",
    "\u66f4\u65b0": "update",
    "\u5220\u9664": "delete",
    "\u521b\u5efa": "create",
    "\u5904\u7406": "process",
    "\u7b49\u5f85": "wait",
    "\u6267\u884c": "execute",
    "\u8fd0\u884c": "run",
    "\u505c\u6b62": "stop",
    "\u542f\u52a8": "start",
    "\u5173\u95ed": "close",
    "\u8fde\u63a5": "connect",
    "\u5df2\u5b58\u5728": "already exists",
    "\u4e0d\u5b58\u5728": "does not exist",
    "\u8bbe\u7f6e": "setting",
    "\u53c2\u6570": "parameter",
    "\u5f00\u5173": "switch",
    "\u5207\u6362": "switch",
    "\u8bf7\u6c42": "request",
    "\u54cd\u5e94": "response",
    "\u8d85\u8fc7": "exceed",
    "\u4e0d\u8db3": "insufficient",
    "\u65e0\u6548": "invalid",
    "\u6709\u6548": "valid",
    "\u8b66\u544a": "warning",
    "\u4fe1\u606f": "info",
    "\u8c03\u8bd5": "debug",
    "\u4e25\u91cd": "critical",
    "\u8fde\u63a5\u5931\u8d25": "connection failed",
    "\u65e0\u6cd5\u8fde\u63a5": "cannot connect",
    "\u8bbf\u95ee": "access",
    "\u6743\u9650": "permission",
    "\u8d8d\u9a8c": "verify",
    "\u7f13\u5b58": "cache",
    "\u547d\u4e2d": "hit",
    "\u672a\u547d\u4e2d": "miss",
    "\u5df2\u8fc7\u671f": "expired",
    "\u6b63\u5e38": "ok",
    "\u5f02\u5e38": "abnormal",
    "\u62a5\u9519": "error reported",
}

def translate_text(text):
    """Replace known Chinese phrases with English."""
    result = text
    for zh, en in TRANSLATE.items():
        result = result.replace(zh, en)
    return result

def process_file(fpath, dry_run=False):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    if not has_cn(content):
        return False

    lines = content.split('\n')
    new_lines = []
    changed = False

    for i, line in enumerate(lines):
        if not has_cn(line):
            new_lines.append(line)
            continue

        # Check if this line should be translated
        should_translate = is_comment(line) or is_logger_or_print(line) or in_docstring_context(lines, i)

        if should_translate:
            new_line = translate_text(line)
            if new_line != line:
                changed = True
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    if changed and not dry_run:
        # Backup
        bak = fpath + '.bak'
        if not os.path.exists(bak):
            with open(bak, 'w', encoding='utf-8') as f:
                f.write(content)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))

    return changed

def main():
    root = sys.argv[1] if len(sys.argv) > 1 else '.'
    dry_run = '--dry-run' in sys.argv

    root = os.path.abspath(root)
    # Handle encoding for Windows console
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    print(f"Root: {root}")
    print(f"Dry run: {dry_run}")
    print()

    total = 0
    modified = 0

    for dir_name in PY_DIRS:
        dir_path = os.path.join(root, dir_name)
        if not os.path.isdir(dir_path):
            continue
        for r, dirs, files in os.walk(dir_path):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for fname in files:
                if not fname.endswith('.py'):
                    continue
                fpath = os.path.join(r, fname)
                total += 1
                if process_file(fpath, dry_run):
                    rel = os.path.relpath(fpath, root)
                    print(f"  {'WOULD MODIFY' if dry_run else 'MODIFIED'}: {rel}")
                    modified += 1

    # Also check main.py and server.py
    for extra in ['main.py', 'server.py']:
        fpath = os.path.join(root, extra)
        if os.path.isfile(fpath):
            total += 1
            if process_file(fpath, dry_run):
                rel = os.path.relpath(fpath, root)
                print(f"  {'WOULD MODIFY' if dry_run else 'MODIFIED'}: {rel}")
                modified += 1

    print(f"\nDone: {modified}/{total} files {'would be' if dry_run else ''} modified")

if __name__ == '__main__':
    main()
