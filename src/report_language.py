# -*- coding: utf-8 -*-
"""Helpers for report output language selection and localization."""

from __future__ import annotations

import re
from typing import Any, Dict, Optional

SUPPORTED_REPORT_LANGUAGES = ("vi", "en", "zh")

_REPORT_LANGUAGE_ALIASES = {
    # Vietnamese
    "vietnamese": "vi",
    "viet": "vi",
    "vn": "vi",
    # English
    "english": "en",
    "en-us": "en",
    "en_us": "en",
    "en-gb": "en",
    "en_gb": "en",
    # Chinese (kept for backward compat with stored data)
    "zh-cn": "zh",
    "zh_cn": "zh",
    "zh-hans": "zh",
    "zh_hans": "zh",
    "zh-tw": "zh",
    "zh_tw": "zh",
    "cn": "zh",
    "chinese": "zh",
}

_OPERATION_ADVICE_CANONICAL_MAP = {
    # Vietnamese
    "mua mạnh": "strong_buy",
    "mua": "buy",
    "tích lũy": "buy",
    "nắm giữ": "hold",
    "giữ": "hold",
    "quan sát": "watch",
    "chờ": "watch",
    "giảm vị thế": "reduce",
    "bán": "sell",
    "bán mạnh": "strong_sell",
    # English
    "strong buy": "strong_buy",
    "strong_buy": "strong_buy",
    "buy": "buy",
    "accumulate": "buy",
    "add position": "buy",
    "hold": "hold",
    "watch": "watch",
    "wait": "watch",
    "wait and see": "watch",
    "reduce": "reduce",
    "trim": "reduce",
    "sell": "sell",
    "strong sell": "strong_sell",
    "strong_sell": "strong_sell",
    # Chinese (backward compat)
    "强烈买入": "strong_buy",
    "买入": "buy",
    "加仓": "buy",
    "持有": "hold",
    "观望": "watch",
    "减仓": "reduce",
    "卖出": "sell",
    "强烈卖出": "strong_sell",
}

_OPERATION_ADVICE_TRANSLATIONS = {
    "strong_buy": {"vi": "Mua Mạnh", "en": "Strong Buy", "zh": "强烈买入"},
    "buy":        {"vi": "Mua",      "en": "Buy",        "zh": "买入"},
    "hold":       {"vi": "Giữ",      "en": "Hold",       "zh": "持有"},
    "watch":      {"vi": "Quan Sát", "en": "Watch",      "zh": "观望"},
    "reduce":     {"vi": "Giảm",     "en": "Reduce",     "zh": "减仓"},
    "sell":       {"vi": "Bán",      "en": "Sell",       "zh": "卖出"},
    "strong_sell":{"vi": "Bán Mạnh", "en": "Strong Sell","zh": "强烈卖出"},
}

_TREND_PREDICTION_CANONICAL_MAP = {
    # Vietnamese
    "rất tích cực": "strong_bullish",
    "tích cực": "bullish",
    "trung tính": "sideways",
    "đi ngang": "sideways",
    "tiêu cực": "bearish",
    "rất tiêu cực": "strong_bearish",
    # English
    "strong bullish": "strong_bullish",
    "very bullish": "strong_bullish",
    "bullish": "bullish",
    "uptrend": "bullish",
    "neutral": "sideways",
    "sideways": "sideways",
    "range-bound": "sideways",
    "bearish": "bearish",
    "downtrend": "bearish",
    "strong bearish": "strong_bearish",
    "very bearish": "strong_bearish",
    # Chinese (backward compat)
    "强烈看多": "strong_bullish",
    "看多": "bullish",
    "震荡": "sideways",
    "看空": "bearish",
    "强烈看空": "strong_bearish",
}

_TREND_PREDICTION_TRANSLATIONS = {
    "strong_bullish": {"vi": "Rất Tích Cực", "en": "Strong Bullish", "zh": "强烈看多"},
    "bullish":        {"vi": "Tích Cực",     "en": "Bullish",       "zh": "看多"},
    "sideways":       {"vi": "Đi Ngang",     "en": "Sideways",      "zh": "震荡"},
    "bearish":        {"vi": "Tiêu Cực",     "en": "Bearish",       "zh": "看空"},
    "strong_bearish": {"vi": "Rất Tiêu Cực","en": "Strong Bearish","zh": "强烈看空"},
}

