# -*- coding: utf-8 -*-
"""
===================================
Data Provider Layer - Package Init
===================================

Implements Strategy Pattern for multiple VN stock data sources:
1. Unified data-fetching interface
2. Automatic failover between sources
3. Rate-limit/anti-ban flow control

Data source priority (dynamic):
  0. VnstockFetcher (Priority 0) — Primary: vnstock library (HOSE/HNX)
  1. TCBSFetcher    (Priority 1) — Fallback: TCBS realtime API
  2. (Future)       VNDirectFetcher / FireAntFetcher

Markets supported: HOSE, HNX (Vietnam only)
"""

from .base import BaseFetcher, DataFetcherManager, is_vn_stock_code
from .vnstock_fetcher import VnstockFetcher
from .tcbs_fetcher import TCBSFetcher

__all__ = [
    "BaseFetcher",
    "DataFetcherManager",
    "is_vn_stock_code",
    "VnstockFetcher",
    "TCBSFetcher",
]
