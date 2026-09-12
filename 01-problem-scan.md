# 01 — Problem Scan & Quick Assessment

> Đây là phần làm cá nhân của Lab 02. Các con số dưới đây là giả định để
> scoping, chưa phải số liệu đã được Vingroup xác nhận. Trước khi triển khai
> cần kiểm tra lại bằng log vận hành, phỏng vấn người dùng và dữ liệu thật.

## 1. Cách tôi quét cơ hội

Tôi dùng bốn lenses của worksheet để tìm các quy trình có khả năng cải thiện:

- **Repetitive:** nhân viên lặp lại cùng một thao tác nhiều lần.
- **Time-consuming:** một ticket hoặc một lượt xử lý chiếm nhiều phút của
  nhân viên hoặc khách hàng.
- **AI-upgrade:** cần hiểu ngôn ngữ tự nhiên, hình ảnh hoặc ngữ cảnh mà mẫu
  câu cố định xử lý kém.
- **Stakeholder pain:** khách hàng, tài xế, bác sĩ hoặc nhân viên đang trực
  tiếp chịu hậu quả của bottleneck.

Tôi ưu tiên những bài toán có đủ ba điều kiện: có actor cụ thể, đo được thời
gian/chất lượng và có thể giới hạn quyền của AI. Tôi không mặc định rằng bài
toán càng dùng AI nhiều thì càng tốt; nếu Rule hoặc UX giải quyết được phần
lõi thì đó là phương án cần được xem xét trước.

## 2. Phase 1 — SCAN: năm bài toán cơ hội

| # | Công ty | Lens chính | Actor chịu ảnh hưởng | Bài toán và bottleneck | Dữ liệu có thể cần | Hướng công nghệ ban đầu |
|---|---|---|---|---|---|---|
| 1 | Vinmec | AI-upgrade, stakeholder pain | Bác sĩ chẩn đoán hình ảnh và bệnh nhân chờ kết quả | Phim X-quang được xử lý gần như FIFO. Ca có dấu hiệu nghiêm trọng có thể bị trễ; bác sĩ phải đọc số lượng lớn phim nên nguy cơ bỏ sót tăng khi quá tải. | Ảnh DICOM, nhãn do bác sĩ xác nhận, timestamp PACS/RIS, thông tin ca khẩn | Computer Vision để hỗ trợ phát hiện và Rule để xếp hàng ưu tiên; không phải LLM thuần túy |
| 2 | VinWonders | Stakeholder pain, AI-upgrade | Khách tham quan và nhân viên vận hành khu vui chơi | Một số trò chơi quá đông trong khi khu khác còn công suất. Khách không biết nên chuyển sang đâu; nhân viên khó cân bằng luồng khách theo thời gian thực. | Thời gian chờ, vị trí/khu vực, công suất trò chơi, lịch sử lượt chơi, điều kiện thời tiết | Rule + dự báo nhu cầu; có thể dùng recommendation, nhưng cần bảo vệ dữ liệu vị trí |
| 3 | VinFast / Xanh SM | Stakeholder pain, time-consuming | Tài xế và điều phối viên tổng đài | Ứng dụng báo trạm sạc còn chỗ nhưng trụ thực tế bận/hỏng/sai cổng. Tài xế đi tới nơi rồi phải gọi tổng đài; điều phối viên tra nhiều hệ thống và gõ lại hướng dẫn. | GPS, phần trăm pin, dòng xe/cổng sạc, trạng thái trụ, timestamp heartbeat, log cuộc gọi/ticket | Rule lọc trạm; LLM chỉ trích xuất mô tả và soạn nháp; HITL bắt buộc |
| 4 | Xanh SM | Repetitive, time-consuming | Nhân viên CSKH, tài xế và khách báo quên đồ | CSKH phải tìm chuyến theo số điện thoại, giờ và mô tả tự do rồi gọi tài xế. Dễ nhầm chuyến khi khách đi nhiều cuốc; tài xế có thể không nghe máy khi đang chạy. | Lịch sử chuyến, ticket, thời gian/điểm đón trả, mô tả món đồ, trạng thái liên lạc | Rule/query để tìm chuyến; LLM trích xuất trường dữ liệu và soạn tin nháp |
| 5 | VinFast | Repetitive, AI-upgrade | CSKH và kỹ thuật viên xưởng dịch vụ | CSKH đọc mô tả lỗi tiếng Việt, tự phân loại mã lỗi và xếp lịch. Mô tả không chuẩn khiến mã lỗi hoặc mức độ ưu tiên bị chọn sai. | Ticket, mô tả lỗi, mã lỗi đã xác nhận, lịch sửa chữa, dòng xe, kết quả chẩn đoán | LLM trích xuất symptom nhưng Rule và kỹ thuật viên phải xác nhận; không cho AI tự kết luận an toàn |

