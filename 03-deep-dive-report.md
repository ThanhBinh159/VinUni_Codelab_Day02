# Phase 3 — DEEP-DIVE: Báo cáo phân tích sâu (Nhóm)

Mảng chọn: **Vinmec**  
Bài toán: **Tự động trích xuất và đối chiếu hồ sơ bệnh nhân**

---

## 1. Current-State Workflow Mapping

```text
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Bước 1       │     │ Bước 2       │     │ Bước 3       │     │ Bước 4       │
│ Bệnh nhân    │     │ Nhân viên    │     │ Đối chiếu    │     │ Kiểm tra     │
│ nộp hồ sơ    │ ──→ │ đọc & ghi    │ ──→ │ thông tin    │ ──→ │ thiếu/sai    │
│              │     │ nhận hồ sơ   │     │ giữa nguồn   │     │ và nhập lại  │
│ Ai: Tiếp nhận│     │ Ai: Tiếp nhận│     │ Ai: Tiếp nhận│     │ Ai: Tiếp nhận│
│ ⏱ 2 phút     │     │ ⏱ 4 phút    │     │ ⏱ 6 phút 🔴 │     │ ⏱ 5 phút 🔴 │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
         │                                                       │
         ▼                                                       ▼
┌──────────────┐                                         ┌──────────────┐
│ Bước 5       │                                         │ Handoff      │
│ Chuyển hồ sơ │                                         │ Hồ sơ được   │
│ cho bác sĩ   │                                         │ lưu vào hệ   │
│ hoặc điều dưỡng│                                       │ thống bệnh án│
│ Ai: Khám     │                                         │ Ai: Hệ thống │
│ ⏱ 3 phút    │                                         │ ⏱ 1 phút    │
└──────────────┘                                         └──────────────┘

🔴 = Bottleneck
⏱ Tổng thời gian xử lý thủ công trung bình: 20-30 phút/lượt hồ sơ
```

**Nhận xét:** Điểm nghẽn nằm ở bước đối chiếu và cập nhật hồ sơ, do dữ liệu từ nhiều nguồn và cần nhập lại nhiều lần.

---

## 2. Problem Statement (6-field)

| Field | Nội dung |
|---|---|
| **1. Actor / Operator** | Nhân viên tiếp nhận, điều dưỡng và bộ phận hồ sơ bệnh án tại Vinmec. |
| **2. Current Workflow** | Bệnh nhân mang hồ sơ giấy hoặc file scan đến quầy tiếp nhận. Nhân viên đọc thông tin, so khớp với dữ liệu bệnh án trong hệ thống, nhập lại thủ công nếu thiếu/sai, rồi chuyển cho bác sĩ hoặc điều dưỡng tiếp theo. |
| **3. Bottleneck** | Bước đối chiếu và nhập dữ liệu thủ công là chậm và dễ sai, vì dữ liệu bệnh nhân phân tán giữa giấy tờ, file PDF, hệ thống bảo hiểm và phần mềm bệnh viện. |
| **4. Business Impact** | Mỗi lượt hồ sơ mất 8–12 phút xử lý thủ công, khiến bệnh nhân chờ lâu, đội ngũ tiếp nhận bị quá tải, và có khoảng 5–8% hồ sơ cần xử lý lại. Giả định một ca làm 200 bệnh nhân, tổn thất ước tính 20–30 giờ công/ngày cho bộ phận tiếp nhận. |
| **5. Success Metric** | Giảm thời gian tiếp nhận từ 10 phút xuống còn dưới 4 phút; giảm tỉ lệ hồ sơ cần xử lý lại từ 8% xuống dưới 2%; tăng tỷ lệ hồ sơ được đối chiếu tự động lên 85%. |
| **6. Operational Boundary** | AI được phép trích xuất dữ liệu từ hồ sơ giấy/scan, đối chiếu với hệ thống, gợi ý trường thiếu/mâu thuẫn, và tạo bản nháp dữ liệu cho nhân viên xác nhận. AI tuyệt đối không được tự động cập nhật hồ sơ bệnh án mà không có phê duyệt của người thật; không được tự quyết định lâm sàng hoặc thay đổi thông tin bảo hiểm mà không kiểm tra. |

---

## 3. Future-State Flow & AI Fit

### AI Fit
- [x] Rule / State-Machine
- [x] LLM Feature
- [ ] Agentic Loop

### Future-State Flow

```text
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Bước 1       │     │ Bước 2       │     │ Bước 3       │     │ Bước 4       │
│ Bệnh nhân    │     │ 🔵 AI OCR &  │     │ 🔵 Rule kiểm │     │ 🟢 Nhân viên │
│ nộp hồ sơ    │ ──→ │ trích xuất   │ ──→ │ tra và đối   │ ──→ │ phê duyệt   │
│              │     │ dữ liệu      │     │ chiếu dữ liệu│     │ và lưu hồ sơ│
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                                                                  │
                                                                  ▼
                                                           ↩️ Fallback:
                                                           Nếu dữ liệu mờ / mâu thuẫn,
                                                           chuyển sang review thủ công.
```

### AI Step
- OCR và trích xuất thông tin từ hồ sơ giấy / PDF / ảnh scan.
- So khớp thông tin bệnh nhân với hệ thống bệnh viện.
- Gợi ý các trường thiếu/sai và cảnh báo dữ liệu mâu thuẫn.

### Human Step (HITL)
- Nhân viên tiếp nhận xác nhận dữ liệu quan trọng.
- Kiểm tra hồ sơ có rủi ro cao hoặc thông tin bảo hiểm không rõ.

### Fallback
- Nếu tài liệu quá mờ, bị mất góc, không đủ thông tin, hệ thống sẽ dừng tự động hóa và chuyển sang người xử lý thủ công.

---

## 4. Evaluate

### AI Readiness Checklist
1. [x] Có sẵn dữ liệu mẫu hồ sơ bệnh nhân và dữ liệu nhập liệu cũ.
2. [x] Rủi ro khi AI sai có thể kiểm soát nhờ Human-in-the-loop.
3. [x] Stakeholders sẵn sàng thử nghiệm ở phạm vi hẹp trước khi mở rộng.

### Quyết định cuối cùng của Ban Giám Đốc Vin Smart Future
[ ] **GO (Bắt đầu xây dựng Prototype)**  
[x] **NOT YET (Cần tích lũy thêm dữ liệu/xác lập baseline)**  
[ ] **NO-GO**

**Justification:**  
Bài toán này có giá trị rõ ràng và dễ đo lường, nhưng để triển khai an toàn, cần có dữ liệu mẫu chất lượng cao và quy trình review người thật rõ ràng. Đặc biệt với dữ liệu y tế, ai sai có thể gây hậu quả nghiêm trọng. Vì vậy, nên bắt đầu bằng prototype hẹp ở 1–2 khoa và triển khai theo từng giai đoạn.

---

## 5. Kết luận

Bài toán **Tự động trích xuất và đối chiếu hồ sơ bệnh nhân** là một cơ hội AI có tiềm năng thực tế, đáng giá về hiệu quả vận hành và có thể đo lường bằng metric rõ ràng. Với đặc thù y tế, cần ưu tiên độ an toàn, ranh giới vận hành và tiêu chuẩn phê duyệt của con người.
