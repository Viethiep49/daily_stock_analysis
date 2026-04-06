# 📖 Hướng Dẫn Cấu Hình & Triển Khai Đầy Đủ

Tài liệu này chứa hướng dẫn cấu hình chi tiết cho hệ thống phân tích cổ phiếu thông minh, phù hợp cho người dùng cần tính năng nâng cao hoặc cách triển khai đặc biệt.

> 💡 Để bắt đầu nhanh, vui lòng tham khảo [README.md](../README.md). Tài liệu này dành cho cấu hình nâng cao.

## 📁 Cấu Trúc Dự Án

```
daily_stock_analysis/
├── main.py              # Điểm vào chính
├── src/                 # Logic nghiệp vụ cốt lõi
│   ├── analyzer.py      # Bộ phân tích AI
│   ├── config.py        # Quản lý cấu hình
│   ├── notification.py  # Đẩy tin thông báo
│   └── ...
├── data_provider/       # Bộ chuyển đổi đa nguồn dữ liệu
├── bot/                 # Module tương tác bot
├── api/                 # Dịch vụ FastAPI
├── apps/dsa-web/        # React frontend
├── docker/              # Cấu hình Docker
├── docs/                # Tài liệu dự án
└── .github/workflows/   # GitHub Actions
```

## 📑 Mục Lục

