# Thư Mục Chiến Lược Giao Dịch / Trading Strategies

Thư mục này chứa **file chiến lược giao dịch ngôn ngữ tự nhiên** (định dạng YAML). Hệ thống tự động tải tất cả file `.yaml` trong thư mục này khi khởi động.

Đối với người dùng và tài liệu, chúng ta tiếp tục gọi các năng lực này là "chiến lược" (strategy); trong code, cấu hình và trường API, chúng được đặt tên thống nhất là `skill`, bạn có thể hiểu nó là "gói năng lực chiến lược tái sử dụng".

## Cách Viết Chiến Lược Tùy Chỉnh (Strategy Skill)

Chỉ cần tạo một file `.yaml`, mô tả chiến lược giao dịch của bạn bằng tiếng Việt (hoặc bất kỳ ngôn ngữ nào), **không cần viết code**.

### Template Tối Giản

```yaml
name: my_strategy          # Định danh duy nhất (tiếng Anh, gạch dưới)
display_name: Chiến lược của tôi  # Tên hiển thị
description: Mô tả ngắn gọn mục đích chiến lược

instructions: |
   Mô tả chiến lược của bạn...
   Viết bằng ngôn ngữ tự nhiên các tiêu chí đánh giá, điều kiện vào lệnh, điều kiện thoát lệnh...
   Có thể tham chiếu tên công cụ (như get_daily_history, analyze_trend) để hướng dẫn AI sử dụng dữ liệu nào.
```

### Template Đầy Đủ

```yaml
name: my_strategy
display_name: Chiến lược của tôi
description: Mô tả ngắn gọn ngữ cảnh thị trường phù hợp của chiến lược

# Phân loại chiến lược: trend (xu hướng), pattern (mô hình), reversal (đảo chiều), framework (khung)
category: trend

# Số ý tưởng giao dịch cốt lõi liên quan (1-7), tùy chọn
core_rules: [1, 2]

# Danh sách công cụ chiến lược cần dùng, tùy chọn
# Công cụ khả dụng: get_daily_history, analyze_trend, get_realtime_quote,
#           get_sector_rankings, search_stock_news
required_tools:
  - get_daily_history
  - analyze_trend

# Bí danh tùy chọn (dùng cho chọn skill ngôn ngữ tự nhiên như /ask)
aliases: [Chiến pháp của tôi, Mô hình của tôi]

# Metadata dưới đây dùng để điều khiển hành vi mặc định (tùy chọn)
# default_active: Có thuộc bộ skill kích hoạt mặc định không
# default_router: Có thuộc bộ skill fallback định tuyến không
# default_priority: Độ ưu tiên hiển thị/sắp xếp mặc định, số càng nhỏ càng trước
# market_regimes: Nhãn trạng thái thị trường chiến lược ưu tiên thích ứng
default_active: true
default_router: false
default_priority: 100
market_regimes: [trending_up]

# Mô tả chi tiết chiến lược (ngôn ngữ tự nhiên, hỗ trợ định dạng Markdown)
instructions: |
   **Tên chiến lược của tôi**

   Tiêu chí đánh giá:

   1. **Điều kiện một**:
      - Dùng `analyze_trend` kiểm tra sắp xếp đường均线.
      - Mô tả đặc trưng xu hướng bạn mong đợi...

   2. **Điều kiện hai**:
      - Mô tả yêu cầu khối lượng...

   Điều chỉnh điểm số:
   - Điều chỉnh sentiment_score gợi ý khi thỏa điều kiện
   - Ghi chú tên chiến lược trong `buy_reason`
```

### Tham Khảo Ý Tưởng Giao Dịch Cốt Lõi

| Số | Ý tưởng |
|------|------|
| 1 | Vào nghiêm ngặt: Độ lệch giá < 5% mới xem xét vào lệnh |
| 2 | Giao dịch xu hướng: MA5 > MA10 > MA20 sắp xếp đa đầu |
| 3 | Ưu tiên hiệu suất: Khối lượng xác nhận tính hiệu quả xu hướng |
| 4 | Ưu tiên điểm mua: Ưu tiên hồi về hỗ trợ đường均线 |
| 5 | Kiểm tra rủi ro: Tin tức tiêu cực phủ quyết một phiếu |
| 6 | Phối hợp lượng giá: Khối lượng giao dịch xác nhận vận động giá |
| 7 | Nới lỏng cổ phiếu xu hướng mạnh: Cổ phiếu đầu ngành có thể nới lỏng tiêu chuẩn |

## Thư Mục Chiến Lược Tùy Chỉnh

Ngoài thư mục này (chiến lược tích hợp sẵn), bạn có thể chỉ định thêm thư mục chiến lược tùy chỉnh qua biến môi trường:

```env
AGENT_SKILL_DIR=./my_skills
```

Hệ thống sẽ tải đồng thời chiến lược tích hợp sẵn và chiến lược tùy chỉnh. Nếu xung đột tên, chiến lược tùy chỉnh ghi đè chiến lược tích hợp sẵn.

Tên biến môi trường vẫn là `AGENT_SKILL_DIR`, đây là cổng cấu hình thống nhất nội bộ sau khi đặt tên lại; về ngữ nghĩa sản phẩm, nó vẫn biểu thị "thư mục chiến lược tùy chỉnh".
