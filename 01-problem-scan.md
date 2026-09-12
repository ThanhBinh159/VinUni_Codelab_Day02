# 01 — Problem Scan & Quick Cards (Vin Smart Future)

> Phase 1 (SCAN) và Phase 2 (QUICK-ASSESS) của Lab 02: AI Product Scoping.
> Các con số thời gian/tỉ lệ là **ước tính** để scoping, cần xác lập baseline
> thực tế bằng log vận hành, phỏng vấn actor và dữ liệu được kiểm chứng.

---

# 🔍 Phase 1 — SCAN

Hãy sử dụng **4 Lenses** dưới đây để quét qua hoạt động vận hành của các công ty thành viên Vingroup. Ghi lại **ít nhất 5 bài toán/bottleneck** thực tế.

### 4 Lenses tìm bài toán AI cho Vingroup:
1. **Lặp lại (Repetitive):** Tác vụ lặp đi lặp lại nhiều lần hằng ngày.
2. **Tốn thời gian (Time-consuming):** Tác vụ ngốn thời gian xử lý thủ công.
3. **AI có thể tốt hơn (AI-upgrade):** Dịch vụ hiện tại còn chậm hoặc phản hồi rập khuôn.
4. **Pain từ người khác (Stakeholder Pain):** Bottleneck khiến khách hàng hoặc nhân viên phàn nàn.

### 📝 List bài toán của tôi:
| # | Subsidiary (VinFast/Xanh SM...) | Lens | Mô tả ngắn bài toán |
|---|----------------------------------|------|---------------------|
| 1 | Vinmec | AI-upgrade + Stakeholder Pain | Bác sĩ chẩn đoán hình ảnh đọc hàng trăm phim X-quang/ngày theo hàng đợi gần FIFO. Ca nghiêm trọng có thể chờ lâu và nguy cơ bỏ sót tăng khi bác sĩ quá tải. |
| 2 | VinWonders | Stakeholder Pain + AI-upgrade | Khách phải xếp hàng lâu ở trò chơi đông trong khi khu khác còn công suất; nhân viên khó phân luồng khách theo thời gian chờ realtime. |
| 3 | VinFast / Xanh SM | Stakeholder Pain + Time-consuming | Ứng dụng báo trạm sạc còn trống nhưng trụ thực tế bận, hỏng hoặc sai cổng; tài xế phải gọi tổng đài và điều phối viên tra cứu thủ công nhiều hệ thống. |
| 4 | Xanh SM | Repetitive + Time-consuming | Khi khách báo quên đồ, CSKH phải tìm chuyến theo số điện thoại, giờ và mô tả tự do rồi gọi tài xế; mỗi vụ có thể mất khoảng 20 phút và dễ nhầm chuyến. |
| 5 | VinFast | Repetitive + AI-upgrade | CSKH đọc mô tả lỗi xe bằng tiếng Việt, tự phân loại mã lỗi và xếp lịch xưởng; mô tả không chuẩn có thể làm sai mức ưu tiên hoặc lịch hẹn. |

**Ghi chú đánh giá ban đầu:** Tôi ưu tiên bài toán có actor rõ, workflow lặp lại,
metric đo được và có thể giới hạn quyền AI. Bài toán Vinmec có giá trị cao
nhưng cần Computer Vision, dữ liệu ảnh gán nhãn và kiểm soát y tế. Bài toán
VinWonders cần dữ liệu realtime phức tạp. Bài toán phân loại lỗi xe có rủi ro
an toàn. Bài toán trạm sạc có khả năng thử nghiệm tốt nhất vì Rule Engine có
thể quyết định phần an toàn, còn LLM chỉ xử lý ngôn ngữ và soạn nháp.

---

# 🃏 Phase 2 — QUICK-ASSESS

Chọn top 3 bài toán từ danh sách trên và hoàn thiện **3 Quick Problem Cards** dưới đây (10 phút/card).

