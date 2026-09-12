# 01 - Problem Scan & Quick Assessment

| Thông tin | Giá trị |
|---|---|
| Cá nhân | Kien |
| Email | kp23012004@gmail.com |
| Branch | `pvksssss` |
| Bối cảnh | AI Product Engineer - Vin Smart Future |

> Lưu ý dữ liệu: các số liệu trong tài liệu này là giả định phục vụ bài lab, chưa phải số liệu chính thức của Vingroup. Trước khi thử nghiệm thực tế cần xác nhận bằng log vận hành và phỏng vấn stakeholder.

## Phase 1 - Scan cơ hội

| # | Công ty thành viên | Lens | Bài toán vận hành | Tác động có thể đo |
|---:|---|---|---|---|
| 1 | VinFast | Lặp lại | Nhân viên đối soát hóa đơn điện từ nhiều nhà cung cấp trạm sạc với phiên sạc trong hệ thống bằng thao tác thủ công. | Thời gian xử lý mỗi hóa đơn, tỷ lệ sai lệch và số hồ sơ cần kiểm tra lại. |
| 2 | Xanh SM | Tốn thời gian; Stakeholder Pain | Khi xe báo pin thấp ngoài hiện trường, điều phối viên phải chuyển qua nhiều màn hình để xác minh xe, tìm trạm tương thích và soạn hướng dẫn cho tài xế. | Thời gian xử lý sự cố, thời gian xe ngừng phục vụ và tỷ lệ chọn đúng phương án hỗ trợ. |
| 3 | Vinhomes | AI-upgrade | Nhân viên chăm sóc cư dân đọc khiếu nại tự do, tra quy định rồi soạn phản hồi; nội dung dễ thiếu nhất quán giữa các ca trực. | Thời gian soạn phản hồi, tỷ lệ chuyển cấp sai và mức hài lòng sau xử lý. |
| 4 | Vinmec | Lặp lại | Nhân viên kiểm tra thủ công mức đầy đủ của hồ sơ bệnh án trước khi chuyển cho bác sĩ hoặc bộ phận bảo hiểm. | Tỷ lệ hồ sơ thiếu trường bắt buộc, thời gian kiểm tra và số lượt trả lại. |
| 5 | Vinpearl / VinWonders | AI-upgrade; Tốn thời gian | Yêu cầu đa ngôn ngữ từ khách được đọc, dịch và chuyển thủ công tới lễ tân, buồng phòng, kỹ thuật hoặc vận chuyển. | Thời gian phân loại, tỷ lệ chuyển đúng bộ phận và SLA phản hồi đầu tiên. |

## Phase 2 - Quick Assessment

## Quick Problem Card #1 - Xanh SM xử lý sự cố pin thấp

| Trường | Nội dung |
|---|---|
| Bài toán một câu | Điều phối viên Xanh SM mất nhiều thời gian tổng hợp dữ liệu và chọn phương án an toàn khi tài xế báo pin thấp ngoài hiện trường. |
| Công ty thành viên | Xanh SM |
| Actor | Điều phối viên Trung tâm Điều vận; người nhận hỗ trợ là tài xế. |
| Workflow hiện tại | (1) Tài xế báo sự cố; (2) điều phối viên xác minh xe, pin và vị trí; (3) mở bản đồ và dashboard trạm sạc; (4) kiểm tra cổng sạc, khoảng cách và tình trạng trạm; (5) soạn hướng dẫn hoặc gọi hỗ trợ lưu động. |
| Bottleneck | Bước 3-4 và soạn hướng dẫn mất khoảng 10 phút/lượt trong tổng thời gian giả định 15 phút/lượt. |
| AI hỗ trợ | Đọc báo cáo tiếng Việt, chuẩn hóa dữ liệu sự cố, tạo đề xuất và nội dung nháp để điều phối viên duyệt. Rule cố định quyết định ngưỡng pin an toàn. |
| Success metric | Giảm median thời gian xử lý từ 15 phút xuống dưới 3 phút; ít nhất 95% chọn đúng action trên tập test gán nhãn; 0 vi phạm ranh giới pin nghiêm trọng. |
| Quick Architecture | **LLM Feature + Rule/State Machine + HITL** |
| Rủi ro chính | Đề xuất trạm không tương thích hoặc quá xa có thể làm xe cạn pin; AI không được tự gửi tin hay tự điều xe. |
| Evidence cần thu thập | Log sự cố 8 tuần, API trạm sạc, ma trận cổng sạc theo dòng xe, baseline thời gian xử lý và phỏng vấn điều phối viên. |

## Quick Problem Card #2 - Vinhomes hỗ trợ soạn phản hồi khiếu nại

