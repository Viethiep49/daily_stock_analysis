# Vietnam Market Migration — Progress Tracker

> Last updated: 2026-03-31

## Commits đã thực hiện

| Commit | Phase | Nội dung |
|--------|-------|----------|
| `pre-vn-migration` | tag | Safety tag trước khi bắt đầu |
| phase 1+2 | Phase 1 + 2 | Xóa CN/US fetchers, thêm vnstock+tcbs, trading_calendar, market_profile, market_context |
| phase 3 | Phase 3 | Thêm ngôn ngữ `vi`, VN market review, Zalo stub |
| phase 4 | Phase 4 | Migrate 11 strategy YAMLs sang VN rules, tạo 3 strategy VN mới |
| phase 5 | Phase 5 | Dịch telegram_sender sang English, fix regex VN trong research.py |

---

## Phase Status

### ✅ Phase 1 — Cleanup (DONE)
- [x] Xóa `efinance`, `akshare`, `tushare`, `pytdx`, `baostock`, `yfinance`, `tickflow` fetchers
- [x] Xóa WeChat, Feishu, PushPlus, Server酱3, AstrBot, Pushover senders
- [x] Xóa DingTalk, Feishu Stream bot platforms
- [x] Xóa `feishu_doc.py`
- [x] Update `data_provider/__init__.py`, `notification_sender/__init__.py`, `bot/platforms/__init__.py`

### ✅ Phase 2 — VN Foundation (DONE)
- [x] Tạo `data_provider/vnstock_fetcher.py` (primary)
- [x] Tạo `data_provider/tcbs_fetcher.py` (fallback)
- [x] Refactor `data_provider/base.py`: xóa CN/HK/US helpers, thêm `is_vn_stock_code()`
- [x] Rewrite `src/core/trading_calendar.py` → VN only (HOSE=XSTC, UTC+7)
- [x] Rewrite `src/core/market_profile.py` → VN only (VNINDEX, VN30)
- [x] Rewrite `src/market_context.py` → VN only (`detect_market()` always returns `vn`)
- [x] Update `main.py`: xóa Feishu Doc block, xóa DingTalk/Feishu stream clients

### ✅ Phase 3 — Reporting & Language (DONE)
- [x] `src/report_language.py`: thêm `vi` làm default language với full Vietnamese labels
- [x] `src/core/market_review.py`: rewrite cho VN only (VNINDEX + VN30)
- [x] `src/notification_sender/zalo_sender.py`: tạo stub (deferred)

### ✅ Phase 4 — Strategy Engine (DONE)
- [x] 11 strategy YAMLs: thêm `vn_market` block (±7%/±10%, lot 100, T+2.5, no short-selling)
- [x] 11 strategy YAMLs: dịch `display_name` và `description` sang tiếng Việt
- [x] Tạo 3 VN scaffold strategies: `vn30_rotation.yaml`, `vn_bank_sector.yaml`, `vn_penny_alert.yaml`

### ✅ Phase 5 — Notifications & Bot (PARTIAL)
- [x] `telegram_sender.py`: dịch tất cả comment/docstring sang English
- [x] `bot/commands/research.py`: fix regex VN stock code, cập nhật examples

### ⬜ Phase 6 — Docs & CHANGELOG (TODO)
- [ ] Thêm VN migration entries vào `docs/CHANGELOG.md [Unreleased]`
- [ ] Cập nhật `docs/full-guide_EN.md` — VN data sources, config vars
- [ ] Cập nhật `.env.example` — thêm VN-specific vars
- [ ] Kiểm tra README_EN.md có mention VN market chưa

### ⬜ Phase 7 — CI Gate & Final QA (TODO)
- [ ] Chạy `./scripts/ci_gate.sh` full
- [ ] Kiểm tra `python -m pytest -m "not network"` pass
- [ ] Verify vnstock + TCBS fetcher import không crash
- [ ] Update `bot/commands/__init__.py` nếu còn reference CN commands

---

## Việc còn lại khi resume

1. **Phase 6 Docs**: Cập nhật CHANGELOG + full-guide_EN + .env.example
2. **Phase 7 CI Gate**: Chạy test suite, fix bất kỳ import lỗi nào còn sót
3. **Scan toàn project** tìm references còn sót của CN/US/HK:
   ```bash
   grep -rn "cn\|a.gu\|SHSE\|SZSE\|FinanceFetcher\|AkshareFetch\|TushareFetch" src/ data_provider/ --include="*.py" | grep -v "__pycache__"
   ```

---

## Thông tin quan trọng

- **Git tag an toàn**: `pre-vn-migration`
- **Rollback**: `git checkout pre-vn-migration`
- **Default report language**: đã đổi `zh` → `vi`
- **Telegram Bot setup**: cần TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID trong `.env` (chat với @BotFather)
- **Zalo**: deferred — cần Zalo OA business account
- **vnstock lib**: `pip install vnstock3`
- **TCBS**: public API, không cần API key
