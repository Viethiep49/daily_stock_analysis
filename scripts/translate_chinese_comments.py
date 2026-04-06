#!/usr/bin/env python3
"""
Scan all .py files and replace Chinese characters in comments with English.
Uses dictionary-based translation for common programming terms.

Usage:
    python scripts/translate_chinese_comments.py [--dry-run] [--verbose]
"""
import os
import re
import sys
import argparse
from pathlib import Path

COMMON = {
    '配置': 'config', '初始化': 'initialize', '获取': 'fetch', '设置': 'set',
    '检查': 'check', '验证': 'validate', '处理': 'process', '返回': 'return',
    '错误': 'error', '异常': 'exception', '日志': 'log', '数据': 'data',
    '文件': 'file', '路径': 'path', '参数': 'param', '函数': 'function',
    '类': 'class', '方法': 'method', '属性': 'property', '接口': 'interface',
    '服务': 'service', '请求': 'request', '响应': 'response', '结果': 'result',
    '成功': 'success', '失败': 'fail', '开始': 'start', '结束': 'end',
    '完成': 'complete', '加载': 'load', '保存': 'save', '创建': 'create',
    '删除': 'delete', '更新': 'update', '查询': 'query', '解析': 'parse',
    '转换': 'convert', '格式化': 'format', '发送': 'send', '接收': 'receive',
    '连接': 'connect', '关闭': 'close', '打开': 'open', '读取': 'read',
    '写入': 'write', '导入': 'import', '导出': 'export', '注册': 'register',
    '订阅': 'subscribe', '发布': 'publish', '通知': 'notify', '回调': 'callback',
    '事件': 'event', '触发': 'trigger', '执行': 'execute', '运行': 'run',
    '停止': 'stop', '重试': 'retry', '超时': 'timeout', '缓存': 'cache',
    '清除': 'clear', '重置': 'reset', '默认': 'default', '可选': 'optional',
    '必填': 'required', '类型': 'type', '名称': 'name', '值': 'value',
    '键': 'key', '索引': 'index', '列表': 'list', '字典': 'dict',
    '集合': 'set', '字符串': 'string', '数字': 'number', '布尔': 'bool',
    '空': 'empty', '真': 'true', '假': 'false', '是': 'yes', '否': 'no',
    '和': 'and', '或': 'or', '非': 'not', '如果': 'if', '否则': 'else',
    '当': 'when', '对于': 'for', '尝试': 'try', '捕获': 'catch',
    '抛出': 'raise', '最终': 'finally', '断言': 'assert', '装饰器': 'decorator',
    '生成器': 'generator', '迭代器': 'iterator', '上下文': 'context',
    '管理器': 'manager', '工厂': 'factory', '代理': 'proxy', '适配器': 'adapter',
    '策略': 'strategy', '模板': 'template', '构建器': 'builder', '命令': 'command',
    '状态': 'state', '股票': 'stock', '市场': 'market', '价格': 'price',
    '成交量': 'volume', '涨幅': 'gain', '跌幅': 'drop', '买入': 'buy',
    '卖出': 'sell', '持仓': 'position', '收益': 'return', '分析': 'analysis',
    '报告': 'report', '指标': 'indicator', '均线': 'MA', '趋势': 'trend',
    '支撑': 'support', '阻力': 'resistance', '突破': 'breakout', '回调': 'pullback',
    '反弹': 'rebound', '震荡': 'consolidate', '牛市': 'bull', '熊市': 'bear',
    '大盘': 'market index', '板块': 'sector', '行业': 'industry', '龙头': 'leader',
    '涨停': 'limit up', '跌停': 'limit down', '开盘': 'open', '收盘': 'close',
    '最高': 'high', '最低': 'low', '均价': 'avg price', '换手率': 'turnover',
    '市盈率': 'PE', '市净率': 'PB', '市值': 'market cap', '流通': 'float',
    '主力': 'main force', '散户': 'retail', '机构': 'institution',
    '资金': 'capital', '流入': 'inflow', '流出': 'outflow', '净额': 'net',
    '的': '', '了': '', '是': 'is', '在': 'in', '有': 'has', '这': 'this',
    '那': 'that', '它': 'it', '们': '', '我': 'I', '你': 'you', '他': 'he',
    '她': 'she', '我们': 'we', '你们': 'you', '他们': 'they', '这个': 'this',
    '那个': 'that', '这些': 'these', '那些': 'those', '什么': 'what',
    '哪里': 'where', '何时': 'when', '如何': 'how', '为什么': 'why',
    '多少': 'how much', '第一': 'first', '第二': 'second', '第三': 'third',
    '最后': 'last', '当前': 'current', '之前': 'before', '之后': 'after',
    '远程': 'remote', '本地': 'local', '全局': 'global', '内部': 'internal',
    '外部': 'external', '公共': 'public', '私有': 'private', '保护': 'protected',
    '静态': 'static', '动态': 'dynamic', '异步': 'async', '同步': 'sync',
    '阻塞': 'blocking', '并发': 'concurrent', '并行': 'parallel', '串行': 'serial',
    '随机': 'random', '唯一': 'unique', '重复': 'dup', '冗余': 'redundant',
    '必要': 'necessary', '重要': 'important', '关键': 'critical', '核心': 'core',
    '基础': 'base', '高级': 'advanced', '简单': 'simple', '复杂': 'complex',
    '完整': 'complete', '部分': 'partial', '组件': 'component', '模块': 'module',
    '包': 'package', '库': 'library', '框架': 'framework', '平台': 'platform',
    '系统': 'system', '应用': 'app', '程序': 'program', '进程': 'process',
    '线程': 'thread', '任务': 'task', '作业': 'job', '调度': 'schedule',
    '队列': 'queue', '栈': 'stack', '堆': 'heap', '树': 'tree', '图': 'graph',
    '表': 'table', '字段': 'field', '记录': 'record', '行': 'row', '列': 'col',
    '标题': 'title', '内容': 'content', '头部': 'header', '尾部': 'footer',
    '主体': 'body', '颜色': 'color', '字体': 'font', '大小': 'size',
    '样式': 'style', '布局': 'layout', '位置': 'position', '方向': 'direction',
    '旋转': 'rotate', '缩放': 'scale', '变换': 'transform', '动画': 'animation',
    '过渡': 'transition', '效果': 'effect', '阴影': 'shadow', '透明度': 'opacity',
    '可见': 'visible', '隐藏': 'hidden', '显示': 'show', '切换': 'toggle',
    '选择': 'select', '确认': 'confirm', '取消': 'cancel', '确定': 'ok',
    '应用': 'apply', '提交': 'submit', '撤销': 'undo', '重做': 'redo',
    '复制': 'copy', '粘贴': 'paste', '剪切': 'cut', '查找': 'find',
    '替换': 'replace', '搜索': 'search', '过滤': 'filter', '排序': 'sort',
    '分组': 'group', '聚合': 'aggregate', '汇总': 'summarize', '统计': 'stats',
    '计算': 'calc', '评估': 'eval', '测试': 'test', '调试': 'debug',
    '优化': 'optimize', '性能': 'perf', '效率': 'efficiency', '质量': 'quality',
    '安全': 'security', '权限': 'permission', '认证': 'auth', '授权': 'authz',
    '加密': 'encrypt', '解密': 'decrypt', '签名': 'sign', '验证': 'verify',
    '编码': 'encode', '解码': 'decode', '压缩': 'compress', '解压': 'decompress',
    '序列化': 'serialize', '反序列化': 'deserialize', '映射': 'map',
    '关联': 'relation', '依赖': 'dep', '引用': 'ref', '指针': 'ptr',
    '地址': 'addr', '内存': 'mem', '磁盘': 'disk', '网络': 'network',
    '带宽': 'bandwidth', '延迟': 'latency', '吞吐量': 'throughput',
    '负载': 'load', '容量': 'capacity', '限制': 'limit', '阈值': 'threshold',
    '范围': 'range', '周期': 'period', '频率': 'freq', '速率': 'rate',
    '速度': 'speed', '时间': 'time', '日期': 'date', '时区': 'timezone',
    '时间戳': 'timestamp', '间隔': 'interval', '等待': 'wait', '休眠': 'sleep',
    '广播': 'broadcast', '协议': 'protocol', '标准': 'standard', '规则': 'rule',
    '选项': 'option', '偏好': 'pref', '自定义': 'custom', '内置': 'builtin',
    '第三方': 'third-party', '开源': 'open-source', '免费': 'free', '付费': 'paid',
    '版本': 'version', '升级': 'upgrade', '降级': 'downgrade', '回滚': 'rollback',
    '迁移': 'migrate', '兼容': 'compatible', '抽象': 'abstract', '封装': 'encapsulate',
    '继承': 'inherit', '多态': 'polymorphism', '重载': 'overload', '重写': 'override',
    '覆盖': 'overwrite', '泛型': 'generic', '常量': 'const', '变量': 'var',
    '返回值': 'retval', '警告': 'warn', '信息': 'info', '跟踪': 'trace',
    '监控': 'monitor', '告警': 'alert', '仪表板': 'dashboard', '可视化': 'viz',
    '图表': 'chart', '图像': 'image', '视频': 'video', '音频': 'audio',
    '文本': 'text', '文档': 'doc', '目录': 'dir', '文件夹': 'folder',
    '链接': 'link', '设备': 'device', '硬件': 'hw', '软件': 'sw',
    '驱动': 'driver', '内核': 'kernel', '终端': 'terminal', '控制台': 'console',
    '输入': 'input', '输出': 'output', '打印': 'print', '识别': 'recognize',
    '检测': 'detect', '测量': 'measure', '合成': 'synthesize', '生成': 'generate',
    '销毁': 'destroy', '分配': 'alloc', '释放': 'free', '回收': 'recycle',
    '死锁': 'deadlock', '竞争': 'race', '原子': 'atomic', '互斥': 'mutex',
    '事务': 'txn', '提交': 'commit', '隔离': 'isolation', '一致性': 'consistency',
    '快照': 'snapshot', '高可用': 'HA', '容错': 'fault-tolerant', '弹性': 'elastic',
    '负载均衡': 'LB', '熔断': 'circuit-breaker', '降级': 'degrade', '限流': 'rate-limit',
    '心跳': 'heartbeat', '健康检查': 'healthcheck', '优雅关闭': 'graceful-shutdown',
    '预热': 'warmup', '优先级': 'priority', '权重': 'weight', '配额': 'quota',
    '指标': 'metric', '标签': 'label', '维度': 'dim', '注解': 'annotation',
    '元数据': 'metadata', '数据质量': 'data-quality', '数据安全': 'data-security',
    '数据模型': 'data-model', '数据仓库': 'DW', '数据湖': 'data-lake',
    '数据管道': 'pipeline', '数据集成': 'integration', '数据迁移': 'migration',
    '数据清洗': 'cleanse', '数据验证': 'validate', '数据采样': 'sample',
    '数据分区': 'partition', '数据分片': 'shard', '数据编码': 'encode',
    '数据压缩': 'compress', '数据缓存': 'cache', '数据预取': 'prefetch',
    '如果为': 'if is', '如果不': 'if not', '是否为': 'whether is',
    '是否为空': 'is empty', '是否存在': 'exists', '是否有效': 'is valid',
    '是否成功': 'succeeded', '是否失败': 'failed', '是否启用': 'enabled',
    '是否支持': 'supported', '是否包含': 'contains', '是否等于': 'equals',
    '当前时间': 'current time', '当前用户': 'current user', '当前环境': 'current env',
    '默认值': 'default value', '最大值': 'max value', '最小值': 'min value',
    '总数': 'total', '平均值': 'average', '中位数': 'median', '标准差': 'stddev',
    '方差': 'variance', '总和': 'sum', '计数': 'count', '最小': 'min',
    '最大': 'max', '平均': 'avg', '累计': 'cumulative', '增量': 'delta',
    '绝对': 'absolute', '相对': 'relative', '百分比': 'percent', '比例': 'ratio',
    '概率': 'probability', '期望': 'expectation', '分布': 'distribution',
    '样本': 'sample', '总体': 'population', '参数': 'param', '统计量': 'statistic',
    '假设': 'hypothesis', '检验': 'test', '显著': 'significant', '置信': 'confidence',
    '区间': 'interval', '估计': 'estimate', '预测': 'predict', '分类': 'classify',
    '聚类': 'cluster', '回归': 'regression', '降维': 'reduce-dim', '特征': 'feature',
    '标签': 'label', '训练': 'train', '测试': 'test', '验证': 'validate',
    '模型': 'model', '算法': 'algorithm', '损失': 'loss', '梯度': 'gradient',
    '学习率': 'learning rate', '批次': 'batch', '轮次': 'epoch', '迭代': 'iterate',
    '收敛': 'converge', '过拟合': 'overfit', '欠拟合': 'underfit',
    '正则化': 'regularize', 'dropout': 'dropout', '激活': 'activate',
    '池化': 'pool', '卷积': 'convolve', '全连接': 'fully-connected',
    '嵌入': 'embed', '注意力': 'attention', '自注意力': 'self-attention',
    '编码器': 'encoder', '解码器': 'decoder', '变换器': 'transformer',
    '预训练': 'pretrain', '微调': 'finetune', '迁移学习': 'transfer-learning',
    '强化学习': 'RL', '监督学习': 'supervised', '无监督学习': 'unsupervised',
    '半监督学习': 'semi-supervised', '主动学习': 'active-learning',
    '在线学习': 'online-learning', '离线学习': 'offline-learning',
    '批量学习': 'batch-learning', '增量学习': 'incremental-learning',
    '集成学习': 'ensemble', '随机森林': 'random-forest', '梯度提升': 'GBDT',
    '支持向量机': 'SVM', '逻辑回归': 'logistic-regression', '决策树': 'decision-tree',
    '朴素贝叶斯': 'naive-bayes', 'K近邻': 'KNN', '神经网络': 'neural-network',
    '深度学习': 'deep-learning', '机器学习': 'ML', '人工智能': 'AI',
    '自然语言处理': 'NLP', '计算机视觉': 'CV', '语音识别': 'ASR',
    '图像识别': 'image-recognition', '目标检测': 'object-detection',
    '语义分割': 'semantic-segmentation', '实例分割': 'instance-segmentation',
    '姿态估计': 'pose-estimation', '场景理解': 'scene-understanding',
    '图像生成': 'image-generation', '文本生成': 'text-generation',
    '机器翻译': 'machine-translation', '问答系统': 'QA-system',
    '对话系统': 'dialogue-system', '推荐系统': 'recsys', '搜索引擎': 'search-engine',
    '知识图谱': 'knowledge-graph', '信息抽取': 'info-extraction',
    '实体识别': 'NER', '关系抽取': 'relation-extraction', '事件抽取': 'event-extraction',
    '情感分析': 'sentiment-analysis', '文本分类': 'text-classification',
    '文本聚类': 'text-clustering', '文本摘要': 'text-summarization',
    '关键词提取': 'keyword-extraction', '主题模型': 'topic-model',
    '词向量': 'word-embedding', '句向量': 'sentence-embedding',
    '文档向量': 'doc-embedding', '相似度': 'similarity', '距离': 'distance',
    '余弦': 'cosine', '欧氏': 'euclidean', '曼哈顿': 'manhattan',
    '杰卡德': 'jaccard', '编辑距离': 'edit-distance', 'BLEU': 'BLEU',
    'ROUGE': 'ROUGE', '准确率': 'accuracy', '精确率': 'precision',
    '召回率': 'recall', 'F1值': 'F1', 'AUC': 'AUC', 'ROC': 'ROC',
    '混淆矩阵': 'confusion-matrix', '交叉验证': 'cross-validation',
    '网格搜索': 'grid-search', '随机搜索': 'random-search', '贝叶斯优化': 'bayesian-opt',
    '早停': 'early-stopping', '学习率衰减': 'lr-decay', '权重衰减': 'weight-decay',
    '动量': 'momentum', '自适应': 'adaptive', '优化器': 'optimizer',
    '损失函数': 'loss-fn', '激活函数': 'activation-fn', '归一化': 'normalize',
    '标准化': 'standardize', '批归一化': 'batch-norm', '层归一化': 'layer-norm',
    '实例归一化': 'instance-norm', '组归一化': 'group-norm',
    '残差连接': 'residual-conn', '跳跃连接': 'skip-conn', '密集连接': 'dense-conn',
    '注意力机制': 'attention-mech', '多头注意力': 'multi-head-attn',
    '位置编码': 'positional-encoding', '掩码': 'mask', '填充': 'pad',
    '截断': 'truncate', '填充词': 'pad-token', '开始词': 'start-token',
    '结束词': 'end-token', '未知词': 'unk-token', '词表': 'vocab',
    '分词': 'tokenize', '词干提取': 'stem', '词形还原': 'lemmatize',
    '停用词': 'stopword', 'n-gram': 'n-gram', 'TF-IDF': 'TF-IDF',
    '词袋': 'bag-of-words', '词频': 'term-freq', '逆文档频率': 'IDF',
}

