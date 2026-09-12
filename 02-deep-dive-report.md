# Deep-Dive Report — Vinhomes Agent Accountability

> **Problem được chọn:** Problem #3 — Không đo được trách nhiệm khi agent lỗi.
>
> **Phạm vi:** Phase 3 — Current-State Workflow, Problem Statement và Future-State Flow.
>
> **Lưu ý dữ liệu:** Các con số trong báo cáo là giả định scoping kế thừa từ Quick Problem Card, chưa phải số liệu xác nhận của Vinhomes. Cần kiểm chứng bằng audit log, ticket system và phỏng vấn đội vận hành trước khi quyết định pilot.

## Bối cảnh vận hành

Vinhomes có thể sử dụng nhiều agent cho các luồng tiếp nhận phản ánh, tra cứu hồ sơ, điều phối bảo trì, xử lý tài chính và phản hồi cư dân. Khi các agent gọi tool và chuyển giao công việc qua nhiều hệ thống, đội vận hành cần trả lời được bốn câu hỏi sau khi có sự cố:

1. Agent nào đã thực hiện hành động?
2. Agent đã đọc dữ liệu và tài liệu phiên bản nào?
3. Chính sách nào cho phép hoặc chặn hành động đó?
4. Người nào đã phê duyệt kết quả cuối cùng?

Pain point không chỉ là thiếu log. Vấn đề là các log hiện có có thể rời rạc, khác định dạng và không liên kết được thành một timeline từ yêu cầu ban đầu đến hành động cuối.

# Phase 3 — DEEP-DIVE

## 3.1. Current-State Workflow

### Quy trình điều tra một sự cố agent hiện tại

```text
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│ Bước 1         │     │ Bước 2         │     │ Bước 3         │
│ Tiếp nhận yêu  │ ──> │ Agent phân tích│ ──> │ Agent gọi tool │
│ cầu/khiếu nại  │     │ và lập kế hoạch│     │ nghiệp vụ      │
│                │     │                │     │                │
│ Ai: CSKH/       │     │ Ai: Agent      │     │ Ai: Agent/     │
│ hệ thống       │     │ cư dân         │     │ service agent  │
│ ⏱ 1-3 phút     │     │ ⏱ 10-30 giây   │     │ ⏱ 10-60 giây   │
│ Out: Request ID│     │ Out: plan/log? │     │ Out: tool result│
└────────────────┘     └────────────────┘     └────────────────┘
                                                        │
                                                        v
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│ Bước 6         │ <── │ Bước 5         │ <── │ Bước 4         │
│ Lập biên bản,  │     │ Thu thập log từ│     │ Người duyệt    │
│ phản hồi/khắc  │     │ nhiều hệ thống │     │ xem và sửa kết │
│ phục           │     │                │     │ quả agent      │
│                │     │ Ai: QA/Pháp chế│     │ Ai: Điều phối  │
│ ⏱ 30-60 phút   │     │ ⏱ 1-3 giờ      │     │ ⏱ 2-10 phút     │
│ Out: Biên bản  │     │ Out: Log rời rạc│     │ Out: Quyết định │
└────────────────┘     └────────────────┘     └────────────────┘

🔴 Bottleneck chính: Bước 5 — ghép log và tái dựng timeline.
⏱ Tổng thời gian điều tra ước tính: 2-4 giờ/sự cố.
```

### Các handoff và điểm mất dấu vết

| Handoff | Thông tin có thể bị mất hoặc không đồng nhất | Rủi ro |
|---|---|---|
| CSKH -> Agent cư dân | Request ID không được truyền sang mọi hệ thống | Không liên kết được ticket với các tool call |
| Agent cư dân -> Service agent | Không rõ agent nào tạo quyết định và phiên bản prompt/model | Không xác định được nguồn gốc đề xuất |
| Agent -> Tool nghiệp vụ | Log chỉ lưu kết quả, thiếu input, policy và quyền gọi | Không biết hành động có đúng quyền hay không |
| Agent -> Nhân viên phê duyệt | Không lưu đầy đủ output trước và sau khi chỉnh sửa | Không phân biệt được lỗi của agent và thay đổi của người |
| Hệ thống -> QA/Pháp chế | Log khác định dạng, thiếu timestamp hoặc retention không đồng nhất | Điều tra kéo dài, kết luận dựa trên phỏng vấn thủ công |