## QUICK PROBLEM CARD #1

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #1                                       │
│                                                             │
│ Bài toán (1 câu): Tài xế Xanh SM chạy tới trạm được app báo │
│ còn trống nhưng không sạc được vì trụ bận, hỏng hoặc sai    │
│ cổng; tài xế phải gọi tổng đài trong khi pin tiếp tục giảm. │
│ Công ty thành viên: [x] VinFast  [x] Xanh SM  [ ] Vinhomes │
│                     [ ] Vinmec   [ ] Khác (Ghi rõ)________  │
│                                                             │
│ Ai đang đau (Actor)? Tài xế Xanh SM; điều phối viên tổng đài;│
│ nhân viên trạm và khách đang chờ cuốc bị ảnh hưởng gián tiếp│
│                                                             │
│ Workflow thủ công hiện tại (5 bước):                       │
│   1. Tài xế chọn trạm trên app                              │
│   ──> 2. Tới trạm và phát hiện trụ bận/hỏng/sai cổng        │
│   ──> 3. Gọi tổng đài, mô tả sự cố                          │
│   ──> 4. ĐPV hỏi thông tin, tra GPS và dashboard trạm       │
│   ──> 5. ĐPV soạn hướng dẫn hoặc gọi đội sạc di động        │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 4-5 (8-10 phút/lượt):  │
│ tra nhiều hệ thống, lọc cổng sạc/khoảng cách và gõ lại tin. │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Rule lọc trạm ở bước  │
│ 4; LLM soạn nháp tiếng Việt ở bước 5; ĐPV duyệt trước gửi.  │
│                                                             │
│ Đo thành công bằng gì (Metric có số)? Giảm thời gian ĐPV    │
│ từ khoảng 10 phút xuống tối đa 3 phút; giảm lượt đến trạm   │
│ nhưng không sạc được xuống dưới 5%; 0 đề xuất trạm trên     │
│ 5km khi pin dưới 5%; 100% tin có [DRAFT_ONLY] và HITL.      │
│                                                             │
│ Quick Architecture: [ ] No AI  [x] Rule  [x] LLM  [ ] Agent│
│ Rule quyết định trạm; LLM chỉ diễn đạt; validator và ĐPV     │
│ kiểm tra. Không cho AI tự gửi tin hoặc tự điều xe cứu hộ.    │
└─────────────────────────────────────────────────────────────┘
```

**Stress-test và boundary:** Không được bịa trạm, địa chỉ, GPS, loại cổng hoặc
trạng thái trụ. Nếu pin dưới 5% và trạm phù hợp xa hơn 5km, action phải là
`dispatch_mobile_charger`, không đề xuất trạm xa. Nếu thiếu dữ liệu, API lỗi,
dữ liệu cũ hơn 5 phút hoặc validator lỗi thì chuyển về template và ĐPV xác minh
thủ công. Đây là card tôi đề xuất đưa sang Deep-Dive.

## QUICK PROBLEM CARD #2

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #2                                       │
│                                                             │
│ Bài toán (1 câu): CSKH Xanh SM mất nhiều thời gian tìm đúng │
│ chuyến và liên hệ tài xế khi khách báo quên đồ trên xe.     │
│ Công ty thành viên: [ ] VinFast  [x] Xanh SM  [ ] Vinhomes │
│                     [ ] Vinmec   [ ] Khác (Ghi rõ)________  │
│                                                             │
│ Ai đang đau (Actor)? Nhân viên CSKH, khách hàng lo mất đồ và │
│ tài xế bị gọi khi đang chạy cuốc.                           │
│                                                             │
│ Workflow thủ công hiện tại (5 bước):                       │
│   1. Khách mô tả món đồ, giờ, điểm đón/trả                  │
│   ──> 2. CSKH tra lịch sử chuyến theo số điện thoại         │
│   ──> 3. Chọn chuyến ứng viên và gọi tài xế xác nhận        │
│   ──> 4. Thống nhất cách trả đồ                             │
│   ──> 5. Cập nhật ticket và báo lại khách                   │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 2-3 (8-10 phút/lượt):  │
│ khách nhớ sai giờ hoặc đi nhiều chuyến nên CSKH dễ chọn sai. │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Bước 1-2: LLM trích   │
│ xuất item/time/pickup/dropoff thành JSON để code query;     │
│ bước 3: LLM soạn nháp tin in-app cho CSKH duyệt.            │
│                                                             │
│ Đo thành công bằng gì (Metric có số)? Giảm tổng thời gian    │
│ xử lý từ khoảng 20 phút xuống dưới 7 phút; xác định đúng    │
│ chuyến ngay lần đầu >= 95%; tỉ lệ trả đồ trong 24 giờ tăng   │
│ 20%.                                                        │
│                                                             │
│ Quick Architecture: [ ] No AI  [x] Rule  [x] LLM  [ ] Agent│
│ Rule/query tìm chuyến; LLM trích xuất và soạn nháp. Không    │
│ lộ số điện thoại, không hứa bồi thường, không tự gửi tin.   │
└─────────────────────────────────────────────────────────────┘
```

