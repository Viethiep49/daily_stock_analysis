# -*- coding: utf-8 -*-
"""
===================================
Unified Realtime Quote Type Definitions & Circuit Breaker
===================================

Design goals:
1. Unify the realtime quote return structure across all data sources
2. Implement a circuit-breaker/cooldown mechanism to avoid repeated requests on
   consecutive failures
3. Support failover across multiple data sources

Usage:
- All Fetcher.get_realtime_quote() calls return a UnifiedRealtimeQuote
- CircuitBreaker manages the circuit-breaker state of each data source
"""

import logging
import time
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Union
from enum import Enum

logger = logging.getLogger(__name__)


# ============================================
# Generic type-conversion utility functions
# ============================================
# Design note:
# Raw data types returned by different data sources are inconsistent
# (str/float/int/NaN). These functions provide uniform conversion to avoid
# duplicating the same logic across individual Fetchers.

def safe_float(val: Any, default: Optional[float] = None) -> Optional[float]:
    """
    Safely convert a value to float.

    Handles:
    - None / empty string → default
    - pandas NaN / numpy NaN → default
    - numeric string → float
    - already numeric → float

    Args:
        val: value to convert
        default: fallback value when conversion fails

    Returns:
        converted float, or the default value
    """
    try:
        if val is None:
            return default
        
        # Handle strings
        if isinstance(val, str):
            val = val.strip()
            if val == "" or val == "-" or val == "--":
                return default

        # Handle pandas/numpy NaN
        # Use math.isnan instead of pd.isna to avoid a hard dependency on pandas
        import math
        try:
            if math.isnan(float(val)):
                return default
        except (ValueError, TypeError):
            pass
        
        return float(val)
    except (ValueError, TypeError):
        return default


def safe_int(val: Any, default: Optional[int] = None) -> Optional[int]:
    """
    Safely convert a value to int.

    Converts to float first and then truncates, to handle cases like "123.0".

    Args:
        val: value to convert
        default: fallback value when conversion fails

    Returns:
        converted integer, or the default value
    """
    f_val = safe_float(val, default=None)
    if f_val is not None:
        return int(f_val)
    return default


class RealtimeSource(Enum):
    """Realtime quote data sources."""
    EFINANCE = "efinance"           # East Money (efinance library)
    AKSHARE_EM = "akshare_em"       # East Money (akshare library)
    AKSHARE_SINA = "akshare_sina"   # Sina Finance
    AKSHARE_QQ = "akshare_qq"       # Tencent Finance
    TUSHARE = "tushare"             # Tushare Pro
    TENCENT = "tencent"             # Tencent direct
    SINA = "sina"                   # Sina direct
    STOOQ = "stooq"                 # Stooq US stock fallback
    FALLBACK = "fallback"           # Degraded fallback


