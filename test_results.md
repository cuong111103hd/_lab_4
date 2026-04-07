# Lab 4 Test Results

Ghi lại console log của ít nhất 5 test cases sau:

## Test 1 – Direct Answer (Không cần tool)
**User:** "Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu."
**Kỳ vọng:** Agent chào hỏi, hỏi thêm về sở thích/ngân sách/thời gian. Không gọi tool nào.

**Kết quả thực tế:**
```text
2026-04-07 23:37:27,917 - agent - INFO - User Input: Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.
2026-04-07 23:37:27,917 - agent - INFO - Đang gọi Agent LLM...
2026-04-07 23:37:30,682 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-04-07 23:37:30,693 - agent - INFO - Agent trả lời: Chào bạn! Rất vui được hỗ trợ bạn trong kế hoạch du lịch. Bạn có thể cho mình biết một số thông tin như:

1. Bạn muốn đi đâu?
2. Thời gian dự kiến đi và về?
3. Ngân sách bạn dự định cho chuyến đi là bao nhiêu?
4. Bạn thích hoạt động gì trong chuyến đi (thăm quan, ẩm thực, nghỉ dưỡng,...)?

Với những thông tin này, mình sẽ giúp bạn tìm ra điểm đến phù hợp nhất!
INFO:     127.0.0.1:39660 - "POST /chat HTTP/1.1" 200 OK
```

## Test 2 - Single Tool Call
**User:** "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng"
**Kỳ vọng:** Gọi search_flights("Hà Nội", "Đà Nẵng"), liệt kê 4 chuyến bay.

**Kết quả thực tế:**
```text
2026-04-07 23:37:53,163 - agent - INFO - User Input: Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng
2026-04-07 23:37:53,163 - agent - INFO - Đang gọi Agent LLM...
2026-04-07 23:37:54,604 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-04-07 23:37:54,615 - agent - INFO - Agent quyết định gọi Tool: search_flights | Tham số: {'origin': 'Hà Nội', 'destination': 'Đà Nẵng'}
2026-04-07 23:37:54,621 - tools - INFO - Tìm chuyến bay giữa Hà Nội và Đà Nẵng
2026-04-07 23:37:54,622 - agent - INFO - Đang gọi Agent LLM...
2026-04-07 23:37:59,665 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-04-07 23:37:59,667 - agent - INFO - Agent trả lời: Dưới đây là các chuyến bay từ Hà Nội đi Đà Nẵng mà tôi tìm thấy:

1. Chuyến bay của VietJet Air:
   - Hạng vé: Economy
   - Giờ khởi hành: 09:50
   - Giờ đến: 11:10
   - Giá: 890.000₫

2. Chuyến bay của Bamboo Airways:
   - Hạng vé: Economy
   - Giờ khởi hành: 08:30
   - Giờ đến: 09:50
   - Giá: 1.200.000₫

3. Chuyến bay của Vietnam Airlines:
   - Hạng vé: Economy
   - Giờ khởi hành: 06:00
   - Giờ đến: 07:20
   - Giá: 1.450.000₫

4. Chuyến bay của Vietnam Airlines (hạng thương gia):
   - Hạng vé: Business
   - Giờ khởi hành: 14:00
   - Giờ đến: 15:20
   - Giá: 2.800.000₫

Nếu bạn cần thêm thông tin hoặc muốn đặt vé, hãy cho tôi biết nhé!
INFO:     127.0.0.1:56928 - "POST /chat HTTP/1.1" 200 OK
```

## Test 3 - Multi-Step Tool Chaining
**User:** "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!"
**Kỳ vọng:** Agent thực hiện chuỗi nhiều bước (search flights -> search hotels -> calculate budget).

