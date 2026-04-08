# ❓ Câu Hỏi Thường Gặp (FAQ)

Tài liệu này tổng hợp các vấn đề thường gặp khi sử dụng và cách khắc phục.

---

## 📊 Liên Quan Đến Dữ Liệu

### Q1: Giá cổ phiếu Mỹ (như AMD, AAPL) hiển thị không chính xác khi phân tích?

**Hiện tượng**: Sau khi nhập mã cổ phiếu Mỹ, giá hiển thị sai rõ rệt (ví dụ AMD hiển thị 7.33 tệ), hoặc bị nhận diện nhầm thành cổ phiếu A-share Trung Quốc.

**Nguyên nhân**: Các phiên bản cũ ưu tiên thử quy tắc cổ phiếu A-share Trung Quốc trước, dẫn đến xung đột mã.

**Giải pháp**:
1. Đã sửa từ v2.3.0, hệ thống giờ hỗ trợ tự động nhận diện mã cổ phiếu Mỹ
2. Nếu vẫn gặp vấn đề, có thể cài đặt trong `.env`:
   ```bash
   YFINANCE_PRIORITY=0
   ```
   Điều này sẽ ưu tiên sử dụng nguồn dữ liệu Yahoo Finance cho cổ phiếu Mỹ

> 📌 Issue liên quan: [#153](https://github.com/ZhuLinsen/daily_stock_analysis/issues/153)

---

### Q2: Trường "lượng tỷ" (volume ratio) trong báo cáo hiển thị trống hoặc N/A?

**Hiện tượng**: Báo cáo phân tích thiếu dữ liệu lượng tỷ, ảnh hưởng đến đánh giá của AI về khối lượng giao dịch.

**Nguyên nhân**: Một số nguồn dữ liệu realtime mặc định (như API Sina) không cung cấp trường lượng tỷ.

**Giải pháp**:
1. Đã sửa từ v2.3.0, API Tencent giờ đã hỗ trợ phân tích lượng tỷ
2. Khuyến nghị cấu hình ưu tiên nguồn dữ liệu realtime:
   ```bash
   REALTIME_SOURCE_PRIORITY=tencent,akshare_sina,efinance,akshare_em
   ```
3. Hệ thống đã tích hợp sẵn logic tính trung bình khối lượng 5 ngày làm phương án dự phòng

> 📌 Issue liên quan: [#155](https://github.com/ZhuLinsen/daily_stock_analysis/issues/155)

---

### Q3: vnstock/TCBS không lấy được dữ liệu?

**Giải pháp**:
1. Cài đúng thư viện: `pip install vnstock3`
2. Kiểm tra kết nối internet — TCBS API là public, không cần API key
3. Nếu vnstock thất bại, hệ thống tự động fallback sang TCBS
4. Tất cả chức năng cốt lõi đều hoạt động với vnstock3 + TCBS, không cần token thêm

---

### Q4: Lấy dữ liệu bị giới hạn tốc độ hoặc trả về rỗng?

**Hiện tượng**: Dữ liệu trả về `None`, lỗi `RemoteDisconnected`, hoặc circuit breaker kích hoạt

**Nguyên nhân**: vnstock/TCBS có cơ chế chống cào, gửi quá nhiều request trong thời gian ngắn sẽ bị giới hạn tốc độ.

**Giải pháp**:
1. Hệ thống đã tích hợp chuyển đổi tự động đa nguồn và bảo vệ circuit breaker
2. Giảm số lượng cổ phiếu tự chọn, hoặc tăng khoảng cách giữa các request
3. Tránh kích hoạt phân tích thủ công quá thường xuyên
4. Đặt `MAX_WORKERS=1` để chuyển sang chế độ tuần tự, giảm áp lực concurrent request

---

## ⚙️ Liên Quan Đến Cấu Hình

### Q5: GitHub Actions chạy thất bại, báo không tìm thấy biến môi trường?

**Hiện tượng**: Log Actions hiển thị `GEMINI_API_KEY` hoặc `STOCK_LIST` chưa được định nghĩa

**Nguyên nhân**: GitHub phân biệt `Secrets` (mã hóa) và `Variables` (biến thông thường), cấu hình sai vị trí sẽ không đọc được.

**Giải pháp**:
1. Vào kho `Settings` → `Secrets and variables` → `Actions`
2. **Secrets** (nhấn `New repository secret`): Lưu thông tin nhạy cảm
   - `GEMINI_API_KEY`
   - `OPENAI_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - Các loại Webhook URL
3. **Variables** (nhấn tab `Variables`): Lưu cấu hình không nhạy cảm
   - `STOCK_LIST`
   - `GEMINI_MODEL`
   - `REPORT_TYPE`

---

### Q6: Sửa file .env nhưng cấu hình không có hiệu lực?

**Giải pháp**:
1. Đảm bảo file `.env` nằm ở thư mục gốc dự án
2. **Triển khai Docker**: Sau khi sửa cần restart container
   ```bash
   docker-compose down && docker-compose up -d
   ```
3. **GitHub Actions**: File `.env` không có hiệu lực, phải cấu hình trong Secrets/Variables
4. Kiểm tra xem có nhiều file `.env` (như `.env.local`) gây ghi đè không

---

### Q7: Cấu hình proxy để truy cập Gemini/OpenAI API như thế nào?

**Giải pháp**:

Cấu hình trong `.env`:
```bash
USE_PROXY=true
PROXY_HOST=127.0.0.1
PROXY_PORT=10809
```

> ⚠️ Lưu ý: Cấu hình proxy chỉ có hiệu lực khi chạy cục bộ, môi trường GitHub Actions không cần cấu hình proxy.

---

### Câu Hỏi Thường Gặp Về Cấu Hình LLM

> Xem chi tiết tại [Hướng Dẫn Cấu Hình LLM](LLM_CONFIG_GUIDE.md).

**Q: Đã cấu hình GEMINI_API_KEY và LLM_CHANNELS, tại sao hệ thống chỉ dùng kênh?**

Hệ thống chỉ lấy một loại theo thứ tự ưu tiên: `LITELLM_CONFIG` (YAML) > `LLM_CHANNELS` > legacy keys. Một khi đã cấu hình kênh hoặc YAML, khu vực legacy (`GEMINI_API_KEY`...) sẽ không tham gia phân tích.

**Q: test_env xuất ✗ chưa cấu hình bất kỳ LLM nào thì làm sao?**

Cấu hình `LITELLM_CONFIG` / `LLM_CHANNELS` hoặc ít nhất một `*_API_KEY` (như `GEMINI_API_KEY`, `DEEPSEEK_API_KEY`, `AIHUBMIX_KEY`). Chạy `python test_env.py --config` để xác thực cấu hình, `python test_env.py --llm` để gọi API thực tế kiểm tra.

**Q: Làm sao dùng đồng thời nhiều mô hình (như AIHubmix + DeepSeek + Gemini)?**

Sử dụng chế độ kênh: Đặt `LLM_CHANNELS=aihubmix,deepseek,gemini`, và cấu hình `LLM_{NAME}_BASE_URL`, `LLM_{NAME}_API_KEY`, `LLM_{NAME}_MODELS` cho từng kênh. Cũng có thể cấu hình trực quan tại trang Settings → AI Models → Channel Editor trên Web.

---

## 📱 Liên Quan Đến Đẩy Tin

### Q8: Bot đẩy tin thất bại, báo message quá dài?

**Hiện tượng**: Phân tích thành công nhưng không nhận được đẩy tin, log báo lỗi 400 hoặc `Message too long`

**Nguyên nhân**: Các nền tảng khác nhau có giới hạn độ dài tin nhắn khác nhau:
- WeChat Work: 4KB
- Feishu: 20KB
- DingTalk: 20KB

**Giải pháp**:
1. **Tự động chia nhỏ**: Phiên bản mới nhất đã hỗ trợ tự động cắt tin nhắn dài
2. **Chế độ đẩy từng mã**: Đặt `SINGLE_STOCK_NOTIFY=true`, đẩy tin ngay sau khi phân tích xong mỗi mã
3. **Báo cáo rút gọn**: Đặt `REPORT_TYPE=simple` để dùng định dạng rút gọn

---

### Q9: Telegram không nhận được tin nhắn đẩy?

**Giải pháp**:
1. Xác nhận `TELEGRAM_BOT_TOKEN` và `TELEGRAM_CHAT_ID` đã được cấu hình
2. Cách lấy Chat ID:
   - Gửi tin nhắn bất kỳ cho Bot
   - Truy cập `https://api.telegram.org/bot<TOKEN>/getUpdates`
   - Tìm `chat.id` trong JSON trả về
3. Đảm bảo Bot đã được thêm vào nhóm đích (nếu là group chat)
4. Khi chạy cục bộ cần truy cập được Telegram API (có thể cần proxy)

---

### Q10: Định dạng Markdown WeChat Work hiển thị không bình thường?

**Giải pháp**:
1. WeChat Work hỗ trợ Markdown có hạn, có thể thử đặt:
   ```bash
   WECHAT_MSG_TYPE=text
   ```
2. Điều này sẽ gửi tin nhắn dạng pure text

---

## 🤖 Liên Quan Đến Mô Hình AI

### Q11: Gemini API trả về lỗi 429 (Too Many Requests)?

**Hiện tượng**: Log hiển thị `Resource has been exhausted` hoặc `429 Too Many Requests`

**Giải pháp**:
1. Gemini bản miễn phí có giới hạn tốc độ (khoảng 15 RPM)
2. Giảm số lượng cổ phiếu phân tích đồng thời
3. Tăng độ trễ giữa các request:
   ```bash
   GEMINI_REQUEST_DELAY=5
   ANALYSIS_DELAY=10
   ```
4. Hoặc chuyển sang OpenAI compatible API làm phương án dự phòng

---

### Q12: Làm sao sử dụng mô hình như DeepSeek?

**Cách cấu hình**:

```bash
# Không cần cấu hình GEMINI_API_KEY
OPENAI_API_KEY=sk-xxxxxxxx
OPENAI_BASE_URL=https://api.deepseek.com/v1
OPENAI_MODEL=deepseek-chat
# Chế độ suy luận: deepseek-reasoner, deepseek-r1, qwq... tự động nhận diện; deepseek-chat hệ thống tự kích hoạt theo tên mô hình
```

Các dịch vụ mô hình hỗ trợ:
- DeepSeek: `https://api.deepseek.com/v1`
- Tongyi Qianwen: `https://dashscope.aliyuncs.com/compatible-mode/v1`
- Moonshot: `https://api.moonshot.cn/v1`

---

### Q12b: Làm sao sử dụng mô hình cục bộ Ollama?

**Cách cấu hình**: Sử dụng `OLLAMA_API_BASE` + `LITELLM_MODEL`, hoặc chế độ kênh (`LLM_CHANNELS=ollama` + `LLM_OLLAMA_BASE_URL` + `LLM_OLLAMA_MODELS`).

**Tránh lỗi**: Không dùng `OPENAI_BASE_URL` để cấu hình Ollama, nếu không sẽ kích hoạt bug ghép URL của LiteLLM (như 404, `api/generate/api/show`). Xem ví dụ 4 và ví dụ kênh trong [Hướng Dẫn Cấu Hình LLM](LLM_CONFIG_GUIDE.md).

---

## 🐳 Liên Quan Đến Docker

### Q13: Docker container khởi động xong thoát ngay?

**Giải pháp**:
1. Xem log container:
   ```bash
   docker logs <container_id>
   ```
2. Nguyên nhân thường gặp:
   - Biến môi trường chưa cấu hình đúng
   - File `.env` sai định dạng (có khoảng trắng thừa)
   - Xung đột phiên bản dependency

---

### Q14: Không truy cập được API service trong Docker?

**Giải pháp**:
1. Đảm bảo lệnh khởi động có `--host 0.0.0.0` (không được là 127.0.0.1)
2. Kiểm tra port mapping có đúng không:
   ```yaml
   ports:
     - "8000:8000"
   ```

---

### Q14.1: Lỗi phân giải mạng/DNS trong Docker (như api.tushare.pro, searchapi.eastmoney.com không phân giải được)?

**Hiện tượng**: Log hiển thị `Temporary failure in name resolution` hoặc `NameResolutionError`, cả API dữ liệu cổ phiếu và API mô hình lớn đều không truy cập được.

**Nguyên nhân**: Trong mạng bridge tùy chỉnh, container sử dụng DNS tích hợp của Docker, có thể phân giải thất bại trong môi trường router phụ hoặc mạng đặc thù.

**Giải pháp** (thử theo thứ tự ưu tiên):

1. **Cấu hình DNS rõ ràng**: Thêm vào `x-common` trong `docker/docker-compose.yml`:
   ```yaml
   dns:
     - 223.5.5.5
     - 119.29.29.29
     - 8.8.8.8
   ```
   Sau đó chạy `docker-compose down` và `docker-compose up -d --force-recreate` để tạo lại container.

2. **Chuyển sang chế độ mạng host**: Nếu vẫn không hiệu quả, thêm `network_mode: host` vào service `server`, và xóa mapping `ports`. Khi dùng chế độ host, `ports` không có hiệu lực, **port được chỉ định bởi `--port` trong `command`**. Nếu port mặc định trên host đã bị chiếm, có thể đổi sang port khác (như đặt `API_PORT=8080` trong `.env`), truy cập tại `http://localhost:8080`.

> 📌 Issue liên quan: [#372](https://github.com/ZhuLinsen/daily_stock_analysis/issues/372)

---

## 🔧 Vấn Đề Khác

### Q15: Làm sao chỉ chạy review thị trường, không phân tích cổ phiếu riêng lẻ?

**Cách làm**:
```bash
# Chạy cục bộ
python main.py --market-only

# GitHub Actions
# Khi trigger thủ công chọn mode: market-only
```

---

### Q16: Số lượng thống kê Mua/Chờ/Bán trong kết quả phân tích không đúng?

**Nguyên nhân**: Các phiên bản cũ dùng regex để thống kê, có thể không khớp với khuyến nghị thực tế.

**Giải pháp**: Đã sửa trong phiên bản mới nhất, mô hình AI giờ trực tiếp xuất trường `decision_type` để thống kê chính xác.

---

### Q17: Tại sao cuối tuần trigger thủ công trên GitHub Actions vẫn báo "không phải ngày giao dịch, bỏ qua"?

**Hiện tượng**: Đã cấu hình `TRADING_DAY_CHECK_ENABLED` hoặc muốn chạy thủ công, nhưng log vẫn báo "hôm nay không phải ngày giao dịch, bỏ qua thực thi".

**Giải pháp**:
1. Mở `Actions → Daily Stock Analysis → Run workflow`
2. Khi trigger thủ công đặt `force_run` thành `true` (bắt buộc chạy 1 lần)
3. Nếu muốn tắt kiểm tra ngày giao dịch lâu dài, vào `Settings → Secrets and variables → Actions` đặt:
   ```bash
   TRADING_DAY_CHECK_ENABLED=false
   ```

**Quy tắc**:
- `TRADING_DAY_CHECK_ENABLED=true` và `force_run=false`: Bỏ qua nếu không phải ngày giao dịch (mặc định)
- `force_run=true`: Lần này dù không phải ngày giao dịch cũng thực thi
- `TRADING_DAY_CHECK_ENABLED=false`: Không kiểm tra ngày giao dịch cho cả lịch tự động và thủ công

---

## 💬 Còn Vấn Đề?

Nếu nội dung trên chưa giải quyết được vấn đề của bạn, vui lòng:
1. Xem [Hướng Dẫn Cấu Hình Đầy Đủ](full-guide.md)
2. Tìm kiếm hoặc gửi [GitHub Issue](https://github.com/ZhuLinsen/daily_stock_analysis/issues)
3. Xem [Nhật Ký Thay Đổi](CHANGELOG.md) để biết các bản sửa lỗi mới nhất

---

*Cập nhật lần cuối: 2026-02-28*