| Trường | Nội dung |
|---|---|
| Bài toán một câu | Nhân viên chăm sóc cư dân tốn thời gian đọc khiếu nại, xác định chủ đề và soạn phản hồi nhất quán với quy định. |
| Công ty thành viên | Vinhomes |
| Actor | Nhân viên chăm sóc cư dân và trưởng ca phê duyệt. |
| Workflow hiện tại | (1) Nhận ticket; (2) đọc và phân loại; (3) tra quy định; (4) soạn phản hồi; (5) chuyển cấp hoặc gửi sau khi duyệt. |
| Bottleneck | Tra cứu và soạn phản hồi giả định mất 8-12 phút/ticket, lâu hơn khi ticket chứa nhiều vấn đề. |
| AI hỗ trợ | Phân loại chủ đề, trích xuất dữ kiện và tạo bản nháp có dẫn chiếu điều khoản để nhân viên kiểm tra. |
| Success metric | Giảm median thời gian tạo nháp xuống dưới 3 phút; ít nhất 90% phân loại đúng; 100% ticket phí hoặc tranh chấp phải có người duyệt. |
| Quick Architecture | **LLM Feature + retrieval + HITL** |
| Rủi ro chính | Hallucination về phí, quy định hoặc trách nhiệm pháp lý có thể làm khiếu nại nghiêm trọng hơn. |
| Evidence cần thu thập | Bộ ticket đã ẩn danh, taxonomy, kho quy định có phiên bản và kết quả QA phản hồi. |

## Quick Problem Card #3 - Vinpearl phân luồng yêu cầu đa ngôn ngữ

| Trường | Nội dung |
|---|---|
| Bài toán một câu | Nhân viên trực tổng đài phải dịch và chuyển thủ công yêu cầu đa ngôn ngữ của khách tới đúng bộ phận. |
| Công ty thành viên | Vinpearl / VinWonders |
| Actor | Nhân viên guest service và bộ phận tiếp nhận yêu cầu. |
| Workflow hiện tại | (1) Nhận tin nhắn; (2) nhận diện ngôn ngữ; (3) dịch ý chính; (4) chọn bộ phận; (5) chuyển ticket và theo dõi. |
| Bottleneck | Dịch và phân loại giả định mất 5-7 phút/yêu cầu, dễ sai với từ địa phương hoặc yêu cầu có nhiều ý. |
| AI hỗ trợ | Tóm tắt song ngữ, gắn nhãn bộ phận và độ ưu tiên, sau đó để nhân viên xác nhận trước khi chuyển. |
| Success metric | 90% yêu cầu được phân luồng trong 60 giây; ít nhất 92% đúng bộ phận; 100% tình huống an toàn được chuyển người trực. |
| Quick Architecture | **LLM Feature + Rule escalation** |
| Rủi ro chính | Dịch sai dị ứng, tai nạn hoặc nhu cầu y tế có thể làm chậm phản ứng khẩn cấp. |
| Evidence cần thu thập | Ticket đa ngôn ngữ đã ẩn danh, nhãn bộ phận, SLA và danh sách từ khóa khẩn cấp. |

## Quyết định lựa chọn

Chọn **Card #1 - Xanh SM xử lý sự cố pin thấp** để deep-dive.

| Tiêu chí | Xanh SM pin thấp | Vinhomes khiếu nại | Vinpearl phân luồng |
|---|---|---|---|
| Tác động vận hành | Cao, xe ngừng phục vụ theo thời gian thực | Trung bình-cao, ảnh hưởng SLA và hài lòng | Trung bình-cao, ảnh hưởng trải nghiệm khách |
| Dữ liệu đầu vào | Có cấu trúc tương đối rõ: pin, vị trí, dòng xe, trạm | Nhiều văn bản và quy định có phiên bản | Nhiều ngôn ngữ, nhãn và mức khẩn cấp |
| Rủi ro có thể giới hạn | Có thể khóa bằng ngưỡng pin, HITL và fallback | Rủi ro tranh chấp cần retrieval chặt | Rủi ro dịch sai tình huống khẩn cấp |
| Phù hợp prototype 30 phút | Rất phù hợp với hai boundary kiểm thử được | Cần kho tri thức quy định | Cần tập dữ liệu đa ngôn ngữ rộng |

Lý do chọn: bài toán Xanh SM có actor, trigger và metric rõ; có thể tách phần quyết định an toàn sang rule, chỉ dùng LLM cho hiểu ngôn ngữ và tạo nháp. Phạm vi này đủ nhỏ để stress-test bằng prompt nhưng vẫn thể hiện được AI Fit, HITL và fallback. Hai card còn lại có tiềm năng, song cần kho tri thức hoặc dữ liệu đa ngôn ngữ lớn hơn trước khi chứng minh độ an toàn.
