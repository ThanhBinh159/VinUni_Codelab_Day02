# Phase 2 — QUICK-ASSESS: 3 Quick Problem Cards (Cá nhân)

Mảng chọn: **Vinmec**

---

## Chọn top 3 bài toán

### Quick Problem Card #1 — Tự động trích xuất và đối chiếu hồ sơ bệnh nhân

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                                       │
│                                                             │
│ Bài toán: Tự động trích xuất và đối chiếu thông tin bệnh   │
│ nhân từ hồ sơ giấy, file scan và dữ liệu số.               │
│ Công ty thành viên: [x] Vinmec                              │
│                                                             │
│ Ai đang đau (Actor)? Nhân viên tiếp nhận, điều dưỡng, bộ   │
│ phận hồ sơ bệnh án                                          │
│                                                             │
│ Workflow thủ công hiện tại (3-5 bước):                     │
│   1. Bệnh nhân nộp hồ sơ giấy / file scan                  │
│   → 2. Nhân viên đọc và đối chiếu thông tin cá nhân        │
│   → 3. Nhập lại dữ liệu vào hệ thống bệnh viện             │
│   → 4. Kiểm tra thiếu/thừa thông tin                       │
│   → 5. Gửi hồ sơ lại nếu phát hiện sai lệch                │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Đối chiếu và nhập dữ liệu │
│ thủ công (⏱ 8-12 phút/bệnh nhân/lượt)                      │
│ AI có thể nhảy vào hỗ trợ ở bước nào? OCR + trích xuất dữ  │
│ liệu + đối chiếu tự động + cảnh báo mâu thuẫn               │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                      │
│ Giảm thời gian tiếp nhận từ 10 phút xuống dưới 4 phút;     │
│ giảm sai sót hồ sơ từ 8% xuống dưới 2%.                    │
│                                                             │
│ Quick Architecture: [ ] No AI  [x] Rule  [x] LLM  [ ] Agent │
└─────────────────────────────────────────────────────────────┘
```

---

### Quick Problem Card #2 — Lập lịch khám bác sĩ theo chuyên khoa

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #2                                       │
│                                                             │
│ Bài toán: Tối ưu lịch khám bác sĩ và ca làm theo chuyên    │
│ khoa, số lượng bệnh nhân và mức độ khẩn cấp.               │
│ Công ty thành viên: [x] Vinmec                              │
│                                                             │
│ Ai đang đau (Actor)? Điều phối viên, trưởng khoa, bác sĩ   │
│                                                             │
│ Workflow thủ công hiện tại (3-5 bước):                     │
│   1. Nhận lịch hẹn từ kênh đặt lịch                        │
│   → 2. Kiểm tra lịch làm của bác sĩ                        │
│   → 3. Sắp xếp lịch khám theo chuyên khoa                  │
│   → 4. Điều chỉnh khi bệnh nhân đổi giờ                    │
│   → 5. Gửi xác nhận lại cho bệnh nhân                      │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Sắp xếp lại lịch khi có   │
│ sự cố hoặc cao điểm (⏱ 30-60 phút/ngày/khoa)               │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Dự báo nhu cầu và    │
│ tối ưu lịch khám theo ràng buộc ca làm và ưu tiên           │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                      │
│ Giảm thời gian chờ khám 20-30%; tăng năng suất bác sĩ 10-15%; │
│ giảm số ca hoãn lịch xuống dưới 5%.                         │
│                                                             │
│ Quick Architecture: [ ] No AI  [x] Rule  [ ] LLM  [ ] Agent │
└─────────────────────────────────────────────────────────────┘
```

---

### Quick Problem Card #3 — Hỗ trợ trả lời câu hỏi bệnh nhân qua Zalo/Hotline

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #3                                       │
│                                                             │
│ Bài toán: Phân loại và trả lời các câu hỏi thường gặp của  │
│ bệnh nhân về lịch khám, thủ tục và hướng dẫn sau khám.     │
│ Công ty thành viên: [x] Vinmec                              │
│                                                             │
│ Ai đang đau (Actor)? Tư vấn viên, CSKH, nhân sự phòng khám │
│                                                             │
│ Workflow thủ công hiện tại (3-5 bước):                     │
│   1. Bệnh nhân gửi câu hỏi qua hotline / Zalo / website    │
│   → 2. Tư vấn viên đọc tin nhắn và phân loại câu hỏi       │
│   → 3. Trả lời theo template thủ công                       │
│   → 4. Chuyển tiếp cho nhân sự chuyên trách nếu cần        │
│   → 5. Ghi log nội dung để dùng lại sau này                  │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Phân loại tin nhắn và trả │
│ lời lặp lại (⏱ 4-7 phút/câu hỏi)                           │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Trích xuất intent,   │
│ draft câu trả lời và chuyển tiếp lên người thật nếu cần     │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                      │
│ Giảm thời gian phản hồi trung bình từ 8 phút xuống dưới 2 phút; │
│ tăng tỷ lệ giải quyết tức thời 30-40%.                     │
│                                                             │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent │
└─────────────────────────────────────────────────────────────┘
```

---

## Quyết định lựa chọn bài toán Deep-Dive

Nhóm chọn bài toán **Card #1 — Tự động trích xuất và đối chiếu hồ sơ bệnh nhân** vì:
- xác định rõ pain point và người chịu đau,
- dữ liệu có thể thu thập và đánh giá được,
- dễ đo thành công bằng thời gian và tỷ lệ sai sót,
- phù hợp với model AI có trọng tâm là OCR + Rule + HITL.
