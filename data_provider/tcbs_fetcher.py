# -*- coding: utf-8 -*-
"""
===================================
TCBSFetcher — VN Realtime & Fallback
===================================

Uses TCBS (Techcom Securities) public REST API to fetch:
- Realtime tick data
- Intraday OHLCV
- Daily historical candles (fallback when vnstock unavailable)

TCBS public API base: https://apipubaws.tcbs.com.vn
No authentication required for public endpoints (rate-limit applies).

Priority: 1 (fallback after VnstockFetcher)
"""

import logging
from typing import Any, Dict, List, Optional

import pandas as pd

from .base import BaseFetcher, DataFetchError

logger = logging.getLogger(__name__)

# TCBS public API endpoints
_TCBS_BASE = "https://apipubaws.tcbs.com.vn"
_TCBS_STOCK_OHLCV = f"{_TCBS_BASE}/stock-insight/v1/stock/bars-long-term"
_TCBS_REALTIME = f"{_TCBS_BASE}/stock-insight/v1/stock/snap-shot"

try:
    import requests as _requests
    _REQUESTS_AVAILABLE = True
except ImportError:
    _REQUESTS_AVAILABLE = False
    logger.warning("requests not installed. TCBSFetcher disabled. Run: pip install requests")


class TCBSFetcher(BaseFetcher):
    """
    Fallback fetcher for Vietnam stock data via TCBS public REST API.

    Used when VnstockFetcher fails or for realtime intraday data.
    """

    name = "TCBSFetcher"
    priority = 1  # Fallback

    _HEADERS = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (compatible; DSA-VN/1.0)",
    }
    _TIMEOUT = 10  # seconds

    def __init__(self) -> None:
        if not _REQUESTS_AVAILABLE:
            raise ImportError("requests is not installed. Run: pip install requests")

    # ------------------------------------------------------------------
    # BaseFetcher interface
    # ------------------------------------------------------------------

    def _fetch_raw_data(
        self, stock_code: str, start_date: str, end_date: str
    ) -> pd.DataFrame:
        """
        Fetch historical OHLCV from TCBS bars-long-term endpoint.

        Args:
            stock_code: VN stock ticker (e.g. 'VCB')
            start_date: 'YYYY-MM-DD'
            end_date:   'YYYY-MM-DD'

        Returns:
            Raw DataFrame with TCBS column names
        """
        import requests
        from datetime import datetime

        code = stock_code.strip().upper()
        # Convert to UNIX timestamps (TCBS uses seconds)
        start_ts = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
        end_ts = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())

        params = {
            "ticker": code,
            "type": "stock",
            "resolution": "D",   # Daily
            "from": start_ts,
            "to": end_ts,
            "countBack": 500,
        }

        try:
            resp = requests.get(
                _TCBS_STOCK_OHLCV,
                params=params,
                headers=self._HEADERS,
                timeout=self._TIMEOUT,
            )
            resp.raise_for_status()
            data = resp.json()
            bars = data.get("data", [])
            if not bars:
                raise DataFetchError(f"[TCBSFetcher] No data for {code}")
            return pd.DataFrame(bars)
        except DataFetchError:
            raise
        except Exception as exc:
            raise DataFetchError(f"[TCBSFetcher] {code} fetch failed: {exc}") from exc

    def _normalize_data(self, df: pd.DataFrame, stock_code: str) -> pd.DataFrame:
        """
        Normalize TCBS columns to standard schema:
        ['date', 'open', 'high', 'low', 'close', 'volume', 'amount', 'pct_chg']
        """
        df = df.copy()

        column_map = {
            "tradingDate": "date",
            "open": "open",
            "high": "high",
            "low": "low",
            "close": "close",
            "volume": "volume",
            "value": "amount",
        }
        df.rename(columns=column_map, inplace=True)

        if "pct_chg" not in df.columns and "close" in df.columns:
            df["pct_chg"] = df["close"].pct_change() * 100

        if "amount" not in df.columns:
            df["amount"] = 0.0

        return df

    # ------------------------------------------------------------------
    # Realtime / Intraday
    # ------------------------------------------------------------------

    def get_realtime_data(self, stock_code: str) -> Optional[Dict[str, Any]]:
        """
        Fetch current snapshot (bid/ask/last price) for a VN stock.

        Args:
            stock_code: e.g. 'VCB'

        Returns:
            Dict with keys: ticker, price, change, change_pct, volume, time
            None on failure.
        """
        import requests

        code = stock_code.strip().upper()
        try:
            resp = requests.get(
                _TCBS_REALTIME,
                params={"listSymbol": code},
                headers=self._HEADERS,
                timeout=self._TIMEOUT,
            )
            resp.raise_for_status()
            data = resp.json()
            snaps = data.get("data", [])
            if not snaps:
                return None
            snap = snaps[0]
            price = float(snap.get("lastPrice", 0))
            ref = float(snap.get("referencePrice", price))
            change = price - ref
            change_pct = (change / ref * 100) if ref else 0.0
            return {
                "ticker": code,
                "price": price,
                "change": round(change, 2),
                "change_pct": round(change_pct, 2),
                "volume": snap.get("totalVolume", 0),
                "time": snap.get("lastTradingDate"),
            }
        except Exception as exc:
            logger.warning("[TCBSFetcher] Realtime %s failed: %s", code, exc)
            return None

    def get_intraday(
        self, stock_code: str, date: Optional[str] = None
    ) -> Optional[pd.DataFrame]:
        """
        Fetch intraday 1-minute OHLCV bars.

        Args:
            stock_code: e.g. 'VCB'
            date: 'YYYY-MM-DD' (defaults to today)

        Returns:
            DataFrame with 1-min bars, or None on failure
        """
        import requests
        from datetime import datetime as dt

        code = stock_code.strip().upper()
        target_date = date or dt.now().strftime("%Y-%m-%d")
        start_ts = int(dt.strptime(target_date, "%Y-%m-%d").timestamp())
        end_ts = start_ts + 86400  # +1 day

        try:
            resp = requests.get(
                _TCBS_STOCK_OHLCV,
                params={
                    "ticker": code,
                    "type": "stock",
                    "resolution": "1",
                    "from": start_ts,
                    "to": end_ts,
                    "countBack": 500,
                },
                headers=self._HEADERS,
                timeout=self._TIMEOUT,
            )
            resp.raise_for_status()
            bars = resp.json().get("data", [])
            if not bars:
                return None
            df = pd.DataFrame(bars)
            df = self._normalize_data(df, code)
            return df
        except Exception as exc:
            logger.warning("[TCBSFetcher] Intraday %s failed: %s", code, exc)
            return None
