# Vietnam Market Migration Plan

> Brainstorm session: 2026-03-30
> Status: **Pending confirmation** — chờ user xác nhận Understanding Lock trước khi bắt đầu implementation

## 1. Mục tiêu

Chuyển toàn bộ hệ thống `daily_stock_analysis` từ phục vụ 3 thị trường (A-share TQ / HK / US)
sang **chỉ phục vụ thị trường chứng khoán Việt Nam (HOSE)**.

## 2. Quyết định đã chốt (Brainstorm Q&A)

### Q1: Nguồn dữ liệu
- **Quyết định:** Kết hợp `vnstock` (cần chốt version API/vnstock3) + `TCBS` + fallback (VNDirect / FireAnt)
- **Thay thế:** efinance, akshare, tushare, pytdx, baostock, yfinance, tickflow → tất cả bị loại bỏ
- **Mô hình:** Giữ nguyên kiến trúc multi-source priority (Strategy Pattern trong `data_provider/`)

### Q2: Sàn giao dịch
- **Quyết định:** Tạm thời ưu tiên HOSE (VN30 + mid-cap) và HNX (các tập cổ phiếu có thanh khoản lớn)
- **Không làm:** UPCOM (tạm thời bỏ qua do biên độ 15% và điều kiện niêm yết lỏng lẻo, dễ làm nhiễu data)
- **Ảnh hưởng:** `trading_calendar.py`, `market_context.py`, `market_profile.py`

### Q3: Ngôn ngữ
- **Quyết định:** Báo cáo tiếng Việt, code/comment tiếng Anh
- **Thay thế:** `report_language.py` bỏ `zh`/`en`, thêm `vi`
- **Prompt LLM:** Viết bằng tiếng Anh, output trả về tiếng Việt

### Q4: Kênh thông báo
- **Giữ:** Telegram, Discord, Email (SMTP), Custom Webhook, Slack (tùy chọn)
- **Thêm:** Zalo (cần webhook hoặc bot API)
- **Bỏ:** WeChat Work, Feishu/Lark, DingTalk, Server酱3, PushPlus, AstrBot, Pushover
- **Ảnh hưởng:** `src/notification_sender/`, `bot/platforms/`

### Q5: Chiến lược giao dịch
- **Quyết định:** Chuyển đổi 11 YAML hiện có + thêm chiến lược VN-specific
- **Lưu ý đặc thù VN:**
  - Giới hạn T+2.5 (cổ phiếu mua T+0 sẽ về tài khoản 13h00 ngày T+2, chỉ bán được phiên chiều T+2)
  - Biên độ giá: +/-7% (HOSE), +/-10% (HNX)
  - Không có short selling hợp pháp theo quy định chung
  - Tạm bỏ qua logic Margin để đơn giản hệ thống Phase 1 (thực tế retail VN dùng margin rất nhiều nhưng call margin phức tạp)
  - Khối lượng lô chẵn 100 cổ phiếu
- **Chiến lược VN-specific cần thêm:**
  - VN30 rotation (xoay vòng cổ phiếu VN30)
  - Ngân hàng sector (VCB, CTG, BID, TCB, MBB...)
  - BĐS sector recovery
  - Penny pump detection (cảnh báo cổ phiếu penny)

### Q6: Market Review
- **Quyết định:** VN-INDEX + VN30
- **Chỉ số:** `VNINDEX`, `VN30`
- **Sector:** Ngân hàng, BĐS, Thép, Bán lẻ, Công nghệ
- **Nguồn tin:** CafeF, VnExpress, Vietstock (chuyên sâu BCTC/cổ tức), FireAnt (có API REST JSON)

### Q7: Định dạng mã CK
- **Quyết định:** Hỗ trợ 3 ký tự (Cổ phiếu) và 6-8 ký tự (Chứng chỉ quỹ ETF, ví dụ: E1VFVN30)
- **Logic detect:** Dùng Regex thay vì fix cứng 3 ký tự, khác hoàn toàn format 6 số (A-share TQ), 5 số + HK prefix, 1-5 chữ cái US
- **Ví dụ:** Cổ phiếu (VCB, FPT, VNM...), ETF (E1VFVN30, FUEVFVND)

