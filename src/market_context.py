# -*- coding: utf-8 -*-
"""
===================================
Market Context — Vietnam Market
===================================

Provides market-specific role descriptions and analysis guidelines
for LLM prompts. Vietnam (HOSE/HNX) is the only supported market.

The detect_market() function always returns 'vn'; the multi-market
routing logic for CN/HK/US has been removed.
"""

from typing import Optional


def detect_market(stock_code: Optional[str]) -> str:
    """
    Return the market tag for the given stock code.

    Vietnam-only build: always returns 'vn' regardless of input.

    Args:
        stock_code: VN ticker like 'VCB', 'E1VFVN30', etc.

    Returns:
        Always 'vn'.
    """
    return "vn"


# Market-specific role descriptions (LLM prompt injection)
_MARKET_ROLES = {
    "vn": {
        "vi": "Chứng khoán Việt Nam (HOSE/HNX)",
        "en": "Vietnam stock market (HOSE/HNX)",
    },
}

# Market-specific analysis guidelines (injected into LLM system prompt)
_MARKET_GUIDELINES = {
    "vn": {
        "vi": (
            "- Đối tượng phân tích là **cổ phiếu Việt Nam** niêm yết trên HOSE hoặc HNX.\n"
            "- Lưu ý các đặc thù thị trường VN: biên độ giá HOSE ±7% / HNX ±10%, "
            "quy tắc thanh toán T+2.5, lô chẵn 100 cổ phiếu, không có bán khống hợp pháp.\n"
            "- Sử dụng ngôn ngữ tiếng Việt chuyên ngành tài chính chứng khoán."
        ),
        "en": (
            "- This analysis covers a **Vietnam-listed stock** (HOSE or HNX).\n"
            "- Vietnam market specifics: HOSE ±7% / HNX ±10% daily price limits, "
            "T+2.5 settlement, lot size multiples of 100, no legal short-selling.\n"
            "- Respond in professional Vietnamese financial terminology."
        ),
    },
}


def get_market_role(stock_code: Optional[str], lang: str = "vi") -> str:
    """
    Return a market-specific role label for the LLM prompt.

    Args:
        stock_code: Ignored (Vietnam only).
        lang:       'vi' (default) or 'en'.

    Returns:
        Role string, e.g. 'Chứng khoán Việt Nam (HOSE/HNX)'.
    """
    lang_key = "en" if lang == "en" else "vi"
    return _MARKET_ROLES["vn"][lang_key]


def get_market_guidelines(stock_code: Optional[str], lang: str = "vi") -> str:
    """
    Return market-specific analysis guidelines for the LLM system prompt.

    Args:
        stock_code: Ignored (Vietnam only).
        lang:       'vi' (default) or 'en'.

    Returns:
        Multi-line string with VN market rules and conventions.
    """
    lang_key = "en" if lang == "en" else "vi"
    return _MARKET_GUIDELINES["vn"][lang_key]
