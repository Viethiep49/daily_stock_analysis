import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

# Additional comment translations
COMMENT_FIXES = {
    '验证字段顺序': 'Verify field order',
    '应该能成功序列化为 JSON': 'Should serialize to JSON successfully',
    '应该能成功反序列化': 'Should deserialize successfully',
    '创建Test CSV 文件': 'Create test CSV file',
    '加载数据': 'Load data',
    '验证数据': 'Verify data',
    '构建索引': 'Build index',
    '验证索引': 'Verify index',
    '压缩索引': 'Compress index',
    '验证压缩': 'Verify compression',
    '验证字段数量': 'Verify field count',
    '创建Test数据': 'Create test data',
    '统计市场 points布': 'Count market distribution',
    '验证统计': 'Verify statistics',
    'Test ST 前缀去除': 'Test ST prefix removal',
    'Test N 前缀去除': 'Test N prefix removal',
    '注意：这个Test需要 pypinyin 可用': 'Note: This test requires pypinyin to be available',
    '插入5days data': 'Insert 5 days of data',
    'Please求2days data': 'Request 2 days of data',
    'Please求5days data': 'Request 5 days of data',
    '插入3days data': 'Insert 3 days of data',
    '验证日期降序（最新日期在前）': 'Verify date descending (latest date first)',
    '插入不同股票的数据': 'Insert data for different stocks',
    '重置配置与数据库单例，确保Use临时库': 'Reset config and DB singleton, ensure use of temp DB',
    'Safe guardTest，避免无限循环，抛出错误': 'Safe guard test, avoid infinite loop, throw error',
    'Simulation Stooq 返回的 CSV 格式数据（实时 + 日线历史）': 'Simulate Stooq CSV format data (realtime + daily history)',
    'Simulation yfinance 完全失效': 'Simulate yfinance completely failing',
    'Simulation fast_info 属性访问抛出异常': 'Simulate fast_info attribute access throwing exception',
    'Simulation history 返回空': 'Simulate history returning empty',
    'Simulation Stooq 成功返回': 'Simulate Stooq successful return',
    '正常数Value': 'Normal numeric value',
    '包含Medium文描述和': 'Contains Chinese description and',
    '包含干扰数字（修复的Bug场景）': 'Contains noise digits (fixed bug scenario)',
    '之前 "MA5" 会被错误提取为 5.0，现在应该提取 "Yuan" 前面的 100': 'Previously "MA5" was incorrectly extracted as 5.0, now should extract 100 before "Yuan"',
    '更多干扰场景': 'More noise scenarios',
    '当前逻辑是找最后一个冒号，然后找之后的第一个"Yuan"，提取Medium间的数字。': 'Current logic finds the last colon, then finds the first "Yuan" after it, extracting the number in between.',
    'Test没有冒号的情况': 'Test case without colon',
    'Test多个数字在"Yuan"之前': 'Test multiple numbers before "Yuan"',
    '无效输入': 'Invalid input',
    '回归：括号内技术指标数字不应被提取': 'Regression: Technical indicator numbers in parentheses should not be extracted',
    '验证正确Value在区间内': 'Verify correct value is within range',
    '确保能导入 data_provider 模块（直接导入避免加载重量级依赖）': 'Ensure data_provider module can be imported (direct import avoids loading heavy dependencies)',
    '在导入 data_provider 前 mock 可能缺失的依赖，避免环境差异导致Test无法运行': 'Mock possibly missing dependencies before importing data_provider, avoid test failures due to env differences',
    '确保能导入项目模块': 'Ensure project modules can be imported',
    'ST 前缀去除': 'ST prefix removal',
    'N 前缀去除': 'N prefix removal',
    # From test_storage.py
    '建议在': 'Suggested at',
    '价格': 'price',
    '无法给出': 'Unable to provide',
    '需等待': 'Need to wait',
    '数据恢复': 'data recovery',
    '在股价回踩': 'when stock price pulls back',
    '且乖离率': 'and bias rate',
    '时考虑': 'consider when',
    '支撑位': 'Support level',
    '阻力位': 'Resistance level',
    '应该提取最后一个': 'Should extract the last',
    '前面的数字': 'number before',
    '即': 'i.e.',
    '或者更复杂的逻辑': 'or more complex logic',
    '下方': 'Below',
    '支撑': 'support',
    '前期': 'Previous',
    '点阻力': 'point resistance',
    '没有数字': 'No numbers',
    '但没有': 'but no',
    '回踩': 'Pullback',
    '企稳': 'Stabilize',
}

files_changed = 0
total_fixes = 0

for root, dirs, files in os.walk('tests'):
    for f in sorted(files):
        if not f.endswith('.py'):
            continue
        path = os.path.join(root, f)
        content = open(path, encoding='utf-8').read()
        original = content
        lines = content.split('\n')
        new_lines = []

        for line in lines:
            new_line = line
            stripped = line.strip()
            if stripped.startswith('#'):
                # This is a comment - apply comment fixes
                for zh, en in COMMENT_FIXES.items():
                    if zh in new_line:
                        new_line = new_line.replace(zh, en)
            new_lines.append(new_line)

        content = '\n'.join(new_lines)
        if content != original:
            open(path, 'w', encoding='utf-8').write(content)
            files_changed += 1
            changes = sum(1 for a, b in zip(original.split('\n'), content.split('\n')) if a != b)
            total_fixes += changes
            print(f'  {f}: {changes} comments fixed')

print(f'\nTotal: {files_changed} files, {total_fixes} comments fixed')
