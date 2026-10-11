# Ollie — biểu cảm cơ bản thứ 8: đang suy nghĩ

Ngày dựng: 12/10/2026. Key dùng trong ứng dụng: `mood = thinking`.

Biểu cảm này dành cho lúc Ollie cân nhắc một vấn đề, đọc câu hỏi hoặc chuẩn bị trả lời. Tư thế chính là một cánh đặt gần cằm, mắt nhìn chếch lên bên phải, mỏ khép và đầu nghiêng chậm. Ba chấm nhỏ lần lượt sáng lên để giữ cảm giác đang suy nghĩ trong lúc chờ.

`confused` thể hiện thắc mắc bằng dấu hỏi và cánh mở; `thinking` thể hiện sự cân nhắc; `idea` thể hiện lúc tìm ra cách giải quyết bằng bóng đèn. Ứng dụng có thể chuyển `thinking` → `idea` khi đã có câu trả lời.

## Khung chuyển động

Vòng lặp 180 frame ở 60 fps, dài 3 giây. Các đường chuyển động dùng easing nhẹ, trở về cùng giá trị ở đầu và cuối vòng.

| Thời điểm | Chuyển động |
|---|---|
| 0 s | Cánh nghỉ gần cằm, đầu nghiêng nhẹ; chấm suy nghĩ mờ. |
| 0,75 s | Đầu nghiêng thêm, thân nâng theo nhịp thở; các chấm bắt đầu hiện. |
| 1,5 s | Giữ nhịp cân nhắc, cánh nâng nhẹ khoảng 4 px; ba chấm rõ. |
| 2,1–2,3 s | Chớp mắt ngắn trong lúc đầu bắt đầu trở lại. |
| 3 s | Đầu, cánh, thân và chấm trở về tư thế đầu vòng. |

Cánh dùng nguyên bộ bảy lớp lông của rig hiện tại. Tròng mắt và ánh sáng trong mắt dịch nhẹ lên phải, trong khi viền mắt giữ vị trí gốc. Chồi lá tiếp tục chuyển động theo layer của rig.

## Tích hợp và xem lại

- Nút **8. Đang suy nghĩ** trong [playground](../playground/index.html), phím tắt **8**.
- [Dải 5 khung trong build](../build/thinking-strip.png) và [ảnh đại diện](../build/moods/thinking.png).
- `tools/thinking_mood.py`: cánh, ba chấm, keyframe và transition; `tools/build_ollie.py`: mắt và bước ghép rig.
- `data/model.json`: thêm `thinking` với ID `0:608` vào cuối enum, giữ thứ tự toàn bộ 26 giá trị trước đó. Vị trí thứ 8 là thứ tự nút trong nhóm biểu cảm cơ bản.
- `data/presets.json`: preset suy nghĩ; `tests/poses.json`: khung đầu/giữa/cuối vòng và tương tác ngủ/vẫy.

Khi ngủ, layer Sleep thay thế tư thế và ẩn dấu chấm/cánh chống cằm. Sau vẫy hoặc đánh thức, Ollie trở về mood đang chọn. Chế độ frame dự phòng hiển thị ảnh đại diện; chuyển động đầy đủ chạy bằng Rive.

`py tools/build_kit.py` dựng lại cả bộ. Có thể thử preset riêng bằng `py tools/preview.py thinking --capture`.
