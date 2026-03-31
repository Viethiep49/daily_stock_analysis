# -*- coding: utf-8 -*-
"""
===================================
Trading Calendar — Vietnam Market
===================================

Responsibilities:
1. Determine whether today is a trading day for HOSE / HNX
2. Return today's date in Vietnam timezone (Asia/Ho_Chi_Minh, UTC+7)
3. Support per-stock market-open filtering

Exchange codes (exchange-calendars):
  HOSE → XSTC  (Ho Chi Minh Stock Exchange)

Dependencies:
  exchange-calendars (optional — fail-open when unavailable)
"""

import logging
from datetime import date, datetime
from typing import Optional, Set

logger = logging.getLogger(__name__)

# exchange-calendars availability
_XCALS_AVAILABLE = False
try:
    import exchange_calendars as xcals
    _XCALS_AVAILABLE = True
except ImportError:
    logger.warning(
        "exchange-calendars not installed; trading day check disabled. "
        "Run: pip install exchange-calendars"
    )

# Market → exchange code (exchange-calendars)
# Only Vietnam markets are supported.
MARKET_EXCHANGE = {"vn": "XSTC"}

# Market → IANA timezone
MARKET_TIMEZONE = {"vn": "Asia/Ho_Chi_Minh"}


def get_market_for_stock(code: str) -> Optional[str]:
    """
    Infer market region from a stock code.

    Returns:
        'vn' for any valid VN equity/ETF ticker.
        None if the code is unrecognized (fail-open: treated as open).
    """
    if not code or not isinstance(code, str):
        return None

    from data_provider.base import is_vn_stock_code

    if is_vn_stock_code(code.strip().upper()):
        return "vn"
    return None


def is_market_open(market: str, check_date: date) -> bool:
    """
    Check if the given market is open on the specified date.

    Fail-open: returns True when exchange-calendars is unavailable
    or the date is out of the supported range.

    Args:
        market:     'vn'
        check_date: Date to check

    Returns:
        True if it is a trading day (or fail-open), False otherwise.
    """
    if not _XCALS_AVAILABLE:
        return True
    ex = MARKET_EXCHANGE.get(market)
    if not ex:
        return True
    try:
        cal = xcals.get_calendar(ex)
        session = datetime(check_date.year, check_date.month, check_date.day)
        return cal.is_session(session)
    except Exception as exc:
        logger.warning("trading_calendar.is_market_open fail-open: %s", exc)
        return True


def get_open_markets_today() -> Set[str]:
    """
    Return the set of markets open today in their local timezone.

    Returns:
        Set of market keys — always a subset of {'vn'}.
    """
    if not _XCALS_AVAILABLE:
        return {"vn"}

    result: Set[str] = set()
    from zoneinfo import ZoneInfo

    for mkt, tz_name in MARKET_TIMEZONE.items():
        try:
            tz = ZoneInfo(tz_name)
            today = datetime.now(tz).date()
            if is_market_open(mkt, today):
                result.add(mkt)
        except Exception as exc:
            logger.warning("get_open_markets_today fail-open for %s: %s", mkt, exc)
            result.add(mkt)
    return result


def compute_effective_region(
    config_region: str, open_markets: Set[str]
) -> Optional[str]:
    """
    Compute the effective market-review region given config and open markets.

    Args:
        config_region: From MARKET_REVIEW_REGION — expected value: 'vn'
        open_markets:  Markets open today (from get_open_markets_today)

    Returns:
        None  → caller uses config default (check disabled)
        ''    → Vietnam market is closed today; skip market review
        'vn'  → Vietnam market is open; proceed with review
    """
    # Normalize: any non-'vn' value falls back to 'vn'
    if config_region not in ("vn",):
        config_region = "vn"
    return "vn" if "vn" in open_markets else ""