**Kết quả thực tế:**
```text
2026-04-07 23:39:00,411 - agent - INFO - User Input: Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!
2026-04-07 23:39:00,411 - agent - INFO - Đang gọi Agent LLM...
2026-04-07 23:39:02,732 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-04-07 23:39:02,734 - agent - INFO - Agent quyết định gọi Tool: search_flights | Tham số: {'origin': 'Hà Nội', 'destination': 'Phú Quốc'}
2026-04-07 23:39:02,734 - agent - INFO - Agent quyết định gọi Tool: google_hotels | Tham số: {'city': 'Phú Quốc', 'max_price_per_night': 2500000}
2026-04-07 23:39:02,736 - tools - INFO - Tìm chuyến bay giữa Hà Nội và Phú Quốc
2026-04-07 23:39:02,737 - tools - INFO - Tìm khách sạn tại Phú Quốc, max_price: 2.500.000₫
2026-04-07 23:39:02,738 - agent - INFO - Đang gọi Agent LLM...
2026-04-07 23:39:05,652 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-04-07 23:39:05,659 - agent - INFO - Agent quyết định gọi Tool: calculate_budget | Tham số: {'total_budget': 5000000, 'expenses_json': '{"Vé máy bay": 1350000, "Khách sạn (2 đêm)": 400000}"}'}
2026-04-07 23:39:05,661 - tools - INFO - Đang parse expenses và tính tổng ngân sách.
2026-04-07 23:39:05,662 - tools - ERROR - JSONDecodeError trong lúc parse expenses_json
2026-04-07 23:39:05,663 - agent - INFO - Đang gọi Agent LLM...
2026-04-07 23:39:07,246 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-04-07 23:39:07,250 - agent - INFO - Agent quyết định gọi Tool: calculate_budget | Tham số: {'total_budget': 5000000, 'expenses_json': '{"Vé máy bay": 1350000, "Khách sạn (2 đêm)": 400000}"}'}
2026-04-07 23:39:07,252 - tools - INFO - Đang parse expenses và tính tổng ngân sách.
2026-04-07 23:39:07,252 - tools - ERROR - JSONDecodeError trong lúc parse expenses_json
2026-04-07 23:39:07,253 - agent - INFO - Đang gọi Agent LLM...
2026-04-07 23:39:08,513 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-04-07 23:39:08,517 - agent - INFO - Agent quyết định gọi Tool: calculate_budget | Tham số: {'total_budget': 5000000, 'expenses_json': '{"Vé máy bay": 1350000, "Khách sạn (2 đêm)": 4000000}'}
2026-04-07 23:39:08,520 - tools - INFO - Đang parse expenses và tính tổng ngân sách.
2026-04-07 23:39:08,520 - tools - WARNING - CẢNH BÁO: Bạn đã vượt ngân sách số tiền 350.000₫!
2026-04-07 23:39:08,521 - agent - INFO - Đang gọi Agent LLM...
2026-04-07 23:39:10,011 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-04-07 23:39:10,012 - agent - INFO - Agent quyết định gọi Tool: calculate_budget | Tham số: {'total_budget': 5000000, 'expenses_json': '{"Vé máy bay": 1100000, "Khách sạn (2 đêm)": 400000}"}'}
2026-04-07 23:39:10,016 - tools - INFO - Đang parse expenses và tính tổng ngân sách.
2026-04-07 23:39:10,016 - tools - ERROR - JSONDecodeError trong lúc parse expenses_json
2026-04-07 23:39:10,017 - agent - INFO - Đang gọi Agent LLM...
2026-04-07 23:39:11,638 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-04-07 23:39:11,640 - agent - INFO - Agent quyết định gọi Tool: calculate_budget | Tham số: {'total_budget': 5000000, 'expenses_json': '{"Vé máy bay": 1100000, "Khách sạn (2 đêm)": 4000000}'}
2026-04-07 23:39:11,644 - tools - INFO - Đang parse expenses và tính tổng ngân sách.
2026-04-07 23:39:11,644 - tools - WARNING - CẢNH BÁO: Bạn đã vượt ngân sách số tiền 100.000₫!
2026-04-07 23:39:11,645 - agent - INFO - Đang gọi Agent LLM...
2026-04-07 23:39:12,775 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-04-07 23:39:12,776 - agent - INFO - Agent quyết định gọi Tool: calculate_budget | Tham số: {'total_budget': 5000000, 'expenses_json': '{"Vé máy bay": 1350000, "Khách sạn (2 đêm)": 1600000}'}
2026-04-07 23:39:12,779 - tools - INFO - Đang parse expenses và tính tổng ngân sách.
2026-04-07 23:39:12,779 - tools - INFO - TỐT: Trong ngân sách. Số dư còn lại 2.050.000₫.
2026-04-07 23:39:12,781 - agent - INFO - Đang gọi Agent LLM...
2026-04-07 23:39:14,478 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-04-07 23:39:14,483 - agent - INFO - Agent quyết định gọi Tool: update_trip_summary | Tham số: {'flights': 'VietJet Air, hạng vé: economy, giá: 1.350.000₫', 'hotels': 'Khách sạn: 9Station Hostel, hạng phòng: 200.000₫/đêm, lưu ý: 2 đêm', 'total_cost': '2.950.000₫'}
2026-04-07 23:39:14,486 - tools - INFO - Cập nhật Trip Summary trên Frontend UI thành công.
2026-04-07 23:39:14,487 - agent - INFO - Đang gọi Agent LLM...
2026-04-07 23:39:17,996 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-04-07 23:39:17,997 - agent - INFO - Agent trả lời: Dưới đây là thông tin chuyến đi của bạn từ Hà Nội đến Phú Quốc:

1. Chuyến bay: VietJet Air, hạng vé: economy, giá: 1.350.000₫
2. Khách sạn: 9Station Hostel, hạng phòng: 200.000₫/đêm, lưu ý: 2 đêm
3. Tổng chi phí ước tính: 2.950.000₫ (còn dư 2.050.000₫ trong ngân sách)
4. Gợi ý thêm: Bạn có thể khám phá các bãi biển đẹp ở Phú Quốc, thưởng thức hải sản tươi ngon tại các quán ăn địa phương, hoặc tham gia các hoạt động như lặn biển, tham quan Vinpearl Land.

Nếu bạn cần thêm thông tin hoặc hỗ trợ gì khác, hãy cho mình biết nhé!
INFO:     127.0.0.1:49112 - "POST /chat HTTP/1.1" 200 OK
```

