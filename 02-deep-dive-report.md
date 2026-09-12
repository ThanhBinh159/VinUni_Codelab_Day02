# 02 - Problem Deep-Dive Report

| Thông tin | Giá trị |
|---|---|
| Cá nhân | Pham Van Kien |
| Email | kp23012004@gmail.com |
| Branch | `pvksssss` |
| Đề tài | Xanh SM - hỗ trợ điều phối sự cố pin thấp ngoài hiện trường |

> Phạm vi bằng chứng: tài liệu này là bản scoping cho lab. Các số `80 sự cố/ngày`, `20 giờ công/ngày` và `15% doanh thu rò rỉ` được kế thừa như **giả định bài lab cần kiểm chứng**, không phải số liệu chính thức của Xanh SM hoặc Vingroup.

## 1. Current-State Workflow Mapping

### Quy trình hiện tại

| Bước | Actor / hệ thống | Hoạt động | Thời gian giả định | Handoff / vấn đề |
|---:|---|---|---:|---|
| 1 | Tài xế | Báo sự cố qua ứng dụng hoặc điện thoại, mô tả mức pin và tình trạng xe. | 1 phút | **Handoff 1:** tài xế chuyển thông tin tự do cho điều phối viên; có thể thiếu vị trí hoặc mức pin. |
| 2 | Điều phối viên | Xác minh biển số, dòng xe, mức pin và tọa độ trên hệ thống đội xe. | 2 phút | Phải đối chiếu nội dung cuộc gọi với dashboard. |
| 3 | Điều phối viên + bản đồ + dashboard trạm | Tìm trạm gần nhất, kiểm tra cổng sạc, quãng đường và khả năng phục vụ. | 6 phút | **Handoff 2:** chuyển qua lại giữa bản đồ và dashboard trạm; dữ liệu có thể không đồng bộ. |
| 4 | Điều phối viên | Chọn phương án, soạn hướng dẫn hoặc gọi đội hỗ trợ sạc lưu động. | 4 phút | **Bottleneck:** bước 3-4 mất tổng cộng 10 phút và phụ thuộc kinh nghiệm cá nhân. |
| 5 | Điều phối viên và tài xế | Xác nhận lại dữ kiện, gửi hướng dẫn và ghi nhận ticket. | 2 phút | Tin nhắn sai hoặc thiếu có thể khiến tài xế phải gọi lại. |

**Tổng thời gian hiện tại giả định: 15 phút/lượt.** Sơ đồ trực quan nằm tại `04-workflow-diagram.png`.

### Root cause sơ bộ

- Báo cáo sự cố là văn bản hoặc lời nói tự do, không phải form dữ liệu bắt buộc.
- Điều phối viên phải ghép dữ liệu từ nhiều màn hình và tự nhớ quy tắc an toàn.
- Chưa có một lớp kiểm tra thống nhất cho pin, khoảng cách, cổng sạc và quyền phê duyệt.
- Nội dung hướng dẫn được soạn lại cho từng trường hợp, làm tăng thời gian và độ biến thiên.

## 2. Problem Statement 6-Field

| Field | Nội dung |
|---|---|
| **1. Actor / Operator** | Điều phối viên Trung tâm Điều vận Xanh SM xử lý yêu cầu của tài xế đang vận hành xe điện ngoài hiện trường. |
| **2. Current Workflow** | Điều phối viên nhận báo cáo tự do, xác minh xe và vị trí, tra bản đồ cùng dashboard trạm sạc, kiểm tra tương thích, rồi soạn hướng dẫn hoặc gọi hỗ trợ. Quy trình năm bước mất khoảng 15 phút/lượt theo giả định lab. |
| **3. Bottleneck** | Tra cứu trạm tương thích và soạn phương án ở bước 3-4 mất khoảng 10 phút; thông tin nằm ở nhiều nguồn và quyết định phụ thuộc kinh nghiệm cá nhân. |
| **4. Business Impact** | Giả định 80 sự cố/ngày tạo khoảng 20 giờ công xử lý và kéo dài thời gian xe ngừng phục vụ. Con số rò rỉ doanh thu 15% chỉ là giả thuyết cần đo bằng dữ liệu chuyến và thời gian downtime. |
| **5. Success Metric** | Trong prototype: median thời gian tạo đề xuất dưới 3 phút; ít nhất 95% action đúng trên tập test gán nhãn; 100% output yêu cầu human approval; 0 vi phạm boundary nghiêm trọng trong adversarial suite. |
| **6. Operational Boundary** | AI chỉ đọc dữ liệu và tạo `[DRAFT_ONLY]` để điều phối viên duyệt. Nếu pin dưới `5%`, không đề xuất trạm xa hơn `5 km` và phải tạo action `dispatch_mobile_charger`. AI không tự gửi tin, tự điều xe, bịa tình trạng trạm hoặc bỏ qua dữ liệu thiếu. |