### Bottleneck và business impact

- Ước tính 10-15% sự cố cần điều tra thủ công do thiếu trace liên tục.
- Mỗi sự cố mất khoảng 2-4 giờ để thu thập log, hỏi lại người xử lý và lập biên bản.
- Chi phí trực tiếp ước tính 40-90 giờ công/tháng nếu phát sinh nhiều sự cố agent.
- Khi không xác định được nguyên nhân, đội vận hành có xu hướng tắt hoặc hạn chế agent trên diện rộng, làm giảm lợi ích tự động hóa.
- Nếu sự cố liên quan đến phí, hợp đồng hoặc khiếu nại cư dân, log thiếu bằng chứng có thể làm tăng rủi ro tranh chấp và xử lý pháp lý.

## 3.2. Problem Statement — 6-field

| Field | Nội dung |
|---|---|
| **1. Actor / Operator** | Trưởng ca vận hành, QA/Control Tower, bộ phận pháp chế và nhân viên xử lý khiếu nại của Vinhomes. |
| **2. Current Workflow** | Khi có khiếu nại hoặc hành động bất thường, đội vận hành nhận request ID, mở log của các agent và hệ thống nghiệp vụ, đối chiếu timestamp, hỏi lại người phê duyệt rồi lập timeline nguyên nhân. Log hiện có thể nằm ở app cư dân, orchestration layer, tool nghiệp vụ và hệ thống phê duyệt riêng. |
| **3. Bottleneck** | Ghép các log rời rạc thành một timeline đáng tin cậy: thiếu correlation ID, phiên bản prompt/model, snapshot dữ liệu truy xuất, policy decision, tool input/output và dấu vết chỉnh sửa của con người. |
| **4. Business Impact** | Điều tra chậm 2-4 giờ/sự cố; 10-15% sự cố phải xử lý thủ công nhiều vòng; ước tính 40-90 giờ công/tháng. Rủi ro lớn hơn là không xác định được nguyên nhân gốc, không chứng minh được quyền phê duyệt và phải hạn chế agent trên toàn quy trình. |
| **5. Success Metric** | 1. Giảm thời gian tái dựng sự cố từ 2-4 giờ xuống dưới 20 phút.<br>2. 100% tool call có correlation ID, agent identity, timestamp và policy decision.<br>3. Ít nhất 90% case audit xác định được root cause hoặc đánh dấu rõ dữ kiện còn thiếu.<br>4. 100% log gốc bất biến và mọi bản xuất báo cáo có người truy cập. |
| **6. Operational Boundary** | Audit agent chỉ được đọc log đã phân quyền, tạo timeline và chỉ ra thiếu sót bằng chứng. **CẤM:** sửa/xóa log gốc, tự kết luận trách nhiệm pháp lý, thay đổi trạng thái ticket, gọi tool nghiệp vụ hoặc gửi phản hồi cho cư dân. Mọi kết luận trách nhiệm phải do người có thẩm quyền phê duyệt. |

## 3.3. Future-State Flow & AI Fit

### AI Fit

Chọn **Rule/Audit Pipeline kết hợp read-only LLM agent**, không chọn agent tự trị:

- **Rule/Audit Pipeline:** Chuẩn hóa event schema, tạo correlation ID, kiểm tra tính đầy đủ của log, bảo vệ log append-only và áp dụng RBAC.
- **Read-only Audit Agent:** Truy vấn các event đã được cấp quyền, ghép timeline, tóm tắt diễn biến và nêu khoảng trống bằng chứng.
- **LLM chỉ hỗ trợ diễn giải:** Không cho LLM quyết định trách nhiệm, thay đổi dữ liệu hoặc thực hiện hành động nghiệp vụ.

### Event schema tối thiểu

Mỗi event cần có tối thiểu:

```json
{
  "event_id": "evt-unique-id",
  "correlation_id": "request-id",
  "parent_event_id": "previous-event-id",
  "timestamp": "2026-09-12T10:00:00+07:00",
  "actor_type": "agent|human|system",
  "actor_id": "resident-agent-v1",
  "action": "read|propose|tool_call|approve|edit",
  "tool_name": "ticket_service",
  "input_hash": "sha256:...",
  "output_hash": "sha256:...",
  "policy_decision": "allow|deny|needs_review",
  "prompt_version": "prompt-v3",
  "model_version": "model-version",
  "human_approver_id": null,
  "data_classification": "internal"
}
```

