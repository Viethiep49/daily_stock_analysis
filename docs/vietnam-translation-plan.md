# Kế Hoạch Chuyển Đổi Ngôn Ngữ Dự Án (Vietnam Translation Plan)

Mục tiêu: Chuyển đổi toàn bộ dự án từ Tiếng Trung sang Tiếng Việt (cho tài liệu) và Tiếng Anh (cho mã nguồn/comment code), đồng thời loại bỏ hoàn toàn Tiếng Trung khỏi hệ thống nhằm hoàn tất quá trình "Vietnam Migration".

## 1. Phạm Vi Tài Liệu (Documentation)
Yêu cầu: Viết lại docs bằng Tiếng Việt, giữ lại các bản Tiếng Anh (EN), loại bỏ hoàn toàn Tiếng Trung.

### Các file cần chuyển sang Tiếng Việt hoàn toàn:
- `README.md` (Đổi mới toàn bộ sang giao diện/cách dùng tại VN)
- `AGENTS.md` (Tài liệu về Rules cho AI)
- `docs/FAQ.md` (Giải đáp thắc mắc)
- `docs/full-guide.md` (Hướng dẫn sử dụng cấu hình đầy đủ)
- `docs/bot/*-config.md` (Cấu hình Telegram/Discord)
- `docs/PLAN.md` (Tiến độ dự án)
- `strategies/README.md` (Hướng dẫn viết và cấu trúc Bot Strategy)

### Các file bị xoá/thay thế:
- `docs/README_CHT.md` (Xoá vì không dùng tiếng Trung Phồn thể)

### Các file được giữ nguyên (Bản Tiếng Anh):
- `README_EN.md`
- `docs/full-guide_EN.md`
- `docs/INDEX_EN.md`

---

## 2. Phạm Vi Mã Nguồn (Source Code)
Yêu cầu: Tất cả comment, docstring, log nhắn tự động (`logger.info`) có chứa Tiếng Trung trong mã nguồn `.py` sẽ được chuyển thành **Tiếng Anh**. Các nhãn hiển thị ra cho User cuối (Báo cáo thị trường) đã được chuyển thành **Tiếng Việt** từ Phase 3. Mục tiêu là quét để dọn sạch 100% tiếng Trung.

### Các thư mục/mô-đun cần xử lý:
- `src/` (Bao gồm core, notification, agent, services...)
- `bot/` (Dispatcher, commands, handler)
- `api/` (Tất cả middleware, router, schemas)
- `strategies/*.yaml` (Mô tả chiến lược giao dịch cần dùng Tiếng Việt/Anh, xoá text Trung)
- `data_provider/` (Các Data Fetcher còn sót comment Trung)
- `tests/` (Xoá các tên hàm/comment test bằng tiếng Trung)

---

## 3. Cách Thức Triển Khai (Dự Kiến)

Vì lượng file source code quá lớn (hơn 100 file .py), để đảm bảo an toàn và không bị sót:
1. **Giai đoạn 1**: Tôi sẽ dùng AI để tập trung dịch lại thủ công các tài liệu cốt lõi (`README.md`, `AGENTS.md`, `FAQ.md`, `full-guide.md`) sang Tiếng Việt chuẩn chỉ nhất. (Tăng độ dễ hiểu, thêm ngữ cảnh thị trường HOSE/HNX).
2. **Giai đoạn 2**: Sử dụng một script Python (viết riêng bằng OpenAI/LLM API) quét tự động regex ký tự Hoa lặp lại vòng lặp đọc-dịch-ghi lại đè lên `.py` file để chuẩn hóa comment sang `English`. 
3. **Giai đoạn 3**: Chạy lại Terminal `scan_chinese.py` kiểm định danh sách file có ký tự Trung Quốc `= 0`. Gọi lại chạy Unit Test bằng `pytest` để đảm bảo Syntax Python không bị vỡ do Comment.

## 4. Phê Duyệt
(Đợi phản hồi lệnh cho phép chạy từ phía Admin để bắt đầu quá trình code trên file).
