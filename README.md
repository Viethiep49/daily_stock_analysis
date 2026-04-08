<div align="center">

# 📈 Hệ Thống Phân Tích Cổ Phiếu Thông Minh

[![GitHub stars](https://img.shields.io/github/stars/ZhuLinsen/daily_stock_analysis?style=social)](https://github.com/ZhuLinsen/daily_stock_analysis/stargazers)
[![CI](https://github.com/ZhuLinsen/daily_stock_analysis/actions/workflows/ci.yml/badge.svg)](https://github.com/ZhuLinsen/daily_stock_analysis/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Ready-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://hub.docker.com/)

<p>
  <a href="https://trendshift.io/repositories/18527" target="_blank"><img src="https://trendshift.io/api/badge/repositories/18527" alt="ZhuLinsen%2Fdaily_stock_analysis | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>
  <a href="https://hellogithub.com/repository/ZhuLinsen/daily_stock_analysis" target="_blank"><img src="https://api.hellogithub.com/v1/widgets/recommend.svg?rid=6daa16e405ce46ed97b4a57706aeb29f&claim_uid=pfiJMqhR9uvDGlT&theme=neutral" alt="Featured｜HelloGitHub" style="width: 250px; height: 54px;" width="250" height="4" /></a>
</p>

> 🤖 Hệ thống phân tích cổ phiếu tự chọn thông minh dựa trên AI, hỗ trợ HOSE/HNX, tự động phân tích và đẩy "Bảng Điều Khiển Quyết Định" qua Telegram/Discord/Slack/Email/Zalo

[**Tính Năng**](#-tính-năng) · [**Bắt Đầu Nhanh**](#-bắt-đầu-nhanh) · [**Hiệu Ứng Đẩy Tin**](#-hiệu-ứng-đẩy-tin) · [**Hướng Dẫn Đầy Đủ**](docs/full-guide.md) · [**Câu Hỏi Thường Gặp**](docs/FAQ.md) · [**Nhật Ký Thay Đổi**](docs/CHANGELOG.md)

Tiếng Việt | [English](docs/README_EN.md)

</div>

## 💖 Nhà Tài Trợ (Sponsors)
<div align="center">
  <a href="https://serpapi.com/baidu-search-api?utm_source=github_daily_stock_analysis" target="_blank">
    <img src="./sources/serpapi_banner_en.png" alt="SerpApi - Thu thập dữ liệu tài chính thời gian thực" height="160">
  </a>
</div>
<br>


## ✨ Tính Năng

| Mô-đun | Tính năng | Mô tả |
|------|------|------|
| AI | Bảng điều khiển quyết định | Kết luận chính một câu + điểm mua/bán chính xác + danh sách kiểm tra thao tác |
| Phân tích | Phân tích đa chiều | Kỹ thuật (MA thời gian thực/cấu trúc bullish) + phân phối chip + thông tin thị trường + báo giá thời gian thực |
| Thị trường | Thị trường Việt Nam | Hỗ trợ HOSE, HNX, cổ phiếu và ETF (VCB, FPT, E1VFVN30...) |
| Cơ bản | Tổng hợp có cấu trúc | Thêm `fundamental_context` (valuation/growth/earnings/institution/capital_flow/dragon_tiger/boards), hạ cấp fail-open trên chuỗi chính |
| Chiến lược | Hệ thống chiến lược thị trường | Tích hợp chiến lược "3 bước tổng kết" VN và "Regime Strategy" quốc tế, xuất ra kế hoạch tấn công/cân bằng/phòng thủ |
| Tổng kết | Tổng kết thị trường | Tổng quan VNINDEX + VN30 hàng ngày, tăng/giảm theo ngành |
| Giao diện | Không gian làm việc 2 chủ đề | Web hỗ trợ chuyển đổi sáng/tối, trang chủ / hỏi / backtest / danh mục / cài đặt thống nhất hệ thống giao diện |
| Tự động hoàn thành | Tự động hoàn thành thông minh (MVP) | **[Giai đoạn thử nghiệm]** Ô tìm kiếm trang chủ hỗ trợ gợi ý mã/tên/viết tắt/biệt danh; đã phủ HOSE, HNX |
| Nhập thông minh | Nhập đa nguồn | Hỗ trợ ảnh, file CSV/Excel, dán từ clipboard; Vision LLM trích xuất mã+tên; xác nhận theo tầng tin cậy |
| Lịch sử | Quản lý hàng loạt | Hỗ trợ chọn nhiều, chọn tất cả và xóa hàng loạt bản ghi phân tích lịch sử |
| Backtest | Xác minh backtest AI | Tự động đánh giá độ chính xác phân tích lịch sử, tỷ lệ thắng hướng, tỷ lệ chốt lời/chốt lỗ |
| **Agent hỏi cổ phiếu** | **Trò chuyện chiến lược** | **Hỏi đáp chiến lược đa lượt, hỗ trợ 11 chiến lược tích hợp, Web/Bot/API toàn chuỗi** |
| Đẩy tin | Thông báo đa kênh | Telegram, Discord, Slack, Zalo, Email, Webhook tùy chỉnh |
| Tự động hóa | Chạy theo lịch | GitHub Actions thực thi theo lịch, không cần máy chủ |

> Chi tiết báo cáo lịch sử sẽ ưu tiên hiển thị văn bản "điểm bắn tỉa" gốc do AI trả về, tránh việc vùng giá và điều kiện phức tạp bị nén thành một con số khi xem lại lịch sử.

> Không gian làm việc Web đã hoàn thành nâng cấp giao diện: thêm chủ đề sáng đầy đủ, hỗ trợ chuyển đổi sáng/tối một chạm; trang chủ, hỏi cổ phiếu, backtest, danh mục, trang cài đặt dùng chung hệ thống design token, bề mặt nhập liệu, phản hồi trạng thái và ngữ nghĩa drawer cuộn.

### Công Nghệ & Nguồn Dữ Liệu

| Loại | Hỗ trợ |
|------|------|
| Mô hình AI | [AIHubMix](https://aihubmix.com/?aff=CfMq), Gemini, OpenAI tương thích, DeepSeek, Claude, Ollama cục bộ, v.v. (thông qua [LiteLLM](https://github.com/BerriAI/litellm) gọi thống nhất, hỗ trợ cân bằng tải nhiều Key) |
| Dữ liệu giá | vnstock (primary), TCBS (fallback) |
| Tìm kiếm tin tức | Tavily, SerpAPI, Brave, MiniMax |

### Kỷ Luật Giao Dịch Tích Hợp

| Quy tắc | Mô tả |
|------|------|
| Cấm đuổi giá | Tỷ lệ lệch vượt ngưỡng (mặc định 5%, cấu hình được) tự động cảnh báo rủi ro; cổ phiếu xu hướng mạnh tự động nới lỏng |
| Giao dịch theo xu hướng | MA5 > MA10 > MA20 cấu trúc tăng |
| Điểm chính xác | Giá mua, giá cắt lỗ, giá mục tiêu |
| Danh sách kiểm tra | Mỗi điều kiện được đánh dấu "đáp ứng / chú ý / chưa đáp ứng" |
| Thời hiệu tin tức | Có thể cấu hình thời hiệu tối đa (mặc định 3 ngày), tránh sử dụng thông tin cũ |

## 🚀 Bắt Đầu Nhanh

### Cách 1: GitHub Actions (Khuyên dùng)

> Hoàn thành triển khai trong 5 phút, không tốn chi phí, không cần máy chủ.


#### 1. Fork kho lưu trữ này

Nhấn nút `Fork` ở góc trên bên phải (và nhấn Star⭐ để ủng hộ)

#### 2. Cấu hình Secrets

`Settings` → `Secrets and variables` → `Actions` → `New repository secret`

**Cấu hình mô hình AI (cấu hình ít nhất một)**

> Chi tiết xem [Hướng dẫn cấu hình LLM](docs/LLM_CONFIG_GUIDE.md). Người dùng nâng cao có thể cấu hình `LITELLM_MODEL`, `LITELLM_FALLBACK_MODELS` hoặc `LLM_CHANNELS` chế độ đa kênh.

> 💡 **Khuyên dùng [AIHubMix](https://aihubmix.com/?aff=CfMq)**: Một Key có thể sử dụng Gemini, GPT, Claude, DeepSeek và các mô hình phổ biến toàn cầu, không cần VPN, bao gồm cả mô hình miễn phí.

| Tên Secret | Mô tả | Bắt buộc |
|------------|------|:----:|
| `AIHUBMIX_KEY` | [AIHubMix](https://aihubmix.com/?aff=CfMq) API Key, một Key dùng được toàn bộ mô hình | Tùy chọn |
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com/) lấy Key miễn phí | Tùy chọn |
| `ANTHROPIC_API_KEY` | [Anthropic Claude](https://console.anthropic.com/) API Key | Tùy chọn |
| `OPENAI_API_KEY` | OpenAI tương thích API Key (hỗ trợ DeepSeek, v.v.) | Tùy chọn |
| `OPENAI_BASE_URL` | OpenAI tương thích API địa chỉ | Tùy chọn |
| `OPENAI_MODEL` | Tên mô hình | Tùy chọn |
| `OLLAMA_API_BASE` | Ollama dịch vụ cục bộ địa chỉ | Tùy chọn |

<details>
<summary><b>Cấu hình kênh thông báo</b> (nhấn để mở, cấu hình ít nhất một)</summary>


| Tên Secret | Mô tả | Bắt buộc |
|------------|------|:----:|
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token (lấy từ @BotFather) | Tùy chọn |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID | Tùy chọn |
| `TELEGRAM_MESSAGE_THREAD_ID` | Telegram Topic ID (gửi đến chủ đề con) | Tùy chọn |
| `DISCORD_WEBHOOK_URL` | Discord Webhook URL | Tùy chọn |
| `DISCORD_BOT_TOKEN` | Discord Bot Token (chọn một trong hai với Webhook) | Tùy chọn |
| `DISCORD_MAIN_CHANNEL_ID` | Discord Channel ID (cần khi dùng Bot) | Tùy chọn |
| `SLACK_BOT_TOKEN` | Slack Bot Token (khuyên dùng, hỗ trợ upload ảnh) | Tùy chọn |
| `SLACK_CHANNEL_ID` | Slack Channel ID (cần khi dùng Bot) | Tùy chọn |
| `SLACK_WEBHOOK_URL` | Slack Incoming Webhook URL (chỉ text, không hỗ trợ ảnh) | Tùy chọn |
| `EMAIL_SENDER` | Email người gửi | Tùy chọn |
| `EMAIL_PASSWORD` | Mật khẩu ứng dụng (không phải mật khẩu đăng nhập) | Tùy chọn |
| `EMAIL_RECEIVERS` | Email người nhận (nhiều email cách nhau dấu phẩy) | Tùy chọn |
| `EMAIL_SENDER_NAME` | Tên hiển thị người gửi email | Tùy chọn |
| `CUSTOM_WEBHOOK_URLS` | Webhook tùy chỉnh (hỗ trợ nhiều URL, cách nhau dấu phẩy) | Tùy chọn |
| `CUSTOM_WEBHOOK_BEARER_TOKEN` | Bearer Token cho Webhook tùy chỉnh | Tùy chọn |
| `SCHEDULE_RUN_IMMEDIATELY` | Chế độ lịch: khởi động có thực thi ngay lần đầu không | Tùy chọn |
| `RUN_IMMEDIATELY` | Chế độ thủ công: khởi động có thực thi ngay không | Tùy chọn |
| `SINGLE_STOCK_NOTIFY` | Chế độ đẩy từng cổ phiếu: đặt `true` để đẩy ngay sau khi phân tích xong mỗi cổ phiếu | Tùy chọn |
| `REPORT_TYPE` | Loại báo cáo: `simple`(rút gọn), `full`(đầy đủ), `brief`(3-5 câu tóm tắt) | Tùy chọn |
| `REPORT_LANGUAGE` | Ngôn ngữ báo cáo: `vi`(mặc định Tiếng Việt) / `en`(Tiếng Anh) | Tùy chọn |
| `REPORT_SUMMARY_ONLY` | Chỉ tóm tắt kết quả phân tích | Tùy chọn |
| `MAX_WORKERS` | Số luồng xử lý đồng thời (mặc định `3`) | Tùy chọn |
| `MERGE_EMAIL_NOTIFICATION` | Gộp push cá nhân và tổng kết thị trường vào một email (mặc định false) | Tùy chọn |
| `MARKDOWN_TO_IMAGE_CHANNELS` | Chuyển Markdown thành ảnh để gửi (cách nhau dấu phẩy) | Tùy chọn |
| `MARKDOWN_TO_IMAGE_MAX_CHARS` | Vượt quá độ dài này không chuyển ảnh (mặc định `15000`) | Tùy chọn |
| `MD2IMG_ENGINE` | Công cụ chuyển ảnh: `wkhtmltoimage` (mặc định) hoặc `markdown-to-file` | Tùy chọn |

> Cấu hình ít nhất một kênh, cấu hình nhiều kênh sẽ đẩy đồng thời. Chi tiết xem [Hướng dẫn đầy đủ](docs/full-guide.md)

</details>

**Cấu hình khác**

| Tên Secret | Mô tả | Bắt buộc |
|------------|------|:----:|
| `STOCK_LIST` | Mã cổ phiếu tự chọn, ví dụ `VCB,VNM,FPT` | ✅ |
| `TAVILY_API_KEYS` | [Tavily](https://tavily.com/) Search API (tìm kiếm tin tức) | Khuyên dùng |
| `MINIMAX_API_KEYS` | [MiniMax](https://platform.minimaxi.com/) Coding Plan Web Search | Tùy chọn |
| `SERPAPI_API_KEYS` | [SerpAPI](https://serpapi.com/baidu-search-api?utm_source=github_daily_stock_analysis) tìm kiếm dự phòng | Tùy chọn |
| `BRAVE_API_KEYS` | [Brave Search](https://brave.com/search/api/) API | Tùy chọn |
| `AGENT_MODE` | Bật chế độ Agent hỏi chiến lược (`true`/`false`, mặc định false) | Tùy chọn |
| `AGENT_LITELLM_MODEL` | Mô hình chính Agent | Tùy chọn |
| `AGENT_SKILLS` | Kỹ năng chiến lược được kích hoạt (cách nhau dấu phẩy), `all` = bật hết | Tùy chọn |
| `AGENT_MAX_STEPS` | Số bước suy luận tối đa Agent (mặc định 10) | Tùy chọn |
| `TRADING_DAY_CHECK_ENABLED` | Kiểm tra ngày giao dịch (mặc định `true`): bỏ qua ngày không giao dịch | Tùy chọn |

#### 3. Kích hoạt Actions

Nhấn tab `Actions` → `I understand my workflows, go ahead and enable them`

#### 4. Test thủ công

`Actions` → `Daily Stock Analysis` → `Run workflow` → `Run workflow`

#### Hoàn thành

Mặc định mỗi **ngày làm việc 18:00 (Giờ VN)** tự động thực thi, cũng có thể kích hoạt thủ công. Mặc định bỏ qua ngày nghỉ lễ VN.

### Cách 2: Chạy cục bộ / Docker

```bash
# Clone dự án
git clone https://github.com/ZhuLinsen/daily_stock_analysis.git && cd daily_stock_analysis

# Cài đặt thư viện
pip install -r requirements.txt

# Cấu hình biến môi trường
cp .env.example .env && vim .env

# Chạy phân tích
python main.py
```

Nếu không dùng Web, khuyên cấu hình trực tiếp trong `.env`:

```env
LLM_CHANNELS=primary
LLM_PRIMARY_PROTOCOL=openai
LLM_PRIMARY_BASE_URL=https://api.deepseek.com/v1
LLM_PRIMARY_API_KEY=sk-xxxxxxxx
LLM_PRIMARY_MODELS=deepseek-chat
LITELLM_MODEL=openai/deepseek-chat
```

> Triển khai Docker, cấu hình lịch chạy tự động xem [Hướng dẫn đầy đủ](docs/full-guide.md)
> Đóng gói desktop xem [Hướng dẫn đóng gói desktop](docs/desktop-package.md)

## 📱 Hiệu Ứng Đẩy Tin

### Bảng Điều Khiển Quyết Định
```
🎯 2026-04-07 Bảng Điều Khiển Quyết Định
Phân tích 3 cổ phiếu | 🟢Mua:1 🟡Quan sát:1 🔴Bán:1

📊 Tóm tắt kết quả phân tích
🟢 VCB (Vietcombank): Mua | Điểm 72 | Bullish
⚪ FPT (FPT Corp): Quan sát | Điểm 55 | Sideway
🔴 HPG (Hoa Phat): Bán | Điểm 38 | Bearish
```

## ⚙️ Mô Tả Cấu Hình

> 📖 Biến môi trường đầy đủ, cấu hình lịch task xem [Hướng dẫn cấu hình đầy đủ](docs/full-guide.md)


## 🖥️ Giao Diện Web

![img.png](sources/fastapi_server.png)

Bao gồm quản lý cấu hình đầy đủ, giám sát task và phân tích thủ công.

**Điểm nổi bật nâng cấp giao diện:**

- **Chủ đề sáng hoàn toàn mới**: Không chỉ chế độ tối — chế độ sáng được vẽ lại toàn bộ cho ô nhập liệu, cấp bậc card, biên tương phản, trạng thái cảnh báo.
- **Chuyển đổi chủ đề lưu trạng thái**: Sidebar có thể chuyển sáng/tối bất kỳ lúc nào, sau khi refresh trang vẫn giữ lựa chọn.
- **Các trang cốt lõi thống nhất**: Trang chủ, hỏi cổ phiếu, backtest, danh mục, cài đặt dùng chung một bộ design token, nguyên tử trạng thái và bề mặt component.
- **Trải nghiệm mobile và cảm ứng cải thiện**: Drawer overlay, hợp đồng cuộn, khả năng tiếp cận thao tác tin nhắn và ngữ nghĩa nút chính được đồng bộ.

**Bảo vệ mật khẩu tùy chọn**: Đặt `ADMIN_AUTH_ENABLED=true` trong `.env` để bật đăng nhập Web. Xem [Hướng dẫn đầy đủ](docs/full-guide.md).

### Nhập Thông Minh

Tại **Cài đặt → Cài đặt cơ bản** tìm khối "Nhập thông minh", hỗ trợ 3 cách thêm cổ phiếu tự chọn:

1. **Ảnh**: Kéo thả hoặc chọn ảnh chụp màn hình danh mục, Vision AI tự động nhận diện mã+tên
2. **File**: Upload CSV hoặc Excel (.xlsx), tự động phân tích cột mã/tên
3. **Dán**: Copy từ Excel hoặc bảng rồi dán, nhấn "Giải mã"

**Xem trước & Gộp**: Tin cậy cao mặc định được chọn, trung/thấp cần chọn thủ công; hỗ trợ loại trùng theo mã, xóa tất cả, chọn tất cả.

### Tìm Kiếm Thông Minh Tự Động Hoàn Thành (MVP)

Ô nhập liệu phân tích trang chủ đã được nâng cấp thành ô tự động hoàn thành kiểu "search engine":

- **Khớp đa chiều**: Hỗ trợ nhập mã cổ phiếu, tên, viết tắt hoặc biệt danh.
- **Phủ thị trường VN**: Chỉ số cục bộ đã phủ **HOSE, HNX**; tạo từ vnstock hoặc TCBS, hỗ trợ cập nhật theo yêu cầu.
- **Logic fallback tự động**: Cổ phiếu mới/bất thường hệ thống tự động về chế độ nhập thường.

### 🤖 Agent Hỏi Chiến Lược

Đặt `AGENT_MODE=true` trong `.env` rồi khởi động dịch vụ, truy cập `/chat` để bắt đầu hỏi đáp chiến lược đa lượt.

- **Chọn chiến lược**: MA golden cross, Chan theory, Wave theory, Bull trend, v.v. 11 chiến lược tích hợp
- **Hỏi bằng ngôn ngữ tự nhiên**: Ví dụ "dùng Chan theory phân tích VCB", Agent tự động gọi công cụ thị trường, nến, chỉ số kỹ thuật, tin tức
- **Phản hồi tiến trình stream**: Hiển thị quá trình suy luận AI theo thời gian thực
- **Trò chuyện đa lượt**: Hỗ trợ hỏi tiếp theo ngữ cảnh, lịch sử phiên được lưu lại
- **Bot lệnh**: `/ask` phân tích kỹ năng (hỗ trợ so sánh nhiều mã), `/chat` trò chuyện tự do, `/history` lịch sử phiên, `/strategies` danh sách chiến lược

### Cách Khởi Động

1. **Khởi động dịch vụ** (mặc định tự động biên dịch frontend)
   ```bash
   python main.py --webui       # Khởi động Web + thực thi phân tích theo lịch
   python main.py --webui-only  # Chỉ khởi động Web
   ```

Truy cập `http://127.0.0.1:8000` để sử dụng.

## 🗺️ Lộ Trình

Xem các tính năng đã hỗ trợ và kế hoạch tương lai: [Nhật ký thay đổi](docs/CHANGELOG.md)

> Có gợi ý? Hoan nghênh [Gửi Issue](https://github.com/ZhuLinsen/daily_stock_analysis/issues)

---

## ☕ Ủng Hộ Dự Án

Nếu dự án này hữu ích cho bạn, hoan nghênh ủng hộ để duy trì và phát triển tiếp 🙏

Nhấn ⭐ **Star** trên GitHub là cách ủng hộ đơn giản nhất!

---

## 🤝 Đóng Góp

Hoan nghênh gửi Issue và Pull Request!

Chi tiết xem [Hướng dẫn đóng góp](docs/CONTRIBUTING.md)

### Kiểm tra cục bộ (khuyên chạy trước)

```bash
pip install -r requirements.txt
pip install flake8 pytest
./scripts/ci_gate.sh
```

Nếu sửa frontend (`apps/dsa-web`):

```bash
cd apps/dsa-web
npm ci
npm run lint
npm run build
```

## 📄 Giấy Phép
[MIT License](LICENSE) © 2026 ZhuLinsen

Nếu bạn sử dụng hoặc phát triển dựa trên dự án này,
hoan nghênh ghi rõ nguồn trong README hoặc tài liệu và đính kèm link kho lưu trữ này.

## 📬 Liên Hệ & Hợp Tác
- GitHub Issues: [Gửi Issue](https://github.com/ZhuLinsen/daily_stock_analysis/issues)
- Email hợp tác: zhuls345@gmail.com

## ⭐ Lịch Sử Star
**Nếu thấy hữu ích, hãy nhấn ⭐ Star để ủng hộ!**

<a href="https://star-history.com/#ZhuLinsen/daily_stock_analysis&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=ZhuLinsen/daily_stock_analysis&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=ZhuLinsen/daily_stock_analysis&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=ZhuLinsen/daily_stock_analysis&type=Date" />
 </picture>
</a>

## ⚠️ Tuyên Bố Miễn Trừ Trách Nhiệm

Dự án này chỉ phục vụ mục đích học tập và nghiên cứu, không cấu thành bất kỳ lời khuyên đầu tư nào. Thị trường chứng khoán có rủi ro, đầu tư cần thận trọng. Tác giả không chịu trách nhiệm cho bất kỳ tổn thất nào phát sinh từ việc sử dụng dự án này.

---
