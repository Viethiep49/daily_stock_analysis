# Hướng Dẫn Bot Commands

Hệ thống hỗ trợ bot tương tác qua **Telegram** và **Discord**. Bot nhận lệnh từ người dùng, gọi pipeline phân tích, và trả về báo cáo tiếng Việt.

---

## 1. Kiến Trúc Tổng Quan

```
Telegram / Discord
       ↓
  bot/platforms/         ← Adapter nhận message từng nền tảng
       ↓
  bot/dispatcher.py      ← Phân tích lệnh, định tuyến đến handler
       ↓
  bot/commands/          ← Xử lý từng lệnh cụ thể
       ↓
  src/ (AnalysisService, MarketAnalyzer, NotificationService)
```

### Cấu Trúc Thư Mục

```
bot/
├── __init__.py
├── dispatcher.py           # Phân tích lệnh và định tuyến
├── commands/
│   ├── __init__.py
│   ├── base.py             # Abstract base command
│   ├── analyze.py          # /analyze — phân tích cổ phiếu
│   ├── ask.py              # /ask — hỏi đáp chiến lược Agent
│   ├── batch.py            # /batch — phân tích nhiều mã
│   ├── chat.py             # /chat — trò chuyện tự do
│   ├── help.py             # /help — danh sách lệnh
│   ├── history.py          # /history — lịch sử phiên
│   ├── market.py           # /market — tổng kết thị trường
│   ├── research.py         # /research — tra cứu nhanh
│   ├── status.py           # /status — trạng thái hệ thống
│   └── strategies.py       # /strategies — danh sách chiến lược
└── platforms/
    ├── __init__.py
    ├── base.py             # Abstract platform adapter
    └── discord.py          # Discord bot adapter
```

---

## 2. Danh Sách Lệnh

### Phân Tích Cổ Phiếu

| Lệnh | Mô tả | Ví dụ |
|------|-------|-------|
| `/analyze <MÃ>` | Phân tích đầy đủ một mã cổ phiếu | `/analyze VCB` |
| `/research <MÃ>` | Tra cứu nhanh thông tin mã | `/research FPT` |
| `/batch <MÃ1,MÃ2,...>` | Phân tích nhiều mã cùng lúc | `/batch VCB,FPT,VNM` |
| `/market` | Tổng kết thị trường VNINDEX + VN30 | `/market` |

### Agent & Chiến Lược

| Lệnh | Mô tả | Ví dụ |
|------|-------|-------|
| `/ask <câu hỏi>` | Hỏi đáp chiến lược đa lượt (Agent mode) | `/ask dùng Chan theory phân tích VCB` |
| `/chat <nội dung>` | Trò chuyện tự do với AI | `/chat giải thích RSI` |
| `/strategies` | Liệt kê tất cả chiến lược đã tích hợp | `/strategies` |
| `/history` | Xem lịch sử phiên hỏi đáp | `/history` |

### Hệ Thống

| Lệnh | Mô tả |
|------|-------|
| `/help` | Hiển thị danh sách lệnh và hướng dẫn |
| `/status` | Trạng thái hệ thống, data source, uptime |

---

## 3. Cấu Hình Bot

### Telegram

```env
TELEGRAM_BOT_TOKEN=<token từ @BotFather>
TELEGRAM_CHAT_ID=<Chat ID hoặc Channel ID>
TELEGRAM_MESSAGE_THREAD_ID=<Topic ID nếu dùng Forum Group> # Tùy chọn
```

Xem chi tiết: [`docs/bot/discord-bot-config.md`](bot/discord-bot-config.md) (tương tự cho Telegram).

### Discord

```env
DISCORD_BOT_TOKEN=<Bot Token>
DISCORD_MAIN_CHANNEL_ID=<Channel ID>
```

Hoặc dùng Webhook (chỉ gửi, không nhận lệnh):

```env
DISCORD_WEBHOOK_URL=<Webhook URL>
```

---

## 4. Định Dạng Mã Cổ Phiếu VN

Bot nhận diện các định dạng:

| Loại | Format | Ví dụ |
|------|--------|-------|
| Cổ phiếu HOSE/HNX | 3 chữ cái | `VCB`, `FPT`, `HPG` |
| ETF | 6-8 ký tự | `E1VFVN30`, `FUEVFVND` |

---

## 5. Luồng Xử Lý Lệnh

```
1. Người dùng gửi: /analyze VCB
2. dispatcher.py nhận, parse → command="analyze", args=["VCB"]
3. analyze.py.execute("VCB")
   → validate: is_vn_stock_code("VCB") ✓
   → AnalysisService.run("VCB")
   → Trả về báo cáo tiếng Việt
4. Platform adapter format và gửi lại người dùng
```

---

## 6. Thêm Platform Mới

1. Tạo `bot/platforms/<tên_platform>.py` kế thừa `BotPlatform`
2. Implement: `verify_request()`, `parse_message()`, `format_response()`
3. Đăng ký trong `bot/platforms/__init__.py`
4. Thêm biến môi trường cần thiết vào `.env.example`

```python
from bot.platforms.base import BotPlatform

class MyPlatform(BotPlatform):
    @property
    def platform_name(self) -> str:
        return "myplatform"

    def verify_request(self, headers, body) -> bool:
        # Xác thực chữ ký webhook
        ...

    def parse_message(self, data) -> Optional[BotMessage]:
        # Parse raw request → BotMessage
        ...

    def format_response(self, response) -> dict:
        # BotResponse → dict theo format nền tảng
        ...
```