def translate(text):
    result = text
    for zh, en in sorted(COMMON.items(), key=lambda x: len(x[0]), reverse=True):
        if zh in result:
            result = result.replace(zh, en)
    return result

def process_file(filepath, dry_run=False, verbose=False):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return False

    if not re.search(r'[\u4e00-\u9fff]', content):
        return False

    lines = content.split('\n')
    new_lines = []
    changed = False

    for line in lines:
        if '#' in line:
            idx = line.index('#')
            code = line[:idx]
            comment = line[idx:]
            if re.search(r'[\u4e00-\u9fff]', comment):
                translated = translate(comment)
                new_lines.append(code + translated)
                changed = True
                if verbose:
                    safe_old = comment.strip()[:80]
                    safe_new = translated.strip()[:80]
                    sys.stdout.buffer.write(f"  {filepath}: [{safe_old}] -> [{safe_new}]\n".encode('utf-8', errors='replace'))
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    if changed and not dry_run:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
        except Exception:
            return False

    return changed

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--path', default='.')
    args = parser.parse_args()

    root = Path(args.path).resolve()
    skip = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', 'env', '.agents', '.claude'}
    processed = 0
    changed = 0

    for r, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in skip]
        for f in files:
            if not f.endswith('.py'):
                continue
            fp = os.path.join(r, f)
            processed += 1
            if process_file(fp, dry_run=args.dry_run, verbose=args.verbose):
                changed += 1

    verb = "Would change" if args.dry_run else "Changed"
    print(f"\n{verb} {changed}/{processed} Python files")
    if args.dry_run:
        print("Remove --dry-run to apply changes")

if __name__ == '__main__':
    main()