### Nhận định sơ bộ

- Bài toán Vinmec có giá trị cao nhưng rủi ro y tế/pháp lý rất lớn, cần mô hình
  Computer Vision được đánh giá chuyên môn. Nó không phù hợp làm prototype LLM
  nhỏ trong buổi lab.
- Bài toán VinWonders có giá trị trải nghiệm rõ, nhưng cần dữ liệu realtime và
  bài toán tối ưu luồng khách phức tạp hơn phạm vi một prompt prototype.
- Bài toán trạm sạc có workflow cụ thể, metric thời gian rõ và có thể tách
  quyết định an toàn cho Rule Engine.
- Bài toán quên đồ phù hợp LLM ở khâu hiểu mô tả, nhưng UX cho khách chọn trực
  tiếp chuyến đi có thể giải quyết phần lớn lỗi mà không cần LLM.
- Bài toán phân loại lỗi xe có rủi ro an toàn: AI chỉ nên hỗ trợ phân loại ban
  đầu, không được tự hướng dẫn sửa chữa hoặc kết luận xe an toàn.

## 3. Ma trận ưu tiên cá nhân

Thang điểm 1-5: 5 là tốt nhất. `AI fit` đo mức phù hợp với prototype; `risk`
đo mức rủi ro khi AI sai, nên điểm cao nghĩa là **ít rủi ro hơn**.

| Bài toán | Giá trị vận hành | AI fit | Dữ liệu/khả năng thử | Risk safety | Tổng | Nhận xét |
|---|---:|---:|---:|---:|---:|---|
| Vinmec X-quang | 5 | 2 | 2 | 1 | 10/20 | Giá trị lớn nhưng cần Computer Vision, dữ liệu gán nhãn và kiểm soát y tế |
| VinWonders phân luồng khách | 4 | 3 | 2 | 3 | 12/20 | Có tiềm năng nhưng phụ thuộc dữ liệu realtime và tích hợp vận hành |
| Trạm sạc VinFast/Xanh SM | 5 | 5 | 4 | 4 | **18/20** | Workflow rõ, có thể dùng Rule + LLM + HITL, boundary kiểm thử được |
| Xanh SM quên đồ | 4 | 4 | 4 | 4 | **16/20** | Có ích nhưng cần cân nhắc UX/Rule trước LLM |
| VinFast phân loại lỗi xe | 4 | 4 | 3 | 2 | 13/20 | Cần kỹ thuật viên xác nhận; không được để AI đưa ra kết luận an toàn |

## 4. Phase 2 — Ba Quick Problem Cards

### Card #1 — VinFast / Xanh SM: Trạm sạc báo còn trống nhưng không sạc được

**Bài toán một câu:** Tài xế chạy tới trạm được ứng dụng báo còn trống nhưng
không thể sạc vì trụ bận, hỏng hoặc không tương thích cổng; sau đó tài xế phải
gọi tổng đài trong khi pin tiếp tục giảm.

**Actor và stakeholder:**

- Actor trực tiếp: tài xế Xanh SM.
- Operator: điều phối viên tại tổng đài.
- Stakeholder liên quan: nhân viên trạm, đội cứu hộ pin, khách đang chờ cuốc.

**Workflow hiện tại (giả định 5 bước):**

1. Tài xế thấy pin thấp và chọn một trạm trên ứng dụng.
2. Tài xế tới trạm, phát hiện trụ bận/hỏng/sai cổng.
3. Tài xế gọi tổng đài và mô tả sự cố bằng lời.
4. Điều phối viên hỏi biển số, dòng xe, vị trí, phần trăm pin; sau đó mở
   dashboard trạm để tìm phương án thay thế.