**Phản biện:** Có thể thêm nút “Báo quên đồ” trong lịch sử chuyến để khách tự
chọn chuyến. Nếu UX + Rule giải quyết được phần lớn lỗi, giải pháp đó rẻ và
đáng tin hơn LLM. Vì vậy card này là phương án dự phòng, cần thử UX trước.

## QUICK PROBLEM CARD #3

```text
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #3                                       │
│                                                             │
│ Bài toán (1 câu): Phim X-quang ngực của ca nghiêm trọng     │
│ có thể phải chờ trong hàng FIFO khi bác sĩ đang quá tải.    │
│ Công ty thành viên: [ ] VinFast  [ ] Xanh SM  [ ] Vinhomes │
│                     [x] Vinmec   [ ] Khác (Ghi rõ)________  │
│                                                             │
│ Ai đang đau (Actor)? Bác sĩ chẩn đoán hình ảnh; bác sĩ lâm  │
│ sàng và bệnh nhân chờ kết quả bị ảnh hưởng gián tiếp.       │
│                                                             │
│ Workflow thủ công hiện tại (4 bước):                       │
│   1. KTV chụp phim, đẩy lên PACS                            │
│   ──> 2. Phim vào hàng đợi gần FIFO                         │
│   ──> 3. Bác sĩ đọc, đối chiếu bệnh sử/phim cũ              │
│   ──> 4. Bác sĩ viết kết luận trên RIS                      │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Bước 2-3 (5-7 phút/phim);   │
│ ca khẩn có thể chờ khoảng 60 phút giờ cao điểm, rủi ro bỏ   │
│ sót tăng khi bác sĩ đọc số lượng lớn.                       │
│ AI có thể nhảy vào hỗ trợ ở bước nào? Computer Vision chấm  │
│ điểm nghi ngờ và Rule ưu tiên hàng đợi ở bước 2; bác sĩ     │
│ vẫn phải đọc và ký kết luận ở bước 3-4.                     │
│                                                             │
│ Đo thành công bằng gì (Metric có số)? Sensitivity >= 95%     │
│ trên tập test do bác sĩ gán nhãn; thời gian ca khẩn tới lúc │
│ bác sĩ mở phim từ khoảng 60 phút xuống dưới 15 phút; giảm   │
│ 30% ca bỏ sót phát hiện ở lần đọc lại.                      │
│                                                             │
│ Quick Architecture: [ ] No AI  [x] Rule  [ ] LLM  [ ] Agent│
│ Computer Vision + Rule + bác sĩ HITL. Không dùng LLM để tự  │
│ chẩn đoán hoặc trả kết quả cho bệnh nhân.                   │
└─────────────────────────────────────────────────────────────┘
```

**Phản biện:** Đây là bài toán có giá trị cao nhưng cần dữ liệu DICOM gán nhãn,
đánh giá chuyên môn, kiểm soát bias và phê duyệt y tế. Tôi không chọn card này
cho prompt prototype LLM của lab vì rủi ro và phạm vi kỹ thuật quá lớn.

## 🗳️ Lựa chọn cá nhân để đề xuất với nhóm

Tôi đề xuất **QUICK PROBLEM CARD #1 — Co-pilot xử lý sự cố trạm sạc cho điều
phối viên Xanh SM**. Card này có actor và bottleneck rõ, metric định lượng,
phần quyết định an toàn có thể giao cho Rule Engine, còn LLM chỉ soạn nháp.
Tuy nhiên đây mới là đề xuất cá nhân; nhóm cần hội ý, kiểm tra baseline và
quyết định cuối cùng trước khi làm `02-deep-dive-report.md`.