_CONFIDENCE_LEVEL_CANONICAL_MAP = {
    "cao": "high", "high": "high",
    "trung bình": "medium", "medium": "medium", "med": "medium",
    "thấp": "low", "low": "low",
    # Chinese compat
    "高": "high", "中": "medium", "低": "low",
}
_CONFIDENCE_LEVEL_TRANSLATIONS = {
    "high":   {"vi": "Cao",      "en": "High",   "zh": "高"},
    "medium": {"vi": "Trung Bình","en": "Medium", "zh": "中"},
    "low":    {"vi": "Thấp",     "en": "Low",    "zh": "低"},
}

_CHIP_HEALTH_CANONICAL_MAP = {
    "tốt": "healthy", "healthy": "healthy",
    "trung bình": "average", "average": "average",
    "cảnh báo": "caution", "caution": "caution",
    # Chinese compat
    "健康": "healthy", "一般": "average", "警惕": "caution",
}
_CHIP_HEALTH_TRANSLATIONS = {
    "healthy": {"vi": "Tốt",      "en": "Healthy", "zh": "健康"},
    "average": {"vi": "Trung Bình","en": "Average", "zh": "一般"},
    "caution": {"vi": "Cảnh Báo", "en": "Caution", "zh": "警惕"},
}

_BIAS_STATUS_CANONICAL_MAP = {
    "an toàn": "safe", "safe": "safe",
    "cảnh giác": "caution", "caution": "caution",
    "nguy hiểm": "danger", "risk": "danger", "danger": "danger",
    # Chinese compat
    "安全": "safe", "警戒": "caution", "警惕": "caution", "危险": "danger",
}
_BIAS_STATUS_TRANSLATIONS = {
    "safe":    {"vi": "An Toàn",   "en": "Safe",    "zh": "安全"},
    "caution": {"vi": "Cảnh Giác", "en": "Caution", "zh": "警戒"},
    "danger":  {"vi": "Nguy Hiểm", "en": "Danger",  "zh": "危险"},
}

_PLACEHOLDER_BY_LANGUAGE = {"vi": "Chưa có", "en": "TBD", "zh": "待补充"}
_UNKNOWN_BY_LANGUAGE = {"vi": "Không rõ", "en": "Unknown", "zh": "未知"}
_NO_DATA_BY_LANGUAGE = {"vi": "Không có dữ liệu", "en": "Data unavailable", "zh": "数据缺失"}
_GENERIC_STOCK_NAME_BY_LANGUAGE = {"vi": "Cổ phiếu chưa xác định", "en": "Unnamed Stock", "zh": "待确认股票"}