## Test 4 - Missing Info / Clarification
**User:** "Tôi muốn đặt khách sạn"
**Kỳ vọng:** Agent hỏi lại thông tin còn thiếu.

**Kết quả thực tế:**
```text
2026-04-07 23:39:50,569 - agent - INFO - User Input: Tôi muốn đặt khách sạn
2026-04-07 23:39:50,569 - agent - INFO - Đang gọi Agent LLM...
2026-04-07 23:39:52,608 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-04-07 23:39:52,609 - agent - INFO - Agent trả lời: Để giúp bạn đặt khách sạn, mình cần biết một số thông tin sau:

1. Bạn sẽ đi đâu?
2. Ngân sách của bạn cho mỗi đêm là bao nhiêu?
3. Số đêm bạn dự định lưu trú là bao nhiêu?

Hãy cung cấp cho mình những thông tin này nhé!
INFO:     127.0.0.1:44458 - "POST /chat HTTP/1.1" 200 OK
```

## Test 5 - Guardrail / Refusal
**User:** "Giải giúp tôi bài tập lập trình Python về linked list"
**Kỳ vọng:** Từ chối lịch sự và chỉ tập trung vào du lịch.

**Kết quả thực tế:**
```text
2026-04-07 23:40:06,050 - agent - INFO - User Input: Giải giúp tôi bài tập lập trình Python về linked list
2026-04-07 23:40:06,050 - agent - INFO - Đang gọi Agent LLM...
2026-04-07 23:40:07,455 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2026-04-07 23:40:07,457 - agent - INFO - Agent trả lời: Xin lỗi, nhưng mình không thể giúp bạn với bài tập lập trình. Tuy nhiên, nếu bạn cần thông tin hoặc gợi ý về du lịch, mình rất sẵn lòng hỗ trợ! Bạn đang có kế hoạch đi đâu không?
INFO:     127.0.0.1:60872 - "POST /chat HTTP/1.1" 200 OK
```








