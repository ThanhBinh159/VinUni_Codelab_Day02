Họ và Tên: Nguyễn Thanh Bình
Mã học viên: 2A202602777
Level 3

# Phase 1 — PROBLEM-SCAN:
| # | Subsidiary | Lens | Mô tả ngắn bài toán |
|---|------------|------|---------------------|
| 1 | **Vinhomes** | Tốn thời gian | **Xung đột giữa các agent:** agent cư dân, agent bảo trì và agent tài chính cùng cập nhật một yêu cầu nhưng không có cơ chế phân quyền và khóa trạng thái thống nhất. Ước tính 5-10% ticket liên phòng ban bị trùng hoặc trả về lẫn nhau, làm tăng 1-2 ngày thời gian xử lý và tạo 30-50 giờ công điều phối mỗi tháng. |
| 2 | **Vinhomes** | AI có thể tốt hơn | **Context và quyền truy cập bị lỗi thời:** agent dùng thông tin căn hộ, hợp đồng, biểu phí hoặc quy định cũ để tư vấn. Nếu 3-5% trong 5,000 lượt tư vấn/tháng cần sửa lại, khoảng 150-250 lượt có thể dẫn tới cam kết sai, thất thu phí hoặc 100-200 giờ xử lý khiếu nại. |
| 3 | **Vinhomes** | Pain từ người khác | **Không đo được trách nhiệm khi agent lỗi:** nhiều agent cùng sửa một hồ sơ hoặc gọi tool nhưng audit log không ghi đủ phiên bản prompt, dữ liệu đầu vào và người phê duyệt. 10-15% sự cố phải điều tra lại thủ công; mỗi sự cố mất 2-4 giờ, tương đương 40-90 giờ công/tháng và làm chậm xử lý khiếu nại. |
| 4 | **VinFast** | AI có thể tốt hơn | **Agent hướng dẫn sạc dùng dữ liệu không đồng bộ:** agent lập lịch dựa trên trạng thái trụ sạc, loại cổng hoặc hàng đợi đã cũ, khiến xe được dẫn tới trạm không phù hợp hoặc hết chỗ. Giả định 3-5% trong 10,000 lượt gợi ý/tháng cần đổi tuyến; mỗi lượt mất thêm 10-20 phút và tạo chi phí CSKH, cứu hộ hoặc bồi hoàn. |
| 5 | **VinFast** | Pain từ người khác | **Agent chẩn đoán lỗi xe quá tự tin:** agent chuyển mô tả tiếng Việt của khách thành mã lỗi ban đầu nhưng đánh giá thấp các dấu hiệu liên quan đến phanh, pin cao áp hoặc nhiệt độ bất thường. Chỉ 1% trong 3,000 ca/tháng bị phân luồng sai đã tạo 30 ca phải gọi lại/đổi lịch; mỗi ca có thể mất 30-60 phút và buộc kỹ sư kiểm duyệt lại. |

---

# Phase 2 — QUICK-ASSESS: 3 Quick Problem Cards

## QUICK PROBLEM CARD #1 — Vinhomes: Xung đột trạng thái giữa các agent

**Bài toán (1 câu):** Các agent cư dân, bảo trì và tài chính cùng xử lý một yêu cầu nhưng cập nhật trạng thái không nhất quán, khiến ticket bị trùng, trả về sai bộ phận hoặc bị xử lý song song.

**Công ty thành viên:** Vinhomes

**Ai đang đau (Actor):** Điều phối viên vận hành, nhân viên ban quản lý tòa nhà và cư dân chờ xử lý.

**Workflow hiện tại:**

1. Agent cư dân tiếp nhận yêu cầu và tạo ticket.
2. Agent điều phối đọc nội dung, gán bộ phận và cập nhật trạng thái.
3. Agent bảo trì hoặc tài chính gọi tool riêng để xử lý.
4. Các agent ghi kết quả về hệ thống với quyền và trạng thái khác nhau.
5. Điều phối viên kiểm tra ticket trùng, sửa trạng thái và thông báo lại cho cư dân.

**Bước tốn thời gian/lỗi nhất:** Bước 4-5, khoảng 5-8 phút/ticket cần điều phối lại; 5-10% ticket liên phòng ban có thể bị trùng hoặc trả về lẫn nhau.

**AI có thể hỗ trợ ở đâu:** Agent điều phối chỉ được đề xuất owner, trạng thái tiếp theo và hành động cần gọi; một state machine và policy engine kiểm tra quyền, khóa ticket và ngăn hai agent cập nhật cùng lúc.

**Đo thành công bằng gì:** Giảm ticket bị trùng hoặc trả sai bộ phận từ 5-10% xuống dưới 2%; giảm thời gian điều phối thủ công từ 5-8 phút xuống dưới 2 phút/ticket; 100% thay đổi trạng thái có actor, timestamp và reason code.

**Operational boundary:** Agent không được tự ý đóng ticket, thay đổi phí hoặc ghi đè trạng thái đã được người khác phê duyệt. Conflict phải chuyển về điều phối viên; source of truth là workflow engine, không phải nội dung suy luận của LLM.

