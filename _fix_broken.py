import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

# Restore broken test data - reverse partial translations in code strings
RESTORE = {
    # test_backtest_engine.py - test input data
    '不要Sell': '不要卖出',
    
    # test_agent_orchestrator_sniper_fallback.py - test data values
    'Trend仍强，等待回踩。': '趋势仍强，等待回踩。',
    
    # test_bot_dispatcher_async.py - test user input
    '帮我Analysis430001': '帮我分析430001',
    '帮我Analysis600519': '帮我分析600519',
    '帮我Analysis茅台': '帮我分析茅台',
    
    # test_multi_agent.py - test input data
    '看看TSLA': '看看TSLA',  # TSLA is English, OK
    'Analysis600519的走势': '分析600519的走势',
    '情绪Medium性偏谨慎': '情绪面偏谨慎',
    'Industry复苏': '行业复苏',
    '继续Hold': '继续持有',
    'Trend仍强，回踩可Watch。': '趋势仍强，回踩可观望。',
    'Trend偏强': '趋势偏强',
    '建议继续Watch量价配合，分批参与。': '建议继续观望，量价配合，分批参与。',
    '这是natural language回复': '这是自然语言回复',
    '🟢Buy信号': '🟢买入信号',
    '分批Buy': '分批买入',
    '降级结果': '降级结果',
    '之前的问题': '之前的问题',
    '之前的回答': '之前的回答',
    '请总结一下': '请总结一下',
    '帮我总结一下': '帮我总结一下',
    '原始结论': '原始结论',
    '原风险提示': '原风险提示',
    '可以参与': '可以参与',
    '信号': '信号',
    '分批': '分批',
    '继续': '继续',
    '重大风险': '重大风险',
    '存在重大减持风险': '存在重大减持风险',
    '大股东减持': '大股东减持',
    '风控接管': '风控接管',
    '存在重大风险': '存在重大风险',
    '超时': '超时',
    '风险': '风险',
    '强势多头排列，价格回踩': '强势多头排列，价格回踩',
    '分批布局': '分批布局',
    '仍强，回踩可': '仍强，回踩可',
    '偏强': '偏强',
    '仍强': '仍强',
    
    # test_ask_command.py - test data
    '用Chan TheoryAnalysis': '用缠论分析',
    '茅台 summary': '茅台 summary',
    '五粮液 summary': '五粮液 summary',
    '600519 与 000858 相关性偏High': '600519 与 000858 相关性偏高',
    '组合偏消费集中，建议控制仓位。': '组合偏消费集中，建议控制仓位。',
    
    # test_fetcher_logging.py - log message test data
    'Eastmoney 历史K线接口失败: ': 'Eastmoney 历史K线接口失败: ',
    'Eastmoney 历史K线接口失败:': 'Eastmoney 历史K线接口失败:',
    '[SuccessFetcher] 开始获取 600519 日线数据': '[SuccessFetcher] 开始获取 600519 日线数据',
    '[SuccessFetcher] 600519 获取成功:': '[SuccessFetcher] 600519 获取成功:',
    '[数据源尝试 1/2] [FailureFetcher] 获取 601006...': '[数据源尝试 1/2] [FailureFetcher] 获取 601006...',
    '[数据源失败 1/2] [FailureFetcher] 601006:': '[数据源失败 1/2] [FailureFetcher] 601006:',
    '[数据源切换] 601006: [FailureFetcher] -> [SuccessFetcher]': '[数据源切换] 601006: [FailureFetcher] -> [SuccessFetcher]',
    '[数据源完成] 601006 Use [SuccessFetcher] 获取成功:': '[数据源完成] 601006 使用 [SuccessFetcher] 获取成功:',
    '[EfinanceFetcher] 601006 获取失败:': '[EfinanceFetcher] 601006 获取失败:',
    
    # test_analysis_history.py - test data strings
    '120-121 Yuan分批': '120-121 元分批',
    '跌破 110 Yuan止损': '跌破 110 元止损',
    
    # test_storage.py - test data strings
    '建议在 100 YuannearbyBuy': '建议在 100 元附近买入',
    '价格：100.5Yuan': '价格：100.5元',
    '无法给出。需等待MA5数据恢复，在股价回踩MA5且乖离率<2%时考虑100Yuan': '无法给出。需等待MA5数据恢复，在股价回踩MA5且乖离率<2%时考虑100元',
    'MA10为20.5，建议在30YuanBuy': 'MA10为20.5，建议在30元买入',
    '支撑位10Yuan，阻力位20Yuan': '支撑位10元，阻力位20元',
    '108.00-110.00（前期High点阻力）': '108.00-110.00（前期高点阻力）',
    'MA5但没有Yuan': 'MA5但没有元',
    '1.52-1.53 (回踩MA5/10nearby)': '1.52-1.53 (回踩MA5/10附近)',
    '1.49-1.50(MA60nearby企稳)': '1.49-1.50(MA60附近企稳)',
    
    # test_fundamental_adapter.py
    '每10股Dividend发2.5Yuan': '每10股派发2.5元',
    '每股Dividend0.8Yuan': '每股派0.8元',
    '10Dividend3Yuan(税后)': '10派3元(税后)',
    
    # test_tickflow_fetcher.py
    '科创板Test': '科创板测试',
    '北交Test': '北交测试',
    '上证Index': '上证指数',
    '当前套餐不支持标的池查询，请升级或Use symbols 参数': '当前套餐不支持标的池查询，请升级或使用 symbols 参数',
    
    # test_us_index_mapping.py
    '道琼斯工业Index': '道琼斯工业指数',
    '纳斯达克综合Index': '纳斯达克综合指数',
    'VIX恐慌Index': 'VIX恐慌指数',
    
    # test_market_analyzer_generate_text.py
    '市场Analysis报告': '市场分析报告',
    '上证Index': '上证指数',
    
    # test_market_strategy.py
    'A股市场三段式复盘Strategy': 'A股市场三段式复盘策略',
    'Strategy计划': '策略计划',
    
    # test_report_integrity.py
    '可Buy': '可买入',
    '建议Sell': '建议卖出',
    'Retry prompt should carry previous response so补全是增量的。': 'Retry prompt should carry previous response so补全是增量的。',
    
    # test_report_schema.py
    '基本面Stable': '基本面稳健',
    'Test摘要': '测试摘要',
    
    # test_report_language.py
    'Medium性': '中性',
    
    # test_image_stock_extractor_litellm.py
    '未配置 Vision API': '未配置 Vision API',
    '关注 600519、300750 和 AAPL。': '关注 600519、300750 和 AAPL。',
    '证券ETF': '证券ETF',
    '银行ETF': '银行ETF',
    'Vision API 调用失败': 'Vision API 调用失败',
    
    # test_import_parser.py
    '仅支持 .xlsx': '仅支持 .xlsx',
    'CSV 解析失败': 'CSV 解析失败',
    '不存在的股票名称xyz': '不存在的股票名称xyz',
    
    # test_main_schedule_mode.py
    '定时模式下检测到 --stocks 参数；计划执行将忽略启动时股票快照，并在每次运行前重新读取最新的 STOCK_LIST。': '定时模式下检测到 --stocks 参数；计划执行将忽略启动时股票快照，并在每次运行前重新读取最新的 STOCK_LIST。',
    
    # test_name_to_code_resolver.py
    '不存在的股票名称xyz': '不存在的股票名称xyz',
    
    # test_news_intel.py
    '构造 SearchResponse 快捷函数': '构造 SearchResponse 快捷函数',
    '相同 URL 去重，仅保留一条记录': '相同 URL 去重，仅保留一条记录',
    'Test用户': '测试用户',
    '无 URL 时Use兜底键去重': '无 URL 时使用兜底键去重',
    '可按时间范围查询最新News': '可按时间范围查询最新新闻',
    '盘Medium波动较大...': '盘中波动较大...',
    '未找到保存的News记录': '未找到保存的新闻记录',
    
    # test_notification.py
    '报告生成与选路相关Test。': '报告生成与选路相关测试。',
    
    # test_notification_sender.py
    'daily_stock_analysis股票Analysis助手': 'daily_stock_analysis股票分析助手',
    'Test主题': '测试主题',
    
    # test_pipeline_notification_image_routing.py
    '企业微信 Markdown 转图片失败': '企业微信 Markdown 转图片失败',
    
    # test_search_searxng.py
    '公共 SearXNG 实例': '公共 SearXNG 实例',
    
    # test_webui_frontend.py
    '未检测到 npm，无法自动构建前端': '未检测到 npm，无法自动构建前端',
    
    # test_yfinance_us_indices.py
    '沪深300ETF': '沪深300ETF',
    
    # test_search_news_freshness.py
    '沪深300ETF': '沪深300ETF',
    
    # test_search_tavily_provider.py
    '沪深300ETF': '沪深300ETF',
    
    # test_data_fetcher_prefetch_stock_names.py
    'Test股票': '测试股票',
    '股票{index:06d}': '股票{index:06d}',
    
    # test_agent_executor.py - reporter type context
    '报告类型: daily': '报告类型: daily',
}

