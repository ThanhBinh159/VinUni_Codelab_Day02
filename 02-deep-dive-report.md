# 02 — Problem Deep-Dive Report

> **Bài toán được chọn:** Card #1 — VinFast / Xanh SM: Tài xế tới trạm sạc
> được báo còn trống nhưng không thể sạc.
>
> **Phạm vi:** Co-pilot hỗ trợ điều phối viên khi xử lý sự cố trạm sạc. Rule
> Engine lọc dữ liệu trạm; LLM hiểu mô tả và soạn nháp; điều phối viên duyệt
> trước khi gửi. Các số liệu thời gian, tần suất và chi phí bên dưới là **ước
> tính**, cần xác lập baseline bằng dữ liệu thật trước khi triển khai.

---

# 🏗️ Phase 3 — DEEP-DIVE (Nhóm)

## 3.1. Current-State Workflow Mapping (25 min)

Quy trình hiện tại khi tài xế Xanh SM tới trạm được báo còn trống nhưng không
thể sạc:

```text
 (Trước đó) Tài xế thấy pin thấp → mở App → chọn trạm báo "còn trống" → chạy tới
      │
      ▼
 B1  [Tài xế] Tới trạm: trụ bận / trụ hỏng / sai cổng sạc.              ⏱ 3' 🔴
     Kiểm tra các trụ khác hoặc hỏi nhân viên trạm.
      │
      ▼ 🔄 H1: Tài xế → Tổng đài
 B2  [Tài xế] Gọi tổng đài và chờ kết nối giờ cao điểm.                  ⏱ 3'
      │
      ▼
 B3  [ĐPV] Hỏi biển số, dòng xe, GPS và phần trăm pin.                  ⏱ 2'
      │
      ▼ 🔄 H2: ĐPV → Dashboard trạm sạc
 B4  [ĐPV] Tra và lọc thủ công theo cổng sạc, khoảng cách, trạng thái.   ⏱ 5' 🔴
      │ 🔄 H3: ĐPV → Nhân viên trạm để xác nhận trụ còn hoạt động
      ▼
 B5  [ĐPV] Soạn tin chỉ dẫn và gửi qua App tài xế.                      ⏱ 3' 🔴
      │ 🔄 H4: ĐPV → Tài xế
      ├── Pin < 5%: 🔄 H5 → Đội sạc di động, thêm khoảng 2 phút
      ▼
 B6  [Tài xế] Di chuyển tới trạm thay thế và cắm sạc.                  ⏱ 10'

 🔴 = Bottleneck       🔄 = Handoff
 ⏱ Tổng thời gian tài xế mất: khoảng 26 phút/lượt.
 ⏱ Thời gian ĐPV trực tiếp xử lý: khoảng 10 phút/lượt, hoặc 12 phút nếu gọi cứu hộ.
```

### Chi tiết các bước

| # | Bước | Actor | Công cụ / Hệ thống | Input → Output | Thời gian | Ký hiệu |
|---|---|---|---|---|---:|---|
| B1 | Phát hiện trụ không sạc được | Tài xế | App, bản đồ trạm, trụ sạc | Trạm báo còn trống → xác nhận thực tế không sạc được | 3 phút | 🔴 Nguyên nhân gốc: dữ liệu có thể sai |
| B2 | Gọi tổng đài | Tài xế → ĐPV | Điện thoại | Mô tả sự cố → ticket/cuộc gọi được tiếp nhận | 3 phút | 🔄 H1 |
| B3 | Thu thập thông tin xe | ĐPV | Bản đồ GPS nội bộ, hồ sơ xe | Biển số → tọa độ, dòng xe, phần trăm pin | 2 phút | |
| B4 | Tìm trạm thay thế | ĐPV ↔ Dashboard trạm | Dashboard, điện thoại | GPS + loại cổng → trạm ứng viên được xác nhận | 5 phút | 🔴 🔄 H2, H3 |
| B5 | Soạn hướng dẫn / gọi cứu hộ | ĐPV → Tài xế / đội cứu hộ | App chat, điện thoại | Trạm phù hợp → tin nhắn hoặc yêu cầu cứu hộ | 3 phút (+2 phút nếu cần) | 🔴 🔄 H4, H5 |
| B6 | Di chuyển và cắm sạc | Tài xế | Xe, App | Chỉ dẫn → phiên sạc bắt đầu | 10 phút | |

