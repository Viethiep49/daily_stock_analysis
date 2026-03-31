# Vietnam Migration - Phase & Agent Tasks

> Target document: `docs/vietnam-migration-plan.md`
> Status: **Planning (Understanding Lock ✅)**

Quá trình dịch chuyển toàn bộ hệ thống sang thị trường Chứng khoán Việt Nam là một refactor diện rộng. Dựa trên phân loại chuyên môn của AI Agents (`GEMINI.md`), dưới đây là 6 Phase cần thực hiện tuần tự để đảm bảo hệ thống không bị gãy hỏng (Regression Break).

---

## 📍 Phase 1: Cleanup & Foundation (Legacy Trimming)
**Thực hiện:** `@backend-specialist` (Python)
**Khối lượng:** Nhỏ
**Rủi ro:** Trung bình (cẩn thận xóa nhầm file Core)

- **Nhiệm vụ:**
  - Cắt bỏ các data nguồn Trung Quốc/Mỹ: Xóa `efinance`, `akshare`, `tushare`, `baostock`, `yfinance`, `tickflow` tại `data_provider/`.
  - Cắt bỏ thông báo/mạng xã hội không liên quan: Xóa `wechat_sender`, `dingtalk`, `feishu`, `pushplus`, `serverchan`, `astrbot` tại kênh `src/notification_sender` và `bot/platforms`.
  - Dọn dẹp các biến môi trường rác trong `.env.example` & `src/config.py`.
- **Tiêu chí hoàn thành (DoD):** Clean thành công. Compile không dư thừa import. Python tests chạy không báo crash vì missing file.

---

## 📍 Phase 2: Data Provider & Core Adapter (Trái tim Hệ thống)
**Thực hiện:** `@backend-specialist`
**Khối lượng:** Lớn
**Rủi ro:** Cao (Ảnh hưởng tới toàn bộ pipeline)

- **Nhiệm vụ:**
  - Tích hợp `vnstock_fetcher.py` (Lấy giá, KL, nến, P/E, EPS định kỳ).
  - Tích hợp `tcbs_fetcher.py` (Fallback và get Realtime data).
  - Sửa `base.py`: Viết Regex cho `is_vn_stock_code()` bao trọn 3 chữ cái (cổ phiếu) và 6-8 ký tự (chứng chỉ quỹ ETF).
  - Cấu hình lại Core Adapter `trading_calendar.py` & `market_profile.py`: Thêm `HOSE`, `HNX`. Setup Timezone `Asia/Ho_Chi_Minh`.
- **Tiêu chí hoàn thành (DoD):** Hàm fetcher tải thành công data nến 1 năm và realtime của mã `VCB` và Quỹ `E1VFVN30`.

---

## 📍 Phase 3: Reporting, Prompt & Analysis (Bộ não AI)
**Thực hiện:** `@backend-specialist` kết hợp AI Prompt
**Khối lượng:** Trung bình
**Rủi ro:** Thấp

- **Nhiệm vụ:**
  - Sửa default language sang `vi` trong `report_language.py`. Code context yêu cầu bot LLM trả lời bằng tiếng Việt chuyên ngành tài chính.
  - Sửa `market_review.py`: Bỏ review TQ/Mỹ. Gọi 2 chỉ số duy nhất là `VNINDEX` và `VN30`.
  - Crawler/API lấy tin từ Vietstock / FireAnt.
- **Tiêu chí hoàn thành (DoD):** Bot build thành công 1 report phân tích công ty VN bằng tiếng Việt chuẩn xác (không dính Hán ngữ gốc).

---

## 📍 Phase 4: Strategy Engines (Logic Giao Dịch)
**Thực hiện:** `@backend-specialist` (Đọc các skills Financial)
**Khối lượng:** Lớn
**Rủi ro:** Cao (Trade lỗi)

- **Nhiệm vụ:**
  - Gỡ bỏ logic Day Trading (T+0). Thay bằng logic chặn bán T+2.5 (cổ mua chưa về sẽ không sinh tín hiệu Bán).
  - Chuyển bộ 11 YAML Strategy cũ sang biên độ dao động +/-7% và +/-10%. Khối lượng lô luôn chia hết cho 100.
  - Khởi tạo 3 YAML chiến lược mới rỗng (cho tương lai): `vn30_rotation`, `vn_bank_sector`, `vn_penny_alert`.
- **Tiêu chí hoàn thành (DoD):** Chạy backtest trên YAML chiến lược không văng lỗi biên độ, hiểu được lô chẵn 100 cổ phiếu.

---

## 📍 Phase 5: Notification & Bot Commands (Cổng Giao Tiếp)
**Thực hiện:** `@backend-specialist`
**Khối lượng:** Thấp
**Rủi ro:** Cực thấp

- **Nhiệm vụ:**
  - Chuyển trọng tâm gửi notification qua Telegram & Discord làm Primary.
  - Refactor `Discord/Telegram Cogs`: Các lệnh của Bot (như `/research`, `/chart`) sẽ nhận diện regex mã VN.
  - Bổ sung nút bấm inline Telegram link ra trang Vietstock/FireAnt của mã cổ phiếu. (Tạm gác logic cấp Margin / Zalo OA sang tương lai vì tốn chi phí và phức tạp).
- **Tiêu chí hoàn thành (DoD):** Nhập lệnh `/research FPT` từ Discord sinh ra Report tiếng Việt thành công.

---

## 📍 Phase 6: Web / Desktop UI & QA (Trải nghiệm người dùng)
**Thực hiện:** `@frontend-specialist` & `@debugger`
**Khối lượng:** Trung bình
**Rủi ro:** Trung bình

- **Nhiệm vụ:**
  - `apps/dsa-web`: Dịch các chuỗi tiếng Anh/TQ mồ côi sang tiếng Việt (i18n).
  - Cập nhật hiển thị Chart Component (TradingView/Echarts) render Timezone +07 theo thị trường VN.
  - Desktop package (`electron`): Thay đổi metadata Desktop App (Tên App, Icon nếu cần).
  - Chạy toàn bộ Validation Check (`checklist.py`, `lint_runner.py`, `test_runner.py`).
- **Tiêu chí hoàn thành (DoD):** Build `npm run build` thành công trên nhánh web/desktop. Giao diện hiển thị đúng layout tiếng Việt.

---

> 💡 **Quy trình Code (Work Flow):**
> 1. Mỗi một file tạo ra/sửa đổi phải chạy theo tư duy `@[skills/clean-code]`. 
> 2. Phải viết kèm Test Case trước khi chốt file (`@[skills/testing-patterns]`).
> 3. Không nhảy Phase. Kết thúc Phase 1 audit sạch mới làm Phase 2.
>
> 🚀 **Vui lòng thông báo cho tôi để bắt đầu thực thi `Phase 1` bằng "@backend-specialist"!**
