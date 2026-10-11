# Ollie — cánh gốc cho cử chỉ, cầm và nâng đồ (bản dựng 08)

## Phân tích dáng cánh

Các bản cánh cầm trước biến cánh thành khối tròn bóng, đường viền và mảng sáng chồng tại mép vật. Chúng không giống hai cánh front gốc mà người dùng cung cấp: vai hẹp hơn, hai lông dài nhọn phía dưới và các lớp xanh non chạy dọc thân cánh.

Bản này lấy trực tiếp bảy đường Bézier của `LeftWing` trong `artwork/build_artwork.py`, rồi phản chiếu cho cánh phải. `HOLD_SOURCE` ở `tools/wing_poses.py` giữ nguyên thứ tự và màu từng lớp:

| Lớp | Vai trò |
|---|---|
| `LowerWingOutline` | Đường bao và hai đầu lông nhọn phía dưới. |
| `LongLowerFeather`, `MiddleLowerFeather`, `LongSideFeather` | Ba lớp lông dài xếp tầng như cánh front. |
| `FoldedUpperWing` | Khối cánh chính, vẫn có nếp gập của mẫu gốc. |
| `LongLimeCovert`, `UpperLeafCovert` | Hai mảng xanh non dạng lá. |

Cả cánh tạo dáng và cánh cầm đều dùng màu phẳng, bỏ gradient bóng. `hug_warp` neo vai tại `(155,322)` và `(345,322)` trên artboard 500 × 500; cùng một phép xoay và thu nhỏ đều áp dụng cho mọi đỉnh lẫn tay nắm Bézier. Đầu lông vì thế giữ nguyên góc nhọn và tỷ lệ như mẫu. Ở cảnh cầm đồ, đích của cánh lấy từ vị trí/góc vật tại từng keyframe; các mốc của cánh được nội suy theo cùng nhịp nâng–giữ–hạ.

## Khung chuyển động cần đọc

Mỗi vòng lặp có năm mốc xem trong [wing-review.html](../playground/wing-review.html). `build/wing-redesign/` chứa ảnh 500 px ở mốc giữa cùng dải năm khung lớn của mười lăm cảnh tạo dáng hoặc cầm/nâng. Mốc 0 và 100% kiểm tra vòng lặp khép kín; 25%, 50% và 75% cho thấy nhịp giữa. Các cảnh có nhịp riêng:

| Cảnh | Điểm cầm và hướng lực | Điều cần thấy ở 5 mốc |
|---|---|---|
| `love`, `letter` | Hai đầu cánh ôm hai cạnh dưới; tim và thư vẫn đọc trọn hình. | Vai đứng yên, cánh siết nhẹ theo vật nảy, rồi trở về vị trí đầu. |
| `nutrition` | Hai thùy dưới đỡ đáy bát; mặt bát và rau không bị che. | Bát lên rồi xuống, đầu cánh bám đáy ở toàn bộ vòng. |
| `wallet`, `sad`, `saving` | Cánh đỡ hai cạnh ví hoặc heo đất; phần tiền/đồng xu vẫn rõ. | Đầu cánh không trượt qua mép khi vật nhún. |
| `checklist`, `alarm` | Đầu cánh giữ cạnh bảng và đồng hồ; tâm vật để trống. | Vật rung hoặc nâng mà vai không tách khỏi thân. |
| `pomodoro` | Cánh tì ở mép dưới màn hình, nhịp gõ trái/phải so le. | Hai đầu cánh dịch ngắn, không tạo các ngón nhỏ trên màn hình. |
| `workout` | Hai cánh gốc xoay vào thanh tạ ở hai bên thân. | Thanh tạ lên, giữ ngắn ở đỉnh, hạ có kiểm soát; cánh theo hai điểm nắm. |
| `celebrate` | Cánh trái xoay lên giữ cạnh chân cúp; mặt cúp nằm trước cánh. | Cánh và cúp nâng cùng nhịp, không để lông che mặt cúp. |
| `meditate` | Hai cánh mở thấp ra hai bên thân. | Đầu lông dài hướng ra ngoài, không thành hai nắm tay tròn trước ngực. |
| `worried` | Hai cánh chạm mép má ngoài. | Đường lông giữ rõ và không che đồng tử. |
| `idea`, `bedtime` | Một cánh nâng trước ngực hoặc miệng. | Cánh còn lại giữ dáng đứng gốc; đầu lông không biến thành khối tròn. |

Các cảnh chạy, mệt, reo vui và tràn năng lượng dùng cánh front gốc. Không sửa ảnh front chuẩn trong `artwork/build_artwork.py`.

## Chỉnh và xuất lại

1. Sửa cánh chuẩn trong `artwork/build_artwork.py` nếu cần đổi dáng lông của cả nhân vật. Sửa `WingPoses.hold` và từng lệnh `wings.add` trong `tools/expression_library.py` nếu cần đổi điểm chạm riêng của hành động.
2. Chạy `python tools/build_kit.py` từ thư mục `ollie-mascot`. Lệnh này tạo lại `runtime.rml`, ảnh trong `build/expressions/`, 95 frame ở `playground/frames/wings/` và `dist/ollie.riv`.
3. Mở [bảng kiểm tra cánh](../playground/wing-review.html). Xem cả nền sáng/tối và từng mốc của các cảnh trên. Kiểm tra viền vai, mép vật, điểm nắm và khung đầu/cuối trước khi chọn bản cuối.

Khi chỉ sửa một vài cảnh sau lần build đầy đủ, dùng `python tools/build_expressions.py --scenes celebrate workout` để xuất lại cảnh đó và cập nhật bảng tổng hợp. Sau đó chạy `python tools/build_wing_review.py` để đồng bộ các dải khung lớn.
