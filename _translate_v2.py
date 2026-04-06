import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

# Careful translations - only for comments and docstrings
# Order matters: longer phrases first to avoid partial replacements
TRANSLATIONS = [
    # Long phrases first
    ('A股自选股智能分析系统', 'A-Share Watchlist Smart Analysis System'),
    ('分析历史存储单元测试', 'Analysis History Storage Unit Tests'),
    ('验证分析历史保存逻辑', 'Verify analysis history save logic'),
    ('验证上下文快照保存开关', 'Verify context snapshot save toggle'),
    ('提供单元测试包结构', 'Provide unit test package structure'),
    ('统一测试模块入口', 'Unified test module entry point'),
    ('删除历史记录时应一并清理关联回测结果。', 'Should also clean up associated backtest results when deleting history records.'),
    ('保存一条测试历史记录并返回主键 ID。', 'Save a test history record and return the primary key ID.'),
    ('为每个用例初始化独立数据库', 'Initialize independent database for each test case'),
    ('未找到保存的历史记录', 'Saved history record not found'),
    ('保存历史记录并写入上下文快照', 'Save history record and write context snapshot'),
    ('关闭快照保存时不写入 context_snapshot', 'Do not write context_snapshot when snapshot saving is disabled'),
    ('构造分析结果', 'Build analysis result'),
    ('分析历史存储测试', 'Analysis history storage test'),
    ('清理资源', 'Clean up resources'),
    ('基本信息稳健，短期震荡', 'Fundamentals are stable, short-term fluctuation'),
    ('基本面稳健，短期震荡', 'Fundamentals are stable, short-term fluctuation'),

    # Shorter phrases
    ('测试包', 'Test Package'),
    ('职责：', 'Responsibilities:'),
    ('新闻摘要', 'News summary'),

    # Sniper points
    ('理想买入点：', 'Ideal Buy Point: '),
    ('止损位：', 'Stop Loss: '),
    ('目标位：', 'Target: '),
    ('核心结论', 'Core Conclusion'),
    ('核心结论：', 'Core Conclusion:'),
    ('决策仪表盘', 'Decision Dashboard'),

    # Trend/skill terms
    ('关注中枢与背驰', 'Focus on pivot zones and divergence'),
    ('关注支撑确认', 'Focus on support confirmation'),
    ('默认多头趋势', 'Default bull trend'),
    ('多头趋势', 'Bull trend'),
    ('缠论', 'Chan Theory'),
    ('波浪理论', 'Wave Theory'),
    ('箱体震荡', 'Box Oscillation'),
    ('龙头策略', 'Dragon Head Strategy'),
    ('缩量回踩', 'Shrink Pullback'),
    ('放量突破', 'Volume Breakout'),
    ('趋势跟随', 'Trend following'),
    ('结构分析', 'Structural analysis'),
    ('趋势', 'Trend'),
    ('趋势分析', 'Trend Analysis'),
    ('缠论分析', 'Chan Theory Analysis'),
    ('轮动', 'Rotation'),
    ('龙头侦察', 'Leader Scout'),
    ('严进策略', 'Strict entry strategy'),
    ('专注于趋势交易', 'Focus on trend trading'),
    ('默认技能基线', 'Default skill baseline'),
    ('必须严格遵守', 'Must be strictly followed'),
    ('多头排列必须条件', 'Required bull arrangement conditions'),
    ('多头排列：', 'Bull arrangement: '),

    # Error messages
    ('股票代码不能为空或仅包含空白字符', 'Stock code cannot be empty or contain only whitespace'),
    ('请输入有效的股票代码或股票名称', 'Please enter a valid stock code or stock name'),
    ('最多支持', 'Maximum supported'),

    # Board/sector
    ('白酒', 'Baijiu'),
    ('行业', 'Industry'),
    ('消费', 'Consumer'),
    ('坏数据', 'Bad Data'),
    ('煤炭', 'Coal'),

    # Portfolio
    ('组合视角', 'Portfolio Perspective'),
    ('组合摘要', 'Portfolio Summary'),
    ('估值偏高', 'Overvalued'),
    ('自由文本分析', 'Free text analysis'),

    # News prompt
    ('超出近7日窗口的新闻一律忽略', 'News outside the past 7-day window must be ignored'),
    ('超出近1日窗口的新闻一律忽略', 'News outside the past 1-day window must be ignored'),
    ('超出近30日窗口的新闻一律忽略', 'News outside the past 30-day window must be ignored'),
    ('近7日的新闻搜索结果', 'News search results from the past 7 days'),
    ('近1日的新闻搜索结果', 'News search results from the past 1 day'),
    ('近30日的新闻搜索结果', 'News search results from the past 30 days'),
    ('每一条都必须带具体日期（YYYY-MM-DD）', 'Each entry must include a specific date (YYYY-MM-DD)'),
    ('时间未知、无法确定发布日期的新闻一律忽略', 'News with unknown time or undeterminable publication date must be ignored'),
    ('财报与分红（价值投资口径）', 'Financial reports and dividends (value investing perspective)'),
    ('禁止编造', 'Fabrication is prohibited'),

    # Trend analysis context
    ('当前结构是否满足激活技能的关键触发条件', 'Whether the current structure meets the key trigger conditions for activating the skill'),
    ('超过5%必须标注"严禁追高"', 'Must mark "Do not chase highs" if exceeding 5%'),
    ('MA5>MA10>MA20为多头', 'MA5>MA10>MA20 indicates bullish'),
    ('严禁追高', 'Do not chase highs'),
    ('警惕', 'Caution'),

    # Skills
    ('测试策略', 'Test Strategy'),
    ('测试YAML策略', 'Test YAML Strategy'),
    ('一个用于测试的策略', 'A strategy for testing'),
    ('最简策略', 'Minimal Strategy'),
    ('最简描述', 'Minimal description'),
    ('元数据技能', 'Metadata Skill'),
    ('带有默认元数据的技能', 'A skill with default metadata'),
    ('不完整', 'Incomplete'),
    ('自定义龙头策略', 'Custom Dragon Head Strategy'),
    ('我自己的龙头策略', 'My own dragon head strategy'),
    ('按照我的规则分析龙头股', 'Analyze leading stocks according to my rules'),
    ('别名一', 'alias_one'),
    ('别名二', 'alias_two'),
    ('自然语言', 'natural language'),

    # Log messages
    ('实时行情接口失败', 'Realtime quote API failed'),

    # Specific Chinese terms (careful not to break compounds)
    ('批量股票', 'Batch stocks'),
    ('搜索引擎', 'Search engine'),
    ('观察', 'Watch'),

    # Common terms
    ('稳健', 'Stable'),
    ('健康', 'Healthy'),
    ('分析', 'Analysis'),
    ('技能', 'Skill'),
    ('策略', 'Strategy'),
    ('测试', 'Test'),
    ('模拟', 'Simulation'),
    ('新闻', 'News'),
    ('组合', 'Portfolio'),
    ('指数', 'Index'),
    ('标普', 'S&P'),
]

