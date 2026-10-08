# Ollie — phân tích mẫu front

Chuẩn chính: `reference/ollie-front-master.png`, 1254×1254 RGBA, do người dùng cung cấp ngày 08/10/2026. Giữ nguyên toàn bộ canvas; đổi sang artboard 500×500 bằng hệ số `500/1254`, không tự crop rồi làm lệch tỉ lệ.

## Đặc điểm phải giữ

1. **Tỉ lệ chibi:** đầu lớn và gần tròn, rộng hơn thân; chân thấp, cánh gập dài ôm hai bên thân.
2. **Chồi hai lá bất đối xứng:** lá chính nghiêng phải, đầu nhọn; lá nhỏ mở sang trái. Chồi là một nét nhận diện, không thay bằng hai hình bầu dục.
3. **Chỏm ba tầng:** mỗi bên có ba đầu lông vuốt ra ngoài, lớp sáng liền mạch chạy thành chữ V sâu giữa trán. Mép lá có góc nhọn có chủ đích và phần bụng cong.
4. **Mặt kem một khối:** hai thùy lớn ôm mắt, đỉnh giữa hạ xuống sâu, má nở rộng; dưới tách thành ba lông cổ mềm. Không có đường chia đứng ở giữa mặt.
5. **Mắt lớn có tròng trắng:** mí trên đen dày, đuôi mi phía ngoài, mống mắt xanh, đồng tử gần đen. Hai đốm phản sáng cùng phía nguồn sáng; không lật đốm sáng khi phản chiếu mắt phải.
6. **Mỏ cười mở:** mỏ trên vàng cam có bờ cong, nối liền khoang miệng sẫm và lưỡi đỏ. Neutral dùng chính nụ cười này; mỏ kín là biến thể cho ngủ/suy nghĩ.
7. **Cánh lá xếp lớp:** màu rừng ở lớp sâu, xanh tươi giữa, hai mảng lime trên cánh. Lông dài có đầu nhọn và phần vai tròn.
8. **Ngực kem và huy hiệu:** lông ngực phân tầng, huy hiệu lớn màu mint, viền trắng và hai lá trắng. Đặt đúng trên ngực, không thu nhỏ thành huy hiệu phụ.
9. **Chân cam ba ngón:** một khối bàn chân liên tục, phân ngón bằng rãnh và bóng; không dùng ba hình tròn rời.

## Điểm neo trên artboard 500×500

Các số khớp với `build/trace/landmarks.png`; số làm tròn để đọc. Nguồn Bézier dùng tọa độ trên ảnh 1254×1254.

| Mốc | Vị trí gần đúng | Vai trò |
|---|---|---|
| 01 | 305, 14 | đầu lá chính |
| 02 | 250, 106 | chân chồi |
| 03 | 189, 223 | tâm mắt trái |
| 04 | 311, 223 | tâm mắt phải |
| 05 | 250, 248 | trung tâm mỏ |
| 06 | 250, 324 | chóp lông cổ |
| 07 / 08 | 166 / 334, 318 | vai, tâm xoay cánh |
| 09 | 250, 366 | tâm huy hiệu |
| 10 / 11 | 200 / 300, 474 | bàn chân |

## Tách hình để animate

`artwork/build_artwork.py` là nguồn duy nhất cho nét front, xuất đồng thời SVG và RML. Path dùng đoạn cubic rõ tay nắm; không tự làm trơn qua toàn bộ mốc vì sẽ làm tròn sai đầu lá. Nguồn khai báo lớp từ sau ra trước, khi xuất RML đảo thứ tự để khớp quy tắc vẽ Rive.

Rig giữ ID cố định cho đầu, cánh, mắt, miệng và dữ liệu. Nét nhập vào được cấp ID mới. Tâm chớp mắt nằm ngang tâm mắt để mắt không trượt xuống khi scaleY đóng lại. Góc cánh được retarget từ dáng nghỉ Nez về góc 0 của bản front; biên độ nhún cơ thể giảm để chồi lá không vượt khung.

## Phạm vi bản hiện tại

Ảnh front xác định tốt hình dáng chính. Bảy mood và chuyển động là phần triển khai mới dựa trên hướng biểu cảm từ bảng cũ; chưa phải expression sheet cuối cùng được người dùng duyệt. Lớp sáng/tối tái dựng bằng gradient và mảng vector, không giữ toàn bộ biến thiên màu từng pixel của raster.

Chờ bổ sung: mặt nghiêng trái/phải, sau lưng, biểu cảm cần khớp tuyệt đối, cánh mở nhìn rõ từng lông, props tính năng. Sau mỗi ảnh mới, cập nhật ưu tiên trong manifest và đối chiếu lại frame liên quan.
