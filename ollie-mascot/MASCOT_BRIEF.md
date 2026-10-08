# Ollie — mascot brief

Ollie là cú lá xanh chibi, người bạn đồng hành giúp lập kế hoạch, theo dõi thói quen và nhắc lịch. Chuẩn nhận diện hiện tại là ảnh front **Cú lá xanh chibi đáng yêu.png** người dùng cung cấp, lưu tại `reference/ollie-front-master.png`.

- Đầu lớn, mặt kem hai thùy liền nhau, mắt xanh rộng với mi đen.
- Chồi hai lá bất đối xứng; chỏm lông ba tầng, phần sáng hình V sâu.
- Mỏ cam cười mở, cánh lá xếp nhọn, thân xanh/ngực kem, chân cam.
- Huy hiệu mint tròn lớn với biểu tượng hai lá trắng.

Giải phẫu và điểm neo: [docs/MODEL_BRIEF.md](docs/MODEL_BRIEF.md). Nguồn nét vẽ: `artwork/build_artwork.py`; hình cần đối chiếu: [review.html](review.html).

Hợp đồng hiện có: Artboard `Runtime` 500×500, State Machine `Main`, View Model `Mascot`/`Default`; 7 mood, `isAsleep`, `wave`. Nguồn chuẩn nằm trong [data/model.json](data/model.json). Lời thoại: [speech/lines.vi.json](speech/lines.vi.json), do app hiển thị bên ngoài hình Rive.

Nguồn và cách build: [docs/BUILD_DATA.md](docs/BUILD_DATA.md). Chỉnh hình/chuyển động: [docs/TUNING.md](docs/TUNING.md). Góc nghiêng, sau và đạo cụ tính năng cần thêm ảnh để dựng tiếp; preset biểu cảm không đại diện cho một đạo cụ đã hoàn thành.
