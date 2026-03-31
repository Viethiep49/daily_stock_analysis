# -*- coding: utf-8 -*-
"""
===================================
VnstockFetcher — Primary VN Data Source
===================================

Uses the `vnstock` library (vnstock3-compatible) to fetch:
- OHLCV daily candle data (HOSE/HNX)
- Fundamental data: P/E, EPS, EPS TTM
- Dividend history
- Realtime indices: VNINDEX, VN30

Supported code formats:
  - 3-char equities: VCB, FPT, VNM, HPG
  - 6-8 char ETF:    E1VFVN30, FUEVFVND

Priority: 0 (highest — primary source)
"""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import pandas as pd

from .base import BaseFetcher, DataFetchError, is_vn_stock_code

logger = logging.getLogger(__name__)

# vnstock availability guard
_VNSTOCK_AVAILABLE = False
try:
    from vnstock import Vnstock  # vnstock3 API
    _VNSTOCK_AVAILABLE = True
except ImportError:
    try:
        import vnstock as _vns  # legacy vnstock
        _VNSTOCK_AVAILABLE = True
    except ImportError:
        logger.warning(
            "vnstock not installed. Run: pip install vnstock\n"
            "VnstockFetcher will be unavailable."
        )


class VnstockFetcher(BaseFetcher):
    """
    Primary fetcher for Vietnam stock market data via vnstock library.

    Supports HOSE and HNX listed securities including ETFs.
    """

    name = "VnstockFetcher"
    priority = 0  # Highest priority in the VN data source chain

    def __init__(self) -> None:
        if not _VNSTOCK_AVAILABLE:
            raise ImportError(
                "vnstock is not installed. Run: pip install vnstock"
            )

    # ------------------------------------------------------------------
    # Internal: normalize raw vnstock DataFrame to standard columns
    # ------------------------------------------------------------------

    def _fetch_raw_data(
        self, stock_code: str, start_date: str, end_date: str
    ) -> pd.DataFrame:
        """
        Fetch OHLCV daily data from vnstock.

        Args:
            stock_code: VN stock code (e.g. 'VCB', 'E1VFVN30')
            start_date: 'YYYY-MM-DD'
            end_date:   'YYYY-MM-DD'

        Returns:
            Raw DataFrame from vnstock (columns vary by version)
        """
        code = stock_code.strip().upper()
        logger.debug("[VnstockFetcher] Fetching %s: %s → %s", code, start_date, end_date)

        try:
            stock = Vnstock().stock(symbol=code, source="VCI")
            df = stock.quote.history(
                start=start_date,
                end=end_date,
                interval="1D",
            )
            if df is None or (isinstance(df, pd.DataFrame) and df.empty):
                raise DataFetchError(f"[VnstockFetcher] No data returned for {code}")
            return df
        except DataFetchError:
            raise
        except Exception as exc:
            raise DataFetchError(
                f"[VnstockFetcher] Failed to fetch {code}: {exc}"
            ) from exc

    def _normalize_data(self, df: pd.DataFrame, stock_code: str) -> pd.DataFrame:
        """
        Normalize vnstock raw columns to standard schema:
        ['date', 'open', 'high', 'low', 'close', 'volume', 'amount', 'pct_chg']
        """
        df = df.copy()

        # vnstock3 column mapping
        column_map = {
            "time": "date",
            "open": "open",
            "high": "high",
            "low": "low",
            "close": "close",
            "volume": "volume",
            "value": "amount",    # value = turnover in VND
        }
        df.rename(columns=column_map, inplace=True)

        # Compute pct_chg if missing
        if "pct_chg" not in df.columns and "close" in df.columns:
            df["pct_chg"] = df["close"].pct_change() * 100

        # Ensure amount column exists
        if "amount" not in df.columns:
            df["amount"] = 0.0

        return df

    # ------------------------------------------------------------------
    # Market indices
    # ------------------------------------------------------------------

    def get_main_indices(self, region: str = "vn") -> Optional[List[Dict[str, Any]]]:
        """
        Fetch VNINDEX and VN30 realtime data.

        Returns:
            List of dicts with keys: code, name, current, change, change_pct
        """
        if not _VNSTOCK_AVAILABLE:
            return None

        indices = [
            {"code": "VNINDEX", "name": "VN-Index"},
            {"code": "VN30",    "name": "VN30"},
        ]
        results = []
        for idx in indices:
            try:
                stock = Vnstock().stock(symbol=idx["code"], source="VCI")
                df = stock.quote.history(
                    start=(datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
                    end=datetime.now().strftime("%Y-%m-%d"),
                    interval="1D",
                )
                if df is not None and not df.empty:
                    latest = df.iloc[-1]
                    prev = df.iloc[-2] if len(df) > 1 else latest
                    current = float(latest.get("close", 0))
                    prev_close = float(prev.get("close", current))
                    change = current - prev_close
                    change_pct = (change / prev_close * 100) if prev_close else 0.0
                    results.append({
                        "code": idx["code"],
                        "name": idx["name"],
                        "current": round(current, 2),
                        "change": round(change, 2),
                        "change_pct": round(change_pct, 2),
                        "volume": float(latest.get("volume", 0)),
                        "amount": float(latest.get("value", 0)),
                    })
            except Exception as exc:
                logger.warning("[VnstockFetcher] Index %s fetch failed: %s", idx["code"], exc)

        return results if results else None

    # ------------------------------------------------------------------
    # Fundamental data
    # ------------------------------------------------------------------

    def get_fundamental_data(self, stock_code: str) -> Optional[Dict[str, Any]]:
        """
        Fetch fundamental metrics for VN stock.

        Returns:
            Dict with keys: pe, eps, eps_ttm, roe, roa, book_value
        """
        code = stock_code.strip().upper()
        try:
            stock = Vnstock().stock(symbol=code, source="VCI")
            ratio = stock.finance.ratio(period="quarter", lang="en")
            if ratio is None or (isinstance(ratio, pd.DataFrame) and ratio.empty):
                return None
            latest = ratio.iloc[-1].to_dict() if isinstance(ratio, pd.DataFrame) else {}
            return {
                "pe": latest.get("priceToEarning"),
                "eps": latest.get("earningPerShare"),
                "roe": latest.get("returnOnEquity"),
                "roa": latest.get("returnOnAsset"),
                "book_value": latest.get("bookValuePerShare"),
            }
        except Exception as exc:
            logger.warning("[VnstockFetcher] Fundamental %s failed: %s", code, exc)
            return None

    def get_dividends(self, stock_code: str) -> Optional[pd.DataFrame]:
        """
        Fetch dividend history for VN stock.

        Returns:
            DataFrame with columns: ex_date, cash_dividend, stock_dividend
        """
        code = stock_code.strip().upper()
        try:
            stock = Vnstock().stock(symbol=code, source="VCI")
            dvd = stock.company.dividends()
            return dvd if isinstance(dvd, pd.DataFrame) and not dvd.empty else None
        except Exception as exc:
            logger.warning("[VnstockFetcher] Dividends %s failed: %s", code, exc)
            return None
