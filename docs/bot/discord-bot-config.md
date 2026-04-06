# Cấu Hình Robot Discord

## Robot Discord
Robot Discord nhận tin nhắn cần tạo ứng dụng robot qua Discord Developer Portal
https://discord.com/developers/applications

Robot Discord hỗ trợ hai cách gửi tin nhắn:
1. **Chế độ Webhook**: Cấu hình đơn giản, quyền thấp, phù hợp chỉ cần gửi tin nhắn
2. **Chế độ Bot API**: Quyền cao, hỗ trợ nhận lệnh, cần cấu hình Bot Token và Channel ID

## Tạo Robot Discord

### 1. Đăng nhập Discord Developer Portal
Truy cập https://discord.com/developers/applications và đăng nhập bằng tài khoản Discord

### 2. Tạo ứng dụng
Nhấn nút "New Application", nhập tên ứng dụng (ví dụ: A股智能分析机器人), sau đó nhấn "Create"

### 3. Cấu hình robot
Trong menu trái nhấn "Bot", sau đó nhấn "Add Bot", xác nhận thêm

### 4. Lấy Bot Token
Trong trang Bot, nhấn "Reset Token", sau đó sao chép Token tạo ra (đây là `DISCORD_BOT_TOKEN` của bạn)

### 5. Cấu hình quyền
Trong phần "Privileged Gateway Intents" của trang Bot, bật các tùy chọn:
- Presence Intent
- Server Members Intent
- Message Content Intent

### 6. Thêm vào server
1. Trong menu trái nhấn "OAuth2" > "URL Generator"
2. Trong "Scopes" chọn:
   - `bot`
   - `applications.commands`
3. Trong "Bot Permissions" chọn:
   - Send Messages
   - Embed Links
   - Attach Files
   - Read Message History
   - Use Slash Commands
4. Sao chép URL tạo ra, mở trong trình duyệt, chọn server muốn thêm robot

### 7. Lấy Channel ID
1. Trong Discord client, bật chế độ developer: Settings > Advanced > Developer Mode
2. Phải chuột vào kênh muốn robot gửi tin nhắn, chọn "Copy ID" (đây là `DISCORD_MAIN_CHANNEL_ID` của bạn)

## Cấu Hình Biến Môi Trường

Thêm các cấu hình sau vào file `.env`:

```env
# Cấu hình robot Discord
DISCORD_BOT_TOKEN=your-discord-bot-token
DISCORD_MAIN_CHANNEL_ID=your-channel-id
DISCORD_WEBHOOK_URL=your-webhook-url (tùy chọn)
DISCORD_BOT_STATUS=A股智能分析 | /help
```

## Cấu Hình Chế Độ Webhook (tùy chọn)

Nếu chỉ muốn dùng chế độ Webhook gửi tin nhắn, không cần Bot Token, làm theo các bước:

1. Phải chuột vào kênh, chọn "Edit Channel"
2. Nhấn "Integrations" > "Webhooks" > "New Webhook"
3. Cấu hình tên và avatar Webhook
4. Sao chép Webhook URL (đây là `DISCORD_WEBHOOK_URL` của bạn)

## Lệnh Hỗ Trợ

Robot Discord hỗ trợ các lệnh Slash sau:

1. `/analyze <stock_code> [full_report]` - Phân tích theo mã cổ phiếu
   - `stock_code`: Mã cổ phiếu, vd 600519
   - `full_report`: Tùy chọn, có tạo báo cáo đầy đủ (bao gồm大盘) không

2. `/market_review` - Lấy báo cáo复盘大盘

3. `/help` - Xem thông tin trợ giúp

## Kiểm Tra Robot

1. Đảm bảo robot đã thêm thành công vào server
2. Nhập `/help` trong kênh, robot sẽ trả về thông tin trợ giúp
3. Nhập `/analyze 600519` để kiểm tra chức năng phân tích cổ phiếu
4. Nhập `/market_review` để kiểm tra chức năng复盘大盘

## Lưu Ý

1. Đảm bảo robot có đủ quyền gửi tin nhắn và dùng Slash command trong kênh
2. Định kỳ cập nhật Bot Token, đảm bảo an toàn
3. Không chia sẻ Bot Token với bất kỳ ai
4. Nếu robot không phản hồi, kiểm tra:
   - Bot Token có đúng không
   - Channel ID có đúng không
   - Robot có online không
   - Robot có quyền gửi tin nhắn không

## Xử Lý Sự Cố

- **Robot không phản hồi lệnh**: Kiểm tra Bot Token và Channel ID có đúng không, đảm bảo robot đã thêm vào server
- **Slash command không hiển thị**: Đợi một thời gian (Discord cần đồng bộ lệnh), hoặc thêm lại robot
- **Gửi tin nhắn thất bại**: Kiểm tra quyền kênh, đảm bảo robot có quyền gửi tin nhắn

## Link Liên Quan

- [Discord Developer Portal](https://discord.com/developers/applications)
- [Discord Bot Documentation](https://discordpy.readthedocs.io/en/stable/)
- [Discord Slash Commands](https://discord.com/developers/docs/interactions/application-commands)
