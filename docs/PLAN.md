# Vietnam Migration - Execution Plan (PLAN.md)

> Generated: 2026-03-31
> Source: `docs/vietnam-migration-tasks.md` + `docs/vietnam-migration-plan.md`
> Status: **Awaiting user approval → Phase 2 implementation**

---

## 🏛️ Agent Assignment Matrix

| Phase | Agent | Scope | Risk |
|-------|-------|-------|------|
| 1 | `backend-specialist` | Cleanup legacy code | Medium |
| 2 | `backend-specialist` | Data Provider (VN fetchers + base.py) | High |
| 3 | `backend-specialist` | Reporting, Prompt, Market Review | Low |
| 4 | `backend-specialist` | Strategy YAML migration | High |
| 5 | `backend-specialist` | Notification & Bot commands | Very Low |
| 6 | `frontend-specialist` + `debugger` | Web/Desktop UI + QA | Medium |

---

## 📍 Phase 1: Cleanup & Foundation

### Files to DELETE
```
data_provider/
  ├── efinance_fetcher.py    [CN market, ~50KB]
  ├── akshare_fetcher.py     [CN market, ~76KB]
  ├── tushare_fetcher.py     [CN market, ~49KB]
  ├── pytdx_fetcher.py       [CN market, ~16KB]
  ├── baostock_fetcher.py    [CN market, ~13KB]
  ├── yfinance_fetcher.py    [US market, ~29KB]
  ├── tickflow_fetcher.py    [CN/TW market, ~12KB]
  └── us_index_mapping.py    [US index mapping, ~3KB]

src/notification_sender/
  ├── wechat_sender.py       [CN channel]
  ├── feishu_sender.py       [CN channel]
  ├── pushplus_sender.py     [CN channel]
  ├── serverchan3_sender.py  [CN channel]
  ├── astrbot_sender.py      [CN channel]
  └── pushover_sender.py     [low VN usage]

bot/platforms/
  ├── dingtalk.py            [CN platform]
  ├── dingtalk_stream.py     [CN platform]
  └── feishu_stream.py       [CN platform]

src/
  └── feishu_doc.py          [CN platform]
```

### Files to MODIFY (Phase 1)
- `data_provider/__init__.py` — Remove all CN fetcher imports
- `data_provider/base.py` — Remove `_get_tickflow_fetcher()`, `feishu`/`wechat` references, `_is_us_market()`, `_is_hk_market()`, `is_bse_code()`, `is_kc_cy_stock()` functions
- `src/notification_sender/__init__.py` — Remove deleted sender imports
- `bot/platforms/__init__.py` — Remove DingTalk/Feishu imports
- `src/config.py` — Remove: `TUSHARE_TOKEN`, `TICKFLOW_API_KEY`, WeChat/Feishu/DingTalk configs
- `.env.example` — Remove CN-specific env vars

### DoD (Definition of Done)
- [ ] `python -m py_compile data_provider/base.py` passes
- [ ] `python -m py_compile data_provider/__init__.py` passes
- [ ] `python -m pytest tests/ -x -q --ignore=tests/network` passes

---

## 📍 Phase 2: Data Provider & Core Adapter

### Files to CREATE
```
data_provider/
  ├── vnstock_fetcher.py     [NEW — Primary VN data source]
  └── tcbs_fetcher.py        [NEW — Realtime + fallback]
```

### `vnstock_fetcher.py` spec
```python
class VnstockFetcher(BaseFetcher):
    name = "VnstockFetcher"
    priority = 0  # Highest priority

    # Implements:
    # - _fetch_raw_data(code, start, end) → OHLCV DataFrame
    # - _normalize_data() → standard columns
    # - get_main_indices(region="vn") → VNINDEX, VN30
    # - get_fundamental_data(code) → P/E, EPS, EPS TTM
    # - get_dividends(code) → dividend history
```

### `tcbs_fetcher.py` spec
```python
class TCBSFetcher(BaseFetcher):
    name = "TCBSFetcher"
    priority = 1  # Fallback

    # Implements:
    # - _fetch_raw_data() → OHLCV
    # - get_realtime_data(code) → tick data
    # - get_intraday(code) → intraday OHLCV
```

### `data_provider/base.py` additions
```python
# New VN-specific functions to ADD:
def is_vn_stock_code(code: str) -> bool:
    """VN stock: 3 uppercase letters (VCB, FPT)
       VN ETF: 6-8 chars (E1VFVN30, FUEVFVND)"""
    pattern = r'^[A-Z]{3}$|^[A-Z0-9]{6,8}$'
    return bool(re.match(pattern, code.upper().strip()))

def _market_tag(code: str) -> str:
    """Returns: 'vn' for all VN codes"""
    return "vn"  # Simplified — only VN market
```