**Quick Architecture:** [ ] No AI  [x] Rule/State Machine  [ ] LLM  [x] Agent có policy guard

## QUICK PROBLEM CARD #3 — Vinhomes: Không truy được trách nhiệm khi agent lỗi

**Bài toán (1 câu):** Khi nhiều agent và nhân viên cùng sửa hồ sơ cư dân hoặc gọi tool, Vinhomes không tái dựng được agent đã đọc dữ liệu nào, dùng phiên bản prompt nào và ai đã phê duyệt hành động.

**Công ty thành viên:** Vinhomes

**Ai đang đau (Actor):** Trưởng ca vận hành, bộ phận kiểm soát chất lượng, pháp chế và nhân viên tiếp nhận khiếu nại.

**Workflow hiện tại:**

1. Hệ thống tiếp nhận yêu cầu từ app, hotline hoặc email.
2. Một hoặc nhiều agent phân tích và gọi tool nghiệp vụ.
3. Nhân viên xem kết quả rồi phê duyệt hoặc chỉnh sửa.
4. Khi có khiếu nại, quản lý thu thập log từ nhiều hệ thống.
5. Đội vận hành phỏng vấn lại người liên quan và lập biên bản nguyên nhân.

**Bước tốn thời gian/lỗi nhất:** Bước 4-5, khoảng 2-4 giờ/sự cố; 10-15% sự cố cần điều tra thủ công do thiếu trace liên tục từ input đến quyết định cuối.

**AI có thể hỗ trợ ở đâu:** Một audit agent có quyền chỉ đọc liên kết request ID, phiên bản prompt/model, dữ liệu truy xuất, tool call, policy decision, người duyệt và output cuối thành timeline có thể kiểm tra.

**Đo thành công bằng gì:** Giảm thời gian tái dựng một sự cố từ 2-4 giờ xuống dưới 20 phút; 100% tool call có request ID và người/chính sách phê duyệt; xác định được nguyên nhân gốc trong ít nhất 90% case audit.

**Operational boundary:** Audit agent không được sửa log gốc, xóa bằng chứng hoặc tự kết luận trách nhiệm pháp lý. Log phải append-only, có phân quyền và che dữ liệu cá nhân không cần thiết.

**Quick Architecture:** [ ] No AI  [x] Rule/Audit Pipeline  [ ] LLM  [x] Agent chỉ đọc để điều tra

## QUICK PROBLEM CARD #5 — VinFast: Triage lỗi xe từ mô tả tiếng Việt

**Bài toán (1 câu):** Agent diễn giải mô tả lỗi xe bằng tiếng Việt có thể phân loại sai mức độ nghiêm trọng, đặc biệt với dấu hiệu liên quan đến phanh, pin cao áp hoặc nhiệt độ bất thường.

**Công ty thành viên:** VinFast

**Ai đang đau (Actor):** Khách hàng, nhân viên tổng đài, cố vấn dịch vụ và kỹ sư kỹ thuật.

**Workflow hiện tại:**

1. Khách hàng mô tả triệu chứng qua tổng đài, app hoặc tin nhắn.
2. Nhân viên hỏi lại để xác định thời điểm, điều kiện và mức độ xảy ra lỗi.
3. Cố vấn dịch vụ đối chiếu mô tả với mã lỗi và tài liệu kỹ thuật.
4. Trung tâm dịch vụ xếp mức độ ưu tiên, lịch kiểm tra và hình thức hỗ trợ.
5. Kỹ sư kiểm tra thực tế và xác nhận nguyên nhân.

**Bước tốn thời gian/lỗi nhất:** Bước 2-3, khoảng 10-15 phút/ca; với giả định 3,000 ca/tháng, 1% phân luồng sai tạo khoảng 30 ca phải gọi lại hoặc đổi lịch.

**AI có thể hỗ trợ ở đâu:** LLM trích xuất triệu chứng, bộ phận xe, điều kiện xuất hiện và dấu hiệu nguy hiểm thành JSON; rule engine kiểm tra safety trigger trước khi đề xuất mã lỗi sơ bộ hoặc lịch hẹn.

**Đo thành công bằng gì:** Trích xuất đúng trường thông tin trong ít nhất 90% ca; giảm thời gian intake từ 10-15 phút xuống dưới 4 phút; recall của nhóm cảnh báo an toàn đạt 99%; 100% ca có safety trigger được kỹ sư hoặc cố vấn xác nhận.

**Operational boundary:** AI chỉ được triage và draft câu hỏi bổ sung, không được kết luận xe an toàn, hướng dẫn khách tự sửa hệ thống phanh/pin cao áp hoặc tự đóng ca. Khi thiếu dữ kiện, có tín hiệu an toàn hoặc confidence thấp, bắt buộc chuyển người phụ trách.

**Quick Architecture:** [ ] No AI  [ ] Rule  [x] LLM Feature  [ ] Agent tự trị + safety gate và HITL bắt buộc