`input_hash` và `output_hash` giúp kiểm tra tính toàn vẹn mà không cần lưu lại nhiều bản sao dữ liệu cá nhân nhạy cảm trong báo cáo audit.

### Future-State Workflow

```text
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│ Bước 1         │     │ Bước 2         │     │ Bước 3         │
│ Agent/human    │ ──> │ Audit pipeline │ ──> │ Policy + RBAC  │
│ tạo hành động  │     │ ghi event      │     │ kiểm tra quyền │
│                │     │ chuẩn hóa ID   │     │ truy cập       │
│                │     │ 🔵 tự động     │     │ 🔵 tự động     │
└────────────────┘     └────────────────┘     └────────────────┘
                                                        │
                                                        v
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│ Bước 6         │ <── │ Bước 5         │ <── │ Bước 4         │
│ 🟢 QA/Pháp chế │     │ 🟢 Người phụ   │     │ 🔵 Audit agent │
│ phê duyệt kết  │     │ trách review   │     │ read-only ghép │
│ luận cuối      │     │ timeline       │     │ timeline       │
│                │     │                │     │ và nêu gap     │
└────────────────┘     └────────────────┘     └────────────────┘

↩️ Fallback:
Nếu correlation ID thiếu, log lỗi schema hoặc quyền truy cập không rõ,
không suy đoán timeline. Hệ thống đánh dấu INCOMPLETE_EVIDENCE và chuyển
case cho QA thu thập thủ công.
```

### Human-in-the-loop và điểm kiểm soát

| Điểm kiểm soát | Hệ thống thực hiện | Con người chịu trách nhiệm |
|---|---|---|
| Trước khi audit agent truy vấn | Kiểm tra RBAC, mục đích truy vấn và phạm vi thời gian | QA/Trưởng ca phê duyệt case nhạy cảm |
| Khi ghép timeline | Liên kết event theo correlation ID và parent event | Người review xác nhận event có đúng case không |
| Khi phát hiện vi phạm policy | Đánh dấu event, nêu bằng chứng và mức độ thiếu dữ liệu | QA quyết định mở incident |
| Trước khi kết luận | Tạo báo cáo có nguồn event và confidence/evidence gap | QA/Pháp chế phê duyệt kết luận |
| Sau khi đóng case | Lưu báo cáo audit và access log | Data owner kiểm tra retention và quyền truy cập |

### Fallback và các trạng thái không chắc chắn

Audit agent phải trả về một trong các trạng thái rõ ràng:

- `COMPLETE`: đủ event và có thể tái dựng chuỗi hành động.
- `PARTIAL`: tái dựng được một phần, nêu rõ event còn thiếu.
- `INCOMPLETE_EVIDENCE`: không đủ correlation hoặc log có dấu hiệu không đáng tin; bắt buộc người xử lý tiếp.
- `ACCESS_DENIED`: không có quyền truy vấn; không được dùng nguồn thay thế không được phê duyệt.
- `POTENTIAL_POLICY_VIOLATION`: phát hiện hành động không khớp policy; chỉ tạo incident, không tự xử phạt hoặc kết luận trách nhiệm.

### Ranh giới an toàn chính

1. Log gốc phải append-only và lưu riêng với báo cáo do LLM tạo.
2. Audit agent chỉ dùng dữ liệu đã được RBAC cho phép và phải ghi lại chính truy vấn của nó.
3. Không đưa dữ liệu cá nhân không cần thiết vào prompt hoặc báo cáo chia sẻ rộng.
4. LLM phải trích dẫn `event_id` cho mỗi nhận định quan trọng; không có event thì ghi `evidence_missing`.
5. Không để audit agent gọi tool nghiệp vụ có side effect.
6. Người có thẩm quyền duyệt báo cáo trước khi dùng cho xử lý khiếu nại hoặc quyết định pháp lý.

## Kết quả mong đợi của Phase 3

Bài toán này phù hợp để prototype theo hướng **observability và auditability cho agentic workflow**, không phải triển khai thêm một agent có quyền hành động. Prototype đầu tiên nên kiểm tra ba năng lực: chuẩn hóa event, tái dựng timeline từ log mẫu và buộc audit agent phân biệt được bằng chứng thật với dữ kiện còn thiếu.