### `data_provider/__init__.py` new content
```python
from .base import BaseFetcher, DataFetcherManager
from .vnstock_fetcher import VnstockFetcher
from .tcbs_fetcher import TCBSFetcher
```

### Core files to MODIFY
```
src/core/trading_calendar.py
  - MARKET_EXCHANGE: {"vn": "XSTC"}  (replace XSHG/XHKG/XNYS)
  - MARKET_TIMEZONE: {"vn": "Asia/Ho_Chi_Minh"}
  - get_market_for_stock(): use is_vn_stock_code() from data_provider
  - get_open_markets_today(): only check "vn"
  - compute_effective_region(): accept "vn" as valid config

src/core/market_profile.py
  - Remove CN_PROFILE/US_PROFILE
  - Add VN_PROFILE: {indices: ["VNINDEX", "VN30"], timezone: "Asia/Ho_Chi_Minh",
                     exchanges: ["HOSE", "HNX"], currency: "VND"}

src/core/market_context.py
  - Simplify: always return "vn" regardless of code
  - Remove get_market_for_stock multi-market logic
```

### DoD
- [ ] `VnstockFetcher().get_daily_data("VCB", days=365)` returns non-empty DataFrame
- [ ] `VnstockFetcher().get_daily_data("E1VFVN30", days=365)` returns non-empty DataFrame
- [ ] `TCBSFetcher().get_realtime_data("VCB")` returns current price

---

## 📍 Phase 3: Reporting, Prompt & Market Review

### Files to MODIFY
```
src/report_language.py
  - Default lang: "vi"
  - Remove "zh" language support
  - Keep "en" as fallback only

src/core/market_review.py
  - Remove CN/US review logic
  - Call only VNINDEX + VN30 via VnstockFetcher
  - Fetch news from Vietstock / FireAnt API

src/core/pipeline.py
  - market_context: hardcode "vn"
  - Remove cn/us/hk branching

src/analyzer.py
  - Update system prompt: "You are a Vietnamese stock market analyst..."
  - Response language: "vi"

src/market_analyzer.py
  - VN market analysis context
  - Sectors: Banking, Real Estate, Steel, Retail, Tech (VN)

src/services/name_to_code_resolver.py
  - VN name mapping: "Vietcombank" → "VCB", "FPT Corporation" → "FPT"
  - Use vnstock company listing as lookup source
```

### News crawler targets
```python
VIETSTOCK_NEWS_URL = "https://vietstock.vn/tin-tuc-chung-khoan"
FIREANT_API_BASE = "https://restv2.fireant.vn"  # Public REST API available
```

### DoD
- [ ] Bot generates 1 full VN stock report in Vietnamese (no Chinese characters)
- [ ] Market review returns VNINDEX + VN30 data only

---

## 📍 Phase 4: Strategy Engines

### 11 existing YAML files to UPDATE (all in `strategies/`)

Each YAML needs these parameter changes:
```yaml
# OLD (CN market)
price_limit: 0.10  # 10%
lot_size: 1        # 1 share

# NEW (VN market)
price_limit_up: 0.07    # HOSE +7%
price_limit_down: -0.07 # HOSE -7%
# For HNX: ±10%
lot_size: 100           # Must be multiple of 100
settlement_rule: "T+2.5"
short_selling: false    # Not legally available in VN
```

Files:
- `bottom_volume.yaml` → adjust limits
- `box_oscillation.yaml` → adjust limits
- `bull_trend.yaml` → adjust limits
- `chan_theory.yaml` → adjust limits
- `dragon_head.yaml` → adjust limits
- `emotion_cycle.yaml` → adjust limits
- `ma_golden_cross.yaml` → adjust limits
- `one_yang_three_yin.yaml` → adjust limits
- `shrink_pullback.yaml` → adjust limits
- `volume_breakout.yaml` → adjust limits
- `wave_theory.yaml` → adjust limits

### 3 new YAML files to CREATE
```
strategies/
  ├── vn30_rotation.yaml    [VN30 rotation strategy — empty scaffold]
  ├── vn_bank_sector.yaml   [Banking sector: VCB, CTG, BID, TCB, MBB]
  └── vn_penny_alert.yaml   [Penny stock alert: price < 5000 VND]
```

