┌──────────────────────────────────────────────────────────────
│ QUICK PROBLEM CARD #1
│ Lens: AI có thể tốt hơn + Pain từ người khác (bác sĩ quá tải)
│
│ Bài toán (1 câu): Bác sĩ CĐHA đọc hàng trăm phim X-quang ngực
│   mỗi ngày theo thứ tự FIFO, nên dễ bỏ sót tổn thương nhỏ khi
│   quá tải và phim bất thường khẩn cấp phải chờ tới lượt.
│ Công ty thành viên: [ ] VinFast  [ ] Xanh SM  [ ] Vinhomes
│                     [x] Vinmec   [ ] Khác
│
│ Ai đang đau (Actor)? Bác sĩ chẩn đoán hình ảnh (người đọc phim);
│   gián tiếp: bác sĩ lâm sàng và bệnh nhân chờ kết quả.
│
│ Workflow thủ công hiện tại (5 bước):
│   1. KTV chụp phim, đẩy lên PACS
│   ──> 2. Phim vào hàng đợi theo thời gian (FIFO), không phân
│          biệt mức độ khẩn
│   ──> 3. Bác sĩ mở phim, đọc, đối chiếu tiền sử/phim cũ
│   ──> 4. Soạn kết luận trên RIS
│   ──> 5. Trả kết quả cho bác sĩ lâm sàng
│
│ Bước nào tốn thời gian/lỗi nhất? Bước 2-3
│   (⏱ đọc + kết luận ~5-7 phút/phim; ca khẩn có thể chờ ~60 phút
│    trong hàng đợi giờ cao điểm; lỗi bỏ sót tăng cuối ca)
│ AI có thể nhảy vào hỗ trợ ở bước nào?
│   - Bước 2: chấm điểm nghi ngờ bất thường -> đẩy phim nghi
│     nặng (tràn khí màng phổi, nốt phổi, tràn dịch) lên đầu hàng.
│   - Bước 3: khoanh vùng nghi ngờ trên ảnh làm "người đọc thứ 2".
│   - AI KHÔNG tự kết luận, không trả kết quả trực tiếp cho bệnh
│     nhân; bác sĩ ký kết luận cuối (bắt buộc HITL).
│
│ Đo thành công bằng gì (Metric có số)?
│   - Độ nhạy (sensitivity) >= 95% với nhóm bất thường nghiêm
│     trọng trên tập test do bác sĩ gán nhãn.
│   - Thời gian từ lúc chụp tới lúc bác sĩ mở phim khẩn:
│     ~60 phút ──> dưới 15 phút.
│   - Tỉ lệ bỏ sót (phát hiện ở lần đọc lại/hội chẩn) giảm 30%.
│
│ Quick Architecture: [ ] No AI  [x] Rule  [ ] LLM  [ ] Agent
│   [x] Khác: Computer Vision (Deep Learning trên ảnh) + Rule xếp
│   ưu tiên hàng đợi. KHÔNG phải bài toán LLM.
│   ⚠️ Rủi ro: cần dữ liệu ảnh gán nhãn lớn, cấp phép thiết bị y
│   tế, rủi ro pháp lý khi sai -> nhiều khả năng NOT YET.
└──────────────────────────────────────────────────────────────
```

### Card #2 — VinFast / Xanh SM: Gợi ý trạm sạc thực sự còn trống (từ Scan #3)

```text
┌──────────────────────────────────────────────────────────────
│ QUICK PROBLEM CARD #2
│ Lens: Pain từ người khác (tài xế phàn nàn)
│
│ Bài toán (1 câu): Tài xế Xanh SM chạy tới trạm sạc theo bản đồ
│   nhưng đến nơi trụ đã có xe khác sạc hoặc bị hỏng, phải gọi
│   tổng đài và đi tìm trạm khác trong khi pin tiếp tục tụt.
│ Công ty thành viên: [x] VinFast  [x] Xanh SM  [ ] Vinhomes
│                     [ ] Vinmec   [ ] Khác
│
│ Ai đang đau (Actor)? Tài xế Xanh SM (mất thời gian, mất cuốc);
│   Điều phối viên tổng đài (xử lý cuộc gọi thủ công).
│
│ Workflow thủ công hiện tại (5 bước):
│   1. Tài xế thấy pin thấp, mở app xem bản đồ trạm sạc
│   ──> 2. Chọn trạm gần nhất, chạy tới
│   ──> 3. Đến nơi: trụ bận/hỏng/không đúng cổng sạc
│   ──> 4. Gọi tổng đài; ĐPV tra Dashboard trạm, gọi hỏi trạm
│   ──> 5. ĐPV nhắn tin chỉ trạm khác hoặc gọi cứu hộ nếu pin
│          quá thấp
│
│ Bước nào tốn thời gian/lỗi nhất? Bước 3-5
│   (⏱ tài xế mất ~20-30 phút/lượt; ĐPV tra cứu + soạn tin
│    ~8-10 phút/cuộc gọi)
│ AI có thể nhảy vào hỗ trợ ở bước nào?
│   - Trước bước 2: Rule lọc trụ theo trạng thái realtime, loại
│     cổng sạc phù hợp dòng xe, khoảng cách, thời gian còn lại
│     của phiên sạc đang chạy.
│   - Bước 4-5: LLM soạn NHÁP tin chỉ dẫn cho ĐPV duyệt (gắn
│     [DRAFT_ONLY]); pin < 5% và trạm > 5km -> đề xuất điều xe
│     sạc pin di động (dispatch_mobile_charger).
│
│ Đo thành công bằng gì (Metric có số)?
│   - Tỉ lệ "đến trạm nhưng không sạc được" giảm xuống dưới 5%.
│   - Thời gian ĐPV xử lý 1 cuộc gọi: ~10 phút ──> dưới 3 phút.
│   - 0 trường hợp gợi ý trạm > 5km khi pin < 5% (test ranh giới).
│
│ Quick Architecture: [ ] No AI  [x] Rule  [x] LLM  [ ] Agent
│   Rule làm phần lọc/tính toán trạm (cần chính xác tuyệt đối);
│   LLM chỉ soạn tin nhắn tiếng Việt. Không cần Agent vì quy
│   trình cố định.
└──────────────────────────────────────────────────────────────
```

### Card #3 — Xanh SM: Xử lý khiếu nại khách quên đồ trên xe (từ Scan #4)

```text
┌──────────────────────────────────────────────────────────────
│ QUICK PROBLEM CARD #3
│ Lens: Tốn thời gian + Lặp lại
│
│ Bài toán (1 câu): Khi khách báo quên đồ trên xe, CSKH phải tra
│   thủ công lịch sử chuyến, gọi tài xế nhiều lần và hẹn cách trả
│   đồ, mỗi vụ kéo dài và dễ tra nhầm chuyến.
│ Công ty thành viên: [ ] VinFast  [x] Xanh SM  [ ] Vinhomes
│                     [ ] Vinmec   [ ] Khác
│
│ Ai đang đau (Actor)? Nhân viên CSKH Xanh SM; khách hàng (lo mất
│   đồ); tài xế (bị gọi khi đang chạy cuốc).
│
│ Workflow thủ công hiện tại (5 bước):
│   1. Khách gọi hotline/chat, mô tả món đồ, giờ đi, điểm đón/trả
│   ──> 2. CSKH tra lịch sử chuyến theo SĐT + khung giờ để tìm
│          đúng chuyến và tài xế
│   ──> 3. Gọi tài xế xác nhận (thường không nghe vì đang chạy)
│   ──> 4. Thống nhất cách trả: tài xế quay lại / gửi hub / khách
│          tới lấy
│   ──> 5. Cập nhật ticket, báo lại khách
│
│ Bước nào tốn thời gian/lỗi nhất? Bước 2-3
│   (⏱ ~8-10 phút/lượt; tổng một vụ ~20 phút; dễ nhầm chuyến khi
│    khách đi nhiều chuyến trong ngày hoặc nhớ sai giờ)
│ AI có thể nhảy vào hỗ trợ ở bước nào?
│   - Bước 1-2: LLM trích xuất lời khách thành JSON (món đồ, khung
│     giờ, điểm đón/trả) -> code query API lịch sử chuyến -> trả
│     danh sách chuyến ứng viên cho CSKH chọn.
│   - Bước 3: LLM soạn NHÁP tin nhắn in-app gửi tài xế, CSKH duyệt.
│   - CẤM: lộ SĐT tài xế cho khách, cam kết bồi thường, khẳng
│     định "đã tìm thấy đồ" khi tài xế chưa xác nhận.
│
│ Đo thành công bằng gì (Metric có số)?
│   - Thời gian xử lý 1 ticket: ~20 phút ──> dưới 7 phút.
│   - Xác định đúng chuyến ngay lần tra đầu >= 95%.
│   - Tỉ lệ trả đồ thành công trong 24h tăng 20%.
│
│ Quick Architecture: [ ] No AI  [x] Rule  [x] LLM  [ ] Agent
│   Rule/query lo phần tra chuyến; LLM chỉ trích xuất và soạn
│   nháp. ⚠️ Phản biện: nếu thêm nút "Báo quên đồ" ngay trong
│   lịch sử chuyến của app, khách tự chọn đúng chuyến -> phần lớn
│   giải quyết bằng UX + Rule, không cần AI.
└──────────────────────────────────────────────────────────────
```

### 📊 So sánh nhanh 3 card

| Tiêu chí | Card #1 X-quang | Card #2 Trạm sạc | Card #3 Quên đồ |
|---|---|---|---|
| Tần suất | Rất cao (hàng trăm phim/ngày) | Cao (hằng ngày, giờ cao điểm) | Trung bình |
| Rủi ro khi AI sai | Rất cao (sức khoẻ, pháp lý) | Trung bình (kiểm soát bằng HITL + ngưỡng pin) | Thấp |
| Dữ liệu sẵn có | Cần gán nhãn chuyên gia | Có (API trạng thái trụ, GPS xe) | Có (lịch sử chuyến, ticket) |
| Phù hợp LLM | Không (Computer Vision) | Một phần (soạn tin) | Một phần (trích xuất + soạn tin) |
| Đề xuất | NOT YET | **Ưu tiên Deep-Dive** | Cân nhắc giải bằng UX/Rule trước |
