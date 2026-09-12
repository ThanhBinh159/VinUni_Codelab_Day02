01-Problem Scan — Tìm kiếm Cơ hội AI cho Vin Smart Future

> **Người thực hiện:** Nguyễn Thị Minh Tiến
> **MSSV:** 2A202602997
> **Khối nghiệp vụ:** VinFast After-Sales & Customer Service
> **Ngày hoàn thành:** 12/9/2026

---

## 🔍 Phase 1 — SCAN: Quét cơ hội AI

Sử dụng **4 Lenses** để quét vận hành của các công ty thành viên Vingroup và tìm bài toán thực tế có thể tối ưu bằng AI.

### 4 Lenses tìm bài toán:

| Lens                                                | Ý nghĩa                                     | Câu hỏi gợi mở                                                     |
| --------------------------------------------------- | --------------------------------------------- | ---------------------------------------------------------------------- |
| **Lặp lại (Repetitive)**                    | Tác vụ lặp đi lặp lại nhiều lần/ngày | Có tác vụ nào phải làm đi làm lại mỗi ngày?                 |
| **Tốn thời gian (Time-consuming)**          | Ngốn thời gian xử lý thủ công           | Có bước nào mất >5 phút cho mỗi lần xử lý?                   |
| **AI có thể tốt hơn (AI-upgrade)**        | Dịch vụ hiện tại chậm/rập khuôn        | Chatbot/hệ thống hiện tại có thể thông minh hơn?               |
| **Pain từ người khác (Stakeholder Pain)** | Bottleneck gây phàn nàn                    | Khách hàng/nhân viên thường xuyên phàn nàn về vấn đề gì? |

---

### 📋 Bảng quét cơ hội (Tối thiểu 5 bài toán)

| #           | Công ty           | Lens                             | Mô tả bài toán                                                                                                                                                                                                                                                                                                                                                      | Tác vụ thủ công hiện tại                                                  | Ước tính thời gian/chi phí             |
| ----------- | ------------------ | -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------- |
| **1** | **VinFast**  | **AI-upgrade**             | **Sàng lọc & Phân loại sự cố kỹ thuật xe điện (EV Diagnostic Triage):** Khách hàng mô tả lỗi xe bằng tiếng Việt tự do ("xe kêu lọc cọc", "báo rùa vàng sạc không vào"). CSKH mất 25 phút tra cứu sổ tay TSB và gọi Trưởng xưởng để phân loại sơ bộ; tỉ lệ chẩn đoán sai lệch ban đầu lên tới **28%**. | CSKH phỏng vấn triệu chứng → Tra TSB/OBD → Gọi Master Tech → Nhập DMS  | 25 phút/lượt; ~1,200 ticket/ngày        |
| **2** | **VinFast**  | **Lặp lại**              | **Đối soát dữ liệu sạc điện đối tác:** Nhân viên đối soát thủ công hàng chục nghìn phiên sạc giữa log trạm sạc V-GREEN với dữ liệu billing và chỉ số đo đếm EVN hằng tuần, dễ gây sai lệch công nợ.                                                                                                                     | Mở Excel → Ghép dữ liệu → Đối chiếu từng dòng → Ghi nhận sai lệch | 4-6 giờ/tuần                              |
| **3** | **Vinhomes** | **Tốn thời gian**        | **Phân loại & Điều hướng phản ánh cư dân:** Ban quản lý nhận hàng trăm phản ánh mỗi ngày (mất nước, điều hòa hỏng, đỗ xe sai). CSKH đọc và phân loại thủ công mất 4-6 tiếng/ngày, dẫn đến trễ SLA phản hồi.                                                                                                           | Đọc phản ánh → Phân loại thủ công → Chuyển email đến BQL           | 4-6 giờ/ngày; tỉ lệ phân loại sai 15% |
| **4** | **Vinmec**   | **Pain từ người khác** | **Soạn thảo tóm tắt hồ sơ xuất viện (Discharge Summary):** Bác sĩ lâm sàng mất 25-30 phút/bệnh nhân để tổng hợp xét nghiệm, phác đồ điều trị và viết hướng dẫn tái khám, gây quá tải văn bản hành chính.                                                                                                                | Đọc hồ sơ EMR → Viết tóm tắt → Điều chỉnh ngôn ngữ                | 25 phút/bệnh nhân; ~50 bệnh nhân/ngày |
| **5** | **Vinpearl** | **Tốn thời gian**        | **Bóc tách email đặt phòng khách đoàn B2B:** Sales/Reservation phải đọc email đặt phòng phức tạp từ công ty lữ hành, tra cứu tồn kho thủ công trên Opera PMS mất 30 phút/đoàn.                                                                                                                                                       | Đọc email → Trích xuất thủ công → Tra PMS → Báo giá                  | 30 phút/đoàn; bỏ sót 30% khách đoàn |

---

## 🃏 Phase 2 — QUICK-ASSESS: 3 Quick Problem Cards

Chọn **3 bài toán tiềm năng nhất** từ bảng SCAN để phân tích chi tiết.

---

### 🎯 Card #1: VinFast — EV Diagnostic Triage & Workshop Routing