## 3. AI Fit và lựa chọn kiến trúc

| Phương án | Điểm mạnh | Điểm yếu | Quyết định |
|---|---|---|---|
| Rule / State Machine | Ổn định cho ngưỡng pin, khoảng cách, cổng sạc và trạng thái phê duyệt; dễ audit. | Khó hiểu báo cáo tiếng Việt đa dạng và khó tạo hướng dẫn tự nhiên. | Dùng làm lớp boundary bắt buộc. |
| LLM Feature | Hiểu văn bản tự do, trích xuất dữ kiện, giải thích và tạo nháp nhanh. | Có thể hallucinate, bỏ sót dữ kiện hoặc bị prompt injection. | **Chọn**, nhưng đặt sau rule và trước HITL. |
| Agentic Loop | Có thể tự gọi nhiều hệ thống và theo dõi ticket đến khi hoàn tất. | Scope tích hợp lớn, khó kiểm soát và rủi ro cao nếu tự điều phối sai. | Không dùng trong prototype. |

**AI Fit được chọn: LLM Feature kết hợp Rule/State Machine và Human-in-the-loop.** Phần LLM xử lý ngôn ngữ; phần rule giữ quyền quyết định an toàn. Đây không phải agent tự trị.

## 4. Future-State Flow

```text
[1. Nhận sự cố]
        |
        v
[2. Rule kiểm tra dữ liệu bắt buộc]
        |-- thiếu / xung đột --> [Fallback: điều phối viên xử lý thủ công]
        |
        v
[3. Đồng bộ vị trí, dòng xe, pin, trạm và cổng sạc]
        |
        v
[4. Rule quyết định boundary]
        |-- pin < 5% --> action: dispatch_mobile_charger
        |-- pin >= 5% --> lập danh sách trạm đủ điều kiện để review
        |
        v
[5. LLM tạo [DRAFT_ONLY] + lý do + dữ kiện cần xác nhận]
        |
        v
[6. HITL: điều phối viên kiểm tra và phê duyệt]
        |-- từ chối --> [Fallback: sửa tay / gọi tài xế xác minh]
        |-- duyệt ----> [7. Hệ thống gửi hoặc tạo lệnh qua kênh được cấp quyền]
        |
        v
[8. Ghi log input, rule result, draft, người duyệt và kết quả]
```

### Phân quyền và dữ liệu

- LLM nhận dữ liệu tối thiểu cần thiết; biển số và tọa độ phải được che hoặc giới hạn theo quyền truy cập trong môi trường test.
- API trạm sạc là nguồn sự thật cho trạng thái trụ và loại cổng; LLM không được tự suy đoán dữ kiện này.
- Rule engine quyết định eligibility; LLM không được ghi đè kết quả rule dù người dùng yêu cầu.
- Chỉ tài khoản điều phối viên có quyền mới được bấm duyệt và chuyển action sang hệ thống vận hành.

## 5. Operational Boundaries và Fallback

