# -*- coding: utf-8 -*-
"""
===================================
Market Profile — Vietnam Market
===================================

Defines per-region metadata (indices, news queries, prompt hints)
used by MarketAnalyzer for the daily market review.

Only Vietnam (HOSE + HNX) is supported.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class MarketProfile:
    """Configuration metadata for a market region's review."""

    region: str
    # Primary index code used to gauge overall market sentiment
    mood_index_code: str
    # News search keywords
    news_queries: List[str] = field(default_factory=list)
    # Hint text injected into the LLM prompt for index commentary
    prompt_index_hint: str = ""
    # Whether the market provides advance/decline statistics (HOSE/HNX do)
    has_market_stats: bool = True
    # Whether sector rankings are available
    has_sector_rankings: bool = True


VN_PROFILE = MarketProfile(
    region="vn",
    mood_index_code="VNINDEX",
    news_queries=[
        "VN-Index thị trường chứng khoán",
        "cổ phiếu Việt Nam phân tích",
        "HOSE HNX thị trường hôm nay",
        "chứng khoán Việt Nam tin tức",
    ],
    prompt_index_hint=(
        "Phân tích diễn biến VN-Index, VN30 và các ngành dẫn dắt thị trường Việt Nam. "
        "Chú ý biên độ dao động HOSE ±7%, HNX ±10%, quy tắc T+2.5 và lô chẵn 100 cổ phiếu."
    ),
    has_market_stats=True,
    has_sector_rankings=True,
)


def get_profile(region: str) -> MarketProfile:
    """
    Return the MarketProfile for the given region.

    Currently only 'vn' is supported; any other value maps to VN_PROFILE.
    """
    return VN_PROFILE
