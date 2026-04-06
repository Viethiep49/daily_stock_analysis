import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

# Find mixed Chinese-English strings that might be broken translations
broken = []
for root, dirs, files in os.walk('tests'):
    for f in sorted(files):
        if not f.endswith('.py'):
            continue
        path = os.path.join(root, f)
        content = open(path, encoding='utf-8').read()
        for i, line in enumerate(content.split('\n')):
            # Find string literals with mixed CJK and ASCII letters
            for m in re.finditer(r'["\']([^"\']*[\u4e00-\u9fff][^"\']*)["\']', line):
                text = m.group(1)
                if re.search(r'[a-zA-Z]{3,}', text) and re.search(r'[\u4e00-\u9fff]', text):
                    # Skip if it's a stock name pattern or clearly intentional
                    if text in ('贵州茅台', '平安银行', '腾讯控股', '阿里巴巴', '宁德时代',
                               '大秦铁路', '江波龙', '五粮液', '浦发银行', '科创芯片',
                               '苹果', '茅台', '西安奕材'):
                        continue
                    broken.append((f, i+1, text))

for f, line, text in broken:
    print(f'{f}:{line}: {text}')
print(f'\nTotal potentially broken: {len(broken)}')