5. Điều phối viên gọi xác nhận hoặc soạn hướng dẫn gửi tài xế; nếu pin quá
   thấp thì gọi đội sạc di động.

**Bottleneck:** Bước 4-5 mất khoảng 8-10 phút/lượt vì phải đối chiếu GPS,
loại cổng và trạng thái trụ trên các hệ thống khác nhau rồi gõ lại tin nhắn.
Tình huống nguy hiểm nhất là pin dưới 5% nhưng điều phối viên vẫn đề xuất
trạm cách xa do bỏ sót kiểm tra hoặc dữ liệu không đầy đủ.

**AI có thể tham gia ở đâu:**

- Rule Engine lọc danh sách trạm theo trạng thái, cổng sạc, khoảng cách và
  độ mới của dữ liệu.
- LLM hiểu mô tả tự do của tài xế và soạn bản nháp tiếng Việt từ kết quả Rule.
- Validator kiểm tra schema, allow-list và ngưỡng pin trước khi hiển thị.
- Điều phối viên duyệt hoặc sửa; AI không được tự gửi tin hay tự điều xe.

**Metric sơ bộ:**

- Thời gian xử lý của điều phối viên: khoảng 10 phút xuống tối đa 3 phút.
- Tỷ lệ đến trạm nhưng không sạc được: dưới 5%.
- 0 trường hợp đề xuất trạm trên 5 km khi pin dưới 5%.
- 100% tin gửi ra phải có điều phối viên duyệt và bản nháp bắt đầu bằng
  `[DRAFT_ONLY]`.

**Quick architecture:** Rule + LLM Feature, không dùng Agent. Rule quyết định;
LLM diễn đạt; người duyệt chịu trách nhiệm hành động.

**Boundary và fallback:** Không được bịa trạm, địa chỉ, tọa độ hoặc trạng thái
trụ. Nếu thiếu GPS/pin, dữ liệu cũ hơn 5 phút, LLM timeout hoặc validator lỗi,
chuyển về template thủ công và yêu cầu điều phối viên xác minh.

**Rủi ro và điều kiện chọn:** Dữ liệu trạng thái trạm có thể sai nên giải pháp
này không tự sửa được nguyên nhân gốc. Tuy vậy, rủi ro có thể giới hạn bằng
Rule, validator, HITL và fallback. Đây là ứng viên tốt nhất để đưa sang
Deep-Dive, với điều kiện các con số phải được xác nhận bằng baseline thật.

### Card #2 — Xanh SM: Xử lý báo quên đồ trên xe

**Bài toán một câu:** CSKH mất khoảng 20 phút để tìm đúng chuyến, liên hệ tài
xế và thống nhất cách trả đồ khi khách mô tả món đồ bằng ngôn ngữ tự do.

**Actor và workflow:**

1. Khách gọi hotline/chat, nói món đồ, thời gian và điểm đón/trả.
2. CSKH tra lịch sử chuyến theo số điện thoại và khung giờ.
3. CSKH chọn chuyến ứng viên rồi gọi tài xế xác nhận.
4. Hai bên thống nhất tài xế quay lại, gửi về hub hoặc khách tới nhận.
5. CSKH cập nhật ticket và báo lại khách.

**Bottleneck:** Tìm chuyến và gọi tài xế là hai bước tốn thời gian nhất. Khách
có thể nhớ sai giờ hoặc đi nhiều chuyến; AI không được tự tuyên bố đã tìm thấy
đồ khi tài xế chưa xác nhận.

**AI có thể tham gia:** LLM trích xuất `item`, `time_window`, `pickup` và
`dropoff` thành JSON; code dùng các trường đó để query lịch sử chuyến; LLM
soạn nháp tin in-app cho tài xế.

**Metric sơ bộ:**

- Thời gian xử lý: khoảng 20 phút xuống dưới 7 phút.
- Tỷ lệ chọn đúng chuyến ngay lần đầu: ít nhất 95%.
- Tỷ lệ trả đồ thành công trong 24 giờ: tăng 20%.

**Boundary:** Không lộ số điện thoại tài xế, không hứa bồi thường, không khẳng
định đã tìm thấy đồ trước khi tài xế xác nhận, và không tự gửi tin.