# Also fix test_generate_index_from_csv.py docstrings/function names
MORE_FIXES = {
    'Test Symbol 提取函数': 'Test Symbol extraction function',
    'Test A股深圳': 'Test A-share Shenzhen',
    'Test A股上海': 'Test A-share Shanghai',
    'Test港股': 'Test HK stock',
    'Test空 ts_code': 'Test empty ts_code',
    'Test市场判断函数': 'Test market detection function',
    'Test北交所': 'Test BSE',
    'Test US Stock特斯拉': 'Test US stock Tesla',
    'Test US Stock带点号后缀（BRK.B）': 'Test US stock with dot suffix (BRK.B)',
    'Test US Stock A 类股（GOOG.A）': 'Test US stock A class (GOOG.A)',
    'Test股票名称获取函数': 'Test stock name retrieval function',
    'Test A股Use name 字段': 'Test A-share using name field',
    'Test港股Use name 字段': 'Test HK stock using name field',
    'Test US StockUse enname 字段': 'Test US stock using enname field',
    'Test空名称': 'Test empty name',
    'Test数据清洗逻辑': 'Test data cleaning logic',
    'Test有效的 A股记录': 'Test valid A-share records',
    'Test有效的港股记录': 'Test valid HK stock records',
    'Test有效的美股记录': 'Test valid US stock records',
    'Test有效的美股记录（带点号后缀，如 BRK.B）': 'Test valid US stock records (with dot suffix, e.g. BRK.B)',
    'Test US Stock DUMMY 记录被过滤': 'Test US stock DUMMY records filtered',
    'Test DUMMY 过滤不区 points大小写': 'Test DUMMY filtering is case-insensitive',
    'Test空 ts_code 被过滤': 'Test empty ts_code filtered',
    'Test空名称被过滤': 'Test empty name filtered',
    'Test US Stock空 enname 被过滤': 'Test US stock empty enname filtered',
    'Test US Stock去重优先级：空 delist_date 优先于 NaT': 'Test US stock dedup priority: empty delist_date over NaT',
    'Test别名生成函数': 'Test alias generation function',
    'Test A股别名': 'Test A-share alias',
    'Test港股别名': 'Test HK stock alias',
    'Test US Stock别名': 'Test US stock alias',
    'Test无别名的情况': 'Test case with no alias',
    'Test输出格式': 'Test output format',
    'Test压缩格式的字段顺序': 'Test compressed format field order',
    'Test JSON 序列化': 'Test JSON serialization',
    '集成Test': 'Integration test',
    'Test完整的 Tushare 工作流': 'Test complete Tushare workflow',
    'Test市场 points布统计': 'Test market distribution statistics',
    'Test US Stock复用 ticker 在加载时会先去重': 'Test US stock reused tickers deduplicated on load',
    'Test拼音生成': 'Test pinyin generation',
    'Test名称标准化': 'Test name normalization',
    'get_latest_data 方法Test': 'get_latest_data method test',
    '插入Test用股票数据': 'Insert test stock data',
    
    # test_stooq_fallback.py
    'Test Stooq 正常抓取与解析逻辑': 'Test Stooq normal fetch and parse logic',
    'Test yfinance 失败后自动触发 Stooq 逻辑': 'Test yfinance failure auto-triggers Stooq logic',
    
    # test_storage.py
    'Test解析狙击点位数Value': 'Test parsing sniper point values',
    
    # test_news_intel.py
    'News情报存储Test': 'News intel storage test',
}

# Merge all restore mappings
ALL_FIXES = {}
ALL_FIXES.update(RESTORE)
ALL_FIXES.update(MORE_FIXES)

files_changed = 0
total_fixes = 0

for root, dirs, files in os.walk('tests'):
    for f in sorted(files):
        if not f.endswith('.py'):
            continue
        path = os.path.join(root, f)
        content = open(path, encoding='utf-8').read()
        original = content
        
        for broken, fixed in ALL_FIXES.items():
            if broken in content and broken != fixed:
                content = content.replace(broken, fixed)
        
        if content != original:
            open(path, 'w', encoding='utf-8').write(content)
            files_changed += 1
            changes = sum(1 for a, b in zip(original.split('\n'), content.split('\n')) if a != b)
            total_fixes += changes
            print(f'  {f}: {changes} fixes')

print(f'\nTotal: {files_changed} files, {total_fixes} fixes')
