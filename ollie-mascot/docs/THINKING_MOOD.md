# Ollie — biểu cảm cơ bản thứ 8: đang suy nghĩ

Ngày dựng: 12/10/2026. Key dùng trong ứng dụng: `mood = thinking`.

Biểu cảm này dành cho lúc Ollie cân nhắc một vấn đề, đọc câu hỏi hoặc chuẩn bị trả lời. Tư thế chính là một cánh đặt gần cằm, mắt nhìn chếch lên bên phải, mỏ khép và đầu nghiêng chậm. Một đám mây suy nghĩ nối với đầu bằng ba bong bóng nhỏ dần, bên trong có năm dấu chấm hiện lần lượt.

Tỉ lệ nhân vật bằng bảy biểu cảm gốc. Đám mây và các bong bóng được đặt quanh Ollie, không thu nhỏ toàn bộ nhân vật.

`confused` thể hiện thắc mắc bằng dấu hỏi và cánh mở; `thinking` thể hiện sự cân nhắc bằng đám mây suy nghĩ; `idea` thể hiện lúc tìm ra cách giải quyết bằng bóng đèn. Ứng dụng có thể chuyển `thinking` → `idea` khi đã có câu trả lời.

## Đám mây suy nghĩ

Đám mây gồm bốn hình elip chồng lên nhau (Puff1–Puff4), tạo ra hình dáng mây mềm mại mà không cần đường path phức tạp. Ba bong bóng nối (LinkBubble1–3) tăng dần kích thước từ đỉnh đầu Ollie lên tới đám mây. Bên trong mây có năm dấu chấm xếp hàng ngang, hiện lần lượt từ trái sang phải.

## Khung chuyển động

Vòng lặp 180 frame ở 60 fps, dài 3 giây. Các đường chuyển động dùng easing nhẹ, trở về cùng giá trị ở đầu và cuối vòng.

| Thời điểm | Chuyển động |
|---|---|
| 0 s | Cánh nghỉ gần cằm, đầu nghiêng nhẹ; bong bóng nối và đám mây mờ. |
| 0,25–0,58 s | Ba bong bóng nối hiện lần lượt từ dưới lên (offset 14 frame). |
| 0,5–0,92 s | Đám mây fade in (opacity 0→0.85), bắt đầu nhịp thở (scale 0.95→1.05). |
| 0,67–1,75 s | Năm dấu chấm bên trong mây sáng lần lượt trái→phải (offset 8 frame). |
| 2,1–2,3 s | Chớp mắt ngắn; đám mây và dấu chấm bắt đầu mờ dần. |
| 2,42–2,58 s | Bong bóng nối mờ lần lượt từ trên xuống. |
| 3 s | Đầu, cánh, thân, đám mây và bong bóng trở về tư thế đầu vòng. |

Cánh dùng nguyên bộ bảy lớp lông của rig hiện tại. Tròng mắt và ánh sáng trong mắt dịch nhẹ lên phải, trong khi viền mắt giữ vị trí gốc. Chồi lá tiếp tục chuyển động theo layer của rig.

## Tích hợp và xem lại

- Nút **8. Đang suy nghĩ** trong [playground](../playground/index.html), phím tắt **8**.
- [Dải 5 khung trong build](../build/thinking-strip.png) và [ảnh đại diện](../build/moods/thinking.png).
- `tools/thinking_mood.py`: cánh, ba chấm, keyframe và transition; `tools/build_ollie.py`: mắt và bước ghép rig.
- `data/model.json`: thêm `thinking` với ID `0:608` vào cuối enum, giữ thứ tự toàn bộ 26 giá trị trước đó. Vị trí thứ 8 là thứ tự nút trong nhóm biểu cảm cơ bản.
- `data/presets.json`: preset suy nghĩ; `tests/poses.json`: khung đầu/giữa/cuối vòng và tương tác ngủ/vẫy.

Khi ngủ, layer Sleep thay thế tư thế và ẩn dấu chấm/cánh chống cằm. Sau vẫy hoặc đánh thức, Ollie trở về mood đang chọn. Chế độ frame dự phòng hiển thị ảnh đại diện; chuyển động đầy đủ chạy bằng Rive.

`py tools/build_kit.py` dựng lại cả bộ. Có thể thử preset riêng bằng `py tools/preview.py thinking --capture`.