- [Cấu Trúc Dự Án](#cấu-trúc-dự-án)
- [Cấu Hình GitHub Actions Chi Tiết](#cấu-hình-github-actions-chi-tiết)
- [Danh Sách Đầy Đủ Biến Môi Trường](#danh-sách-đầy-đủ-biến-môi-trường)
- [Triển Khai Docker](#triển-khai-docker)
- [Cấu Hình Chạy Cục Bộ Chi Tiết](#cấu-hình-chạy-cục-bộ-chi-tiết)
- [Cấu Hình Tác Vụ Định Kỳ](#cấu-hình-tác-vụ-định-kỳ)
- [Cấu Hình Chi Tiết Kênh Thông Báo](#cấu-hình-chi-tiết-kênh-thông-báo)
- [Cấu Hình Nguồn Dữ Liệu](#cấu-hình-nguồn-dữ-liệu)
- [Tính Năng Nâng Cao](#tính-năng-nâng-cao)
- [Chức Năng Backtest](#chức-năng-backtest)
- [Giao Diện Quản Lý WebUI Cục Bộ](#giao-diện-quản-lý-webui-cục-bộ)

---

## Cấu Hình GitHub Actions Chi Tiết

### 1. Fork Kho Lưu Trữ

Nhấn nút `Fork` ở góc trên phải

### 2. Cấu Hình Secrets

Vào kho bạn đã Fork → `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

<div align="center">
  <img src="../sources/secret_config.png" alt="Sơ đồ cấu hình GitHub Secrets" width="600">
</div>

#### Cấu Hình Mô Hình AI (chọn 1 trong 2)

| Tên Secret | Mô tả | Bắt buộc |
|------------|------|:----:|
| `GEMINI_API_KEY` | Lấy Key miễn phí từ [Google AI Studio](https://aistudio.google.com/) | ✅* |
| `OPENAI_API_KEY` | OpenAI compatible API Key (hỗ trợ DeepSeek, Tongyi Qianwen...) | Tùy chọn |
| `OPENAI_BASE_URL` | Địa chỉ OpenAI compatible API (vd `https://api.deepseek.com/v1`) | Tùy chọn |
| `OPENAI_MODEL` | Tên mô hình (vd `gemini-3.1-pro-preview`, `deepseek-chat`, `gpt-5.2`) | Tùy chọn |

> *Lưu ý: Ít nhất phải cấu hình một trong `GEMINI_API_KEY` hoặc `OPENAI_API_KEY`

#### Cấu Hình Kênh Thông Báo (có thể cấu hình nhiều kênh, đẩy tin đồng thời)

| Tên Secret | Mô tả | Bắt buộc |
|------------|------|:----:|
| `WECHAT_WEBHOOK_URL` | WeChat Work Webhook URL | Tùy chọn |
| `FEISHU_WEBHOOK_URL` | Feishu Webhook URL | Tùy chọn |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token (lấy từ @BotFather) | Tùy chọn |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID | Tùy chọn |
| `TELEGRAM_MESSAGE_THREAD_ID` | Telegram Topic ID (dùng để gửi vào sub-topic) | Tùy chọn |
| `DISCORD_WEBHOOK_URL` | Discord Webhook URL ([cách tạo](https://support.discord.com/hc/en-us/articles/228383668)) | Tùy chọn |
| `DISCORD_BOT_TOKEN` | Discord Bot Token (chọn 1 trong 2 với Webhook) | Tùy chọn |
| `DISCORD_MAIN_CHANNEL_ID` | Discord Channel ID (cần khi dùng Bot) | Tùy chọn |
| `SLACK_BOT_TOKEN` | Slack Bot Token (khuyến nghị, hỗ trợ upload ảnh; ưu tiên hơn Webhook khi cấu hình cả hai) | Tùy chọn |
| `SLACK_CHANNEL_ID` | Slack Channel ID (cần khi dùng Bot) | Tùy chọn |
| `SLACK_WEBHOOK_URL` | Slack Incoming Webhook URL (chỉ text, không hỗ trợ ảnh) | Tùy chọn |
| `EMAIL_SENDER` | Email người gửi (vd `xxx@qq.com`) | Tùy chọn |
| `EMAIL_PASSWORD` | Mật khẩu ủy quyền email (không phải mật khẩu đăng nhập) | Tùy chọn |
| `EMAIL_RECEIVERS` | Email người nhận (cách nhau bởi dấu phẩy, để trống thì gửi cho chính mình) | Tùy chọn |
| `EMAIL_SENDER_NAME` | Tên hiển thị người gửi (mặc định: daily_stock_analysis股票分析助手) | Tùy chọn |
| `PUSHPLUS_TOKEN` | PushPlus Token ([lấy tại đây](https://www.pushplus.plus), dịch vụ đẩy tin nội địa TQ) | Tùy chọn |
| `SERVERCHAN3_SENDKEY` | Server³ Sendkey ([lấy tại đây](https://sc3.ft07.com/), dịch vụ đẩy tin qua app điện thoại) | Tùy chọn |
| `CUSTOM_WEBHOOK_URLS` | Custom Webhook (hỗ trợ DingTalk..., cách nhau bởi dấu phẩy) | Tùy chọn |
| `CUSTOM_WEBHOOK_BEARER_TOKEN` | Bearer Token cho Custom Webhook (dùng cho webhook cần xác thực) | Tùy chọn |
| `WEBHOOK_VERIFY_SSL` | Xác thực chứng chỉ HTTPS cho Webhook (mặc định true). Đặt false để hỗ trợ chứng chỉ tự ký. Cảnh báo: tắt có rủi ro bảo mật nghiêm trọng (MITM), chỉ dùng cho intranet đáng tin | Tùy chọn |

> *Lưu ý: Ít nhất phải cấu hình một kênh, nếu cấu hình nhiều kênh sẽ đẩy tin đồng thời

#### Cấu Hình Hành Vi Đẩy Tin

| Tên Secret | Mô tả | Bắt buộc |
|------------|------|:----:|
| `SINGLE_STOCK_NOTIFY` | Chế độ đẩy từng mã: đặt `true` để đẩy tin ngay sau khi phân tích xong mỗi mã | Tùy chọn |
| `REPORT_TYPE` | Loại báo cáo: `simple`(rút gọn), `full`(đầy đủ), `brief`(3-5 câu tóm tắt), khuyến nghị đặt `full` cho môi trường Docker | Tùy chọn |
| `REPORT_LANGUAGE` | Ngôn ngữ xuất báo cáo: `zh`(mặc định tiếng Trung) / `en`(tiếng Anh) / `vi`(tiếng Việt); ảnh hưởng đồng thời đến Prompt, template, notification fallback và văn bản cố định trên trang Web report | Tùy chọn |
| `REPORT_SUMMARY_ONLY` | Chỉ tóm tắt kết quả phân tích: đặt `true` chỉ đẩy tin tổng hợp, không có chi tiết từng mã; phù hợp xem nhanh khi nhiều mã (mặc định false, Issue #262) | Tùy chọn |
| `REPORT_TEMPLATES_DIR` | Thư mục template Jinja2 (tương đối so với gốc dự án, mặc định `templates`) | Tùy chọn |
| `REPORT_RENDERER_ENABLED` | Bật render template Jinja2 (mặc định `false`, đảm bảo zero regression) | Tùy chọn |
| `REPORT_INTEGRITY_ENABLED` | Bật kiểm tra tính toàn vẹn báo cáo, thử lại hoặc điền placeholder khi thiếu trường bắt buộc (mặc định `true`) | Tùy chọn |
| `REPORT_INTEGRITY_RETRY` | Số lần thử lại kiểm tra toàn vẹn (mặc định `1`, `0` nghĩa là chỉ điền placeholder không thử lại) | Tùy chọn |
| `REPORT_HISTORY_COMPARE_N` | Số lượng tín hiệu lịch sử để so sánh, `0` tắt (mặc định), `>0` bật | Tùy chọn |
| `ANALYSIS_DELAY` | Độ trễ giữa phân tích个股 và大盘 (giây), tránh API rate limit, vd `10` | Tùy chọn |
| `MERGE_EMAIL_NOTIFICATION` | Gộp đẩy tin个股 và大盘复盘 (mặc định false), giảm số lượng email, giảm nguy cơ spam; loại trừ lẫn nhau với `SINGLE_STOCK_NOTIFY` (không hiệu lực trong chế độ单股) | Tùy chọn |
| `MARKDOWN_TO_IMAGE_CHANNELS` | Kênh gửi Markdown chuyển thành ảnh (cách nhau bởi dấu phẩy): telegram,wechat,custom,email,slack; chế độ单股 cần cấu hình đồng thời và cài công cụ chuyển ảnh | Tùy chọn |
| `MARKDOWN_TO_IMAGE_MAX_CHARS` | Không chuyển ảnh nếu vượt quá độ dài này, tránh ảnh siêu lớn (mặc định 15000) | Tùy chọn |
| `MD2IMG_ENGINE` | Engine chuyển ảnh: `wkhtmltoimage` (mặc định, cần wkhtmltopdf) hoặc `markdown-to-file` (emoji đẹp hơn, cần `npm i -g markdown-to-file`) | Tùy chọn |
| `PREFETCH_REALTIME_QUOTES` | Đặt `false` để tắt prefetch realtime quote, tránh efinance/akshare_em kéo toàn thị trường (mặc định true) | Tùy chọn |

#### Cấu Hình Khác

| Tên Secret | Mô tả | Bắt buộc |
|------------|------|:----:|
| `STOCK_LIST` | Mã cổ phiếu tự chọn, vd `600519,300750,002594` | ✅ |
| `TAVILY_API_KEYS` | [Tavily](https://tavily.com/) Search API (tìm kiếm tin tức) | Khuyến nghị |
| `MINIMAX_API_KEYS` | [MiniMax](https://platform.minimaxi.com/) Coding Plan Web Search (kết quả tìm kiếm có cấu trúc) | Tùy chọn |
| `BOCHA_API_KEYS` | [Bocha Search](https://open.bocha.cn/) Web Search API (tối ưu tiếng Trung, hỗ trợ tóm tắt AI, nhiều key cách nhau bởi dấu phẩy) | Tùy chọn |
| `BRAVE_API_KEYS` | [Brave Search](https://brave.com/search/api/) API (ưu tiên quyền riêng tư, tối ưu美股, nhiều key cách nhau bởi dấu phẩy) | Tùy chọn |
| `SERPAPI_API_KEYS` | [SerpAPI](https://serpapi.com/baidu-search-api?utm_source=github_daily_stock_analysis) dự phòng | Tùy chọn |
| `SEARXNG_BASE_URLS` | SearXNG tự dựng (dự phòng không giới hạn quota, cần bật format: json trong settings.yml); để trống sẽ tự động phát hiện public instance | Tùy chọn |
| `SEARXNG_PUBLIC_INSTANCES_ENABLED` | Có tự động lấy public instance từ `searx.space` khi `SEARXNG_BASE_URLS` trống (mặc định `true`) | Tùy chọn |
| `TUSHARE_TOKEN` | [Tushare Pro](https://tushare.pro/weborder/#/login?reg=834638) Token | Tùy chọn |
| `ENABLE_CHIP_DISTRIBUTION` | Bật phân tích筹码分布 (Actions mặc định false; cần dữ liệuchấm khi cấu hình trong Variables thành true, interface có thể không ổn định) | Tùy chọn |

#### ✅ Ví Dụ Cấu Hình Tối Thiểu

Nếu bạn muốn bắt đầu nhanh, tối thiểu cần cấu hình:

1. **Mô hình AI**: `AIHUBMIX_KEY` ([AIHubmix](https://aihubmix.com/?aff=CfMq), một Key đa mô hình), `GEMINI_API_KEY` hoặc `OPENAI_API_KEY`
2. **Kênh thông báo**: Ít nhất một kênh, vd `WECHAT_WEBHOOK_URL` hoặc `EMAIL_SENDER` + `EMAIL_PASSWORD`
3. **Danh sách cổ phiếu**: `STOCK_LIST` (bắt buộc)
4. **Search API**: `TAVILY_API_KEYS` (khuyến nghị mạnh, dùng cho tìm kiếm tin tức)

> 💡 Sau khi cấu hình 4 mục trên là có thể bắt đầu sử dụng!

### 3. Bật Actions

1. Vào kho bạn đã Fork
2. Nhấn tab `Actions`
3. Nếu thấy thông báo nhắc nhở, nhấn `I understand my workflows, go ahead and enable them`

### 4. Kiểm Tra Thủ Công

1. Vào tab `Actions`
2. Chọn workflow `每日股票分析` ở cột trái
3. Nhấn nút `Run workflow` ở cột phải
4. Chọn chế độ chạy
5. Nhấn `Run workflow` màu xanh để xác nhận

### 5. Hoàn Tất!

Mặc định tự động thực thi vào **18:00 (giờ Bắc Kinh)** mỗi ngày làm việc.

---

## Danh Sách Đầy Đủ Biến Môi Trường

### Cấu Hình Mô Hình AI

> Xem chi tiết tại [Hướng Dẫn Cấu Hình LLM](LLM_CONFIG_GUIDE.md) (cấu hình 3 lớp, chế độ kênh, Vision, Agent, xử lý sự cố).

| Tên biến | Mô tả | Giá trị mặc định | Bắt buộc |
|--------|------|--------|:----:|
| `LITELLM_MODEL` | Mô hình chính, định dạng `provider/model` (vd `gemini/gemini-2.5-flash`), khuyến nghị ưu tiên sử dụng | - | Không |
| `AGENT_LITELLM_MODEL` | Mô hình chính cho Agent (tùy chọn); để trống kế thừa `LITELLM_MODEL`, không có prefix provider sẽ phân tích theo `openai/<model>` | - | Không |
| `LITELLM_FALLBACK_MODELS` | Mô hình dự phòng, cách nhau bởi dấu phẩy | - | Không |
| `LLM_CHANNELS` | Danh sách tên kênh (cách nhau bởi dấu phẩy), dùng kèm `LLM_{NAME}_*`, xem [Hướng Dẫn Cấu Hình LLM](LLM_CONFIG_GUIDE.md) | - | Không |
| `LITELLM_CONFIG` | Đường dẫn file cấu hình LiteLLM YAML (nâng cao) | - | Không |
| `AIHUBMIX_KEY` | [AIHubmix](https://aihubmix.com/?aff=CfMq) API Key, một Key chuyển đổi toàn bộ mô hình, không cần cấu hình thêm Base URL | - | Tùy chọn |
| `GEMINI_API_KEY` | Google Gemini API Key | - | Tùy chọn |
| `GEMINI_MODEL` | Tên mô hình chính (legacy, ưu tiên `LITELLM_MODEL`) | `gemini-3-flash-preview` | Không |
| `GEMINI_MODEL_FALLBACK` | Mô hình dự phòng (legacy) | `gemini-2.5-flash` | Không |
| `OPENAI_API_KEY` | OpenAI compatible API Key | - | Tùy chọn |
| `OPENAI_BASE_URL` | OpenAI compatible API URL | - | Tùy chọn |
| `OLLAMA_API_BASE` | Địa chỉ dịch vụ Ollama cục bộ (vd `http://localhost:11434`), xem [Hướng Dẫn Cấu Hình LLM](LLM_CONFIG_GUIDE.md) | - | Tùy chọn |
| `OPENAI_MODEL` | Tên mô hình OpenAI (legacy, người dùng AIHubmix có thể điền vd `gemini-3.1-pro-preview`, `gpt-5.2`) | `gpt-5.2` | Tùy chọn |
| `ANTHROPIC_API_KEY` | Anthropic Claude API Key | - | Tùy chọn |
| `ANTHROPIC_MODEL` | Tên mô hình Claude | `claude-3-5-sonnet-20241022` | Tùy chọn |
| `ANTHROPIC_TEMPERATURE` | Tham số nhiệt độ Claude (0.0-1.0) | `0.7` | Tùy chọn |
| `ANTHROPIC_MAX_TOKENS` | Số token tối đa phản hồi Claude | `8192` | Tùy chọn |

> *Lưu ý: Ít nhất phải cấu hình một trong `AIHUBMIX_KEY`, `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`, `OPENAI_API_KEY` hoặc `OLLAMA_API_BASE`. Người dùng `AIHUBMIX_KEY` không cần cấu hình `OPENAI_BASE_URL`, hệ thống tự động适配.

### Cấu Hình Kênh Thông Báo

| Tên biến | Mô tả | Bắt buộc |
|--------|------|:----:|
| `WECHAT_WEBHOOK_URL` | WeChat Work robot Webhook URL | Tùy chọn |
| `FEISHU_WEBHOOK_URL` | Feishu robot Webhook URL | Tùy chọn |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token | Tùy chọn |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID | Tùy chọn |
| `TELEGRAM_MESSAGE_THREAD_ID` | Telegram Topic ID | Tùy chọn |
| `DISCORD_WEBHOOK_URL` | Discord Webhook URL | Tùy chọn |
| `DISCORD_BOT_TOKEN` | Discord Bot Token (chọn 1 trong 2 với Webhook) | Tùy chọn |
| `DISCORD_MAIN_CHANNEL_ID` | Discord Channel ID (cần khi dùng Bot) | Tùy chọn |
| `DISCORD_MAX_WORDS` | Giới hạn số từ tối đa Discord (mặc định giới hạn server miễn phí 2000) | Tùy chọn |
| `SLACK_BOT_TOKEN` | Slack Bot Token (khuyến nghị, hỗ trợ upload ảnh; ưu tiên hơn Webhook khi cấu hình cả hai) | Tùy chọn |
| `SLACK_CHANNEL_ID` | Slack Channel ID (cần khi dùng Bot) | Tùy chọn |
| `SLACK_WEBHOOK_URL` | Slack Incoming Webhook URL (chỉ text, không hỗ trợ ảnh) | Tùy chọn |
| `EMAIL_SENDER` | Email người gửi | Tùy chọn |
| `EMAIL_PASSWORD` | Mật khẩu ủy quyền email (không phải mật khẩu đăng nhập) | Tùy chọn |
| `EMAIL_RECEIVERS` | Email người nhận (cách nhau bởi dấu phẩy, để trống gửi cho mình) | Tùy chọn |
| `EMAIL_SENDER_NAME` | Tên hiển thị người gửi | Tùy chọn |
| `STOCK_GROUP_N` / `EMAIL_GROUP_N` | Nhóm cổ phiếu gửi đến email khác nhau (Issue #268), vd `STOCK_GROUP_1=600519,300750`配对 với `EMAIL_GROUP_1=user1@example.com` | Tùy chọn |
| `CUSTOM_WEBHOOK_URLS` | Custom Webhook (cách nhau bởi dấu phẩy) | Tùy chọn |
| `CUSTOM_WEBHOOK_BEARER_TOKEN` | Custom Webhook Bearer Token | Tùy chọn |
| `WEBHOOK_VERIFY_SSL` | Xác thực chứng chỉ HTTPS Webhook (mặc định true). Đặt false để hỗ trợ tự ký. Cảnh báo: tắt có rủi ro bảo mật nghiêm trọng | Tùy chọn |
| `PUSHOVER_USER_KEY` | Pushover User Key | Tùy chọn |
| `PUSHOVER_API_TOKEN` | Pushover API Token | Tùy chọn |
| `PUSHPLUS_TOKEN` | PushPlus Token (dịch vụ đẩy tin nội địa TQ) | Tùy chọn |
| `SERVERCHAN3_SENDKEY` | Server³ Sendkey | Tùy chọn |

#### Cấu Hình Feishu Cloud Document (tùy chọn, giải quyết vấn đề tin nhắn bị cắt)

| Tên biến | Mô tả | Bắt buộc |
|--------|------|:----:|
| `FEISHU_APP_ID` | Feishu App ID | Tùy chọn |
| `FEISHU_APP_SECRET` | Feishu App Secret | Tùy chọn |
| `FEISHU_FOLDER_TOKEN` | Feishu Cloud Drive Folder Token | Tùy chọn |

> Các bước cấu hình Feishu Cloud Document:
> 1. Tạo ứng dụng tại [Feishu Developer Console](https://open.feishu.cn/app)
> 2. Cấu hình GitHub Secrets
> 3. Tạo nhóm và thêm robot ứng dụng
> 4. Thêm nhóm vào folder cloud với quyền cộng tác viên (quản lý)

### Cấu Hình Dịch Vụ Tìm Kiếm

| Tên biến | Mô tả | Bắt buộc |
|--------|------|:----:|
| `TAVILY_API_KEYS` | Tavily Search API Key (khuyến nghị) | Khuyến nghị |
| `MINIMAX_API_KEYS` | MiniMax Coding Plan Web Search (kết quả tìm kiếm có cấu trúc) | Tùy chọn |
| `BOCHA_API_KEYS` | Bocha Search API Key (tối ưu tiếng Trung) | Tùy chọn |
| `BRAVE_API_KEYS` | Brave Search API Key (tối ưu美股) | Tùy chọn |
| `SERPAPI_API_KEYS` | SerpAPI dự phòng | Tùy chọn |
| `SEARXNG_BASE_URLS` | SearXNG tự dựng (dự phòng không giới hạn quota, cần bật format: json trong settings.yml); để trống sẽ tự động phát hiện public instance | Tùy chọn |
| `SEARXNG_PUBLIC_INSTANCES_ENABLED` | Có tự động lấy public instance từ `searx.space` khi `SEARXNG_BASE_URLS` trống (mặc định `true`) | Tùy chọn |
| `NEWS_STRATEGY_PROFILE` | Cấu hình cửa sổ chiến lược tin tức: `ultra_short`(1 ngày)/`short`(3 ngày)/`medium`(7 ngày)/`long`(30 ngày); cửa sổ thực tế lấy giá trị nhỏ nhất với `NEWS_MAX_AGE_DAYS` | Mặc định `short` |
| `NEWS_MAX_AGE_DAYS` | Thời hạn tin tức tối đa (ngày), giới hạn kết quả tìm kiếm trong khoảng này | Mặc định `3` |
| `BIAS_THRESHOLD` | Ngưỡng lệch giá (%), vượt quá sẽ cảnh báo không đuổi theo đỉnh; cổ phiếu xu hướng mạnh tự động nới lỏng 1.5 lần | Mặc định `5.0` |

### Cấu Hình Nguồn Dữ Liệu

| Tên biến | Mô tả | Giá trị mặc định | Bắt buộc |
|--------|------|--------|:----:|
| `TUSHARE_TOKEN` | Tushare Pro Token | - | Tùy chọn |
| `TICKFLOW_API_KEY` | TickFlow API Key; sau khi cấu hình,复盘 chỉ số A-share sẽ ưu tiên thử TickFlow, nếu gói hỗ trợ tra cứu pool标的 thì thống kê thị trường cũng ưu tiên TickFlow | - | Tùy chọn |
| `ENABLE_REALTIME_QUOTE` | Bật realtime quote (tắt thì dùng giá đóng cửa lịch sử để phân tích) | `true` | Tùy chọn |
| `ENABLE_REALTIME_TECHNICAL_INDICATORS` | Chỉ số kỹ thuật realtime trong phiên: bật thì dùng giá realtime tính MA5/MA10/MA20 và sắp xếp đa đầu (Issue #234); tắt thì dùng đóng cửa hôm qua | `true` | Tùy chọn |
| `ENABLE_CHIP_DISTRIBUTION` | Bật phân tích筹码分布 (interface không ổn định, khuyến nghị tắt khi deploy cloud). Người dùng GitHub Actions cần đặt `ENABLE_CHIP_DISTRIBUTION=true` trong Repository Variables để bật; workflow mặc định tắt. | `true` | Tùy chọn |
| `ENABLE_EASTMONEY_PATCH` | Patch接口 Đông Phương: khi接口 Đông Phương liên tục thất bại (vd RemoteDisconnected, kết nối bị đóng) khuyến nghị đặt `true`, tiêm token NID và User-Agent ngẫu nhiên để giảm xác suất bị giới hạn | `false` | Tùy chọn |
| `REALTIME_SOURCE_PRIORITY` | Ưu tiên nguồn dữ liệu realtime quote (cách nhau bởi dấu phẩy), vd `tencent,akshare_sina,efinance,akshare_em` | Xem .env.example | Tùy chọn |
| `ENABLE_FUNDAMENTAL_PIPELINE` | Tổng开关聚合基本面; tắt thì chỉ trả về khối `not_supported`, không thay đổi chuỗi phân tích gốc | `true` | Tùy chọn |
| `FUNDAMENTAL_STAGE_TIMEOUT_SECONDS` | Ngân sách độ trễ giai đoạn基本面 (giây) | `1.5` | Tùy chọn |
| `FUNDAMENTAL_FETCH_TIMEOUT_SECONDS` | Timeout gọi nguồn đơn (giây) | `0.8` | Tùy chọn |
| `FUNDAMENTAL_RETRY_MAX` | Số lần thử lại nguồn基本面 (bao gồm lần đầu) | `1` | Tùy chọn |
| `FUNDAMENTAL_CACHE_TTL_SECONDS` | TTL cache聚合基本面 (giây), cache ngắn giảm kéo lặp | `120` | Tùy chọn |
| `FUNDAMENTAL_CACHE_MAX_ENTRIES` | Số entry tối đa cache基本面 (loại bỏ theo thời gian trong TTL) | `256` | Tùy chọn |

> Giải thích hành vi:
> - A-share:聚合 trả về theo `valuation/growth/earnings/institution/capital_flow/dragon_tiger/boards`;
> - ETF: trả về mục có được, năng lực thiếu đánh dấu `not_supported`, tổng thể không ảnh hưởng quy trình gốc;
> -美股/港股: trả về khối dự phòng `not_supported`;
> - Bất kỳ ngoại lệ nào đều fail-open, chỉ ghi lỗi, không ảnh hưởng chuỗi chính kỹ thuật/tin tức/chấm.
> - Sau khi cấu hình `TICKFLOW_API_KEY`, chỉ复盘 chỉ số A-share sẽ ưu tiên thử TickFlow cho chỉ số chính; nếu gói hiện tại hỗ trợ tra cứu pool标的 thì thống kê thị trường cũng ưu tiên TickFlow. Chuỗi个股 và realtime quote không thay đổi ưu tiên.
> - Năng lực TickFlow phân lớp theo quyền gói: gói quyền hạn chế vẫn có thể dùng tra cứu chỉ số chính; gói hỗ trợ pool标的 `CN_Equity_A` mới bật thống kê thị trường TickFlow.
> - Quickstart chính thức đã document hóa `quotes.get(universes=["CN_Equity_A"])`, nhưng smoke test online xác nhận thêm: `TICKFLOW_API_KEY` không đồng nghĩa có quyền này, và `quotes.get(symbols=[...])` có giới hạn số标的 mỗi lần.
> - TickFlow thực tế trả về `change_pct` / `amplitude` là tỷ lệ; hệ thống đã chuyển đổi thống nhất thành giá trị phần trăm tại lớp接入, đảm bảo nhất quán ngữ nghĩa trường với nguồn dữ liệu hiện có.
> - Hợp đồng trường:
>   - `fundamental_context.belong_boards` = danh sách板块 liên quan个股 (hiện chỉ A-share; không có dữ liệu thì `[]`);
>   - `fundamental_context.boards.data` = `sector_rankings` (bảng xếp hạng板块, cấu trúc `{top, bottom}`);
>   - `fundamental_context.earnings.data.financial_report` = tóm tắt báo cáo tài chính (kỳ báo cáo, doanh thu, lợi nhuận ròng, dòng tiền hoạt động, ROE);
>   - `fundamental_context.earnings.data.dividend` = chỉ số chia cổ tức (chỉ口径 cổ tức tiền mặt trước thuế, gồm `events`, `ttm_cash_dividend_per_share`, `ttm_dividend_yield_pct`);
>   - `get_stock_info.belong_boards` = danh sách板块 thuộc个股;
>   - `get_stock_info.boards` là alias tương thích, giá trị giống `belong_boards` (tương lai chỉ xem xét xóa ở major version);
>   - `get_stock_info.sector_rankings` nhất quán với `fundamental_context.boards.data`.
>   - `AnalysisReport.details.belong_boards` = danh sách板块 liên quan trong chi tiết báo cáo có cấu trúc;
>   - `AnalysisReport.details.sector_rankings` = bảng xếp hạng板块 trong chi tiết báo cáo có cấu trúc (dùng cho联动板块 frontend).
> - Thứ tự nguồn dữ liệu bảng xếp hạng板块: nhất quán với priority toàn cục.
> - Kiểm soát timeout là soft-timeout `best-effort`: giai đoạn sẽ downgrade nhanh theo ngân sách, nhưng không đảm bảo hard-interrupt gọi bên thứ ba.
> - `FUNDAMENTAL_STAGE_TIMEOUT_SECONDS=1.5` là ngân sách mục tiêu cho giai đoạn基本面 mới, không phải SLA cứng nghiêm ngặt.
> - Nếu cần SLA cứng, vui lòng nâng cấp lên thực thi cách ly tiến trình con và buộc终止 khi timeout ở phiên bản sau.

### Cấu Hình Khác

| Tên biến | Mô tả | Giá trị mặc định |
|--------|------|--------|
| `STOCK_LIST` | Mã cổ phiếu tự chọn (cách nhau bởi dấu phẩy) | - |
| `ADMIN_AUTH_ENABLED` | Đăng nhập Web: đặt `true` để bật bảo vệ mật khẩu; lần đầu truy cập đặt mật khẩu ban đầu trên trang web, có thể đổi tại 「System Settings > Change Password」; quên mật khẩu chạy `python -m src.auth reset_password` | `false` |
| `TRUST_X_FORWARDED_FOR` | Đặt `true` khi deploy sau reverse proxy đáng tin 1 lớp, lấy giá trị ngoài cùng bên phải của `X-Forwarded-For` làm IP client thực (dùng cho rate limit đăng nhập...); giữ `false` khi kết nối trực tiếp internet để chống giả mạo. Với multi-proxy/CDN, key rate limit có thể退 hóa thành IP edge proxy, cần đánh giá thêm | `false` |
| `MAX_WORKERS` | Số luồng并发 | `3` |
| `MARKET_REVIEW_ENABLED` | Bật复盘大盘 | `true` |
| `MARKET_REVIEW_REGION` | Thị trường复盘: cn(A-share), us(美股), both(cả hai), us phù hợp người dùng chỉ quan tâm美股 | `cn` |
| `TRADING_DAY_CHECK_ENABLED` | Kiểm tra ngày giao dịch: mặc định `true`, bỏ qua nếu không phải ngày giao dịch; đặt `false` hoặc dùng `--force-run` để bắt buộc thực thi (Issue #373) | `true` |
| `SCHEDULE_ENABLED` | Bật tác vụ định kỳ | `false` |
| `SCHEDULE_TIME` | Giờ thực thi định kỳ | `18:00` |
| `LOG_DIR` | Thư mục log | `./logs` |

---

## Triển Khai Docker

Dockerfile sử dụng multi-stage build, frontend sẽ tự động đóng gói khi build image và tích hợp sẵn vào `static/`.
Nếu muốn ghi đè static resource, có thể mount `static/` cục bộ vào `/app/static` trong container.
Container `server` đang chạy mặc định tái sử dụng artifact pre-build trong `/app/static`, không yêu cầu giữ thư mục nguồn `apps/dsa-web` hoặc cài `npm` runtime trong container; nếu WebUI không mở được, vui lòng ưu tiên xác nhận `/app/static/index.html` có tồn tại.

### Khởi Động Nhanh

```bash
# 1. Clone kho
git clone https://github.com/ZhuLinsen/daily_stock_analysis.git
cd daily_stock_analysis

# 2. Cấu hình biến môi trường
cp .env.example .env
vim .env  # Điền API Key và cấu hình

# 3. Khởi động container
docker-compose -f ./docker/docker-compose.yml up -d server     # Chế độ Web service (khuyến nghị, cung cấp API và WebUI)
docker-compose -f ./docker/docker-compose.yml up -d analyzer   # Chế độ tác vụ định kỳ
docker-compose -f ./docker/docker-compose.yml up -d            # Khởi động cả hai chế độ

# 4. Truy cập WebUI
# http://localhost:8000

# 5. Xem log
docker-compose -f ./docker/docker-compose.yml logs -f server
```

### Giải Thích Chế Độ Chạy

| Lệnh | Mô tả | Cổng |
|------|------|------|
| `docker-compose -f ./docker/docker-compose.yml up -d server` | Chế độ Web service, cung cấp API và WebUI | 8000 |
| `docker-compose -f ./docker/docker-compose.yml up -d analyzer` | Chế độ tác vụ định kỳ, tự động thực thi hàng ngày | - |
| `docker-compose -f ./docker/docker-compose.yml up -d` | Khởi động cả hai chế độ | 8000 |

### Cấu Hình Docker Compose

`docker-compose.yml` sử dụng anchor YAML để tái sử dụng cấu hình:

```yaml
version: '3.8'

x-common: &common
  build:
    context: ..
    dockerfile: docker/Dockerfile
  restart: unless-stopped
  env_file:
    - ../.env
  environment:
    - TZ=Asia/Shanghai
  volumes:
    - ../data:/app/data
    - ../logs:/app/logs
    - ../reports:/app/reports
    - ../.env:/app/.env

services:
  # Chế độ tác vụ định kỳ
  analyzer:
    <<: *common
    container_name: stock-analyzer

  # Chế độ FastAPI
  server:
    <<: *common
    container_name: stock-server
    command: ["python", "main.py", "--serve-only", "--host", "0.0.0.0", "--port", "8000"]
    ports:
      - "8000:8000"
```

### Lệnh Thường Dùng

```bash
# Xem trạng thái chạy
docker-compose -f ./docker/docker-compose.yml ps

# Xem log
docker-compose -f ./docker/docker-compose.yml logs -f server

# Dừng dịch vụ
docker-compose -f ./docker/docker-compose.yml down

# Build lại image (sau khi cập nhật code)
docker-compose -f ./docker/docker-compose.yml build --no-cache
docker-compose -f ./docker/docker-compose.yml up -d server
```

### Build Image Thủ Công

```bash
docker build -f docker/Dockerfile -t stock-analysis .
docker run -d --env-file .env -p 8000:8000 -v ./data:/app/data stock-analysis python main.py --serve-only --host 0.0.0.0 --port 8000
```

---

## Cấu Hình Chạy Cục Bộ Chi Tiết

### Cài Đặt Dependency

```bash
# Khuyến nghị Python 3.10+
pip install -r requirements.txt

# Hoặc dùng conda
conda create -n stock python=3.10
conda activate stock
pip install -r requirements.txt
```

**Import thông minh**: `pypinyin` (ghép tên→mã bằng pinyin) và `openpyxl` (phân tích Excel .xlsx) đã bao gồm trong `requirements.txt`, sẽ tự động cài khi chạy `pip install -r requirements.txt`. Nếu dùng chức năng import thông minh (ảnh/CSV/Excel/clipboard), vui lòng đảm bảo dependency đã cài đúng; khi thiếu có thể báo `ModuleNotFoundError`.

### Tham Số Dòng Lệnh

```bash
python main.py                        # Phân tích đầy đủ (个股 +复盘大盘)
python main.py --market-review        # Chỉ复盘大盘
python main.py --no-market-review     # Chỉ phân tích个股
python main.py --stocks 600519,300750 # Chỉ định cổ phiếu
python main.py --dry-run              # Chỉ lấy dữ liệu, không AI phân tích
python main.py --no-notify            # Không gửi thông báo
python main.py --schedule             # Chế độ định kỳ
python main.py --force-run            # Bắt buộc thực thi cả ngày không giao dịch (Issue #373)
python main.py --debug                # Chế độ debug (log chi tiết)
python main.py --workers 5            # Chỉ định số并发
```

---

## Cấu Hình Tác Vụ Định Kỳ

### GitHub Actions Định Kỳ

Sửa `.github/workflows/daily_analysis.yml`:

```yaml
schedule:
  # Giờ UTC, giờ Bắc Kinh = UTC + 8
  - cron: '0 10 * * 1-5'   # Thứ 2 đến thứ 6 18:00 (giờ Bắc Kinh)
```

Bảng tham chiếu thời gian thường dùng:

| Giờ Bắc Kinh | UTC cron expression |
|---------|----------------|
| 09:30 | `'30 1 * * 1-5'` |
| 12:00 | `'0 4 * * 1-5'` |
| 15:00 | `'0 7 * * 1-5'` |
| 18:00 | `'0 10 * * 1-5'` |
| 21:00 | `'0 13 * * 1-5'` |

#### GitHub Actions Chạy Thủ Công Ngày Không Giao Dịch (Issue #461 / #466)

`daily_analysis.yml` hỗ trợ hai cách điều khiển:

- `TRADING_DAY_CHECK_ENABLED`: Cấu hình cấp kho (`Settings → Secrets and variables → Actions`), mặc định `true`
- `workflow_dispatch.force_run`: Công tắc một lần khi trigger thủ công, mặc định `false`

Hiểu ưu tiên khuyến nghị:

| Tổ hợp cấu hình | Hành vi ngày không giao dịch |
|---------|-------------|
| `TRADING_DAY_CHECK_ENABLED=true` + `force_run=false` | Bỏ qua (hành vi mặc định) |
| `TRADING_DAY_CHECK_ENABLED=true` + `force_run=true` | Bắt buộc thực thi lần này |
| `TRADING_DAY_CHECK_ENABLED=false` + `force_run=false` | Luôn thực thi (định kỳ và thủ công đều không kiểm tra ngày giao dịch) |
| `TRADING_DAY_CHECK_ENABLED=false` + `force_run=true` | Luôn thực thi |

Các bước trigger thủ công:

1. Mở `Actions → 每日股票分析 → Run workflow`
2. Chọn `mode` (`full` / `market-only` / `stocks-only`)
3. Nếu hôm nay là ngày không giao dịch và vẫn muốn thực thi, đặt `force_run` thành `true`
4. Nhấn `Run workflow`

### Tác Vụ Định Kỳ Cục Bộ

Trình lập lịch định kỳ tích hợp hỗ trợ chạy phân tích vào giờ chỉ định mỗi ngày (mặc định 18:00).

#### Cách Dòng Lệnh

```bash
# Khởi động chế độ định kỳ (thực thi ngay 1 lần khi khởi động, sau đó 18:00 hàng ngày)
python main.py --schedule

# Khởi động chế độ định kỳ (không thực thi khi khởi động, chỉ chờ trigger định kỳ)
python main.py --schedule --no-run-immediately
```

> Lưu ý: Mỗi lần trigger định kỳ đều đọc lại `STOCK_LIST` hiện tại đã lưu. Nếu truyền `--stocks` đồng thời, tham số này sẽ không khóa danh sách cổ phiếu cho các lần chạy theo lịch; nếu cần tạm thời chỉ chạy cổ phiếu chỉ định, vui lòng dùng lệnh chạy một lần không định kỳ.

#### Cách Biến Môi Trường

Bạn cũng có thể cấu hình hành vi định kỳ qua biến môi trường (phù hợp Docker hoặc .env):

| Tên biến | Mô tả | Mặc định | Ví dụ |
|--------|------|:-------:|:-----:|
| `SCHEDULE_ENABLED` | Có bật tác vụ định kỳ không | `false` | `true` |
| `SCHEDULE_TIME` | Giờ thực thi hàng ngày (HH:MM) | `18:00` | `09:30` |
| `SCHEDULE_RUN_IMMEDIATELY` | Có thực thi ngay khi khởi động dịch vụ không | `true` | `false` |
| `TRADING_DAY_CHECK_ENABLED` | Kiểm tra ngày giao dịch: bỏ qua nếu không phải ngày giao dịch; đặt `false` để bắt buộc | `true` | `false` |

Ví dụ cấu hình trong Docker:

```bash
# Đặt không phân tích ngay khi khởi động
docker run -e SCHEDULE_ENABLED=true -e SCHEDULE_RUN_IMMEDIATELY=false ...
```

#### Phán Đoán Ngày Giao Dịch (Issue #373)

Mặc định phán đoán dựa trên thị trường cổ phiếu tự chọn (A-share / HK /美股) và `MARKET_REVIEW_REGION`:
- Sử dụng `exchange-calendars` để phân biệt lịch giao dịch riêng của A-share / HK /美股 (bao gồm ngày lễ)
- Với danh mục hỗn hợp, mỗi cổ phiếu chỉ phân tích vào ngày thị trường của nó mở cửa, cổ phiếu nghỉ thì bỏ qua hôm đó
- Khi tất cả thị trường liên quan đều là ngày không giao dịch, tổng thể bỏ qua (không khởi động pipeline, không đẩy tin)
- Ghi đè: `TRADING_DAY_CHECK_ENABLED=false` hoặc dòng lệnh `--force-run`

#### Dùng Crontab

Nếu không muốn dùng process常驻, có thể dùng Cron của hệ thống:

```bash
crontab -e
# Thêm: 0 18 * * 1-5 cd /path/to/project && python main.py
```

---

## Cấu Hình Chi Tiết Kênh Thông Báo

### WeChat Work

1. Thêm "group robot" trong nhóm chat WeChat Work
2. Sao chép Webhook URL
3. Đặt `WECHAT_WEBHOOK_URL`

### Feishu

1. Thêm "custom robot" trong nhóm chat Feishu
2. Sao chép Webhook URL
3. Đặt `FEISHU_WEBHOOK_URL`

### Telegram

1. Nói chuyện với @BotFather để tạo Bot
2. Lấy Bot Token
3. Lấy Chat ID (có thể qua @userinfobot)
4. Đặt `TELEGRAM_BOT_TOKEN` và `TELEGRAM_CHAT_ID`
5. (Tùy chọn) Nếu cần gửi vào Topic, đặt `TELEGRAM_MESSAGE_THREAD_ID` (lấy từ cuối link Topic)

### Email

1. Bật dịch vụ SMTP của email
2. Lấy mã ủy quyền (không phải mật khẩu đăng nhập)
3. Đặt `EMAIL_SENDER`, `EMAIL_PASSWORD`, `EMAIL_RECEIVERS`

Email hỗ trợ:
- QQ Mail: smtp.qq.com:465
- 163 Mail: smtp.163.com:465
- Gmail: smtp.gmail.com:587

**Gửi cổ phiếu nhóm đến email khác nhau** (Issue #268, tùy chọn):
Cấu hình `STOCK_GROUP_N` và `EMAIL_GROUP_N` để gửi báo cáo nhóm cổ phiếu khác nhau đến email khác nhau, ví dụ nhiều người chia sẻ phân tích không ảnh hưởng lẫn nhau.复盘大盘 sẽ gửi đến tất cả email đã cấu hình.

```bash
STOCK_GROUP_1=600519,300750
EMAIL_GROUP_1=user1@example.com
STOCK_GROUP_2=002594,AAPL
EMAIL_GROUP_2=user2@example.com
```

### Custom Webhook

Hỗ trợ bất kỳ Webhook POST JSON nào, bao gồm:
- Robot DingTalk
- Discord Webhook
- Slack Webhook
- Bark (iOS push)
- Dịch vụ tự dựng

Đặt `CUSTOM_WEBHOOK_URLS`, nhiều cái cách nhau bởi dấu phẩy.

### Discord

Discord hỗ trợ hai cách đẩy tin:

**Cách 1: Webhook (khuyến nghị, đơn giản)**

1. Tạo Webhook trong cài đặt kênh Discord
2. Sao chép Webhook URL
3. Cấu hình biến môi trường:

```bash
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/xxx/yyy
```

**Cách 2: Bot API (cần nhiều quyền hơn)**

1. Tạo ứng dụng tại [Discord Developer Portal](https://discord.com/developers/applications)
2. Tạo Bot và lấy Token
3. Mời Bot vào server
4. Lấy Channel ID (chế độ developer, phải chuột kênh sao chép)
5. Cấu hình biến môi trường:

```bash
DISCORD_BOT_TOKEN=your_bot_token
DISCORD_MAIN_CHANNEL_ID=your_channel_id
```

### Slack

Slack hỗ trợ hai cách đẩy tin, khi cấu hình cả hai ưu tiên dùng Bot API, đảm bảo text và ảnh gửi đến cùng kênh:

**Cách 1: Bot API (khuyến nghị, hỗ trợ upload ảnh)**

1. Tạo Slack App: https://api.slack.com/apps → Create New App
2. Thêm Bot Token Scopes: `chat:write`, `files:write`
3. Cài vào workspace và lấy Bot Token (xoxb-...)
4. Lấy Channel ID: Chi tiết kênh → sao chép Channel ID ở dưới
5. Cấu hình biến môi trường:

```bash
SLACK_BOT_TOKEN=xoxb-...
SLACK_CHANNEL_ID=C01234567
```

**Cách 2: Incoming Webhook (cấu hình đơn giản, chỉ text)**

1. Tạo Incoming Webhook trong trang quản lý Slack App
2. Sao chép Webhook URL
3. Cấu hình biến môi trường:

```bash
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/T.../B.../xxx
```

### Pushover (iOS/Android Push)

[Pushover](https://pushover.net/) là dịch vụ push cross-platform, hỗ trợ iOS và Android.

1. Đăng ký tài khoản Pushover và tải App
2. Lấy User Key từ [Pushover Dashboard](https://pushover.net/)
3. Tạo Application và lấy API Token
4. Cấu hình biến môi trường:

```bash
PUSHOVER_USER_KEY=your_user_key
PUSHOVER_API_TOKEN=your_api_token
```

Đặc điểm:
- Hỗ trợ cả iOS/Android
- Hỗ trợ ưu tiên thông báo và cài đặt âm thanh
- Miễn phí đủ cho cá nhân (10,000 tin/tháng)
- Tin nhắn lưu giữ 7 ngày

### Markdown Chuyển Ảnh (tùy chọn)

Cấu hình `MARKDOWN_TO_IMAGE_CHANNELS` để gửi báo cáo dưới dạng ảnh đến kênh không hỗ trợ Markdown (telegram, wechat, custom, email, slack).

**Cài đặt dependency**:

1. **imgkit**: Đã bao gồm trong `requirements.txt`, tự động cài khi chạy `pip install -r requirements.txt`
2. **wkhtmltopdf** (engine mặc định): Phụ thuộc hệ thống, cần cài thủ công:
   - **macOS**: `brew install wkhtmltopdf`
   - **Debian/Ubuntu**: `apt install wkhtmltopdf`
3. **markdown-to-file** (tùy chọn, hỗ trợ emoji tốt hơn): `npm i -g markdown-to-file`, và đặt `MD2IMG_ENGINE=markdown-to-file`

Nếu chưa cài hoặc cài thất bại, sẽ tự động fallback gửi text Markdown.

**Đẩy từng mã + gửi ảnh** (Issue #455):

Trong chế độ đẩy từng mã (`SINGLE_STOCK_NOTIFY=true`), nếu muốn kênh như Telegram gửi dưới dạng ảnh, cần cấu hình đồng thời `MARKDOWN_TO_IMAGE_CHANNELS=telegram` và cài công cụ chuyển ảnh (wkhtmltopdf hoặc markdown-to-file). Tóm tắt nhật ký个股 cũng hỗ trợ chuyển ảnh, không cần cấu hình thêm.

**Xử lý sự cố**: Nếu log xuất hiện「Markdown chuyển ảnh thất bại, sẽ fallback về text」, vui lòng kiểm tra cấu hình `MARKDOWN_TO_IMAGE_CHANNELS` và công cụ chuyển ảnh đã cài đúng chưa (`which wkhtmltoimage` hoặc `which m2f`).

---

## Cấu Hình Nguồn Dữ Liệu

Hệ thống mặc định dùng AkShare (miễn phí), cũng hỗ trợ các nguồn khác:

### AkShare (mặc định)
- Miễn phí, không cần cấu hình
- Nguồn dữ liệu: cào Đông Phương Tài Phú

### Tushare Pro
- Cần đăng ký để lấy Token
- Ổn định hơn, dữ liệu đầy đủ hơn
- Đặt `TUSHARE_TOKEN`

### Baostock
- Miễn phí, không cần cấu hình
- Làm nguồn dự phòng

### YFinance
- Miễn phí, không cần cấu hình
- Hỗ trợ美股/港股
- Dữ liệu lịch sử và realtime美股 đều thống nhất dùng YFinance, tránh技术指标 sai do akshare美股复权 bất thường

### Xử Lý Khi接口 Đông Phương Liên Tục Thất Bại

Nếu log xuất hiện `RemoteDisconnected`, kết nối `push2his.eastmoney.com` bị đóng..., đa số do Đông Phương giới hạn tốc độ. Khuyến nghị:

1. Đặt `ENABLE_EASTMONEY_PATCH=true` trong `.env`
2. Giảm并发 `MAX_WORKERS=1`
3. Nếu đã cấu hình Tushare, ưu tiên dùng nguồn Tushare

---

## Tính Năng Nâng Cao

### Hỗ Trợ HK Stock

Dùng prefix `hk` để chỉ định mã HK:

```bash
STOCK_LIST=600519,hk00700,hk01810
```

### Phân Tích ETF Và Chỉ Số

Đối với ETF theo dõi chỉ số và美股指数 (như VOO, QQQ, SPY, 510050, SPX, DJI, IXIC), phân tích chỉ tập trung vào**xu hướng chỉ số, sai số theo dõi, thanh khoản thị trường**, không đưa vào rủi ro cấp công ty của nhà quản lý/phát hành quỹ (kiện tụng, danh tiếng, thay đổi lãnh đạo...). Cảnh báo rủi ro và dự kiến hiệu suất đều dựa trên biểu hiện tổng thể của cổ phiếu thành phần chỉ số, tránh nhầm lẫn tin tức quỹ thành利空 của标的. Xem Issue #274.

### Chuyển Đổi Đa Mô Hình

Cấu hình nhiều mô hình, hệ thống tự động chuyển đổi:

```bash
# Gemini (chính)
GEMINI_API_KEY=xxx
GEMINI_MODEL=gemini-3-flash-preview

# OpenAI compatible (dự phòng)
OPENAI_API_KEY=xxx
OPENAI_BASE_URL=https://api.deepseek.com/v1
OPENAI_MODEL=deepseek-chat
# Chế độ suy luận: deepseek-reasoner, deepseek-r1, qwq... tự động nhận diện; deepseek-chat hệ thống tự kích hoạt theo tên mô hình
```

### Tích Hợp Trực Tiếp LiteLLM (đa mô hình + cân bằng tải đa Key)

Xem chi tiết tại [Hướng Dẫn Cấu Hình LLM](LLM_CONFIG_GUIDE.md). Dự án này thống nhất gọi tất cả LLM qua [LiteLLM](https://github.com/BerriAI/litellm), không cần khởi động riêng Proxy service.

**Cơ chế 2 lớp**: Luân phiên nhiều Key cho cùng mô hình (Router) và降级跨模型 (Fallback) tách biệt độc lập, không ảnh hưởng lẫn nhau.

**Ví dụ cấu hình đa Key +降级跨模型**:

```env
# Mô hình chính: 3 Key Gemini luân phiên, Router tự chuyển Key tiếp theo khi 429
GEMINI_API_KEYS=key1,key2,key3
LITELLM_MODEL=gemini/gemini-3-flash-preview

#降级跨模型: khi tất cả Key mô hình chính đều thất bại, thử Claude → GPT theo thứ tự
# Cần cấu hình API Key tương ứng: ANTHROPIC_API_KEY, OPENAI_API_KEY
LITELLM_FALLBACK_MODELS=anthropic/claude-3-5-sonnet-20241022,openai/gpt-4o-mini
```

**Hành vi dự kiến**: Request đầu tiên dùng `key1`; nếu 429, Router lần sau dùng `key2`; nếu 3 Key đều không dùng được, chuyển sang Claude, thất bại nữa thì chuyển sang GPT.

> ⚠️ `LITELLM_MODEL` phải chứa prefix provider (như `gemini/`, `anthropic/`, `openai/`),
> nếu không hệ thống không nhận diện được dùng nhóm API Key nào. Định dạng cũ `GEMINI_MODEL` (không prefix) chỉ dùng để tự suy luận khi chưa cấu hình `LITELLM_MODEL`.

**Giải thích dependency**: `requirements.txt` giữ `openai>=1.0.0`, vì LiteLLM phụ thuộc vào OpenAI SDK làm interface thống nhất; giữ rõ ràng đảm bảo tương thích phiên bản, người dùng không cần cấu hình riêng.

**Mô hình Vision (ảnh trích mã cổ phiếu)**: Xem chi tiết [Hướng Dẫn Cấu Hình LLM - Vision](LLM_CONFIG_GUIDE.md#41-vision-模型图片识别股票代码).

Trích mã cổ phiếu từ ảnh (như `/api/v1/stocks/extract-from-image`) dùng LiteLLM Vision, áp dụng định dạng OpenAI `image_url`, hỗ trợ mô hình có khả năng Vision như Gemini, Claude, OpenAI, DeepSeek... Trả về `items` (code, name, confidence) và mảng `codes` tương thích.

> Giải thích tương thích: Phản hồi `/api/v1/stocks/extract-from-image` bổ sung trường `items` trên cơ sở `codes` gốc. Nếu client downstream dùng JSON Schema nghiêm ngặt và không chấp nhận trường lạ, vui lòng cập nhật schema đồng bộ.

**Import thông minh**: Ngoài ảnh, còn hỗ trợ file CSV/Excel và dán clipboard (`/api/v1/stocks/parse-import`), tự động phân tích cột mã/tên, phân tích tên→mã hỗ trợ ánh xạ cục bộ, khớp pinyin và fallback online AkShare. Phụ thuộc `pypinyin` (khớp pinyin) và `openpyxl` (phân tích Excel), đã bao gồm trong `requirements.txt`.

- **Cache phân tích tên AkShare**: Khi dùng fallback online AkShare để phân tích tên→mã, kết quả cache 1 giờ (TTL), tránh request频繁; tự động refresh khi gọi lần đầu hoặc cache hết hạn.
- **Tên cột CSV/Excel**: Hỗ trợ `code`, `股票代码`, `代码`, `name`, `股票名称`, `名称`... (không phân biệt hoa thường); không có header thì mặc định cột 1 là mã, cột 2 là tên.
- **Phân tích thất bại thường gặp**: File quá lớn (>2MB), encoding không phải UTF-8/GBK, Excel sheet trống hoặc hỏng, CSV sai delimiter/số cột... API sẽ trả về thông báo lỗi cụ thể.

- **Ưu tiên mô hình**: `VISION_MODEL` > `LITELLM_MODEL` > suy luận từ API Key hiện có (`OPENAI_VISION_MODEL` đã bỏ, vui lòng dùng `VISION_MODEL`)
- **Fallback Provider**: Khi mô hình chính thất bại, tự động chuyển sang provider tiếp theo theo `VISION_PROVIDER_PRIORITY` (mặc định `gemini,anthropic,openai`)
- **Khi mô hình chính không hỗ trợ Vision**: Nếu mô hình chính là DeepSeek hoặc mô hình không có Vision, có thể cấu hình rõ `VISION_MODEL=openai/gpt-4o` hoặc `gemini/gemini-2.0-flash` cho trích xuất ảnh
- **Kiểm tra cấu hình**: Nếu cấu hình `VISION_MODEL` nhưng không cấu hình API Key provider tương ứng, sẽ xuất hiện warning khi khởi động, chức năng trích xuất ảnh sẽ không khả dụng

### Chế Độ Debug

```bash
python main.py --debug
```

Vị trí file log:
- Log thường: `logs/stock_analysis_YYYYMMDD.log`
- Log debug: `logs/stock_analysis_debug_YYYYMMDD.log`

---

## Chức Năng Backtest

Module backtest tự động xác minh事后 đối với bản ghi phân tích AI lịch sử, đánh giá độ chính xác của khuyến nghị phân tích.

### Nguyên Lý Hoạt Động

1. Chọn bản ghi `AnalysisHistory` đã qua thời gian làm lạnh (mặc định 14 ngày)
2. Lấy dữ liệu nến ngày sau ngày phân tích (K-line hướng tới)
3. Suy luận hướng dự kiến dựa trên khuyến nghị thao tác, so sánh với xu hướng thực tế
4. Đánh giá tình hình kích hoạt chốt lời/cắt lỗ, mô phỏng lợi nhuận thực thi
5. Tổng hợp thành chỉ số biểu hiện ở cả hai cấp độ tổng thể và từng mã

### Ánh Xạ Khuyến Nghị Thao Tác

| Khuyến nghị thao tác | Suy luận vị thế | Hướng dự kiến | Điều kiện thắng |
|---------|---------|---------|---------|
| Mua/thêm mua/strong buy | long | up | Tăng ≥ dải trung tính |
| Bán/giảm vị thế/strong sell | cash | down | Giảm ≥ dải trung tính |
| Giữ/hold | long | not_down | Không giảm đáng kể |
| Chờ/đợi/wait | cash | flat | Giá trong dải trung tính |

### Cấu Hình

Đặt các biến sau trong `.env` (đều có giá trị mặc định, tùy chọn):

| Biến | Mặc định | Mô tả |
|------|-------|------|
| `BACKTEST_ENABLED` | `true` | Có tự động chạy backtest sau phân tích hàng ngày không |
| `BACKTEST_EVAL_WINDOW_DAYS` | `10` | Cửa sổ đánh giá (số ngày giao dịch) |
| `BACKTEST_MIN_AGE_DAYS` | `14` | Chỉ backtest bản ghi từ N ngày trước, tránh dữ liệu không hoàn chỉnh |
| `BACKTEST_ENGINE_VERSION` | `v1` | Phiên bản engine, dùng để phân biệt kết quả khi nâng cấp logic |
| `BACKTEST_NEUTRAL_BAND_PCT` | `2.0` | Ngưỡng vùng trung tính (%), ±2% coi là震荡 |

### Chạy Tự Động

Backtest tự động kích hoạt sau khi hoàn thành quy trình phân tích hàng ngày (không chặn, thất bại không ảnh hưởng đẩy tin thông báo). Cũng có thể kích hoạt thủ công qua API.

### Chỉ Số Đánh Giá

| Chỉ số | Mô tả |
|------|------|
| `direction_accuracy_pct` | Độ chính xác dự đoán hướng (hướng dự kiến nhất quán với thực tế) |
| `win_rate_pct` | Tỷ lệ thắng (thắng / (thắng+thua), không tính trung tính) |
| `avg_stock_return_pct` | Tỷ suất lợi nhuận trung bình cổ phiếu |
| `avg_simulated_return_pct` | Lợi nhuận mô phỏng thực thi trung bình (bao gồm thoát chốt lời/cắt lỗ) |
| `stop_loss_trigger_rate` | Tỷ lệ kích hoạt cắt lỗ (chỉ thống kê bản ghi có cấu hình cắt lỗ) |
| `take_profit_trigger_rate` | Tỷ lệ kích hoạt chốt lời (chỉ thống kê bản ghi có cấu hình chốt lời) |

---

## Dịch Vụ API FastAPI

FastAPI cung cấp dịch vụ RESTful API, hỗ trợ quản lý cấu hình và trigger phân tích.

### Cách Khởi Động

| Lệnh | Mô tả |
|------|------|
| `python main.py --serve` | Khởi động API + thực thi 1 lần phân tích đầy đủ |
| `python main.py --serve-only` | Chỉ khởi động API, trigger phân tích thủ công |

### Tính Năng

- 📝 **Quản lý cấu hình** - Xem/sửa danh sách cổ phiếu tự chọn
- 🚀 **Phân tích nhanh** - Trigger phân tích qua API
- 📊 **Tiến độ realtime** - Trạng thái tác vụ phân tích cập nhật realtime, hỗ trợ đa tác vụ song song
- 📈 **Xác minh backtest** - Đánh giá độ chính xác phân tích lịch sử, tra cứu tỷ lệ thắng hướng và lợi nhuận mô phỏng
- 🔗 **Tài liệu API** - Truy cập `/docs` xem Swagger UI

### API Endpoints

| Endpoint | Method | Mô tả |
|------|------|------|
| `/api/v1/analysis/analyze` | POST | Trigger phân tích cổ phiếu |
| `/api/v1/analysis/tasks` | GET | Tra cứu danh sách tác vụ |
| `/api/v1/analysis/status/{task_id}` | GET | Tra cứu trạng thái tác vụ |
| `/api/v1/history` | GET | Tra cứu lịch sử phân tích |
| `/api/v1/backtest/run` | POST | Trigger backtest |
| `/api/v1/backtest/results` | GET | Tra cứu kết quả backtest (phân trang) |
| `/api/v1/backtest/performance` | GET | Lấy biểu hiện backtest tổng thể |
| `/api/v1/backtest/performance/{code}` | GET | Lấy biểu hiện backtest từng mã |
| `/api/v1/stocks/extract-from-image` | POST | Trích mã cổ phiếu từ ảnh (multipart, timeout 60s) |
| `/api/v1/stocks/parse-import` | POST | Phân tích CSV/Excel/clipboard (multipart file hoặc JSON `{"text":"..."}`, file≤2MB, text≤100KB) |
| `/api/health` | GET | Kiểm tra sức khỏe |
| `/docs` | GET | Tài liệu Swagger API |

> Lưu ý: `POST /api/v1/analysis/analyze` khi `async_mode=false` chỉ hỗ trợ 1 cổ phiếu; `stock_codes` batch cần dùng `async_mode=true`. Phản hồi async `202` trả về `task_id` cho个股, trả về cấu trúc tổng hợp `accepted` / `duplicates` cho batch.

**Ví dụ gọi**:
```bash
# Kiểm tra sức khỏe
curl http://127.0.0.1:8000/api/health

# Trigger phân tích (A-share)
curl -X POST http://127.0.0.1:8000/api/v1/analysis/analyze \
  -H 'Content-Type: application/json' \
  -d '{"stock_code": "600519"}'

# Tra cứu trạng thái tác vụ
curl http://127.0.0.1:8000/api/v1/analysis/status/<task_id>

# Trigger backtest (tất cả cổ phiếu)
curl -X POST http://127.0.0.1:8000/api/v1/backtest/run \
  -H 'Content-Type: application/json' \
  -d '{"force": false}'

# Trigger backtest (chỉ định cổ phiếu)
curl -X POST http://127.0.0.1:8000/api/v1/backtest/run \
  -H 'Content-Type: application/json' \
  -d '{"code": "600519", "force": false}'

# Tra cứu biểu hiện backtest tổng thể
curl http://127.0.0.1:8000/api/v1/backtest/performance

# Tra cứu biểu hiện backtest từng mã
curl http://127.0.0.1:8000/api/v1/backtest/performance/600519

# Tra cứu phân trang kết quả backtest
curl "http://127.0.0.1:8000/api/v1/backtest/results?page=1&limit=20"
```

### Cấu Hình Tùy Chỉnh

Sửa cổng mặc định hoặc cho phép truy cập mạng LAN:

```bash
python main.py --serve-only --host 0.0.0.0 --port 8888
```

### Định Dạng Mã Cổ Phiếu Hỗ Trợ

| Loại | Định dạng | Ví dụ |
|------|------|------|
| A-share | 6 chữ số | `600519`, `000001`, `300750` |
| Sở Bắc Kinh | Bắt đầu 8/4/92, 6 chữ số | `920748`, `838163`, `430047` |
| HK stock | hk + 5 chữ số | `hk00700`, `hk09988` |
|美股 | 1-5 chữ cái (có thể hậu tố .X) | `AAPL`, `TSLA`, `BRK.B` |
|美股指数 | SPX/DJI/IXIC... | `SPX`, `DJI`, `NASDAQ`, `VIX` |

### Lưu Ý

- Truy cập trình duyệt: `http://127.0.0.1:8000` (hoặc cổng bạn đã cấu hình)
- Sau khi deploy lên cloud server, không biết nhập địa chỉ gì trên trình duyệt? Xem [Hướng Dẫn Truy Cập Giao Diện Web Cloud Server](deploy-webui-cloud.md)
- Sau khi phân tích xong tự động đẩy tin thông báo đến kênh đã cấu hình
- Chức năng này sẽ tự động vô hiệu hóa trong môi trường GitHub Actions
- Xem thêm [Hướng Dẫn Tích Hợp openclaw Skill](openclaw-skill-integration.md)

---

## Câu Hỏi Thường Gặp

### Q: Tin nhắn đẩy bị cắt?
A: WeChat Work/Feishu có giới hạn độ dài tin nhắn, hệ thống đã tự động phân đoạn gửi. Nếu cần nội dung đầy đủ, có thể cấu hình chức năng Feishu Cloud Document.

### Q: Lấy dữ liệu thất bại?
A: AkShare dùng cơ chế crawler, có thể bị giới hạn tạm thời. Hệ thống đã cấu hình cơ chế thử lại, thường đợi vài phút rồi thử lại là được.

### Q: Làm sao thêm cổ phiếu tự chọn?
A: Sửa biến môi trường `STOCK_LIST`, nhiều mã cách nhau bởi dấu phẩy.

### Q: GitHub Actions không thực thi?
A: Kiểm tra xem đã bật Actions chưa, và cron expression có đúng không (lưu ý là giờ UTC).

---

Thêm câu hỏi vui lòng [tạo Issue](https://github.com/ZhuLinsen/daily_stock_analysis/issues)

## Portfolio P0 PR1 (Sổ Cái Cốt Lõi Và Snapshot)

### Phạm vi
- Mô hình domain danh mục cốt lõi:
  - account, trade, cash ledger, corporate action, position cache, lot cache, daily snapshot, fx cache
- Năng lực dịch vụ cốt lõi:
  - CRUD account
  - Ghi event
  - Snapshot replay read-time cho một account hoặc tất cả account đang hoạt động

### Ngữ nghĩa kế toán
- Phương pháp giá vốn:
  - `fifo` (mặc định)
  - `avg`
- Thứ tự event cùng ngày:
  - `cash -> corporate action -> trade`
- Quy tắc ngày hiệu lực corporate action:
  - `effective_date` được xem là hiệu lực trước khi giao dịch thị trường trong ngày đó.

### Ngữ nghĩa lỗi và ổn định
- Xung đột unique `trade_uid` trả về `409` (ngữ nghĩa xung đột API).
- Lệnh bán giờ kiểm tra số lượng khả dụng trước khi insert; bán vượt quá bị từ chối với `409 portfolio_oversell`.
- Ghi event nguồn portfolio giờ tuần tự hóa qua khóa ghi SQLite; endpoint ghi/xóa trực tiếp có thể trả về `409 portfolio_busy` khi có đột biến sổ cái khác đang tiến hành.
- Đường ghi snapshot nguyên tử cho position/lot/daily snapshot.
- Chuyển đổi FX giữ hành vi fail-open (fallback 1:1 với marker stale) để tránh gián đoạn pipeline.

### Phạm vi kiểm thử trong PR1
- Replay bán một phần FIFO/AVG
- Replay cổ tức và split
- Sắp xếp cùng ngày (cổ tức/giao dịch, split/giao dịch)
- Hợp đồng API account/event/snapshot
- Xung đột trade_uid trùng API

## Portfolio P0 PR2 (Import Và Rủi Ro)

### Import CSV
- Broker hỗ trợ: `huatai`, `citic`, `cmb`.
- Quy trình thống nhất: phân tích CSV thành bản ghi chuẩn hóa, sau đó commit vào trade portfolio.
- Commit vẫn theo từng dòng thay vì một giao dịch dài; dòng bận tính vào `failed_count` thay vì chuyển toàn bộ request thành `409`.
- Chính sách loại trùng:
  - Khóa chính: `trade_uid` (phạm vi account)
  - Khóa fallback: hash xác định từ date/symbol/side/qty/price/fee/tax/currency

### Báo cáo rủi ro
- Giám sát tập trung: cảnh báo trọng lượng vị thế top theo ngưỡng cấu hình.
- Giám sát sụt giảm: sụt giảm tối đa/hiện tại tính từ daily snapshot.
- Cảnh báo gần dừng lỗ: đánh dấu mục gần cảnh báo và đã kích hoạt với echo ngưỡng.

### FX fail-open
- FX refresh trước tiên thử nguồn online (YFinance).
- Khi online thất bại, fallback sang tỷ giá cache mới nhất và đánh dấu `is_stale=true`.
- Pipeline snapshot/rủi ro chính vẫn khả dụng ngay cả khi fetch FX online không khả dụng.

## Portfolio P0 PR3 (Web + Tiêu Thụ Agent)

### Trang tiêu thụ Web
- Thêm route trang Web: `/portfolio` (`apps/dsa-web/src/pages/PortfolioPage.tsx`).
- Nguồn dữ liệu:
  - `GET /api/v1/portfolio/snapshot`
  - `GET /api/v1/portfolio/risk`
- Hỗ trợ:
  - Chuyển đổi toàn bộ danh mục / account đơn
  - Chuyển đổi phương pháp giá vốn (`fifo` / `avg`)
  - Biểu đồ tròn tập trung (Top Positions) với Recharts
  - Thẻ KPI snapshot và thẻ tóm tắt rủi ro

### Công cụ Agent
- Thêm công cụ dữ liệu `get_portfolio_snapshot` cho gợi ý LLM nhận biết account.
- Hành vi mặc định:
  - Đầu ra tóm tắt gọn (thân thiện token)
  - Bao gồm khối rủi ro tùy chọn
- Tham số tùy chọn:
  - `account_id`
  - `cost_method` (`fifo` / `avg`)
  - `as_of` (`YYYY-MM-DD`)
  - `include_positions` (mặc định `false`)
  - `include_risk` (mặc định `true`)

### Ổn định và tương thích
- Năng lực mới chỉ mang tính bổ sung; không xóa key/route hiện có.
- Ngữ nghĩa fail-open:
  - Nếu khối rủi ro thất bại, snapshot vẫn được trả về.
  - Nếu module portfolio không khả dụng, công cụ trả về `not_supported` có cấu trúc.

## Portfolio P0 PR4 (Đóng Khoảng Trống)

### Đóng truy vấn API
- Thêm endpoint truy vấn event:
  - `GET /api/v1/portfolio/trades`
  - `GET /api/v1/portfolio/cash-ledger`
  - `GET /api/v1/portfolio/corporate-actions`
- Thêm endpoint xóa event:
  - `DELETE /api/v1/portfolio/trades/{trade_id}`
  - `DELETE /api/v1/portfolio/cash-ledger/{entry_id}`
  - `DELETE /api/v1/portfolio/corporate-actions/{action_id}`
- Tham số truy vấn thống nhất:
  - `account_id`, `date_from`, `date_to`, `page`, `page_size`
- Bộ lọc riêng trade/cash/corporate-action:
  - trades: `symbol`, `side`
  - cash-ledger: `direction`
  - corporate-actions: `symbol`, `action_type`
- Hình dạng phản hồi thống nhất:
  - `items`, `total`, `page`, `page_size`

### Framework import CSV
- Tái cấu trúc logic parser thành registry parser mở rộng.
- Adapter tích hợp sẵn giữ nguyên: `huatai`, `citic`, `cmb` với ánh xạ alias.
- Thêm endpoint khám phá parser:
  - `GET /api/v1/portfolio/imports/csv/brokers`

### Đóng Web
- Trang `/portfolio` giờ bao gồm:
  - Mục tạo account inline với hướng dẫn empty-state và tự chuyển sang account đã tạo
  - Form nhập event thủ công: trade / cash / corporate action
  - Thao tác phân tích + commit CSV (hỗ trợ `dry_run`)
  - Bảng event với bộ lọc và phân trang
  - Xóa event phạm vi account đơn để sửa trade / cash / corporate action
  - Fallback bộ chọn broker về broker tích hợp sẵn (`huatai/citic/cmb`) khi API danh sách broker thất bại hoặc trả về rỗng
  - Hành động refresh thủ công thẻ trạng thái FX gọi `POST /api/v1/portfolio/fx/refresh` hiện có; nếu fetch FX upstream thất bại, trang vẫn có thể hiển thị stale sau refresh và sẽ giải thích kết quả inline
  - khi `PORTFOLIO_FX_UPDATE_ENABLED=false`, API refresh giờ trả về trạng thái disabled rõ ràng và trang sẽ hiển thị "汇率在线刷新已被禁用" thay vì "当前范围无可刷新的汇率对"

### Ngữ nghĩa tập trung sector rủi ro
- Thêm `sector_concentration` trong `GET /api/v1/portfolio/risk`.
- Quy tắc ánh xạ:
  - Position CN thử ánh xạ board từ `get_belong_boards`.
  - Non-CN hoặc ánh xạ thất bại fallback về `UNCLASSIFIED`.
  - Dùng board chính duy nhất mỗi symbol để tránh trọng lượng trùng.
- Fail-open:
  - lỗi tra cứu board không làm gián đoạn phản hồi rủi ro.
  - phản hồi trả về chi tiết coverage/lỗi để giải thích.
