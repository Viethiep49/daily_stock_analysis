import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

TRANSLATIONS = {
    # Module docstrings
    'A股自选股智能分析系统': 'A-Share Watchlist Smart Analysis System',
    '测试包': 'Test Package',
    '分析历史存储单元测试': 'Analysis History Storage Unit Tests',
    '职责：': 'Responsibilities:',
    '提供单元测试包结构': 'Provide unit test package structure',
    '统一测试模块入口': 'Unified test module entry point',
    '验证分析历史保存逻辑': 'Verify analysis history save logic',
    '验证上下文快照保存开关': 'Verify context snapshot save toggle',

    # Test class/method docstrings
    '分析历史存储测试': 'Analysis history storage test',
    '为每个用例初始化独立数据库': 'Initialize independent database for each test case',
    '清理资源': 'Clean up resources',
    '构造分析结果': 'Build analysis result',
    '保存一条测试历史记录并返回主键 ID。': 'Save a test history record and return the primary key ID.',
    '保存历史记录并写入上下文快照': 'Save history record and write context snapshot',
    '关闭快照保存时不写入 context_snapshot': 'Do not write context_snapshot when snapshot saving is disabled',
    '删除历史记录时应一并清理关联回测结果。': 'Should also clean up associated backtest results when deleting history records.',

    # Assertion messages
    '未找到保存的历史记录': 'Saved history record not found',

    # Log messages
    '[实时行情-新浪]': '[Realtime Quote - Sina]',
    '[实时行情-腾讯]': '[Realtime Quote - Tencent]',
    '实时行情接口失败': 'Realtime quote API failed',

    # Error messages
    '股票代码不能为空或仅包含空白字符': 'Stock code cannot be empty or contain only whitespace',
    '请输入有效的股票代码或股票名称': 'Please enter a valid stock code or stock name',
    '最多支持': 'Maximum supported',

    # Config/prompt strings (used in tests as string literals being passed to constructors)
    '默认技能基线': 'Default skill baseline',
    '必须严格遵守': 'Must be strictly followed',
    '严进策略': 'Strict entry strategy',
    '专注于趋势交易': 'Focus on trend trading',
    '多头排列必须条件': 'Required bull arrangement conditions',
    '多头排列：': 'Bull arrangement: ',

    # News prompt strings
    '近7日的新闻搜索结果': 'News search results from the past 7 days',
    '近1日的新闻搜索结果': 'News search results from the past 1 day',
    '近30日的新闻搜索结果': 'News search results from the past 30 days',
    '每一条都必须带具体日期（YYYY-MM-DD）': 'Each entry must include a specific date (YYYY-MM-DD)',
    '超出近7日窗口的新闻一律忽略': 'News outside the past 7-day window must be ignored',
    '超出近1日窗口的新闻一律忽略': 'News outside the past 1-day window must be ignored',
    '超出近30日窗口的新闻一律忽略': 'News outside the past 30-day window must be ignored',
    '时间未知、无法确定发布日期的新闻一律忽略': 'News with unknown time or undeterminable publication date must be ignored',
    '财报与分红（价值投资口径）': 'Financial reports and dividends (value investing perspective)',
    '禁止编造': 'Fabrication is prohibited',

    # Trend analysis strings
    '关注中枢与背驰': 'Focus on pivot zones and divergence',
    '关注支撑确认': 'Focus on support confirmation',
    '当前结构是否满足激活技能的关键触发条件': 'Whether the current structure meets the key trigger conditions for activating the skill',
    '是否满足 MA5>MA10>MA20 多头排列': 'Whether MA5>MA10>MA20 bull arrangement is satisfied',
    '超过5%必须标注"严禁追高"': 'Must mark "Do not chase highs" if exceeding 5%',
    'MA5>MA10>MA20为多头': 'MA5>MA10>MA20 indicates bullish',

    # Portfolio section
    '组合视角': 'Portfolio Perspective',
    '组合摘要': 'Portfolio Summary',
    '组合偏消费集中': 'Portfolio is concentrated in consumer sector',
    '建议仓位': 'Suggested Position',
    '建议控制仓位。': 'Suggest controlling position size.',
    '白酒板块集中度过高': 'Baijiu sector concentration too high',
    '600519 与 000858 相关性偏高': 'High correlation between 600519 and 000858',
    '降低单一行业暴露': 'Reduce single-sector exposure',
    '估值偏高': 'Overvalued',
    '自由文本分析': 'Free text analysis',

    # Board/sector
    '白酒': 'Baijiu',
    '行业': 'Industry',
    '消费': 'Consumer',
    '坏数据': 'Bad Data',
    '煤炭': 'Coal',

    # Common terms in docstrings
    '新闻摘要': 'News summary',
    '基本面稳健，短期震荡': 'Fundamentals are stable, short-term fluctuation',
    '茅台近期震荡走强': 'Moutai showing recent strength with fluctuations',

    # Sniper points
    '理想买入点：': 'Ideal Buy Point: ',
    '止损位：': 'Stop Loss: ',
    '目标位：': 'Target: ',
    '核心结论': 'Core Conclusion',
    '核心结论：': 'Core Conclusion:',
    '跌破 110 元止损': 'Stop loss if it drops below 110',
    '120-121 元分批': 'Buy in batches at 120-121',

    # Skills
    '测试策略': 'Test Strategy',
    '测试YAML策略': 'Test YAML Strategy',
    '一个用于测试的策略': 'A strategy for testing',
    '这是一个用自然语言编写的测试策略。': 'This is a test strategy written in natural language.',
    '判断标准：当 MA5 > MA10 时买入。': 'Entry criteria: Buy when MA5 > MA10.',
    '最简策略': 'Minimal Strategy',
    '最简描述': 'Minimal description',
    '元数据技能': 'Metadata Skill',
    '带有默认元数据的技能': 'A skill with default metadata',
    '这是一个测试技能。': 'This is a test skill.',
    '不完整': 'Incomplete',
    '自定义龙头策略': 'Custom Dragon Head Strategy',
    '我自己的龙头策略': 'My own dragon head strategy',
    '按照我的规则分析龙头股': 'Analyze leading stocks according to my rules',
    '默认多头趋势': 'Default bull trend',
    '多头趋势': 'Bull trend',
    '缠论': 'Chan Theory',
    '波浪理论': 'Wave Theory',
    '箱体震荡': 'Box Oscillation',
    '龙头策略': 'Dragon Head Strategy',
    '缩量回踩': 'Shrink Pullback',
    '放量突破': 'Volume Breakout',
    '趋势跟随': 'Trend following',
    '结构分析': 'Structural analysis',
    '轮动': 'Rotation',
    '龙头侦察': 'Leader Scout',
    '别名一': 'alias_one',
    '别名二': 'alias_two',
    '自然语言': 'natural language',

    # Skill display names
    '决策仪表盘': 'Decision Dashboard',
    '测试美股': 'Test US Stock',

    # Test analysis metadata
    '手动输入': 'manual_input',
    '自动补全': 'auto_complete',
    '图片识别': 'image_recognition',

    # Trend context
    '震荡偏强': 'Fluctuating with bullish bias',
    '粘合后发散': 'Converging then diverging',
    '平量': 'Flat volume',
    '量能温和': 'Volume moderate',
    '观察': 'Watch',
    '结构待确认': 'Structure pending confirmation',
    '无背驰确认': 'No divergence confirmation',

    # Other Chinese in prompts/comments
    '批量股票': 'Batch stocks',
    '搜索引擎': 'Search engine',

    # Ask command
    '趋势': 'Trend',
    '趋势分析': 'Trend Analysis',
    '缠论分析': 'Chan Theory Analysis',
    '请': 'Please',
    '用缠论分析': 'analyze using Chan Theory',
    '波浪理论': 'Wave Theory',
    '组合偏消费集中，建议控制仓位。': 'Portfolio is consumer-concentrated, suggest controlling position.',
    '估值偏高': 'Overvalued',
    '风险等级': 'Risk Level',

    # Misc
    '分析失败': 'Analysis Failed',
    '组合': 'Portfolio',
    '风险': 'Risk',
    '分': ' points',
}

