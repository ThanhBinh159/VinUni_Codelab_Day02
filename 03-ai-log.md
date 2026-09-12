# 03 - AI Log & Reflection

| Thông tin | Giá trị |
|---|---|
| Cá nhân | Kien |
| Email | kp23012004@gmail.com |
| Branch | `pvksssss` |
| Công cụ AI | Codex / ChatGPT làm thought-partner; Gemini 2.5 Flash là model mục tiêu của prototype |

> Trung thực về thử nghiệm: môi trường hiện tại chưa có `GEMINI_API_KEY`, vì vậy tôi kiểm tra boundary bằng chế độ deterministic offline. Code đã giữ đường chạy Gemini online để chạy lại khi có API key; tôi không ghi nhận kết quả offline như kết quả do Gemini sinh ra.

## 1. Mục tiêu làm việc với AI

Tôi dùng AI như một người cùng phân tích để chuyển yêu cầu trong slide và worksheet thành một bài nộp nhất quán. Mục tiêu không phải để AI tự viết một ý tưởng thật dài, mà để hỗ trợ bốn việc: quét pain point, phản biện lựa chọn đề tài, xác định operational boundary và kiểm tra sự khớp nhau giữa báo cáo, code, diagram và autograder.

## 2. AI đã hỗ trợ

### Đọc và cấu trúc yêu cầu

AI giúp tôi tổng hợp các đầu ra bắt buộc từ slide, `README.md`, worksheet và autograder:

- Tối thiểu 5 vấn đề được tìm bằng các lens khác nhau.
- Chọn 3 vấn đề để làm Quick Problem Cards.
- Chọn 1 vấn đề để deep-dive theo 6 trường.
- Có current workflow, handoff, thời gian và bottleneck.
- So sánh Rule, LLM Feature và Agentic Loop; có HITL và fallback.
- Hoàn thiện prompt prototype và ít nhất 2 adversarial tests.
- Nộp đủ 3 file Markdown và 1 workflow diagram.

Việc đối chiếu trực tiếp autograder cũng giúp phát hiện các token bắt buộc như `[DRAFT_ONLY]`, `5%` và `dispatch_mobile_charger` thay vì chỉ diễn giải chung chung.

### Brainstorm và chọn đề tài

AI đề xuất nhiều pain point thuộc VinFast, Xanh SM, Vinhomes, Vinmec và Vinpearl. Sau khi so sánh, tôi chọn xử lý sự cố pin thấp của Xanh SM vì actor và trigger rõ, có tác động thời gian thực, metric có thể đo, và rủi ro có thể khóa bằng rule cùng bước duyệt của điều phối viên.

### Thiết kế boundary

AI giúp tách hai loại công việc:

- Rule/State Machine giữ quyết định định lượng và quyền thực thi.
- LLM hiểu báo cáo tiếng Việt và tạo bản nháp có lý do.

Từ đó, prototype bắt buộc mọi output bắt đầu bằng `[DRAFT_ONLY]`, dùng `dispatch_mobile_charger` khi pin dưới 5%, yêu cầu human approval và fallback khi thiếu dữ liệu.

## 3. AI đã sai hoặc thiếu

### Nhầm actor và phạm vi vận hành

Gợi ý đầu tiên mô tả người dùng chính là chủ xe VinFast tư nhân. Cách mô tả đó gần với chủ đề sạc pin nhưng không khớp code mẫu, trong đó role là dispatcher co-pilot cho Xanh SM. Nếu giữ cách hiểu ban đầu, báo cáo sẽ nói về khách hàng cá nhân trong khi prompt và workflow lại nói về đội xe taxi.

Tôi sửa actor chính thành **điều phối viên Trung tâm Điều vận Xanh SM**, còn tài xế là người báo sự cố và nhận hỗ trợ. Hạ tầng trạm sạc VinFast là dependency, không phải đơn vị sở hữu workflow chính.

### Đưa số liệu ví dụ thành sự thật

Các con số như 80 sự cố/ngày, 20 giờ công/ngày và 15% doanh thu rò rỉ xuất hiện trong worked example. AI có thể viết chúng theo giọng khẳng định, nhưng tài liệu không cung cấp nguồn vận hành để xác nhận đây là số thật.

Tôi giữ các số này chỉ để minh họa cách tính impact và gắn nhãn **giả định bài lab cần kiểm chứng**. Readiness checklist yêu cầu xin log 8 tuần và đo baseline trước khi pilot.

### Quá phụ thuộc vào prompt

Một phiên bản ý tưởng ban đầu cố dùng system prompt để tự bảo vệ mọi rủi ro. Điều này chưa đủ vì LLM vẫn có thể bỏ qua ngưỡng, trả JSON lỗi hoặc bị prompt injection. Tôi chuyển ngưỡng pin, khoảng cách và quyền phê duyệt sang rule deterministic; LLM không được quyền ghi đè rule.

## 4. Cách tôi kiểm chứng

- Đối chiếu từng đầu ra với rubric trong `01-worksheet.md`.
- Đọc `autograder/autograder.py` để biết chính xác tiêu chí file, cấu trúc test và cách kiểm tra output.
- Viết adversarial cases cho pin 2% nhưng bị yêu cầu đi 8 km và cho yêu cầu bỏ `[DRAFT_ONLY]`.
- Chạy test offline với các trường hợp pin dưới ngưỡng, pin bình thường, thiếu mức pin và prompt cố bypass review.
- Tách kết quả offline khỏi Gemini online để không tạo bằng chứng giả khi chưa có API key.
- Kiểm tra lại cùng một threshold, action name và actor trong cả ba báo cáo, code và workflow.

## 5. Cách tôi sửa prompt

Prompt chung chung ban đầu:

```text
Hãy hỗ trợ tài xế tìm trạm sạc gần nhất và trả lời an toàn.
```

Vấn đề: không nói AI có quyền gì, không có ngưỡng số, không định dạng output, không có HITL và không xử lý dữ liệu thiếu.

Prompt sau khi sửa:

```text
Bạn là dispatcher co-pilot cho Xanh SM. Chỉ tạo bản nháp cho điều phối viên.
Mọi phản hồi phải bắt đầu bằng [DRAFT_ONLY] và có
requires_human_approval=true. Nếu mức pin dưới 5%, không đề xuất trạm xa
hơn 5 km; tạo action dispatch_mobile_charger. Không tự gửi tin, không tự
điều xe, không bịa trạng thái trạm. Nếu thiếu pin, vị trí, dòng xe, cổng sạc
hoặc dữ liệu trạm, yêu cầu bổ sung dữ liệu hoặc chuyển xử lý thủ công.
```

Phiên bản sửa biến các khái niệm “an toàn” và “gần” thành điều kiện có thể test, đồng thời nói rõ fallback và quyền quyết định cuối cùng của con người.

## 6. Reflection cá nhân

Điểm hữu ích nhất của AI trong bài này là giúp tôi thấy mâu thuẫn giữa các artifact sớm: chỉ cần actor, metric hoặc threshold khác nhau là toàn bộ câu chuyện sản phẩm mất tính thuyết phục. Điểm tôi không nên giao cho AI là xác nhận số liệu kinh doanh và quyết định an toàn cuối cùng. Những phần đó cần log thật, chuyên gia vận hành và rule có thể audit.

Nếu làm vòng tiếp theo, tôi sẽ xin dữ liệu đã ẩn danh trước, cùng hai điều phối viên xây test set và đo baseline. Chỉ sau khi shadow mode đạt metric ổn định, tôi mới đề xuất pilot có HITL; chưa có cơ sở để tự động hóa hoàn toàn.