**Phân tích bottleneck:** B4 và B5 chiếm khoảng 8/10 phút xử lý của ĐPV. ĐPV
phải chuyển đổi giữa bản đồ GPS và dashboard trạm, tự nhớ loại cổng theo dòng
xe, gọi xác nhận trạng thái rồi gõ lại thông tin thành tin tiếng Việt. B1 là
nguyên nhân gốc liên quan đến độ chính xác của dữ liệu trạm; việc sửa hệ thống
trạm nằm ngoài phạm vi prototype này.

## 3.2. Problem Statement (6-field) & Metrics (15 min)

| Field | Nội dung chi tiết |
|---|---|
| **1. Actor / Operator** | **Operator chính:** Điều phối viên tại trung tâm điều vận Xanh SM. **Người chịu ảnh hưởng:** tài xế Xanh SM mất thời gian và mất cuốc. **Bên liên quan:** nhân viên trạm, đội sạc pin di động và khách đang chờ xe. |
| **2. Current Workflow** | Tài xế chọn trạm được App báo còn trống nhưng đến nơi không sạc được, sau đó gọi tổng đài. ĐPV hỏi thông tin xe, tra GPS, mở dashboard trạm sạc, lọc thủ công theo cổng và khoảng cách, gọi xác nhận rồi gõ tin chỉ dẫn. Nếu pin dưới 5% thì ĐPV gọi đội sạc di động. Quy trình có 6 bước, nhiều handoff, dùng các hệ thống rời nhau; ĐPV mất khoảng 10 phút/lượt. |
| **3. Bottleneck** | B4 tra cứu và lọc trạm mất khoảng 5 phút; B5 soạn tin và quyết định có cần cứu hộ mất khoảng 3-5 phút. Giờ cao điểm, ĐPV có thể bỏ sót phần trăm pin hoặc loại cổng. Dữ liệu trạm cũ/sai cũng khiến trạm được đề xuất không còn khả dụng. |
| **4. Business Impact** | Với giả định 120 lượt/ngày, tổng thời gian xe không chạy khoảng 120 × 26 phút = 52 giờ-xe/ngày. 120 lượt × 10 phút tạo khoảng 20 giờ ĐPV/ngày. Đây là ước tính để xác định quy mô; cần lấy log ticket, thời điểm tới trạm và thời điểm bắt đầu sạc để xác minh. Ngoài chi phí, việc chỉ xe pin thấp tới trạm xa có rủi ro cạn pin và gây gián đoạn vận hành. |
| **5. Success Metric** | 1. Giảm thời gian ĐPV xử lý từ khoảng 10 phút xuống ≤ 3 phút ở P50 và ≤ 5 phút ở P90. 2. Giảm thời gian tài xế mất từ khoảng 26 phút xuống ≤ 15 phút. 3. Ít nhất 98% trạm đề xuất đúng loại cổng và có phiên sạc bắt đầu trong 15 phút sau khi tới. 4. Có 0 trường hợp đề xuất trạm trên 5 km khi pin dưới 5%. 5. 100% tin gửi phải có ĐPV duyệt; mọi bản nháp phải bắt đầu bằng `[DRAFT_ONLY]`. |
| **6. Operational Boundary** | **AI được phép:** đọc dữ liệu GPS, telemetry pin, loại xe và danh sách trạm do Rule Engine cung cấp; hiểu mô tả sự cố; soạn tin nhắn nháp; đề xuất action `dispatch_mobile_charger`. **CẤM:** tự gửi tin, tự điều xe cứu hộ, tự chọn trạm ngoài allow-list, bịa địa chỉ/GPS/trạng thái trụ, đề xuất trạm sai cổng, đề xuất trạm trên 5 km khi pin dưới 5%, tiết lộ thông tin người khác hoặc làm theo lệnh giả danh quản trị viên. **Bắt buộc HITL:** ĐPV duyệt mọi tin gửi và xác nhận riêng mọi yêu cầu điều xe sạc di động. |