_REPORT_LABELS: Dict[str, Dict[str, str]] = {
    "zh": {
        "dashboard_title": "决策仪表盘",
        "brief_title": "决策简报",
        "analyzed_prefix": "共分析",
        "stock_unit": "只股票",
        "stock_unit_compact": "只",
        "buy_label": "买入",
        "watch_label": "观望",
        "sell_label": "卖出",
        "summary_heading": "分析结果摘要",
        "info_heading": "重要信息速览",
        "sentiment_summary_label": "舆情情绪",
        "earnings_outlook_label": "业绩预期",
        "risk_alerts_label": "风险警报",
        "positive_catalysts_label": "利好催化",
        "latest_news_label": "最新动态",
        "core_conclusion_heading": "核心结论",
        "one_sentence_label": "一句话决策",
        "time_sensitivity_label": "时效性",
        "default_time_sensitivity": "本周内",
        "position_status_label": "持仓情况",
        "action_advice_label": "操作建议",
        "no_position_label": "空仓者",
        "has_position_label": "持仓者",
        "continue_holding": "继续持有",
        "market_snapshot_heading": "当日行情",
        "close_label": "收盘",
        "prev_close_label": "昨收",
        "open_label": "开盘",
        "high_label": "最高",
        "low_label": "最低",
        "change_pct_label": "涨跌幅",
        "change_amount_label": "涨跌额",
        "amplitude_label": "振幅",
        "volume_label": "成交量",
        "amount_label": "成交额",
        "current_price_label": "当前价",
        "volume_ratio_label": "量比",
        "turnover_rate_label": "换手率",
        "source_label": "行情来源",
        "data_perspective_heading": "数据透视",
        "ma_alignment_label": "均线排列",
        "bullish_alignment_label": "多头排列",
        "yes_label": "是",
        "no_label": "否",
        "trend_strength_label": "趋势强度",
        "price_metrics_label": "价格指标",
        "ma5_label": "MA5",
        "ma10_label": "MA10",
        "ma20_label": "MA20",
        "bias_ma5_label": "乖离率(MA5)",
        "support_level_label": "支撑位",
        "resistance_level_label": "压力位",
        "chip_label": "筹码",
        "battle_plan_heading": "作战计划",
        "ideal_buy_label": "理想买入点",
        "secondary_buy_label": "次优买入点",
        "stop_loss_label": "止损位",
        "take_profit_label": "目标位",
        "suggested_position_label": "仓位建议",
        "entry_plan_label": "建仓策略",
        "risk_control_label": "风控策略",
        "checklist_heading": "检查清单",
        "failed_checks_heading": "检查未通过项",
        "history_compare_heading": "历史信号对比",
        "time_label": "时间",
        "score_label": "评分",
        "advice_label": "建议",
        "trend_label": "趋势",
        "generated_at_label": "报告生成时间",
        "report_time_label": "生成时间",
        "no_results": "无分析结果",
        "report_title": "股票分析报告",
        "avg_score_label": "均分",
        "action_points_heading": "操作点位",
        "position_advice_heading": "持仓建议",
        "analysis_model_label": "分析模型",
        "not_investment_advice": "AI生成，仅供参考，不构成投资建议",
        "details_report_hint": "详细报告见",
    },
    "en": {
        "dashboard_title": "Decision Dashboard",
        "brief_title": "Decision Brief",
        "analyzed_prefix": "Analyzed",
        "stock_unit": "stocks",
        "stock_unit_compact": "stocks",
        "buy_label": "Buy",
        "watch_label": "Watch",
        "sell_label": "Sell",
        "summary_heading": "Summary",
        "info_heading": "Key Updates",
        "sentiment_summary_label": "Sentiment",
        "earnings_outlook_label": "Earnings Outlook",
        "risk_alerts_label": "Risk Alerts",
        "positive_catalysts_label": "Positive Catalysts",
        "latest_news_label": "Latest News",
        "core_conclusion_heading": "Core Conclusion",
        "one_sentence_label": "One-line Decision",
        "time_sensitivity_label": "Time Sensitivity",
        "default_time_sensitivity": "This week",
        "position_status_label": "Position",
        "action_advice_label": "Action",
        "no_position_label": "No Position",
        "has_position_label": "Holding",
        "continue_holding": "Continue holding",
        "market_snapshot_heading": "Market Snapshot",
        "close_label": "Close",
        "prev_close_label": "Prev Close",
        "open_label": "Open",
        "high_label": "High",
        "low_label": "Low",
        "change_pct_label": "Change %",
        "change_amount_label": "Change",
        "amplitude_label": "Amplitude",
        "volume_label": "Volume",
        "amount_label": "Turnover",
        "current_price_label": "Price",
        "volume_ratio_label": "Volume Ratio",
        "turnover_rate_label": "Turnover Rate",
        "source_label": "Source",
        "data_perspective_heading": "Data View",
        "ma_alignment_label": "MA Alignment",
        "bullish_alignment_label": "Bullish Alignment",
        "yes_label": "Yes",
        "no_label": "No",
        "trend_strength_label": "Trend Strength",
        "price_metrics_label": "Price Metrics",
        "ma5_label": "MA5",
        "ma10_label": "MA10",
        "ma20_label": "MA20",
        "bias_ma5_label": "Bias (MA5)",
        "support_level_label": "Support",
        "resistance_level_label": "Resistance",
        "chip_label": "Chip Structure",
        "battle_plan_heading": "Battle Plan",
        "ideal_buy_label": "Ideal Entry",
        "secondary_buy_label": "Secondary Entry",
        "stop_loss_label": "Stop Loss",
        "take_profit_label": "Target",
        "suggested_position_label": "Position Size",
        "entry_plan_label": "Entry Plan",
        "risk_control_label": "Risk Control",
        "checklist_heading": "Checklist",
        "failed_checks_heading": "Failed Checks",
        "history_compare_heading": "Historical Signal Comparison",
        "time_label": "Time",
        "score_label": "Score",
        "advice_label": "Advice",
        "trend_label": "Trend",
        "generated_at_label": "Generated At",
        "report_time_label": "Generated",
        "no_results": "No analysis results",
        "report_title": "Stock Analysis Report",
        "avg_score_label": "Avg Score",
        "action_points_heading": "Action Levels",
        "position_advice_heading": "Position Advice",
        "analysis_model_label": "Model",
        "not_investment_advice": "AI-generated content for reference only. Not investment advice.",
        "details_report_hint": "See detailed report:",
    },
    "vi": {
        "dashboard_title": "Bảng Quyết Định",
        "brief_title": "Tóm Tắt Quyết Định",
        "analyzed_prefix": "Đã phân tích",
        "stock_unit": "cổ phiếu",
        "stock_unit_compact": "cp",
        "buy_label": "Mua",
        "watch_label": "Quan Sát",
        "sell_label": "Bán",
        "summary_heading": "Tóm Tắt",
        "info_heading": "Thông Tin Quan Trọng",
        "sentiment_summary_label": "Tâm Lý Thị Trường",
        "earnings_outlook_label": "Kỳ Vọng KQKD",
        "risk_alerts_label": "Cảnh Báo Rủi Ro",
        "positive_catalysts_label": "Yếu Tố Hỗ Trợ",
        "latest_news_label": "Tin Tức Mới Nhất",
        "core_conclusion_heading": "Kết Luận Cốt Lõi",
        "one_sentence_label": "Quyết Định Một Câu",
        "time_sensitivity_label": "Thời Hạn",
        "default_time_sensitivity": "Trong tuần",
        "position_status_label": "Trạng Thái Vị Thế",
        "action_advice_label": "Khuyến Nghị",
        "no_position_label": "Chưa có vị thế",
        "has_position_label": "Đang nắm giữ",
        "continue_holding": "Tiếp tục giữ",
        "market_snapshot_heading": "Diễn Biến Phiên",
        "close_label": "Đóng cửa",
        "prev_close_label": "Tham chiếu",
        "open_label": "Mở cửa",
        "high_label": "Cao nhất",
        "low_label": "Thấp nhất",
        "change_pct_label": "% Thay đổi",
        "change_amount_label": "Thay đổi",
        "amplitude_label": "Biên độ",
        "volume_label": "Khối lượng",
        "amount_label": "Giá trị GD",
        "current_price_label": "Giá hiện tại",
        "volume_ratio_label": "Tỷ lệ khối lượng",
        "turnover_rate_label": "Tỷ lệ chuyển nhượng",
        "source_label": "Nguồn",
        "data_perspective_heading": "Phân Tích Dữ Liệu",
        "ma_alignment_label": "Xếp Hàng MA",
        "bullish_alignment_label": "Xếp Hàng Tăng",
        "yes_label": "Có",
        "no_label": "Không",
        "trend_strength_label": "Sức Mạnh Xu Hướng",
        "price_metrics_label": "Chỉ Số Giá",
        "ma5_label": "MA5",
        "ma10_label": "MA10",
        "ma20_label": "MA20",
        "bias_ma5_label": "Lệch MA5",
        "support_level_label": "Hỗ Trợ",
        "resistance_level_label": "Kháng Cự",
        "chip_label": "Phân Phối Cổ Phiếu",
        "battle_plan_heading": "Kế Hoạch Giao Dịch",
        "ideal_buy_label": "Điểm Mua Lý Tưởng",
        "secondary_buy_label": "Điểm Mua Thứ Hai",
        "stop_loss_label": "Cắt Lỗ",
        "take_profit_label": "Chốt Lời",
        "suggested_position_label": "Tỷ Lệ Vị Thế",
        "entry_plan_label": "Chiến Lược Vào Lệnh",
        "risk_control_label": "Kiểm Soát Rủi Ro",
        "checklist_heading": "Danh Sách Kiểm Tra",
        "failed_checks_heading": "Mục Chưa Đạt",
        "history_compare_heading": "So Sánh Tín Hiệu Lịch Sử",
        "time_label": "Thời Gian",
        "score_label": "Điểm",
        "advice_label": "Khuyến Nghị",
        "trend_label": "Xu Hướng",
        "generated_at_label": "Thời Gian Tạo Báo Cáo",
        "report_time_label": "Tạo lúc",
        "no_results": "Không có kết quả phân tích",
        "report_title": "Báo Cáo Phân Tích Cổ Phiếu",
        "avg_score_label": "Điểm Trung Bình",
        "action_points_heading": "Điểm Hành Động",
        "position_advice_heading": "Khuyến Nghị Vị Thế",
        "analysis_model_label": "Mô Hình Phân Tích",
        "not_investment_advice": "Nội dung do AI tạo, chỉ mang tính tham khảo. Không phải lời khuyên đầu tư.",
        "details_report_hint": "Xem báo cáo chi tiết:",
    },
}