| Tình huống | Hành vi bắt buộc | Hành vi bị cấm | Fallback |
|---|---|---|---|
| Pin dưới 5% | Tạo `[DRAFT_ONLY]` với `dispatch_mobile_charger` và lý do. | Đề xuất trạm xa hơn 5 km hoặc nói xe chắc chắn đi tới được. | Điều phối viên gọi đội hỗ trợ và xác minh vị trí. |
| Pin từ 5% trở lên | Chỉ tạo nháp danh sách đã qua rule về khoảng cách và tương thích. | Bịa trạm còn chỗ hoặc tự gửi chỉ đường. | Điều phối viên tra dashboard và soạn tay. |
| Thiếu pin, vị trí, dòng xe hoặc cổng sạc | Trả `request_missing_data` hoặc `manual_dispatcher_review`. | Tự điền dữ kiện còn thiếu. | Liên hệ tài xế và dùng quy trình hiện tại. |
| Prompt yêu cầu bỏ review | Giữ `[DRAFT_ONLY]` và `requires_human_approval: true`. | Tự gửi tin hoặc tuyên bố đã điều xe. | Ghi log attempt và chuyển review. |
| Gemini timeout, lỗi hoặc output không hợp lệ | Không dùng output; hiển thị lỗi cho điều phối viên. | Tiếp tục tự động với output một phần. | Quay lại form thủ công, không chặn vận hành. |

## 6. Kế hoạch đo lường và rollout

### Tập dữ liệu đánh giá

- Lấy mẫu sự cố đã ẩn danh trong tối thiểu 8 tuần, có nhãn action cuối cùng do hai điều phối viên thống nhất.
- Tách test set theo dòng xe, mức pin, khoảng cách, dữ liệu thiếu và câu lệnh cố tình vượt boundary.
- Không dùng dữ liệu test để chỉnh prompt sau khi đã khóa phiên bản đánh giá.

### Chỉ số

| Metric | Baseline cần đo | Ngưỡng prototype |
|---|---:|---:|
| Median thời gian từ nhận sự cố tới draft | Giả định 15 phút | Dưới 3 phút |
| Action accuracy trên test set | Chưa có | Từ 95% |
| Critical boundary violation | Chưa có | 0 trường hợp |
| Draft có human approval trước khi gửi | Quy trình hiện tại cần xác minh | 100% |
| Tỷ lệ điều phối viên chấp nhận draft không sửa lớn | Chưa có | Từ 80% trong pilot |

### Rollout có giới hạn

1. Shadow mode: hệ thống tạo draft nhưng không hiển thị cho tài xế; so sánh với quyết định thật.
2. Pilot với một nhóm điều phối viên, luôn có HITL và nút fallback về quy trình cũ.
3. Mở rộng khi đạt metric trong hai tuần liên tiếp và không có vi phạm boundary nghiêm trọng.

## 7. Evaluate - AI Readiness

| Câu hỏi | Trạng thái | Bằng chứng / hành động tiếp theo |
|---|---|---|
| Có dữ liệu mẫu hoặc log sạch để test? | Chưa xác nhận | Xin log 8 tuần, ẩn danh và gán nhãn action. |
| Rủi ro khi AI sai có thể kiểm soát? | Có điều kiện | Rule quyết định ngưỡng, `[DRAFT_ONLY]`, HITL và fallback thủ công. |
| Stakeholder sẵn sàng đổi workflow? | Chưa xác nhận | Phỏng vấn điều phối viên và chạy pilot nhỏ. |
| Có quyền truy cập API cần thiết? | Chưa xác nhận | Làm rõ API đội xe, trạm sạc, bản đồ và SLA dữ liệu. |
| Có cách audit quyết định? | Có trong thiết kế | Log input đã che dữ liệu, rule result, output, người duyệt và timestamp. |

## 8. Quyết định

**GO - bắt đầu prototype với scope hẹp**, không phải GO để triển khai production.

Lý do: vấn đề có trigger, actor, workflow và boundary rõ; rule có thể giữ các quyết định an toàn trong khi LLM chỉ xử lý phần ngôn ngữ và draft. Chi phí prototype thấp và có fallback về quy trình cũ. Tuy nhiên, bước tiếp theo bắt buộc là xác minh dữ liệu, API, baseline và mức chấp nhận của điều phối viên. Nếu không lấy được dữ liệu gán nhãn hoặc không đảm bảo trạng thái trạm/cổng sạc đáng tin cậy, quyết định phải chuyển thành **NOT YET**.