### `src/core/backtest_engine.py` changes
- Add T+2.5 settlement constraint: never generate sell signal for stocks bought within 2.5 days
- Validate lot size is multiple of 100 before generating buy signal
- Add `price_limit_up/price_limit_down` per exchange rule

### DoD
- [ ] `python main.py --dry-run --stocks VCB` runs without strategy errors
- [ ] Backtest on any YAML does not error on lot size or price limit

---

## 📍 Phase 5: Notification & Bot Commands

### Files to MODIFY
```
src/notification_sender/__init__.py
  - PRIMARY: Telegram, Discord
  - OPTIONAL: Email (SMTP), Slack, Custom Webhook
  - Remove: wechat, feishu, pushplus, serverchan3, astrbot, pushover

src/notification_sender/telegram_sender.py
  - Add inline keyboard button: [📊 Vietstock] [🔥 FireAnt]
  - Link format: https://vietstock.vn/TICKER, https://fireant.vn/symbol/TICKER

bot/commands/research.py (currently open in editor)
  - Update regex: accept VN 3-letter codes + ETF codes
  - Update help text in Vietnamese

bot/platforms/discord.py
  - Update /research, /chart command regex for VN format
  - Response language: vi
```

### `src/notification_sender/zalo_sender.py` — CREATE
```python
class ZaloSender:
    """Zalo OA webhook/bot notification (placeholder — awaiting Zalo OA approval)"""
    # Implementation deferred — flag as optional in config
```

### `.env.example` additions
```env
# Zalo (optional, requires Zalo OA approved account)
ZALO_WEBHOOK_URL=
ZALO_OA_TOKEN=
TCBS_API_KEY=
VN_DATA_SOURCE_PRIORITY=vnstock,tcbs,vndirect
```

### DoD
- [ ] `/research FPT` from Discord returns Vietnamese report
- [ ] Telegram message has inline keyboard linking to Vietstock/FireAnt
- [ ] VN stock code regex accepts: "VCB", "E1VFVN30", "FUEVFVND"

---

## 📍 Phase 6: Web/Desktop UI & QA

### `apps/dsa-web/` changes
- Replace EN/ZH orphan strings with VI translations
- Chart timezone: set to `+07:00` / `Asia/Ho_Chi_Minh`
- TradingView widget: `exchange: "HOSE"` for VN tickers
- Display currency as VND (đ) not CNY/USD

### `apps/dsa-desktop/` changes
- `package.json` / `electron-builder.yml`: App name VN-specific
- Icon: update if needed

### Docker changes
```dockerfile
# docker/Dockerfile
ENV TZ=Asia/Ho_Chi_Minh
# Replace Asia/Shanghai
```

### `.github/workflows/daily_analysis.yml`
- cron timezone annotation: `# Vietnam time (UTC+7)`
- Market hours: `09:15-11:30, 13:00-14:45` (HOSE)

### Verification scripts
```bash
cd apps/dsa-web && npm ci && npm run lint && npm run build
python -m pytest tests/ -x -q
python scripts/ci_gate.sh
```

### DoD
- [ ] `npm run build` succeeds in `apps/dsa-web`
- [ ] All UI text in Vietnamese (no orphan Chinese strings)
- [ ] Chart renders with +07:00 timezone

---

## ⚡ Execution Order (Sequential — Do NOT skip phases)

```
Phase 1 (Cleanup)
  → compile check → unit tests
Phase 2 (Data Provider)
  → live data test: VCB, E1VFVN30
Phase 3 (Reporting)
  → generate 1 sample VN report
Phase 4 (Strategies)
  → dry-run backtest
Phase 5 (Bot/Notifications)
  → /research FPT Discord test
Phase 6 (UI + QA)
  → npm build + full test suite
```

---

## 🔴 Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| vnstock API version mismatch | Phase 2 fails | Pin `vnstock==0.2.x`, add fallback to tcbs |
| `exchange_calendars` no XSTC | trading_calendar fails | Add HOSE manual holiday list as fallback |
| Zalo OA not approved | No Zalo channel | Mark as optional, default to Telegram |
| Breaking import chains | All phases | py_compile check every phase |
| strategies YAML silent errors | Wrong signals | Add schema validation in backtest_engine |

---

## 📋 Rollback Plan

1. **Git tag before start:** `git tag pre-vn-migration`
2. **Each phase:** Commit separately with `[phase-N]` prefix
3. **Rollback:** `git checkout pre-vn-migration`
4. **Deleted files:** Recoverable via git history

---

*This plan was generated by @orchestrator after codebase exploration.*
*Implementation starts after user approved with "Y".*
