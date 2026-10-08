# Ollie neutral V2 — kiểm tra hình

> Bản V2 được giữ làm mốc so sánh. Nguồn đang dùng cho `../runtime.rml` là `../visual-v3/`; xem [phân tích V3](../visual-v3/DESIGN_ANALYSIS.md) và [trang đối chiếu V3](../visual-v3/review.html).

## Trạng thái

Bản vẽ này là **checkpoint hình neutral** và vẫn là nguồn có thể chỉnh sửa độc lập. Theo yêu cầu tiếp tục dựng Ollie, bản neutral đã được đưa vào rig tại `../runtime.rml` để kiểm tra biểu cảm và chuyển động. Rig tích hợp đang trong quá trình hoàn thiện hình.

## Đã thay đổi

- Đối chiếu lại với bảng thiết kế Ollie: thêm nét phản chiếu mống mắt, ánh sáng bên mống mắt và đuôi mí nhỏ để ánh nhìn có chiều sâu hơn.
- Bổ sung nét hướng lông ở trán, lông phụ ở đỉnh đầu và má; thêm một lớp sáng cùng gân mảnh cho mỗi cánh. Các chi tiết này nằm trong nhóm vector riêng để có thể chỉnh hoặc rig về sau.
- Vẽ lại đường viền đầu bằng Bézier, giảm góc gấp ở má, chia cụm lông đỉnh đầu thành nhiều lớp mềm hơn.
- Tạo lại mặt kem hai thùy và hõm trán; thêm lớp lông cổ nhỏ. Mảng kem dùng chuyển sắc nhẹ, không phải oval phẳng.
- Mỗi mắt hiện có 10 shape riêng: lòng trắng, vành mống mắt, mống mắt giữa, hai vùng sáng của mống mắt, đồng tử, hai highlight và hai mí. Đồng tử và lòng trắng đều là path Bézier chỉnh được.
- Thay hai cánh bằng bốn lông chồng lớp và một phần vai nhỏ. Mép dưới của các lông so le, nét trong mảnh hơn.
- Thu chân và AI Core; mỏ chuyển thành nêm cong nhỏ, không phải diamond đều.
- Chỉnh mầm lá nghiêng, thêm gân lá phụ; cân lại ba cấp xanh, ánh sáng trên-trái và chuyển sắc rất nhẹ cho đầu, mặt, ngực.

## Đối chiếu với bản cũ

Đầu bớt tròn, mảng mặt có hình cú rõ hơn; mắt giàu lớp hơn; cánh đã có các lông tách biệt; thân không còn một hình ellipse trơn; huy hiệu AI không chiếm trọng tâm. Ở 120 px nhận ra cú, hai mắt, lá, cánh và mỏ. Ở 80 px mắt, đầu và lá vẫn đọc được.

## Điểm còn dưới chất lượng ảnh mẫu

- Cụm lông đầu và lông má vẫn gọn, đều hơn tạo hình rất giàu lớp trong ảnh nhân vật lớn.
- Cánh front đã tách lông nhưng còn ít lông thứ cấp và họa tiết hơn bản minh họa reference.
- Mắt tròn, sáng và đọc rõ; sau khi thêm phản chiếu và nét mí, iris ở 500 px vẫn đơn giản hơn ảnh mẫu. Ở 120 px các lớp mới còn đọc được, nhưng nét trang trí mảnh tự nhiên biến mất ở 80 px.

Các điểm này vẫn cần kiểm tra trực quan khi hoàn thiện bản rig tích hợp. File V2 độc lập được giữ lại để tiếp tục sửa hình mà không mất nguồn gốc.

## File và ảnh kiểm tra

- Nguồn chỉnh sửa: `build_neutral.py`, `neutral.rml`.
- Bảng các phần: `build_parts.py`, `parts.rml`, `build/ollie_parts.png`.
- Ảnh neutral cuối: `build/ollie-neutral-500.png`, `build/ollie-neutral-240.png`, `build/ollie-neutral-120.png` và kiểm tra thêm `build/ollie-neutral-80.png`.
- Ảnh từng bước: `build/stage_01_head.png` đến `build/stage_10_color.png`; trang review có mục mở rộng để xem đủ mười bước.
- Rive: `build/ollie-neutral-v2.riv` (artboard `Neutral` trong suốt và artboard `Parts` để chẩn đoán).
- Trang đối chiếu tương tác: `review.html` tại `http://127.0.0.1:5500/ollie-mascot/visual-v2/review.html` trên Live Server mà người dùng đang mở. Trang playground hiện tại có nút chuyển thẳng sang đây.

## Kiểm tra kỹ thuật

Sau **mỗi** bước từ 1 đến 10: tái sinh RML, `rive . --verify` (0 lỗi, 0 cảnh báo), `rive inspect . --summary` (không problem), render PNG và xem hình. Bốn kích thước cuối và bảng bộ phận được render từ nguồn Rive mới. HTTP cổng 5500 trả 200 cho trang, `.riv` và ba ảnh bắt buộc. Chưa kiểm chứng thao tác trực tiếp trong trình duyệt do không có browser surface trong phiên điều khiển này.

Vòng chỉnh theo bảng mẫu gần nhất: tái sinh `neutral.rml` và `parts.rml`, chạy lại `rive . --verify` (0 lỗi, 0 cảnh báo), `rive inspect . --summary` (`problems: []`), xuất `.riv` và render lại PNG ở 500/240/120/80 px. Các ảnh nhỏ dùng `--fit=contain` để đặt artboard 500 px trọn trong viewport. Đã xem trực tiếp bản 500, 120 và 80 px.

## Vấn đề hình tiếp theo

Rig đã dùng artwork front V2 để thử bảy mood, wave và sleep. Bước hình tiếp theo là tinh chỉnh lông má, mí mắt sleepy và mỏ mở trên các render `../build/mood-review.png`, `../build/wave-mid.png` và `../build/sleep-late.png`. Các góc 3/4, side và back chưa được dựng.