```
┌─────────────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                                               │
│                                                                     │
│ Bài toán (1 câu): Khách hàng mô tả lỗi xe điện VinFast bằng     │
│ tiếng Việt tự do; CSKH và xưởng mất 25 phút để xác định mã lỗi │
│ sơ bộ, mức độ nguy cấp và khoang cầu nâng phù hợp.              │
│                                                                     │
│ Công ty: [x] VinFast  [ ] Xanh SM  [ ] Vinhomes                   │
│                      [ ] Vinmec   [ ] Khác                         │
│                                                                     │
│ Ai đang đau (Actor)?                                                │
│   • Khách hàng sở hữu xe điện (lo lắng, mất an toàn, chờ lâu)    │
│   • Nhân viên CSKH Hotline & Cố vấn Dịch vụ xưởng (quá tải)      │
│   • Master Tech xưởng bị gián đoạn sửa chữa để hỗ trợ hotline    │
│                                                                     │
│ Workflow thủ công hiện tại (5 bước):                               │
│   1. Nhận cuộc gọi/ticket từ khách hàng                           │
│   → 2. Phỏng vấn gạn lọc triệu chứng bằng điện thoại           │
│   → 3. Tra cứu thủ công sổ tay TSB/mã OBD-II                    │
│   → 4. Gọi điện thoại nội bộ hỏi Master Tech 🔄 HANDOFF         │
│   → 5. Lên phiếu hẹn DMS / Điều cứu hộ khẩn cấp                │
│                                                                     │
│ Bước tốn thời gian/lỗi nhất: Bước 3 & 4 (⏱ 14 phút) 🔴         │
│ AI có thể nhảy vào ở bước nào?                                    │
│   → Bước 2-4: Tự động bóc tách triệu chứng → Semantic Search TSB │
│   → Gán Severity → Draft Triage Card cho Cố vấn Dịch vụ          │
│                                                                     │
│ Đo thành công bằng gì (Metric có số)?                              │
│   • Giảm thời gian tiếp nhận: 25 phút → dưới 4 phút (giảm 84%) │
│   • Độ chính xác phân loại phân hệ kỹ thuật: > 92%               │
│   • Phát hiện 100% ca nguy hiểm pin/phanh để kích hoạt cứu hộ   │
│                                                                     │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent        │
│   (LLM Feature với Structured Output + Semantic RAG)               │
└─────────────────────────────────────────────────────────────────────┘
```

---

### 🎯 Card #2: Vinhomes — Smart Resident Complaint Router

```
┌─────────────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #2                                               │
│                                                                     │
│ Bài toán (1 câu): Cư dân gửi hàng trăm phản ánh hỗn hợp qua     │
│ App Vinhomes Resident; nhân viên BQL mất 4-6 tiếng/ngày để đọc,  │
│ gán nhãn và chuyển tiếp thủ công đến từng tổ chức năng.         │
│                                                                     │
│ Công ty: [ ] VinFast  [ ] Xanh SM  [x] Vinhomes                    │
│                      [ ] Vinmec   [ ] Khác                         │
│                                                                     │
│ Ai đang đau (Actor)?                                                │
│   • Cư dân khu đô thị Vinhomes (bức xúc vì phản ánh chậm xử lý) │
│   • Nhân viên Chăm sóc Cư dân Ban Quản lý (ngập trong ticket)     │
│   • Ban Quản lý từng tòa nhà (nhận phản ánh sai đối tượng)       │
│                                                                     │
│ Workflow thủ công hiện tại (4 bước):                               │
│   1. Nhận phản ánh từ App Vinhomes Resident                       │
│   → 2. Đọc & phân loại thủ công theo loại sự cố                 │
│   → 3. Chọn bộ phận tiếp nhận phù hợp                          │
│   → 4. Gõ phản hồi xác nhận và chuyển tiếp email               │
│                                                                     │
│ Bước tốn thời gian/lỗi nhất: Bước 2 & 3 (⏱ 6-8 phút/phản ánh)  │
│ AI có thể nhảy vào ở bước nào?                                    │
│   → Bước 2-3: Tự động đọc hiểu văn bản tiếng Việt, phân loại   │
│   và định tuyến tự động đến đúng tổ đội/bộ phận                 │
│                                                                     │
│ Đo thành công bằng gì (Metric có số)?                              │
│   • Giảm thời gian điều phối ticket: 4 giờ → dưới 5 phút        │
│   • Độ chính xác định tuyến đúng bộ phận: > 95%                   │
│   • Điểm satisfaction cư dân: Tăng từ 3.2 → 4.0/5.0              │
│                                                                     │
│ Quick Architecture: [ ] No AI  [x] Rule + LLM  [ ] Agent           │
│   (LLM phân loại nội dung + Rule điều hướng theo tòa nhà)        │
└─────────────────────────────────────────────────────────────────────┘
```

---

### 🎯 Card #3: Vinpearl — B2B Group Booking Email Parser