**Quick architecture:** Rule/query + LLM extraction/drafting. Không dùng Agent.

**Phản biện:** Có thể thêm nút “Báo quên đồ” trực tiếp trong lịch sử chuyến để
khách tự chọn đúng chuyến. Nếu UX này giải quyết phần lớn lỗi, giải pháp UX +
Rule sẽ rẻ và đáng tin hơn LLM. Vì vậy card này phù hợp làm phương án thứ hai,
nhưng cần thử nghiệm UX trước.

### Card #3 — Vinmec: Hỗ trợ ưu tiên phim X-quang ngực

**Bài toán một câu:** Phim X-quang được đưa vào hàng đợi gần như FIFO khiến ca
nghiêm trọng có thể chờ lâu, trong khi bác sĩ phải đọc hàng trăm phim mỗi ngày.

**Actor và workflow:**

1. Kỹ thuật viên chụp phim và đẩy ảnh lên PACS.
2. Hệ thống xếp phim theo thứ tự nhận.
3. Bác sĩ mở phim, đọc và đối chiếu bệnh sử/phim cũ.
4. Bác sĩ viết kết luận trên RIS và trả cho bác sĩ lâm sàng.

**Bottleneck:** Hàng đợi không ưu tiên mức độ nghiêm trọng; thời gian đọc và
viết kết luận khoảng 5-7 phút/phim, ca khẩn có thể chờ khoảng 60 phút trong
giờ cao điểm.

**AI có thể tham gia:** Computer Vision chấm điểm nghi ngờ và gợi ý vùng cần
chú ý; Rule sắp xếp lại hàng đợi; bác sĩ luôn là người đọc và ký kết luận.
LLM không phù hợp để tự đọc ảnh hoặc chẩn đoán.

**Metric sơ bộ:**

- Độ nhạy ít nhất 95% trên tập ảnh được bác sĩ gán nhãn.
- Thời gian ca khẩn tới lúc bác sĩ mở phim: khoảng 60 phút xuống dưới 15 phút.
- Tỷ lệ bỏ sót phát hiện ở lần đọc lại giảm 30%.

**Boundary:** AI không chẩn đoán, không trả kết quả trực tiếp cho bệnh nhân và
không thay chữ ký bác sĩ. Mọi cảnh báo phải hiển thị là hỗ trợ tham khảo.

**Quick architecture:** Computer Vision + Rule + HITL, không phải LLM prompt
prototype.

**Phản biện:** Giá trị xã hội cao nhưng rủi ro y tế/pháp lý, yêu cầu dữ liệu
gán nhãn, đánh giá bias và phê duyệt thiết bị. Tôi không chọn card này cho
Deep-Dive của lab vì nó vượt phạm vi kỹ thuật và kiểm soát rủi ro hiện tại.

## 5. So sánh và quyết định cá nhân

| Tiêu chí | Card #1 Trạm sạc | Card #2 Quên đồ | Card #3 X-quang |
|---|---:|---:|---:|
| Tác động vận hành | Cao | Trung bình-cao | Rất cao |
| Có thể đo metric nhanh | Có | Có | Khó hơn |
| Phù hợp prompt prototype | Cao | Cao | Thấp |
| Rủi ro khi AI sai | Trung bình, kiểm soát được | Trung bình-thấp | Rất cao |
| Có phương án không dùng LLM | Có, Rule + template | Có, UX + Rule | Có, nhưng cần Computer Vision |
| Quyết định | **Chọn** | Dự phòng | Không chọn cho lab |

Tôi chọn **Card #1 — Co-pilot xử lý sự cố trạm sạc cho điều phối viên Xanh SM**
để đề xuất với nhóm. Lý do là bài toán có pain point cụ thể, tần suất có thể
cao, metric thời gian rõ và có thể thiết kế boundary kiểm thử được. Quan trọng
hơn, phần quyết định an toàn có thể giao cho Rule Engine; LLM chỉ hiểu ngôn ngữ
và soạn nháp.

Đây mới là đề xuất cá nhân, chưa phải quyết định cuối cùng của nhóm. Khi họp,
tôi sẽ trình bày cả phản biện rằng dữ liệu trạm có thể là nguyên nhân gốc và
giá trị tăng thêm của LLM so với template vẫn cần được đo bằng thử nghiệm.