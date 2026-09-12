# Phase 6 — Reflection: AI Log & Personal Learning Notes

## 1. Bối cảnh và mục tiêu

Trong bài lab này, tôi làm vai trò là AI Engineer tại Vin Smart Future, tập trung vào mảng **Vinmec** và chọn bài toán **Tự động trích xuất và đối chiếu hồ sơ bệnh nhân**. Mục tiêu là xác định xem quy trình tiếp nhận hồ sơ bệnh án có thể được tối ưu bằng AI hay không, đồng thời đánh giá ranh giới vận hành và mức độ an toàn khi triển khai.

---

## 2. AI đã giúp tôi điều gì?

AI đã hỗ trợ tôi rất nhiều trong các bước sau:

1. **Brainstorm ý tưởng bài toán**  
   Tôi dùng AI để suy nghĩ về các pain point vận hành trong Vinmec. AI giúp tôi xác định các khu vực có khả năng ứng dụng AI rõ nhất như:
   - tiếp nhận hồ sơ bệnh nhân,
   - lập lịch khám,
   - hỗ trợ tư vấn bệnh nhân,
   - xử lý bảo hiểm và thanh toán.

2. **Lọc các bài toán có giá trị vận hành**  
   Sau khi có danh sách ý tưởng, AI giúp tôi nhìn theo góc độ doanh nghiệp: bài toán nào có impact lớn, bài toán nào dễ đo metric, và bài toán nào phù hợp với AI hơn rule-based.

3. **Tạo cấu trúc bài viết theo đúng format lab**  
   AI đã giúp tôi sắp xếp lại nội dung theo đúng trình tự của worksheet: SCAN → Quick Cards → Deep Dive → Evaluate. Điều này giúp tôi tiết kiệm thời gian viết và ít sai lệch format hơn.

4. **Tạo prompt prototype và kiểm tra ranh giới**  
   Với prompt prototype, AI hỗ trợ tôi thiết kế hệ thống hướng dẫn cho mô hình phải tuân thủ ranh giới an toàn, ví dụ:
   - bắt buộc giữ `[DRAFT_ONLY]` ở đầu output,
   - không được đề xuất trạm sạc xa khi pin dưới 5%,
   - cần yêu cầu approval của con người trước khi gửi thông điệp.

5. **Tạo một bản nháp tốt cho việc trình bày**  
   AI giúp tôi chuyển các ý tưởng thô thành văn bản gọn, rõ, có logic và dễ hiểu hơn khi trình bày trong bài học hoặc báo cáo.

---

## 3. AI đưa ra sai ở đâu? / Hallucination / sai lệch

AI cũng không phải lúc nào cũng đúng, và điều này rất quan trọng khi làm bài về sản phẩm AI.

### 3.1. Sai lệch ở khía cạnh “số liệu quá trừu tượng”
Ban đầu, AI có xu hướng gợi ý các con số rất đẹp nhưng thiếu căn cứ thực tế, ví dụ:
- “giảm 50% thời gian xử lý”
- “dự đoán chính xác 99%”

Với những con số như vậy, tôi nhận ra chúng quá phóng đại nếu không có nền tảng dữ liệu thực tế. Tôi đã sửa lại bằng cách:
- dùng các con số ước tính hợp lý,
- gắn với quy trình thực tế ở bệnh viện,
- nhấn mạnh rằng đây là estimate phục vụ scoping chứ không phải KPI thật.

### 3.2. Sai ở chỗ “quá lạc quan về khả năng tự động hóa”
AI đôi khi mong muốn các quy trình đều có thể tự động hóa hoàn toàn, trong khi thực tế y tế cần phải có người duyệt. Tôi đã nhận ra rằng:
- AI rất mạnh trong trích xuất dữ liệu,
- nhưng không nên tự động cập nhật hồ sơ y tế mà không có con người xác nhận,
- vì rủi ro liên quan đến thông tin bệnh nhân và bảo hiểm là rất cao.