@dataclass
class UnifiedRealtimeQuote:
    """
    Unified realtime quote data structure.

    Design principles:
    - Fields returned by different data sources may vary; missing fields are
      represented as None
    - The main flow uses getattr(quote, field, None) for compatibility
    - The source field records the data origin for debugging purposes
    """
    code: str
    name: str = ""
    source: RealtimeSource = RealtimeSource.FALLBACK
    
    # === Core price data (available in almost all sources) ===
    price: Optional[float] = None           # Latest price
    change_pct: Optional[float] = None      # Change percentage (%)
    change_amount: Optional[float] = None   # Change amount

    # === Volume/price indicators (may be absent in some sources) ===
    volume: Optional[int] = None            # Trading volume (lots)
    amount: Optional[float] = None          # Turnover (CNY)
    volume_ratio: Optional[float] = None    # Volume ratio
    turnover_rate: Optional[float] = None   # Turnover rate (%)
    amplitude: Optional[float] = None       # Amplitude (%)

    # === Price range ===
    open_price: Optional[float] = None      # Open price
    high: Optional[float] = None            # High price
    low: Optional[float] = None             # Low price
    pre_close: Optional[float] = None       # Previous close price

    # === Valuation indicators (only available in full-feed APIs like East Money) ===
    pe_ratio: Optional[float] = None        # P/E ratio (dynamic)
    pb_ratio: Optional[float] = None        # P/B ratio
    total_mv: Optional[float] = None        # Total market cap (CNY)
    circ_mv: Optional[float] = None         # Circulating market cap (CNY)

    # === Other indicators ===
    change_60d: Optional[float] = None      # 60-day change (%)
    high_52w: Optional[float] = None        # 52-week high
    low_52w: Optional[float] = None         # 52-week low
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary (filtering out None values)."""
        result = {
            'code': self.code,
            'name': self.name,
            'source': self.source.value,
        }
        # Only include fields that are not None
        optional_fields = [
            'price', 'change_pct', 'change_amount', 'volume', 'amount',
            'volume_ratio', 'turnover_rate', 'amplitude',
            'open_price', 'high', 'low', 'pre_close',
            'pe_ratio', 'pb_ratio', 'total_mv', 'circ_mv',
            'change_60d', 'high_52w', 'low_52w'
        ]
        for f in optional_fields:
            val = getattr(self, f, None)
            if val is not None:
                result[f] = val
        return result
    
    def has_basic_data(self) -> bool:
        """Check whether basic price data is available."""
        return self.price is not None and self.price > 0

    def has_volume_data(self) -> bool:
        """Check whether volume/price data is available."""
        return self.volume_ratio is not None or self.turnover_rate is not None


@dataclass
class ChipDistribution:
    """
    Chip distribution data.

    Reflects the cost distribution of holdings and profit/loss situation.
    """
    code: str
    date: str = ""
    source: str = "akshare"

    # Profit/loss situation
    profit_ratio: float = 0.0     # Profitable position ratio (0-1)
    avg_cost: float = 0.0         # Average cost

    # Chip concentration
    cost_90_low: float = 0.0      # 90% chip cost lower bound
    cost_90_high: float = 0.0     # 90% chip cost upper bound
    concentration_90: float = 0.0  # 90% chip concentration (smaller = more concentrated)

    cost_70_low: float = 0.0      # 70% chip cost lower bound
    cost_70_high: float = 0.0     # 70% chip cost upper bound
    concentration_70: float = 0.0  # 70% chip concentration
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary."""
        return {
            'code': self.code,
            'date': self.date,
            'source': self.source,
            'profit_ratio': self.profit_ratio,
            'avg_cost': self.avg_cost,
            'cost_90_low': self.cost_90_low,
            'cost_90_high': self.cost_90_high,
            'concentration_90': self.concentration_90,
            'concentration_70': self.concentration_70,
        }
    
    def get_chip_status(self, current_price: float) -> str:
        """
        Get a description of the chip status.

        Args:
            current_price: current stock price

        Returns:
            chip status description string
        """
        status_parts = []

        # Profitable position ratio analysis
        if self.profit_ratio >= 0.9:
            status_parts.append("Extremely high profit ratio (>90% in profit)")
        elif self.profit_ratio >= 0.7:
            status_parts.append("High profit ratio (70-90% in profit)")
        elif self.profit_ratio >= 0.5:
            status_parts.append("Medium profit ratio (50-70% in profit)")
        elif self.profit_ratio >= 0.3:
            status_parts.append("Medium trapped ratio (50-70% trapped)")
        elif self.profit_ratio >= 0.1:
            status_parts.append("High trapped ratio (70-90% trapped)")
        else:
            status_parts.append("Extremely high trapped ratio (>90% trapped)")

        # Chip concentration analysis (90% concentration < 10% means concentrated)
        if self.concentration_90 < 0.08:
            status_parts.append("Chips highly concentrated")
        elif self.concentration_90 < 0.15:
            status_parts.append("Chips moderately concentrated")
        elif self.concentration_90 < 0.25:
            status_parts.append("Chips moderately dispersed")
        else:
            status_parts.append("Chips widely dispersed")

        # Relationship between cost and current price
        if current_price > 0 and self.avg_cost > 0:
            cost_diff = (current_price - self.avg_cost) / self.avg_cost * 100
            if cost_diff > 20:
                status_parts.append(f"Current price {cost_diff:.1f}% above average cost")
            elif cost_diff > 5:
                status_parts.append(f"Current price slightly above cost by {cost_diff:.1f}%")
            elif cost_diff > -5:
                status_parts.append("Current price near average cost")
            else:
                status_parts.append(f"Current price {abs(cost_diff):.1f}% below average cost")

        return ", ".join(status_parts)