def normalize_report_language(value: Optional[str], default: str = "vi") -> str:
    """Normalize report language to a supported short code. Default is 'vi'."""
    candidate = (value or default).strip().lower().replace(" ", "_")
    candidate = _REPORT_LANGUAGE_ALIASES.get(candidate, candidate)
    if candidate in SUPPORTED_REPORT_LANGUAGES:
        return candidate
    return default


def is_supported_report_language_value(value: Optional[str]) -> bool:
    """Return whether the raw value is a supported language code or alias."""
    candidate = (value or "").strip().lower().replace(" ", "_")
    if not candidate:
        return False
    return candidate in SUPPORTED_REPORT_LANGUAGES or candidate in _REPORT_LANGUAGE_ALIASES


def get_report_labels(language: Optional[str]) -> Dict[str, str]:
    """Return UI copy for the selected report language."""
    normalized = normalize_report_language(language)
    return _REPORT_LABELS[normalized]


def get_placeholder_text(language: Optional[str]) -> str:
    """Return placeholder text for missing localized content."""
    return _PLACEHOLDER_BY_LANGUAGE[normalize_report_language(language)]


def get_unknown_text(language: Optional[str]) -> str:
    """Return localized unknown text."""
    return _UNKNOWN_BY_LANGUAGE[normalize_report_language(language)]