```
┌─────────────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #3                                               │
│                                                                     │
│ Bài toán (1 câu): Đội ngũ Sales Vinpearl mất 30 phút/đoàn để     │
│ bóc tách yêu cầu đặt phòng số lượng lớn từ email/file của đối tác│
│ du lịch để kiểm tra quỹ phòng trống trên Opera PMS.               │
│                                                                     │
│ Công ty: [ ] VinFast  [ ] Xanh SM  [ ] Vinhomes                     │
│                      [ ] Vinmec   [x] Khác: Vinpearl               │
│                                                                     │
│ Ai đang đau (Actor)?                                                │
│   • Chuyên viên Đặt phòng (Reservation Agent) & Sales B2B         │
│   • Đại lý du lịch đối tác (chờ xác nhận phòng mất 6-12 tiếng)  │
│                                                                     │
│ Workflow thủ công hiện tại (4 bước):                               │
│   1. Mở email & file đính kèm từ công ty lữ hành                 │
│   → 2. Trích xuất thủ công cấu trúc phòng, ngày check-in/out    │
│   → 3. Mở Opera PMS tra cứu tồn kho phòng trống                  │
│   → 4. Draft email báo giá và gửi lại cho đối tác                │
│                                                                     │
│ Bước tốn thời gian/lỗi nhất: Bước 2 & 3 (⏱ 20 phút/đoàn) 🔴      │
│ AI có thể nhảy vào ở bước nào?                                    │
│   → Bước 2: Bóc tách JSON cấu trúc để gọi thẳng API kiểm tra    │
│   tồn kho Opera PMS tự động                                       │
│                                                                     │
│ Đo thành công bằng gì (Metric có số)?                              │
│   • Giảm thời gian trích xuất & kiểm tra: 30 phút → dưới 3 phút  │
│   • Tỉ lệ bóc tách chính xác số lượng khách & ngày nghỉ: > 98%  │
│   • Thời gian phản hồi đại lý: Giảm từ 12 giờ → 30 phút         │
│                                                                     │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent        │
│   (LLM Feature với Structured JSON Output + API Integration)       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Tổng hợp so sánh 3 Cards

| Tiêu chí                       | Card#1 (VinFast)                         | Card#2 (Vinhomes)           | Card#3 (Vinpearl)   |
| -------------------------------- | ---------------------------------------- | --------------------------- | ------------------- |
| **Độ khẩn cấp**        | 🔴 Cao (an toàn xe)                     | 🔴 Cao (SLA cư dân)       | 🟡 Trung bình      |
| **Tác động kinh doanh** | Trực tiếp đến NPS xe điện          | Ảnh hưởng brand Vinhomes | Tăng doanh số B2B |
| **Rủi ro khi AI sai**     | **Nghiêm trọng** (xe điện/pin) | Thấp (chuyển tiếp sai)   | Trung bình         |
| **Độ phức tạp AI**     | Cao (RAG + Safety Rules)                 | Thấp (Rule + LLM)          | Trung bình (API)   |
| **Metric rõ ràng?**      | ✅ Có (25→4 min, >92%)                 | ✅ Có (4h→5min, >95%)     | ✅ Có (30→3min)   |
| **Khả thi demo?**         | ✅ Có                                   | ✅ Có                      | ✅ Có              |
| **Compliance đặc biệt** | ⚠️ An toàn kỹ thuật cao             | ❌ Không                   | ❌ Không           |

---

## 🗳️ Quyết định lựa chọn của nhóm

**Nhóm chọn Card #1 (VinFast — EV Diagnostic Triage & Workshop Routing)** làm bài toán Deep-Dive chính vì:

| Lý do                                       | Chi tiết                                                                                                              |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **1. Tính chiến lược**             | Dịch vụ hậu mãi xe điện VinFast ảnh hưởng trực tiếp đến NPS và tỉ lệ quay lại của khách hàng       |
| **2. Quy mô tác động**             | ~1,200 ticket/ngày = 300 giờ lãng phí/ngày → ROI cực lớn                                                       |
| **3. Ranh giới vận hành rõ ràng** | Liên quan an toàn tính mạng → Cơ hội showcase AI Safety & HITL                                                  |
| **4. Bộ dữ liệu sẵn có**          | 100,000+ tickets lịch sử + TSB số hóa + OBD-II codes                                                               |
| **5. Loại bỏ Cards khác**           | Card#2 (Vinhomes): Giải quyết tốt bằng Rule nhẹ Card #3 (Vinpearl): Phụ thuộc API bên thứ ba + tính mùa vụ |

---

## ⚠️ Lưu ý quan trọng khi triển khai Card #1

| Yếu tố                        | Xử lý                                                                           |
| ------------------------------- | --------------------------------------------------------------------------------- |
| **An toàn tuyệt đối** | AI chỉ đưa ra **gợi ý nháp** — bắt buộc Cố vấn Dịch vụ duyệt |
| **Pin cao áp / Phanh**   | Cấm AI trấn an "an toàn tiếp tục chạy" — chuyển cứu hộ bắt buộc       |
| **Bảo hành**            | Cấm AI cam kết đền bù/bảo hành miễn phí                                  |
| **Fallback**              | Khi confidence < 70% → chuyển Master Tech xưởn                                |