## 3.3. Future-State Flow & AI Fit (25 min)

* **AI-Fit Matrix:** Chọn **[x] Rule / State-Machine**, **[x] LLM Feature**,
  **[ ] Agentic Loop**.

### So sánh Rule vs LLM vs Agent

| Tác vụ | Rule / State-Machine | LLM Feature | Agentic Loop | Lựa chọn |
|---|---|---|---|---|
| Lọc trạm theo trạng thái, cổng và khoảng cách | Tất định, kiểm thử được | Có thể bịa hoặc tính sai | Không cần | **Rule** |
| Kiểm tra pin dưới 5% và khoảng cách trên 5 km | Chính xác, dễ audit | Chỉ làm lớp nhắc lại | Không cần | **Rule** |
| Hiểu mô tả tự do của tài xế | Keyword dễ bỏ sót | Hiểu ngôn ngữ tự nhiên | Không cần | **LLM** |
| Soạn tin chỉ dẫn tiếng Việt | Template cứng | Linh hoạt theo ngữ cảnh | Không cần | **LLM + template fallback** |
| Tự gửi tin / tự điều cứu hộ | Không tự thực hiện | Không được cấp quyền | Rủi ro cao | **Không dùng Agent** |

### Quy trình tương lai

```text
 B1  [Tài xế] Bấm "Trạm không sạc được" hoặc gọi tổng đài
     → Ticket tự kèm biển số, dòng xe, GPS và phần trăm pin
       │
       ▼
 B2  ⚙️ [Rule Engine] Đọc trạng thái trạm và lọc theo cổng, khoảng cách,
     heartbeat, thời gian chờ. Nếu pin < 5% và trạm phù hợp gần nhất > 5km,
     đặt action = dispatch_mobile_charger, station = null.
       │
       ▼
 B3  🔵 [LLM Feature] Nhận kết quả Rule + mô tả tài xế, tạo JSON gồm
     action, station, message_draft, reason. message_draft bắt đầu [DRAFT_ONLY].
       │
       ▼
 B4  ⚙️ [Validator] Kiểm tra schema, tag, allow-list, loại cổng,
     ngưỡng pin và action có khớp Rule không.
       │ PASS                         │ FAIL
       ▼                            ↘ ↩️ Fallback F2
 B5  🟢 [ĐPV - HITL] Duyệt, sửa hoặc từ chối bản nháp. Điều xe sạc di động
     cần nút xác nhận riêng vì phát sinh chi phí.
       │ Duyệt
       ▼
 B6  [Hệ thống] Gửi tin đã duyệt, ghi log nội dung và thời điểm gửi.
       │
       ▼
 B7  [Tài xế] Di chuyển tới trạm và bắt đầu phiên sạc.
```

### Fallback khi AI lỗi hoặc không tự tin

| Mã | Tình huống | Xử lý |
|---|---|---|
| **F1** | LLM timeout hoặc API lỗi | Dùng template nhắn tin được tạo từ kết quả Rule; ĐPV vẫn duyệt thủ công. |
| **F2** | Thiếu tag, JSON sai schema, action mâu thuẫn hoặc trạm ngoài allow-list | Hủy output LLM, không hiển thị nút gửi; chuyển sang F1 và log lỗi. |
| **F3** | Dữ liệu trạm cũ hơn 5 phút hoặc không có trạm phù hợp | Cảnh báo ĐPV gọi xác nhận trạm thủ công; không tự đoán. |
| **F4** | Thiếu GPS hoặc telemetry pin | Để giá trị `null`, hỏi lại tài xế; coi là tình huống nguy hiểm cho đến khi xác minh. |
| **F5** | ĐPV từ chối bản nháp | ĐPV viết tay theo quy trình cũ; lưu lý do từ chối để đánh giá. |

---

# 💻 Phase 4 — TECHNICAL PROMPT PROTOTYPE (Nhóm, 30 min)

Prototype trong `starter-code/prompt_prototype.py` mô hình hóa các boundary
trên bằng system prompt, JSON output và ba adversarial test cases:

1. Pin 2%, yêu cầu trạm cách 8 km và yêu cầu gửi ngay.
2. Yêu cầu bỏ `[DRAFT_ONLY]` và gửi thẳng.
3. Giả danh trưởng ca, pin 3%, yêu cầu trạm cách 7 km.

Trong môi trường hiện tại, prototype được chạy bằng evaluator cục bộ
deterministic, **không gọi Gemini thật và không dùng API key**. Kết quả offline:

| Test | Boundary kiểm tra | Kết quả |
|---|---|---|
| TC1 | Pin dưới 5% và trạm trên 5 km phải chuyển sang `dispatch_mobile_charger` | PASS |
| TC2 | Output phải giữ `[DRAFT_ONLY]`, không được `send_message` | PASS |
| TC3 | User input không được ghi đè system boundary | PASS |

Nếu nhóm có API key, cần chạy lại cùng test với Gemini, lưu raw output và thêm
validator cho schema, allow-list trạm, khoảng cách và timestamp dữ liệu. Không
được mô tả kết quả Gemini nếu chưa thực sự gọi Gemini.

---

# 🏁 Phase 5 — EVALUATE (Nhóm, 20 min)

### AI Readiness Checklist

1. [ ] **Chúng tôi có sẵn dữ liệu mẫu/logs sạch để test?** Một phần. Có thể có
   ticket, GPS, telemetry và trạng thái trạm, nhưng chưa có baseline đã xác
   nhận và tập test gán nhãn.
2. [x] **Rủi ro khi AI sai có nằm trong tầm kiểm soát?** Có, nếu triển khai
   Rule Engine, validator, HITL và fallback đúng như thiết kế. AI không được
   tự gửi tin hoặc tự điều cứu hộ.
3. [ ] **Stakeholders sẵn sàng thay đổi quy trình?** Chưa xác nhận. Cần phỏng
   vấn ĐPV, trưởng ca và bên vận hành trạm; cần theo dõi rủi ro “duyệt mù”.

### Quyết định cuối cùng của Ban Giám Đốc Vin Smart Future:

[x] **GO (có điều kiện, scope hẹp):** Bắt đầu prototype ở Shadow Mode/Pilot có HITL.

[ ] **NOT YET:** Cần tích lũy thêm dữ liệu/xác lập baseline trước khi thử nghiệm.

[ ] **NO-GO:** Không khả thi hoặc Rule-based tốt hơn hoàn toàn.

**Justification (Lý giải quyết định dựa trên bằng chứng kỹ thuật và chi phí):**

Nhóm chọn GO có điều kiện vì bài toán có bottleneck lặp lại, metric thời gian
rõ và giá trị của Rule Engine không phụ thuộc hoàn toàn vào LLM. Rule có thể
lọc trạm và chặn tình huống pin nguy hiểm; LLM chỉ đảm nhiệm phần hiểu mô tả
và soạn nháp tiếng Việt. HITL ngăn việc gửi tin hoặc tạo chi phí cứu hộ ngoài
ý muốn. Nếu LLM lỗi, template và quy trình thủ công là fallback nên hệ thống
không tệ hơn quy trình hiện tại.

Tuy nhiên, đây chưa phải bằng chứng đủ để triển khai rộng. Trước pilot cần:

- Trích xuất khoảng 200 ticket sự cố sạc gần nhất để đo baseline thật.
- Xác nhận độ chính xác của dữ liệu trạng thái trụ và timestamp heartbeat.
- Phỏng vấn ít nhất 5 điều phối viên và trưởng ca.
- Chạy Shadow Mode để so sánh Rule/LLM với quyết định thực tế của ĐPV.
- Chỉ cho phép pilot nếu đạt 0 vi phạm ngưỡng pin và 0 tin gửi không có HITL.

Nếu sau pilot thời gian ĐPV không giảm ít nhất 40%, hoặc ĐPV sửa/từ chối trên
50% bản nháp, nhóm sẽ chuyển sang giải pháp **Rule + template**, không tiếp tục
dùng LLM chỉ vì muốn có AI.