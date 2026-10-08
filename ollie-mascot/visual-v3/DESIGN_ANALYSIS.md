# Mổ xẻ mẫu Ollie và bản dựng V3

## Hai góc nhìn trong bảng mẫu

Hình Ollie lớn là minh họa góc 3/4, một cánh nghỉ lớn ở phía trái ảnh và cánh kia xòe. Nó cho biết chất liệu lông, ánh sáng, tính cách và độ giàu lớp. Hình **Front** trong ô turnaround mới là mốc cho rig nhìn thẳng. Sao chép nguyên tỉ lệ và tư thế của hình lớn vào rig front sẽ làm mắt, cánh và vai lệch khi đổi biểu cảm. Bản V3 lấy cấu trúc từ Front, ngôn ngữ màu và lông từ hình lớn.

Ở hình lớn, ánh sáng đến từ trên trái: trán và mép trên cánh ngả vàng xanh, vùng dưới cánh và sau đầu xanh rừng, mặt kem ngả vàng ở vùng sâu. Hình không có đường viền đen đồng đều quanh từng mảng; đường viền mạnh nhất ở silhouette, mí trên và ranh giới lông chính. Đây là lý do bản V2 trông như icon phẳng dù đủ bộ phận.

## Những dấu hiệu nhận diện phải giữ

| Phần | Quan sát từ mẫu | Quy tắc dựng V3 |
|---|---|---|
| Đầu | Khối rộng, hai chỏm lông quét lên, má thu dần về cổ | Đường bao Bézier không tròn đều; cụm lông đỉnh đầu gồm nhiều lớp ngắn |
| Mặt | Hai thùy kem gặp nhau thành hõm trán, phần dưới có lông cổ | Một đường bao kem liền với ánh sáng hai bên và hõm trán; không để lộ đường ráp dọc khi đầu nghiêng |
| Mắt | Lòng trắng nổi rõ, mí trên đậm, mống mắt có chiều sâu, đốm sáng đặt cao | Mỗi mắt là các path riêng; mống xanh có chuyển sắc nhẹ, viền mắt mỏng hơn mí |
| Mỏ | Cam ấm, nhỏ và cong, phần dưới sẫm | Mỏ giữ vai trò phụ so với ánh mắt; miệng mở thuộc biến thể biểu cảm |
| Cánh | Vai liên tục với thân, lông dài ngắn so le, mảng sáng nằm trên lớp ngoài | Một silhouette nền, các lông bên trong ít viền để tránh cảm giác áo giáp |
| Ngực/Core | Ngực kem có nhịp lông; biểu tượng lá mint sáng nhưng không át mắt | Lông ngực rời, vòng Core nhỏ và sáng vừa phải |
| Mầm lá | Một lá chính vươn lên, lá phụ lệch bên | Cuống cong, lá bất đối xứng và có gân rõ ở 500 px |

## Vì sao bản trước trông bẩn

- Trán là hai dải xanh sáng quá rộng, tạo hình chữ M cứng và che cấu trúc lông.
- Hai má là các khối oval trôi hai bên mặt, không mọc từ viền đầu.
- Mỗi lông cánh có viền riêng dày nên cánh trông như nhiều tấm giáp xếp tầng.
- Lòng trắng, iris và mí đều có viền đậm, làm mắt giống kính tròn hơn mắt cú.
- Ngực và lưng quá phẳng so với độ nhiều lớp trong tranh mẫu.

## Cách biểu cảm dùng chung một rig

Mắt là điểm nhận diện mạnh nhất nên mọi mood phải giữ vị trí hốc mắt và độ cong đầu, chỉ thay mí, hướng nhìn và độ mở. Joyful nhắm mắt thành hai vòng cung cao và mở mỏ; attentive giữ mắt mở nhưng bớt chuyển động; thinking lệch hướng nhìn và đưa một cánh gần mỏ; motivating nháy một mắt và giơ cánh; surprised mở mắt và mỏ; peaceful nhắm mắt mềm và hạ nhịp Core. Dự án hiện có bảy mood kỹ thuật và wave/sleep. Các đạo cụ và tư thế riêng trong bảng mẫu chưa được dựng.

## Phạm vi V3

`build_neutral.py` dựng lại hình front bằng các path Bézier có tên riêng. `../tools/build_ollie.py` nhập các nhóm đó vào rig đang có và giữ ID của đầu, cánh, mắt, chân, Core cùng state machine. Bản V2 ở `../visual-v2/` còn nguyên để so sánh. V3 là cách diễn giải vector cho runtime, chưa phải bản sao từng pixel của tranh minh họa. Góc side/back và các đạo cụ trong cảnh ứng dụng cần nguồn riêng sau khi hình front ổn.

Phần còn lệch rõ nhất so với tranh mẫu là độ phong phú của lông đỉnh đầu, chuyển sắc mềm trong cánh và các tư thế 3/4. V3 ưu tiên hình rõ ở 120 và 80 px cùng khả năng đổi mood trong Rive. Nếu cần mức hoàn thiện như hình Ollie lớn, phải dựng thêm artboard 3/4 riêng với rig cánh và mặt được vẽ theo phối cảnh đó; không thể đạt bằng cách xoay ngang hình front.