def get_no_data_text(language: Optional[str]) -> str:
    """Return localized data unavailable text."""
    return _NO_DATA_BY_LANGUAGE[normalize_report_language(language)]


def _normalize_lookup_key(value: Any) -> str:
    return str(value or "").strip().lower().replace("_", " ").replace("-", " ")


def _iter_lookup_candidates(value: Any) -> list[str]:
    raw_text = str(value or "").strip()
    if not raw_text:
        return []

    candidates = [raw_text]
    for part in re.split(r"[/|,，、]+", raw_text):
        normalized = part.strip()
        if normalized and normalized not in candidates:
            candidates.append(normalized)
    return candidates


def _canonicalize_lookup_value(value: Any, canonical_map: Dict[str, str]) -> Optional[str]:
    for candidate in _iter_lookup_candidates(value):
        canonical = canonical_map.get(_normalize_lookup_key(candidate))
        if canonical:
            return canonical
    return None


def _is_placeholder_stock_name(value: Any, code: Any = None) -> bool:
    text = str(value or "").strip()
    if not text:
        return True

    lowered = text.lower()
    if lowered in {"n/a", "na", "none", "null", "unknown"}:
        return True
    if text in {"-", "—", "未知", "待补充"}:
        return True

    code_text = str(code or "").strip()
    if code_text and lowered == code_text.lower():
        return True

    return text.startswith("股票")


def _translate_from_map(
    value: Any,
    language: Optional[str],
    *,
    canonical_map: Dict[str, str],
    translations: Dict[str, Dict[str, str]],
) -> str:
    normalized_language = normalize_report_language(language)
    raw_text = str(value or "").strip()
    if not raw_text:
        return raw_text

    canonical = _canonicalize_lookup_value(raw_text, canonical_map)
    if canonical:
        return translations[canonical][normalized_language]
    return raw_text


def localize_operation_advice(value: Any, language: Optional[str]) -> str:
    """Translate operation advice between Chinese and English when recognized."""
    return _translate_from_map(
        value,
        language,
        canonical_map=_OPERATION_ADVICE_CANONICAL_MAP,
        translations=_OPERATION_ADVICE_TRANSLATIONS,
    )


def localize_trend_prediction(value: Any, language: Optional[str]) -> str:
    """Translate trend prediction between Chinese and English when recognized."""
    return _translate_from_map(
        value,
        language,
        canonical_map=_TREND_PREDICTION_CANONICAL_MAP,
        translations=_TREND_PREDICTION_TRANSLATIONS,
    )


def localize_confidence_level(value: Any, language: Optional[str]) -> str:
    """Translate confidence level between Chinese and English when recognized."""
    return _translate_from_map(
        value,
        language,
        canonical_map=_CONFIDENCE_LEVEL_CANONICAL_MAP,
        translations=_CONFIDENCE_LEVEL_TRANSLATIONS,
    )


def localize_chip_health(value: Any, language: Optional[str]) -> str:
    """Translate chip health labels between Chinese and English when recognized."""
    return _translate_from_map(
        value,
        language,
        canonical_map=_CHIP_HEALTH_CANONICAL_MAP,
        translations=_CHIP_HEALTH_TRANSLATIONS,
    )