# Process each file
files_changed = 0
total_replacements = 0

for root, dirs, files in os.walk('tests'):
    for f in sorted(files):
        if not f.endswith('.py'):
            continue
        path = os.path.join(root, f)
        content = open(path, encoding='utf-8').read()
        original = content
        
        # Apply translations - but ONLY in specific contexts:
        # 1. After # (comments)
        # 2. In docstrings (between """)
        # 3. In logging calls
        # 4. In assert message parameters
        
        # Strategy: For each translation, check if it appears in a translatable context
        # We'll do line-by-line processing
        
        lines = content.split('\n')
        new_lines = []
        in_docstring = False
        
        for line in lines:
            new_line = line
            stripped = line.strip()
            
            # Track docstrings
            triple_count = line.count('"""')
            if triple_count >= 2:
                # Could be single-line docstring or closing
                if in_docstring:
                    in_docstring = False
                # If it opens and closes on same line, process it
            elif triple_count == 1:
                if not in_docstring:
                    in_docstring = True
                else:
                    in_docstring = False
            
            # Determine if this line should be translated
            is_comment = stripped.startswith('#')
            is_in_docstring = in_docstring or (triple_count >= 2)
            
            if is_comment or is_in_docstring:
                # Apply all translations
                for zh, en in TRANSLATIONS.items():
                    if zh in new_line:
                        new_line = new_line.replace(zh, en)
            
            new_lines.append(new_line)
        
        content = '\n'.join(new_lines)
        
        if content != original:
            open(path, 'w', encoding='utf-8').write(content)
            files_changed += 1
            replacements = sum(1 for a, b in zip(original.split('\n'), content.split('\n')) if a != b)
            total_replacements += replacements
            print(f'  {f}: {replacements} lines changed')

print(f'\nTotal files changed: {files_changed}')
print(f'Total lines changed: {total_replacements}')
