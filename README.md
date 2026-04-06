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

> 🤖 Hệ thống phân tích cổ phiếu tự chọn thông minh dựa trên AI, hỗ trợ HOSE/HNX/UPCOM và quốc tế, tự động phân tích và đẩy "Bảng Điều Khiển Quyết Định" qua Telegram/Discord/Slack/Email/Zalo

[**Tính Năng**](#-tính-năng) · [**Bắt Đầu Nhanh**](#-bắt-đầu-nhanh) · [**Hiệu Ứng Đẩy Tin**](#-hiệu-ứng-đẩy-tin) · [**Hướng Dẫn Đầy Đủ**](docs/full-guide.md) · [**Câu Hỏi Thường Gặp**](docs/FAQ.md) · [**Nhật Ký Thay Đổi**](docs/CHANGELOG.md)

Tiếng Việt | [English](docs/README_EN.md)

</div>

## 💖 Nhà Tài Trợ (Sponsors)
<div align="center">
  <a href="https://serpapi.com/baidu-search-api?utm_source=github_daily_stock_analysis" target="_blank">
    <img src="./sources/serpapi_banner_zh.png" alt="SerpApi - Thu thập dữ liệu tài chính thời gian thực" height="160">
  </a>
</div>
<br>


## ✨ Tính Năng

| Mô-đun | Tính năng | Mô tả |
|------|------|------|
| AI | Bảng điều khiển quyết định | Kết luận chính một câu + điểm mua/bán chính xác + danh sách kiểm tra thao tác |
| Phân tích | Phân tích đa chiều | Kỹ thuật (MA thời gian thực/cấu trúc bullish) + phân phối筹码 + thông tin舆情 + báo giá thời gian thực |
| Thị trường | Thị trường toàn cầu | Hỗ trợ HOSE, HNX, UPCOM, cổ phiếu quốc tế và chỉ số (SPX, DJI, IXIC, v.v.) |
| Cơ bản | Tổng hợp có cấu trúc | Thêm `fundamental_context` (valuation/growth/earnings/institution/capital_flow/dragon_tiger/boards), hạ cấp fail-open trên chuỗi chính |
| Chiến lược | Hệ thống chiến lược thị trường | Tích hợp chiến lược "3 bước tổng kết" VN và "Regime Strategy" quốc tế, xuất ra kế hoạch tấn công/cân bằng/phòng thủ |
| Tổng kết | Tổng kết thị trường | Tổng quan thị trường hàng ngày, tăng/giảm ngành; hỗ trợ chuyển đổi vn(Chứng khoán VN)/us(Mỹ)/both(Cả hai) |
| Giao diện | Không gian làm việc 2 chủ đề | Web hỗ trợ chuyển đổi sáng/tối, trang chủ / hỏi / backtest / danh mục / cài đặt thống nhất hệ thống giao diện |
| Tự động hoàn thành | Tự động hoàn thành thông minh (MVP) | **[Giai đoạn thử nghiệm]** Ô tìm kiếm trang chủ hỗ trợ gợi ý mã/tên/pinyin/biệt danh; chỉ số đã覆盖 HOSE, HNX, UPCOM |
| Nhập thông minh | Nhập đa nguồn | Hỗ trợ ảnh, file CSV/Excel, dán từ clipboard; Vision LLM trích xuất mã+tên; xác nhận theo tầng tin cậy |
| Lịch sử | Quản lý hàng loạt | Hỗ trợ chọn nhiều, chọn tất cả và xóa hàng loạt bản ghi phân tích lịch sử |
| Backtest | Xác minh backtest AI | Tự động đánh giá độ chính xác phân tích lịch sử, tỷ lệ thắng hướng, tỷ lệ chốt lời/chốt lỗ |
| **Agent hỏi cổ phiếu** | **Trò chuyện chiến lược** | **Hỏi đáp chiến lược đa lượt, hỗ trợ 11 chiến lược tích hợp, Web/Bot/API toàn chuỗi** |
| Đẩy tin | Thông báo đa kênh | Telegram, Discord, Slack, Zalo, Email, Webhook tùy chỉnh |
| Tự động hóa | Chạy theo lịch | GitHub Actions thực thi theo lịch, không cần máy chủ |

> Chi tiết báo cáo lịch sử sẽ ưu tiên hiển thị văn bản "điểm bắn tỉa" gốc do AI trả về, tránh giá区间, giải thích điều kiện và nội dung phức tạp bị压缩 thành một số khi xem lại lịch sử.

> Không gian làm việc Web đã hoàn thành nâng cấp giao diện: thêm chủ đề sáng đầy đủ, hỗ trợ chuyển đổi sáng/tối một chạm; trang chủ, hỏi cổ phiếu, backtest, danh mục, trang cài đặt dùng chung hệ thống design token, bề mặt nhập liệu, phản hồi trạng thái và ngữ nghĩa drawer cuộn.

### Công Nghệ & Nguồn Dữ Liệu

| Loại | Hỗ trợ |
|------|------|
| Mô hình AI | [AIHubMix](https://aihubmix.com/?aff=CfMq), Gemini, OpenAI tương thích, DeepSeek, Claude, Ollama cục bộ, v.v. (thông qua [LiteLLM](https://github.com/BerriAI/litellm) gọi thống nhất, hỗ trợ cân bằng tải nhiều Key) |
| Dữ liệu giá | vnstock, TCBS |
| Tìm kiếm tin tức | Tavily, SerpAPI, Brave, MiniMax |

> Lưu ý: Dữ liệu lịch sử và giá thời gian thực cổ phiếu quốc tế统一使用 YFinance

### Kỷ Luật Giao Dịch Tích Hợp

| Quy tắc | Mô tả |
|------|------|
| Cấm追高 | Tỷ lệ乖离超过 ngưỡng (mặc định 5%, có thể cấu hình) tự động提示风险; cổ phiếu强势放宽 tự động |
| Giao dịch theo xu hướng | MA5 > MA10 > MA20 cấu trúc多头 |
| Điểm chính xác | Giá mua, giá chốt lỗ, giá mục tiêu |
| Danh sách kiểm tra | Mỗi điều kiện标记 là "đáp ứng / chú ý / chưa đáp ứng" |
| Thời效 tin tức | Có thể cấu hình thời效 tối đa tin tức (mặc định 3 ngày),避免 sử dụng thông tin过时 |

## 🚀 Bắt Đầu Nhanh

### Cách 1: GitHub Actions (Khuyên dùng)

> Hoàn thành部署 trong 5 phút,零 chi phí, không cần máy chủ.


#### 1. Fork kho lưu trữ này

Nhấn nút `Fork` ở góc trên bên phải (顺便 nhấn Star⭐ để ủng hộ)

#### 2. Cấu hình Secrets

`Settings` → `Secrets and variables` → `Actions` → `New repository secret`

**Cấu hình mô hình AI (cấu hình ít nhất một)**

> Chi tiết xem [Hướng dẫn cấu hình LLM](docs/LLM_CONFIG_GUIDE.md). Người dùng nâng cao có thể cấu hình `LITELLM_MODEL`, `LITELLM_FALLBACK_MODELS` hoặc `LLM_CHANNELS` chế độ đa kênh.

> 💡 **Khuyên dùng [AIHubMix](https://aihubmix.com/?aff=CfMq)**: Một Key có thể sử dụng Gemini, GPT, Claude, DeepSeek và các mô hình主流 toàn cầu, không cần VPN,包含 mô hình miễn phí.

| Tên Secret | Mô tả | Bắt buộc |
|------------|------|:----:|
| `AIHUBMIX_KEY` | [AIHubMix](https://aihubmix.com/?aff=CfMq) API Key, một Key切换 toàn bộ mô hình | Tùy chọn |
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
| `SLACK_WEBHOOK_URL` | Slack Incoming Webhook URL (chỉ文本, không hỗ trợ ảnh) | Tùy chọn |
| `EMAIL_SENDER` | Email người gửi | Tùy chọn |
| `EMAIL_PASSWORD` | Mật khẩu ứng dụng (không phải mật khẩu đăng nhập) | Tùy chọn |
| `EMAIL_RECEIVERS` | Email người nhận (nhiều email cách nhau dấu phẩy) | Tùy chọn |
| `EMAIL_SENDER_NAME` | Tên hiển thị người gửi email | Tùy chọn |
| `CUSTOM_WEBHOOK_URLS` | Webhook tùy chỉnh (hỗ trợ nhiều URL, cách nhau dấu phẩy) | Tùy chọn |
| `CUSTOM_WEBHOOK_BEARER_TOKEN` | Bearer Token cho Webhook tùy chỉnh | Tùy chọn |
| `SCHEDULE_RUN_IMMEDIATELY` | Chế độ定时: khởi động có thực thi ngay一次 không | Tùy chọn |
| `RUN_IMMEDIATELY` | Chế độ không定时: khởi động có thực thi ngay一次 không | Tùy chọn |
| `SINGLE_STOCK_NOTIFY` | Chế độ đẩy từng cổ phiếu: đặt `true` để đẩy ngay sau khi phân tích xong mỗi cổ phiếu | Tùy chọn |
| `REPORT_TYPE` | Loại báo cáo: `simple`(rút gọn), `full`(đầy đủ), `brief`(3-5 câu tóm tắt) | Tùy chọn |
| `REPORT_LANGUAGE` | Ngôn ngữ báo cáo: `vi`(mặc định Tiếng Việt) / `en`(Tiếng Anh) | Tùy chọn |
| `REPORT_SUMMARY_ONLY` | Chỉ tóm tắt kết quả phân tích | Tùy chọn |
| `MAX_WORKERS` | Số luồng xử lý đồng thời (mặc định `3`) | Tùy chọn |
| `MERGE_EMAIL_NOTIFICATION` | Gộp推送 cá nhân và tổng kết thị trường (mặc định false) | Tùy chọn |
| `MARKDOWN_TO_IMAGE_CHANNELS` | Chuyển Markdown thành ảnh để gửi (cách nhau dấu phẩy) | Tùy chọn |
| `MARKDOWN_TO_IMAGE_MAX_CHARS` | Vượt quá độ dài này không chuyển ảnh (mặc định `15000`) | Tùy chọn |
| `MD2IMG_ENGINE` | Công cụ chuyển ảnh: `wkhtmltoimage` (mặc định) hoặc `markdown-to-file` | Tùy chọn |

> Cấu hình ít nhất một kênh, cấu hình nhiều kênh sẽ đẩy同时. Chi tiết xem [Hướng dẫn đầy đủ](docs/full-guide.md)

</details>

**Cấu hình khác**

| Tên Secret | Mô tả | Bắt buộc |
|------------|------|:----:|
| `STOCK_LIST` | Mã cổ phiếu tự chọn, ví dụ `VCB,VNM,FPT` | ✅ |
| `TAVILY_API_KEYS` | [Tavily](https://tavily.com/) Search API (tìm kiếm tin tức) | Khuyên dùng |
| `MINIMAX_API_KEYS` | [MiniMax](https://platform.minimaxi.com/) Coding Plan Web Search | Tùy chọn |
| `SERPAPI_API_KEYS` | [SerpAPI](https://serpapi.com/baidu-search-api?utm_source=github_daily_stock_analysis) tìm kiếm备用 | Tùy chọn |
| `BRAVE_API_KEYS` | [Brave Search](https://brave.com/search/api/) API | Tùy chọn |
| `TUSHARE_TOKEN` | [Tushare Pro](https://tushare.pro/weborder/#/login?reg=834638 ) Token | Tùy chọn |
| `TICKFLOW_API_KEY` | [TickFlow](https://tickflow.org) API Key | Tùy chọn |
| `AGENT_MODE` | Bật chế độ Agent hỏi chiến lược (`true`/`false`, mặc định false) | Tùy chọn |
| `AGENT_LITELLM_MODEL` | Mô hình chính Agent (tùy chọn) | Tùy chọn |
| `AGENT_SKILLS` | Kỹ năng chiến lược được激活 (cách nhau dấu phẩy), `all`启用全部 | Tùy chọn |
| `AGENT_MAX_STEPS` | Số bước推理 tối đa Agent (mặc định 10) | Tùy chọn |
| `TRADING_DAY_CHECK_ENABLED` | Kiểm tra ngày giao dịch (mặc định `true`):非交易日跳过 thực thi | Tùy chọn |

#### 3. Kích hoạt Actions

Nhấn tab `Actions` → `I understand my workflows, go ahead and enable them`

#### 4. Test thủ công

`Actions` → `每日股票分析` → `Run workflow` → `Run workflow`

#### Hoàn thành

Mặc định mỗi **ngày làm việc 18:00 (Giờ VN)** tự động thực thi, cũng có thể触发 thủ công. Mặc định非交易日 (bao gồm节假日 VN/US) không thực thi.

### Cách 2: Chạy cục bộ / Docker部署

```bash
# Clone dự án
git clone https://github.com/ZhuLinsen/daily_stock_analysis.git && cd daily_stock_analysis

# Cài đặt依赖
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

> Docker部署, cấu hình定时任务 xem [Hướng dẫn đầy đủ](docs/full-guide.md)
> Đóng gói desktop xem [Hướng dẫn đóng gói desktop](docs/desktop-package.md)

## 📱 Hiệu Ứng Đẩy Tin

### Bảng Điều Khiển Quyết Định
```
🎯 2026-02-08 Bảng Điều Khiển Quyết Định
Phân tích 3 cổ phiếu | 🟢Mua:0 🟡Quan sát:2 🔴Bán:1

📊 Tóm tắt kết quả phân tích
⚪ 中钨高新(000657): Quan sát | Điểm 65 | Bullish
⚪ 永鼎股份(600105): Quan sát | Điểm 48 | Sideway
🟡 新莱应材(300260): Bán | Điểm 35 | Bearish
```

## ⚙️ Mô Tả Cấu Hình

> 📖 Biến môi trường đầy đủ, cấu hình定时 task xem [Hướng dẫn cấu hình đầy đủ](docs/full-guide.md)


## 🖥️ Giao Diện Web

![img.png](sources/fastapi_server.png)

Bao gồm quản lý cấu hình đầy đủ, giám sát task và phân tích thủ công.

**Điểm nổi bật nâng cấp giao diện本轮:**

- **Chủ đề sáng hoàn toàn mới**: Không chỉ có模式 tối,模式 sáng được重新绘制 toàn bộ cho ô nhập liệu, cấp bậc卡片,对比 biên,提示 trạng thái.
- **Chuyển đổi主题 có thể持久化**: Sidebar có thể随时 chuyển đổi sáng/tối, sau khi刷新 trang仍然保留 lựa chọn người dùng.
- **Các trang核心 thống nhất收口**: Trang chủ, hỏi cổ phiếu, backtest, danh mục, cài đặt dùng chung一套视觉 token, nguyên tử trạng thái và组件 bề mặt.
- **Trải nghiệm移动端 và cảm ứng增强**: Drawer遮罩, hợp đồng cuộn,可达性 thao tác消息 và语义 nút关键同步补强.

**Bảo vệ mật khẩu tùy chọn**: Đặt `ADMIN_AUTH_ENABLED=true` trong `.env` để启用 đăng nhập Web. Xem [Hướng dẫn đầy đủ](docs/full-guide.md).

### Nhập Thông Minh

Tại **Cài đặt → Cài đặt cơ bản** tìm khối "Nhập thông minh", hỗ trợ 3 cách thêm cổ phiếu tự chọn:

1. **Ảnh**: Kéo thả hoặc chọn ảnh截图持仓, Vision AI tự động识别 mã+tên
2. **File**: Upload CSV hoặc Excel (.xlsx), tự động解析 cột mã/tên
3. **Dán**: Copy từ Excel hoặc表格 rồi dán, nhấn "Giải mã"

**Xem trước & Gộp**: Tin cậy cao mặc định勾选, trung/thấp cần勾选 thủ công; hỗ trợ去重 theo mã, xóa tất cả, chọn tất cả.

### Tìm Kiếm Thông Minh Tự Động Hoàn Thành (MVP)

Ô nhập liệu phân tích trang chủ đã升级 thành ô tự động hoàn thành "kiểu搜索引擎":

- **Khớp đa chiều**: Hỗ trợ nhập mã cổ phiếu, tên, viết tắt拼音 hoặc biệt danh.
- **Phủ多 thị trường**: Chỉ số cục bộ已覆盖 **HOSE, HNX, UPCOM**; tạo từ vnstock hoặc TCBS, hỗ trợ cập nhật theo yêu cầu.
- **Logic降级 tự động**: Cổ phiếu mới/bất thường hệ thống无缝退回模式 nhập普通.

### 🤖 Agent Hỏi Chiến Lược

Đặt `AGENT_MODE=true` trong `.env` rồi启动 dịch vụ, truy cập `/chat` để bắt đầu hỏi đáp chiến lược đa lượt.

- **Chọn chiến lược**: MA golden cross, Chan theory, Wave theory, Bull trend, v.v. 11 chiến lược tích hợp
- **Hỏi bằng ngôn ngữ tự nhiên**: Ví dụ "dùng Chan theory phân tích VCB", Agent tự động gọi công cụ行情, K线, chỉ số kỹ thuật, tin tức
- **Phản hồi tiến trình流式**: Hiển thị实时路径思考 AI
- **Trò chuyện đa lượt**: Hỗ trợ追问上下文, lịch sử phiên持久化
- **Bot lệnh**: `/ask` phân tích技能 (hỗ trợ对比多股), `/chat` trò chuyện自由, `/history` lịch sử phiên, `/strategies` danh sách chiến lược

### Cách Khởi Động

1. **Khởi động dịch vụ** (mặc định tự động编译前端)
   ```bash
   python main.py --webui       # Khởi động Web + thực thi定时 phân tích
   python main.py --webui-only  # Chỉ khởi động Web
   ```

Truy cập `http://127.0.0.1:8000` để sử dụng.

## 🗺️ Lộ Trình

Xem các tính năng đã hỗ trợ và kế hoạch tương lai: [Nhật ký thay đổi](docs/CHANGELOG.md)

> Có gợi ý? Hoan nghênh [Gửi Issue](https://github.com/ZhuLinsen/daily_stock_analysis/issues)

---

## ☕ Ủng Hộ Dự Án

Nếu dự án này hữu ích cho bạn,欢迎 ủng hộ持续维护 và迭代 🙏

| Alipay | WeChat Pay |
| :---: | :---: |
| <img src="./sources/alipay.jpg" width="200" alt="Alipay"> | <img src="./sources/wechatpay.jpg" width="200" alt="WeChat Pay"> |

---

## 🤝 Đóng Góp

Hoan nghênh提交 Issue và Pull Request!

Chi tiết xem [Hướng dẫn đóng góp](docs/CONTRIBUTING.md)

### Kiểm tra cục bộ (khuyên chạy trước)

```bash
pip install -r requirements.txt
pip install flake8 pytest
./scripts/ci_gate.sh
```

Nếu sửa前端 (`apps/dsa-web`):

```bash
cd apps/dsa-web
npm ci
npm run lint
npm run build
```

## 📄 Giấy Phép
[MIT License](LICENSE) © 2026 ZhuLinsen

Nếu bạn sử dụng hoặc phát triển dựa trên dự án này,
hoan nghênh注明来源 trong README hoặc tài liệu và附 link kho lưu trữ này.

## 📬 Liên Hệ & Hợp Tác
- GitHub Issues: [Gửi Issue](https://github.com/ZhuLinsen/daily_stock_analysis/issues)
- Email hợp tác: zhuls345@gmail.com

## ⭐ Lịch Sử Star
**Nếu觉得 hữu ích, hãy nhấn ⭐ Star để ủng hộ!**

<a href="https://star-history.com/#ZhuLinsen/daily_stock_analysis&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=ZhuLinsen/daily_stock_analysis&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=ZhuLinsen/daily_stock_analysis&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=ZhuLinsen/daily_stock_analysis&type=Date" />
 </picture>
</a>

## ⚠️ Tuyên Bố Miễn Trừ Trách Nhiệm

Dự án này仅供 mục đích学习 và nghiên cứu, không构成任何投资建议. Thị trường chứng khoán có风险, đầu tư需谨慎. Tác giả không chịu trách nhiệm cho bất kỳ损失 nào phát sinh từ việc sử dụng dự án này.

---
