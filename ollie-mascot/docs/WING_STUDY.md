# Ollie — cánh mềm, bản dựng 04

Ảnh mẫu mới cho thấy rõ sự khác biệt ở **dáng tổng thể**: cánh bắt đầu rộng tại vai, vòng ra ngoài rồi quét vào dưới mép phong thư. Lông phía dưới dài, xếp chồng như lá; mảng xanh non chỉ nhấn thành các nhịp nhỏ. Bản cũ đặt hai mảng cánh hẹp rủ dọc hai bên đạo cụ. Bo góc của mảng đó không thể tạo ra dáng ôm trong ảnh mẫu.

## Hai dáng vector mới

`tools/wing_poses.py` định nghĩa hai bộ bảy lớp bằng đường Bézier có thể sửa trực tiếp:

| Bộ | Cảnh dùng | Hình dáng |
|---|---|---|
| `HOLD_SOURCE` | `love`, `nutrition`, `sad`, `wallet`, `saving`, `checklist`, `alarm`, `letter` | Vai liền thân; đường bao vòng ra ngoài; ba lớp lông tối cong dài quét về phía trung tâm; lông xanh non thành nhịp ở mặt cánh. |
| `SOURCE` | `idea`, `worried`, `pomodoro`, `bedtime`, `celebrate`, `workout`, `meditate` | Cánh tròn và nhiều lớp hơn khi đưa lên mặt, chạm đạo cụ hoặc nghỉ thấp. |

Các lớp dùng bảng màu xanh, viền tối và gradient của Ollie. Mỗi lớp là một khối lông, không có lòng bàn tay hoặc ngón tay. `HOLD_SOURCE` dùng tọa độ 500 × 500 của cảnh cầm thư làm mốc; `hug_warp` giữ gốc vai và cho phần lông cuối đi theo vị trí/góc của đạo cụ ở từng keyframe. Bộ `SOURCE` dùng đường cong vai–nếp gập–đầu cánh cho những cử chỉ còn lại. Các đầu lông của dáng ôm được nối mượt, kể cả ở điểm gấp.

Bốn cảnh `running`, `tired`, `cheer`, `energized` tiếp tục dùng cánh front gốc: ở đó cánh dang/hạ đủ rộng và các lớp lông đọc rõ, không có dáng cầm đồ cứng. Hình front trong `artwork/build_artwork.py` không bị đổi, để bảy biểu cảm cơ bản và các chuyển động có sẵn giữ đúng nhận diện.

## Chỉnh tiếp theo ảnh mẫu

- Sửa đường bao và từng lớp ở `HOLD_SOURCE` hoặc `SOURCE` trong `tools/wing_poses.py`. `HugMainWing` là mảng xanh chính; `HugLowerFeather`, `HugMiddleFeather`, `HugInnerFeather` tạo ba lông quét dưới mép đạo cụ; `HugLimeScallops` và `HugUpperCovert` tạo điểm sáng.
- Sửa vị trí tiếp xúc của cánh ôm trong `WingPoses.hold`; các cảnh cử chỉ đặt đích và nếp gập riêng trong `tools/expression_library.py`.
- Tạo lại bằng `python tools/build_kit.py`, rồi xem [bảng 95 khung của cả 19 cảnh](../playground/wing-review.html) và [playground Rive](../playground/index.html). Trang khung có hai hình giải phẫu cánh mới, bản cánh front gốc, chế độ nền sáng/tối và năm mốc của mỗi vòng lặp.

Khi kiểm tra, nhìn đặc biệt vào cảnh thư, ví, bát và tim: vai không tách thân, mép đạo cụ vẫn đọc được, các lông cuối không biến thành ba ngón nhỏ. Với cảnh đưa cánh lên mặt, kiểm tra cánh không phủ mắt hoặc mỏ. Với cảnh nâng tạ và đồng hồ, xem cả mốc nâng cao nhất và khung đầu/cuối để phát hiện gãy nét khi nội suy.