## 3. Danh sách module cần thay đổi

### 3.1 Data Provider (`data_provider/`)
| File | Hành động | Chi tiết |
|------|-----------|----------|
| `__init__.py` | Viết lại | Priority init: vnstock → TCBS → fallback |
| `efinance_fetcher.py` | **Xóa** | Thư viện TQ, không dùng được cho VN |
| `akshare_fetcher.py` | **Xóa** | Thư viện TQ |
| `tushare_fetcher.py` | **Xóa** | Thư viện TQ, cần token TQ |
| `pytdx_fetcher.py` | **Xóa** | Thư viện TQ |
| `baostock_fetcher.py` | **Xóa** | Thư viện TQ |
| `yfinance_fetcher.py` | **Xóa** | Có data VN nhưng không chính xác, không realtime |
| `tickflow_fetcher.py` | **Xóa** | API TQ |
| `vnstock_fetcher.py` | **TẠO MỚI** | Fetcher chính dùng vnstock library |
| `tcbs_fetcher.py` | **TẠO MỚI** | Fetcher realtime TCBS API |
| `base.py` | Sửa | Thêm `is_vn_stock_code()`, bỏ `is_hk_market()`, `is_us_stock_code()` |
| `us_index_mapping.py` | **Xóa** | Không cần US index nữa |

### 3.2 Core (`src/core/`)
| File | Hành động | Chi tiết |
|------|-----------|----------|
| `trading_calendar.py` | Viết lại | Bỏ XSHG/XHKG/XNYS, thêm HOSE (XSTC). Timezone: Asia/Ho_Chi_Minh |
| `market_profile.py` | Viết lại | Bỏ CN_PROFILE/US_PROFILE, thêm VN_PROFILE (VNINDEX, VN30) |
| `market_context.py` | Viết lại | Detect logic: chỉ trả 'vn' |
| `market_review.py` | Sửa | Chạy review cho VN thay vì CN/US |
| `market_strategy.py` | Sửa | Strategies VN |
| `pipeline.py` | Sửa | Market context 'vn' |

### 3.3 Services (`src/services/`)
| File | Hành động | Chi tiết |
|------|-----------|----------|
| `name_to_code_resolver.py` | Sửa | Resolve tên VN → mã CK (VCB = Vietcombank...) |
| `social_sentiment_service.py` | Xóa hoặc rewrite | Bỏ api.adanos.org (US sentiment), thêm VN sentiment |
| `image_stock_extractor.py` | Sửa | EXTRACT_PROMPT cho ảnh CK VN |

### 3.4 Report & Language (`src/`)
| File | Hành động | Chi tiết |
|------|-----------|----------|
| `report_language.py` | Viết lại | Bỏ zh/en, thêm vi. Default: vi |
| `analyzer.py` | Sửa | Prompt context cho thị trường VN |
| `market_analyzer.py` | Sửa | Phân tích thị trường VN |

### 3.5 Notification (`src/notification_sender/`)
| File | Hành động | Chi tiết |
|------|-----------|----------|
| `zalo_sender.py` | **TẠO MỚI** | Gửi thông báo qua Zalo webhook/bot |
| `wechat_sender.py` | **Xóa** | Kênh TQ |
| `feishu_sender.py` | **Xóa** | Kênh TQ |
| `dingtalk.py` (bot/platforms) | **Xóa** | Kênh TQ |
| `dingtalk_stream.py` | **Xóa** | Kênh TQ |
| `feishu_stream.py` | **Xóa** | Kênh TQ |
| `pushplus_sender.py` | **Xóa** | Kênh TQ |
| `serverchan3_sender.py` | **Xóa** | Kênh TQ |
| `astrbot_sender.py` | **Xóa** | Kênh TQ |
| `pushover_sender.py` | **Xóa** | Ít dùng ở VN |