class CircuitBreaker:
    """
    Circuit breaker — manages the circuit-breaker/cooldown state of data sources.

    Strategy:
    - Enter the OPEN (tripped) state after N consecutive failures
    - Skip the data source while in the OPEN state
    - Automatically transition to HALF_OPEN after the cooldown period
    - In HALF_OPEN: a single success fully recovers; a failure re-trips the breaker

    State machine:
    CLOSED (normal) --N failures--> OPEN (tripped) --cooldown elapsed--> HALF_OPEN
    HALF_OPEN --success--> CLOSED
    HALF_OPEN --failure--> OPEN
    """

    # State constants
    CLOSED = "closed"        # Normal state
    OPEN = "open"            # Tripped state (unavailable)
    HALF_OPEN = "half_open"  # Half-open state (probe request)

    def __init__(
        self,
        failure_threshold: int = 3,       # Consecutive failure count threshold
        cooldown_seconds: float = 300.0,  # Cooldown duration in seconds (default 5 minutes)
        half_open_max_calls: int = 1      # Maximum probe attempts in half-open state
    ):
        self.failure_threshold = failure_threshold
        self.cooldown_seconds = cooldown_seconds
        self.half_open_max_calls = half_open_max_calls
        
        # Per-source state dict: {source_name: {state, failures, last_failure_time, half_open_calls}}
        self._states: Dict[str, Dict[str, Any]] = {}

    def _get_state(self, source: str) -> Dict[str, Any]:
        """Get or initialize the state for a data source."""
        if source not in self._states:
            self._states[source] = {
                'state': self.CLOSED,
                'failures': 0,
                'last_failure_time': 0.0,
                'half_open_calls': 0
            }
        return self._states[source]
    
    def is_available(self, source: str) -> bool:
        """
        Check whether a data source is available.

        Returns True if a request attempt is allowed.
        Returns False if the data source should be skipped.
        """
        state = self._get_state(source)
        current_time = time.time()

        if state['state'] == self.CLOSED:
            return True

        if state['state'] == self.OPEN:
            # Check whether the cooldown period has elapsed
            time_since_failure = current_time - state['last_failure_time']
            if time_since_failure >= self.cooldown_seconds:
                # Cooldown complete — transition to half-open
                state['state'] = self.HALF_OPEN
                state['half_open_calls'] = 0
                logger.info(f"[CircuitBreaker] {source} cooldown complete, entering half-open state")
                return True
            else:
                remaining = self.cooldown_seconds - time_since_failure
                logger.debug(f"[CircuitBreaker] {source} is tripped, remaining cooldown: {remaining:.0f}s")
                return False

        if state['state'] == self.HALF_OPEN:
            # Limit request count while in half-open state
            if state['half_open_calls'] < self.half_open_max_calls:
                return True
            return False

        return True
    
    def record_success(self, source: str) -> None:
        """Record a successful request."""
        state = self._get_state(source)

        if state['state'] == self.HALF_OPEN:
            # Success in half-open state — fully recover
            logger.info(f"[CircuitBreaker] {source} half-open probe succeeded, recovering to normal")

        # Reset state
        state['state'] = self.CLOSED
        state['failures'] = 0
        state['half_open_calls'] = 0

    def record_failure(self, source: str, error: Optional[str] = None) -> None:
        """Record a failed request."""
        state = self._get_state(source)
        current_time = time.time()

        state['failures'] += 1
        state['last_failure_time'] = current_time

        if state['state'] == self.HALF_OPEN:
            # Failure in half-open state — remain tripped
            state['state'] = self.OPEN
            state['half_open_calls'] = 0
            logger.warning(f"[CircuitBreaker] {source} half-open probe failed, remaining tripped for {self.cooldown_seconds}s")
        elif state['failures'] >= self.failure_threshold:
            # Threshold reached — trip the breaker
            state['state'] = self.OPEN
            logger.warning(f"[CircuitBreaker] {source} failed {state['failures']} consecutive times, tripping "
                          f"(cooldown {self.cooldown_seconds}s)")
            if error:
                logger.warning(f"[CircuitBreaker] Last error: {error}")

    def get_status(self) -> Dict[str, str]:
        """Get the state of all data sources."""
        return {source: info['state'] for source, info in self._states.items()}

    def reset(self, source: Optional[str] = None) -> None:
        """Reset circuit breaker state."""
        if source:
            if source in self._states:
                del self._states[source]
        else:
            self._states.clear()


# Global circuit breaker instance (dedicated to realtime quotes)
_realtime_circuit_breaker = CircuitBreaker(
    failure_threshold=3,      # Trip after 3 consecutive failures
    cooldown_seconds=300.0,   # 5-minute cooldown
    half_open_max_calls=1
)

# Chip-data circuit breaker (more conservative strategy because this API is less stable)
_chip_circuit_breaker = CircuitBreaker(
    failure_threshold=2,      # Trip after 2 consecutive failures
    cooldown_seconds=600.0,   # 10-minute cooldown
    half_open_max_calls=1
)


def get_realtime_circuit_breaker() -> CircuitBreaker:
    """Get the realtime quote circuit breaker."""
    return _realtime_circuit_breaker


def get_chip_circuit_breaker() -> CircuitBreaker:
    """Get the chip-data circuit breaker."""
    return _chip_circuit_breaker