def translate_comment_or_docstring(text):
    """Translate Chinese text in a comment or docstring string."""
    result = text
    for zh, en in TRANSLATIONS:
        if zh in result:
            result = result.replace(zh, en)
    return result

def process_file(filepath):
    """Process a single Python file, translating only comments and docstrings."""
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    original = content
    lines = content.split('\n')
    new_lines = []
    in_docstring = False

    for line in lines:
        new_line = line
        stripped = line.strip()

        # Detect docstring boundaries
        triple_count = stripped.count('"""')

        if triple_count >= 2:
            # Single-line docstring or opens+closes on same line
            # Translate content between the """ pairs
            parts = line.split('"""')
            translated_parts = []
            for i, part in enumerate(parts):
                if i % 2 == 1:  # Content between delimiters
                    translated_parts.append(translate_comment_or_docstring(part))
                else:
                    translated_parts.append(part)
            new_line = '"""'.join(translated_parts)
            in_docstring = False
        elif triple_count == 1:
            if not in_docstring:
                # Opening docstring
                idx = line.find('"""')
                before = line[:idx]
                after = line[idx+3:]
                new_line = before + '"""' + translate_comment_or_docstring(after)
                in_docstring = True
            else:
                # Closing docstring
                idx = line.find('"""')
                before = line[:idx]
                new_line = translate_comment_or_docstring(before) + '"""'
                in_docstring = False
        elif in_docstring:
            # Inside docstring block
            new_line = translate_comment_or_docstring(line)
        elif stripped.startswith('#'):
            # Comment line
            new_line = translate_comment_or_docstring(line)
        # else: code line - don't touch

        new_lines.append(new_line)

    new_content = '\n'.join(new_lines)

    if new_content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        changes = sum(1 for a, b in zip(original.split('\n'), new_content.split('\n')) if a != b)
        return changes
    return 0

# Process all files
files_changed = 0
total_lines = 0

for root, dirs, files in os.walk('tests'):
    for f in sorted(files):
        if not f.endswith('.py'):
            continue
        path = os.path.join(root, f)
        changes = process_file(path)
        if changes > 0:
            files_changed += 1
            total_lines += changes
            print(f'  {f}: {changes} lines')

print(f'\nTotal: {files_changed} files, {total_lines} lines changed')

# Verify all files compile
print('\nVerifying compilation...')
errors = []
for root, dirs, files in os.walk('tests'):
    for f in sorted(files):
        if not f.endswith('.py'):
            continue
        path = os.path.join(root, f)
        try:
            import py_compile
            py_compile.compile(path, doraise=True)
        except py_compile.PyCompileError as e:
            errors.append(str(e))

if errors:
    print(f'\n{len(errors)} COMPILATION ERRORS:')
    for e in errors:
        print(f'  {e}')
else:
    print('All files compile successfully!')
