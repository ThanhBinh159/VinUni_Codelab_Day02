# Phase 1 — SCAN: Tìm kiếm cơ hội (Cá nhân)

Mảng chọn: **Vinmec**  
Bài toán ưu tiên: **Tự động trích xuất và đối chiếu hồ sơ bệnh nhân**

---

## 1. Dùng 4 Lenses để quét cơ hội AI

| # | Subsidiary | Lens | Mô tả ngắn bài toán |
|---|------------|------|---------------------|
| 1 | **Vinmec** | Lặp lại | Nhân viên tiếp nhận bệnh nhân phải nhập lại thông tin từ giấy tờ, file scan và hệ thống nhiều lần trong mỗi ca làm. |
| 2 | **Vinmec** | Tốn thời gian | Bộ phận tiếp nhận và điều dưỡng mất nhiều thời gian đối chiếu hồ sơ giữa giấy tờ, file PDF và nền tảng bệnh viện. |
| 3 | **Vinmec** | AI-upgrade | Hệ thống hiện tại phụ thuộc nhiều thao tác thủ công, khiến thời gian chờ bệnh nhân tăng và dễ sai thông tin. |
| 4 | **Vinmec** | Pain từ người khác | Bệnh nhân chờ lâu tại quầy tiếp nhận; nhân viên phải xử lý hồ sơ lặp lại và báo cáo sai lệch. |
| 5 | **Vinmec** | Lặp lại | Việc kiểm tra thiếu thông tin, sai tên, sai mã bảo hiểm và cập nhật hồ sơ diễn ra hàng ngày với khối lượng lớn. |

---

## 2. Tóm tắt nhận diện pain point

- **Vấn đề cốt lõi:** Hồ sơ bệnh nhân bị phân tán và nhập dữ liệu thủ công quá nhiều.
- **Người chịu đau:** Nhân viên tiếp nhận, điều dưỡng, bộ phận hồ sơ bệnh án.
- **Kết quả thực tế:** Thời gian chờ bệnh nhân kéo dài, tỉ lệ sai sót tăng, năng suất của đội ngũ giảm.
- **Điểm AI phù hợp:** OCR + trích xuất dữ liệu + đối chiếu tự động + cảnh báo thiếu/mâu thuẫn.

---

## 3. Lý do bài toán phù hợp với AI

Bài toán này phù hợp vì:
- Dữ liệu mang tính lặp lại và có cấu trúc tương đối rõ.
- Có nhiều bước thủ công dễ tự động hóa.
- Dễ đo lường hiệu quả bằng thời gian và tỉ lệ sai lệch hồ sơ.
- Rủi ro có thể kiểm soát bằng Human-in-the-loop (phê duyệt cuối cùng của nhân viên).