def localize_bias_status(value: Any, language: Optional[str]) -> str:
    """Translate price bias status labels between Chinese and English when recognized."""
    return _translate_from_map(
        value,
        language,
        canonical_map=_BIAS_STATUS_CANONICAL_MAP,
        translations=_BIAS_STATUS_TRANSLATIONS,
    )


def get_bias_status_emoji(value: Any) -> str:
    """Return the stable alert emoji for a localized or canonical bias status."""
    canonical = _canonicalize_lookup_value(value, _BIAS_STATUS_CANONICAL_MAP)
    if canonical == "safe":
        return "✅"
    if canonical == "caution":
        return "⚠️"
    return "🚨"


def infer_decision_type_from_advice(value: Any, default: str = "hold") -> str:
    """Infer buy/hold/sell from human-readable operation advice."""
    canonical = _canonicalize_lookup_value(value, _OPERATION_ADVICE_CANONICAL_MAP)
    if canonical in {"strong_buy", "buy"}:
        return "buy"
    if canonical in {"reduce", "sell", "strong_sell"}:
        return "sell"
    if canonical in {"hold", "watch"}:
        return "hold"
    return default


def get_signal_level(advice: Any, score: Any, language: Optional[str]) -> tuple[str, str, str]:
    """Return localized signal text, emoji, and stable color tag."""
    normalized_language = normalize_report_language(language)
    canonical = _canonicalize_lookup_value(advice, _OPERATION_ADVICE_CANONICAL_MAP)
    if canonical == "strong_buy":
        return (_OPERATION_ADVICE_TRANSLATIONS["strong_buy"][normalized_language], "💚", "strong_buy")
    if canonical == "buy":
        return (_OPERATION_ADVICE_TRANSLATIONS["buy"][normalized_language], "🟢", "buy")
    if canonical == "hold":
        return (_OPERATION_ADVICE_TRANSLATIONS["hold"][normalized_language], "🟡", "hold")
    if canonical == "watch":
        return (_OPERATION_ADVICE_TRANSLATIONS["watch"][normalized_language], "⚪", "watch")
    if canonical == "reduce":
        return (_OPERATION_ADVICE_TRANSLATIONS["reduce"][normalized_language], "🟠", "reduce")
    if canonical in {"sell", "strong_sell"}:
        return (_OPERATION_ADVICE_TRANSLATIONS["sell"][normalized_language], "🔴", "sell")

    try:
        numeric_score = int(float(score))
    except (TypeError, ValueError):
        numeric_score = 50

    if numeric_score >= 80:
        return (_OPERATION_ADVICE_TRANSLATIONS["strong_buy"][normalized_language], "💚", "strong_buy")
    if numeric_score >= 65:
        return (_OPERATION_ADVICE_TRANSLATIONS["buy"][normalized_language], "🟢", "buy")
    if numeric_score >= 55:
        return (_OPERATION_ADVICE_TRANSLATIONS["hold"][normalized_language], "🟡", "hold")
    if numeric_score >= 45:
        return (_OPERATION_ADVICE_TRANSLATIONS["watch"][normalized_language], "⚪", "watch")
    if numeric_score >= 35:
        return (_OPERATION_ADVICE_TRANSLATIONS["reduce"][normalized_language], "🟠", "reduce")
    return (_OPERATION_ADVICE_TRANSLATIONS["sell"][normalized_language], "🔴", "sell")


def get_localized_stock_name(value: Any, code: Any, language: Optional[str]) -> str:
    """Return a localized stock name placeholder when the original name is missing."""
    raw_text = str(value or "").strip()
    if not _is_placeholder_stock_name(raw_text, code):
        return raw_text
    return _GENERIC_STOCK_NAME_BY_LANGUAGE[normalize_report_language(language)]


def get_sentiment_label(score: int, language: Optional[str]) -> str:
    """Return localized sentiment label by score band."""
    normalized = normalize_report_language(language)

    bands_vi = [(80, "Rất Lạc Quan"), (60, "Lạc Quan"), (40, "Trung Lập"), (20, "Bi Quan")]
    bands_en = [(80, "Very Bullish"), (60, "Bullish"), (40, "Neutral"), (20, "Bearish")]
    bands_zh = [(80, "极度乐观"), (60, "乐观"), (40, "中性"), (20, "悲观")]

    bands = {"vi": bands_vi, "en": bands_en, "zh": bands_zh}.get(normalized, bands_vi)
    for threshold, label in bands:
        if score >= threshold:
            return label
    return {"vi": "Rất Bi Quan", "en": "Very Bearish", "zh": "极度悲观"}.get(normalized, "Rất Bi Quan")
