# Kế Hoạch Dự Án — Daily Stock Analysis (VN)

> Cập nhật: 2026-04-07
> Trạng thái tổng: **Vietnam Migration ✅ DONE** — Đang bước vào giai đoạn dọn sạch ngôn ngữ (Translation Cleanup)

---

## Phần 1 — Vietnam Market Migration

Mục tiêu: Chuyển toàn bộ hệ thống từ phục vụ CN/HK/US sang **chỉ thị trường Việt Nam (HOSE + HNX)**.

| Phase | Mô tả | Trạng thái |
|-------|-------|------------|
| Phase 1 | Xóa fetchers TQ/US, xóa kênh thông báo TQ (WeChat, Feishu, DingTalk...) | ✅ DONE |
| Phase 2 | Tích hợp `vnstock_fetcher`, `tcbs_fetcher`, viết lại `trading_calendar`, `market_profile`, `market_context` | ✅ DONE |
| Phase 3 | Ngôn ngữ mặc định `vi`, viết lại `market_review.py` cho VNINDEX+VN30, tạo `zalo_sender.py` stub | ✅ DONE |
| Phase 4 | Migrate 11 strategy YAMLs (±7%/±10%, lot 100, T+2.5), tạo 3 strategy VN mới | ✅ DONE |
| Phase 5 | Dịch `telegram_sender.py` sang English, fix regex VN trong `research.py` | ✅ DONE |
| Phase 6 | Cập nhật `config.py` defaults (report_language=vi, market_review_region=vn), cập nhật docs & `.env.example` | ✅ DONE |
| Phase 7 | CI Gate: chạy `ci_gate.sh`, pytest pass, verify vnstock+TCBS import | ✅ DONE |

**Tham khảo quyết định kiến trúc:** [`docs/vietnam-migration-plan.md`](./vietnam-migration-plan.md)

---

## Phần 2 — Translation Cleanup (Dọn Tiếng Trung)

Mục tiêu: Loại bỏ hoàn toàn tiếng Trung khỏi source code và tài liệu.

### Giai đoạn A — Tài liệu (Docs)

Viết lại sang tiếng Việt chuẩn. Thực hiện thủ công.

| File | Hành động | Trạng thái |
|------|-----------|------------|
| `README.md` | Viết lại toàn bộ cho thị trường VN | ✅ DONE |
| `AGENTS.md` | Dịch sang tiếng Việt | ✅ DONE |
| `docs/FAQ.md` | Dịch + thêm ngữ cảnh HOSE/HNX | ✅ DONE |
| `docs/full-guide.md` | Dọn sạch Chinese text | ✅ DONE |
| `docs/bot-command.md` | Viết lại cho Telegram/Discord VN | ✅ DONE |
| `strategies/README.md` | Dọn sạch Chinese text | ✅ DONE |
| `docs/README_CHT.md` | **Xóa** (không dùng Phồn thể) | ✅ DONE (file không tồn tại) |
| `docs/CHANGELOG.md` | Dọn sạch label tiếng Trung trong `[Unreleased]` | ✅ DONE |

Giữ nguyên (bản EN): `README_EN.md`, `docs/full-guide_EN.md`, `docs/INDEX_EN.md`

---

### Giai đoạn B — Source Code (`.py`)

Tất cả comment/docstring/log còn tiếng Trung → chuyển thành **tiếng Anh**.

> Snapshot 2026-04-07: **90/244 file sạch** — còn 154 file, 4624 dòng (đang có agents chạy nền)

**Đã sạch (agents đã xử lý):**
- `src/formatters.py` ✅
- `bot/dispatcher.py` ✅ (còn 16 dòng là code data: LLM prompt examples + regex — đúng, không cần dịch)
- `data_provider/realtime_types.py` ✅
- `src/report_language.py` — 120 dòng còn lại là bảng dịch `zh` (data values, không phải comment — đúng)

**Đang xử lý (agents chạy nền):**
- Batch 1: `src/analyzer.py`, `src/search_service.py`
- Batch 2: `src/notification.py`, `src/core/pipeline.py`
- Batch 3: `data_provider/base.py`, `src/stock_analyzer.py`, `src/storage.py`
- Batch 4: `src/agent/executor.py`, `src/market_analyzer.py`, `src/config.py`
- Batch 6: `api/v1/endpoints/` + `api/v1/schemas/` + `api/app.py`
- Batch 7: `bot/commands/` + `bot/handler.py` + `bot/models.py` + `bot/platforms/`
- Batch 8: `src/services/` + `src/repositories/` + `src/data/`
- Batch 9: `src/notification_sender/` + `src/agent/` + `src/scheduler.py`
- Batch 10: `tests/` + `scripts/`

**Phương pháp:** Dùng subagents song song (5-9 agents cùng lúc), mỗi agent đọc-dịch-ghi đè từng nhóm file.

**Tiêu chí hoàn thành:** `python scripts/scan_chinese.py` trả về 0 file dirty. `pytest -m "not network"` pass.

---

### Giai đoạn C — Strategies YAML

| File | Hành động |
|------|-----------|
| `strategies/*.yaml` — 11 file cũ | Xóa text Trung còn sót, đảm bảo `description` bằng tiếng Việt/Anh |
| `vn30_rotation.yaml`, `vn_bank_sector.yaml`, `vn_penny_alert.yaml` | Hoàn thiện nội dung (hiện là scaffold rỗng) |

---

## Phần 3 — Backlog / Tương lai

- **Zalo OA**: `zalo_sender.py` hiện là stub — cần Zalo OA business account để kích hoạt
- **HNX đầy đủ**: Hiện tập trung HOSE, mở rộng HNX sau
- **Backtest VN-specific strategies**: `vn30_rotation`, `vn_bank_sector`, `vn_penny_alert`
- **Vietstock/FireAnt crawler**: Lấy tin tức VN cho market review
- **Web UI i18n**: Dịch chuỗi EN/TQ trong `apps/dsa-web` sang tiếng Việt

---

## Ghi Chú Kỹ Thuật

| Mục | Giá trị |
|-----|---------|
| Git tag an toàn | `pre-vn-migration` |
| Rollback | `git checkout pre-vn-migration` |
| Default report language | `vi` |
| VN lib | `pip install vnstock3` |
| TCBS | Public API, không cần key |
| Zalo | Deferred — cần Zalo OA |
| Timezone | `Asia/Ho_Chi_Minh` (UTC+7) |
| Price limits | HOSE ±7%, HNX ±10% |
| Lot size | 100 cổ phiếu |
| Settlement | T+2.5 |