### 3.6 Bot (`bot/`)
| File | Hành động | Chi tiết |
|------|-----------|----------|
| `platforms/` | Sửa | Bỏ DingTalk/Feishu, giữ Discord, thêm Zalo bot |
| Commands | Sửa | Prompt context VN |

### 3.7 Strategies (`strategies/`)
| File | Hành động | Chi tiết |
|------|-----------|----------|
| 11 YAML hiện có | Chuyển đổi | Điều chỉnh tham số cho VN (biên độ +/-7%, volume lot 100...) |
| `vn30_rotation.yaml` | **TẠO MỚI** | Chiến lược xoay vòng VN30 |
| `vn_bank_sector.yaml` | **TẠO MỚI** | Chiến lược sector ngân hàng |
| `vn_penny_alert.yaml` | **TẠO MỚI** | Cảnh báo penny |

### 3.8 Config (`src/config.py`, `.env.example`)
- Bỏ: `TUSHARE_TOKEN`, `TICKFLOW_API_KEY`, WeChat/Feishu/DingTalk configs
- Thêm: `VN_DATA_SOURCE_PRIORITY`, `ZALO_WEBHOOK_URL`, `TCBS_API_KEY` (nếu cần)
- Sửa: `STOCK_LIST` format → 3 chữ cái VN
- Sửa: `MARKET_REVIEW_REGION` → luôn `vn`

### 3.9 Docker
- `Dockerfile`: Timezone `Asia/Ho_Chi_Minh` (thay `Asia/Shanghai`)
- `docker-compose.yml`: Cập nhật env vars

### 3.10 Templates (`templates/`)
- Cập nhật Jinja2 templates cho tiếng Việt

### 3.11 CI/CD (`.github/workflows/`)
- `daily_analysis.yml`: Cập nhật timezone, market context
- Cập nhật test markers

## 4. Assumptions

1. `vnstock` library (cần đối chiếu bản hiện hành vs `vnstock3`) đủ đáp ứng OHLCV, realtime, fundamentals, cổ tức
2. TCBS API public vẫn available (hoặc sẵn sàng sang fallback VNDirect Dboard / FireAnt)
3. Không cần HNX/UPCOM ngay (có thể mở rộng sau)
4. Zalo có webhook/bot API khả dụng (cần xác minh)
5. User đã cài `vnstock` (`pip install vnstock`)

## 5. Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| vnstock API thay đổi | Data fetch fail | TCBS fallback + cache |
| TCBS rate limit | Realtime delay | Batch request, cache |
| Thiếu data lịch VN | Backtest kém chính xác | Dùng vnstock history API |
| Zalo API hạn chế (Zalo OA thu phí push) | Thông báo không đến, chi phí cao | Ưu tiên số 1 cho Telegram/Discord |
| Strategies VN không hiệu quả | Sai tín hiệu | Backtest kỹ trước khi deploy |

## 6. Decision Log

| # | Quyết định | Alternatives | Lý do |
|---|-----------|-------------|-------|
| 1 | vnstock + TCBS + fallback (VNDirect) | efinance, akshare, tự build | Ổn định, cộng đồng VN dùng phổ biến |
| 2 | HOSE + HNX | Toàn sàn (cả UPCOM) | Đơn giản hóa phase 1, data HNX và HOSE chung cấu trúc |
| 3 | Báo cáo tiếng Việt | Song ngữ, tiếng Anh | Người dùng VN end-user |
| 4 | Zalo + Telegram + Discord | Giữ WeChat/Feishu | Phù hợp thói quen người VN |
| 5 | Chuyển đổi + thêm strategies | Viết mới hoàn toàn | Tận dụng code cũ, giảm effort |
| 6 | Mã CK 3 chữ cái | Sàn:Mã, SSI format | Đơn giản, phổ biến nhất |
| 7 | Market review VN-INDEX + VN30 | Chỉ index, VN + global | Đủ thông tin cho nhà đầu tư VN |

---

*Trạng thái hiện tại: Đã cập nhật chuyên sâu thị trường VN (T+2.5, HNX, ETF, Data source)*
*Next steps: Chờ user xác nhận Understanding Lock → Lên danh sách Task Breakdown → Bắt đầu code*