### 3.3. Sai lệch về “AI có thể làm mọi thứ”
AI từng khuyến nghị rằng có thể thay toàn bộ nhân viên tiếp nhận bằng mô hình. Tôi đã nhấn mạnh rằng đây là lỗi logic vì trong bệnh viện, yếu tố con người vẫn cần ở các bước:
- phê duyệt dữ liệu có độ tin cậy thấp,
- giải quyết trường hợp bất thường,
- xử lý hồ sơ mờ / thiếu / mâu thuẫn.

---

## 4. Tôi đã sửa prompt như thế nào?

Ban đầu, tôi dùng một prompt khá chung, ví dụ:

> "Hãy gợi ý 5 bài toán AI cho Vinmec."

Prompt này quá rộng và AI trả lời rất mơ hồ, thiếu độ thực tế và thiếu metric rõ ràng. Tôi đã cập nhật prompt để cụ thể hơn:

> "Tôi là AI Engineer tại Vin Smart Future. Tôi đang tìm kiếm pain point vận hành cụ thể cho Vinmec. Hãy gợi ý 5 quy trình thủ công, tốn thời gian, có dấu hiệu rò rỉ hiệu suất, kèm ước tính tổn thất về thời gian/chi phí/SLA. Mỗi đề xuất cần có actor, bottleneck, metric và khả năng ứng dụng AI."

Sau đó, tôi tiếp tục chặt chẽ hơn cho từng bài toán:

> "Dưới đây là một thẻ bài toán. Hãy đóng vai trò là CFO và trưởng phòng vận hành cực kỳ khắt khe, chỉ ra 3 điểm yếu về logic, metric và khả năng triển khai."

Điều này giúp AI trở nên nghiêm ngặt hơn, không còn gợi ý những ý tưởng quá mơ hồ hoặc quá hứa hẹn.

---

## 5. Ranh giới vận hành mà tôi đã đặt ra

Trong bài học, tôi học được rằng AI không nên được triển khai “mở” quá rộng. Cụ thể, khi làm bài toán Vinmec, tôi đặt ra các ranh giới sau:

1. **AI chỉ hỗ trợ trích xuất và gợi ý, không thay thế phê duyệt con người**  
   AI được phép đọc và trích xuất dữ liệu, nhưng không được lưu hồ sơ trực tiếp nếu chưa có xác nhận của nhân viên.

2. **AI không được tự ý sửa thông tin quan trọng**  
   Ví dụ: tên bệnh nhân, ngày sinh, bảo hiểm, tiền sử bệnh cần được kiểm tra bởi người thật.

3. **AI phải có fallback khi dữ liệu không rõ**  
   Nếu ảnh scan mờ hoặc hồ sơ thiếu thông tin nhiều, hệ thống phải chuyển sang xử lý thủ công thay vì cố gắng “đoán”.

4. **AI phải làm rõ ràng mức độ tin cậy**  
   Nếu AI không chắc chắn mức độ chính xác, cần trả về cảnh báo thay vì giả định đúng.

5. **Human-in-the-loop là bắt buộc ở các bước có rủi ro cao**  
   Đây là nguyên tắc trọng tâm để đảm bảo hệ thống an toàn và chấp nhận được trong môi trường y tế.

---

## 6. Kết luận cá nhân

Qua bài lab này, tôi nhận ra rằng thành công của một dự án AI không nằm ở việc AI làm được nhiều, mà nằm ở việc AI làm đúng ở đúng nơi và đúng mức độ. Cụ thể:

- AI rất tốt ở việc xử lý văn bản, trích xuất thông tin, phân loại, và gợi ý hành động.
- Nhưng khi bài toán có rủi ro tài chính hoặc rủi ro sức khỏe, cần dùng Rule, checklists, và Human-in-the-loop để giữ an toàn.
- Một bài toán tốt không cần “tự động hóa 100%”; nó chỉ cần giải quyết được bottleneck chính và đem lại giá trị rõ ràng cho doanh nghiệp.

Với bài toán Vinmec về hồ sơ bệnh nhân, tôi tin rằng AI có khả năng tăng hiệu suất đáng kể nếu được triển khai ở phạm vi hẹp, có kiểm soát rõ, và được nhân viên phê duyệt ở các bước quan trọng.
