# Prompt sản xuất linh vật Ollie từ bộ mẫu

Sử dụng prompt này với bảng thiết kế Ollie được đính kèm. Bảng mẫu là chuẩn cho nhận diện và phong cách. Bản Rive kỹ thuật cũ chỉ dùng để hiểu cấu trúc tương tác; không giữ lại các đường nét còn cứng.

## Giai đoạn 1 — neutral front, ưu tiên cao nhất

> Bạn là họa sĩ nhân vật 2D và technical artist Rive. Hãy dựng **Ollie**, một cú xanh nhỏ đại diện cho trợ lý AI về lập kế hoạch, tài chính lành mạnh và sức khỏe. Tính cách: ấm áp 60%, thông minh 25%, tinh nghịch nhẹ 15%. Chỉ dựng **một tư thế neutral nhìn thẳng** trên artboard 500×500, nền trong suốt. Nhân vật nằm khoảng x=95–405, y=55–455. Dùng vector Bézier chỉnh được từng phần, đường viền xanh rừng đậm, mép cong mềm, không dùng tổ hợp hình tròn, capsule hay tam giác làm đường viền cuối.

### Hình dáng và tỷ lệ

- Đầu chiếm khoảng 55–60% chiều cao nhân vật, rộng hơn thân; hai bên má tròn nhưng dưới cằm hơi thu. Đỉnh đầu có hai cụm lông cú gồm những lá lông ngắn chồng nhau, không thành sừng nhọn.
- Thân chiếm 28–32%, thon ở cổ, tròn mềm ở giữa, có 2–3 nhịp lông rất nhẹ ở đáy. Chân chỉ 5–7%, cam ấm, mỗi chân có pad và 2–3 gờ ngón đơn giản.
- Mầm lá trên đầu chiếm khoảng 8–12%, gồm cuống hơi cong, lá chính hướng lên và lá phụ lệch bên. Giữ độ bất đối xứng nhỏ để có sức sống.

### Mặt và biểu cảm neutral

- Mảng mặt màu kem hình tim cú: hõm nhẹ ở chính giữa trán, hai thùy mềm ôm mắt, dưới mặt thu về mỏ. Diện tích khoảng 58–64% mặt trước đầu. Không dùng oval kem lớn.
- Mỗi mắt là các nhóm độc lập: `EyeWhite`, `IrisOuter`, `IrisInner`, `Pupil`, `PrimaryHighlight`, `SecondaryHighlight`, `UpperLid`, `LowerLid`. Mắt mở, dịu, nhìn về phía trước; ánh sáng chiếu từ trên trái ở cả hai mắt. Mống mắt xanh sâu, lõi xanh sáng, đồng tử xanh gần đen. Mí trên theo độ cong của mắt; không vẽ lông mày kiểu người.
- Mỏ nhỏ, cam, có phần trên cong và phần dưới sẫm hơn. Miệng neutral chỉ gợi một nụ cười nhẹ, không chiếm trọng tâm.

### Cánh và ngực

- Mỗi cánh nghỉ tự nhiên bên thân. Nhóm gồm `WingBase`, `PrimaryFeatherA/B/C`, tùy chọn `TipHighlight`; lông dạng lá giọt nước, chồng lớp, đầu dưới so le để ở 120 px vẫn thấy nhịp lông. Tránh viền bao tổng thể hình găng tay hoặc giáp.
- Mảng ngực màu kem cùng họ với mặt, hẹp ở trên, rộng giữa, có đầu lông mềm ở dưới. Huy hiệu AI nằm trong ngực: vòng mint nhẹ đường kính khoảng 42–54 px ở artboard 500 px, biểu tượng hai lá trắng/kem, không dùng hào quang cyan lớn.

### Màu và nét

| Vai trò | Màu tham chiếu |
|---|---|
| Viền | `#173F2A` |
| Lông sâu | `#286B3B` |
| Xanh chính | `#44924D` |
| Xanh tươi | `#78B95B` |
| Điểm sáng | `#A2D66D` |
| Mặt/ngực | `#FFF2CF` |
| Bóng kem | `#EEDFB9` |
| Mống mắt sâu | `#123E28` |
| Mống mắt giữa | `#2F8A45` |
| Mống mắt sáng | `#79CE69` |
| Mỏ/chân | `#F6A62B`, bóng `#D97A18` |
| AI mint | `#67DFC1` |

Viền chính khoảng 4–5 px ở 500 px, nét nội bộ khoảng 2.5–3.5 px. Mỗi phần lớn chỉ dùng màu nền, một mảng bóng và một mảng sáng. Chiều sâu chủ yếu đến từ lông chồng nhau. Tránh hiệu ứng 3D, không khí máy móc, màu cyberpunk và glow mạnh.

### Thứ tự lớp và file bàn giao giai đoạn 1

Thứ tự từ sau ra trước: bóng nền nhẹ → đuôi → thân → ngực → chân → cánh → đầu → mảng mặt → mắt → mỏ → lông đầu/má → mầm lá → huy hiệu AI. Đặt tên nhóm rõ và giữ mỗi bộ phận phù hợp với rig sau này.

Xuất `neutral_500.png`, `neutral_240.png`, `neutral_120.png`, `neutral_80.png`, nguồn vector/Rive chỉnh sửa được, và `ollie_parts.png` tách đầu, mặt, hai mắt, mỏ, hai cánh, thân, ngực, hai chân, mầm lá, đuôi, huy hiệu AI. Kiểm tra bốn kích thước trực tiếp cạnh ảnh mẫu. Nếu đầu còn tròn, mặt quá phẳng, cánh giống giáp, mắt thô hoặc huy hiệu lấn át mắt thì sửa neutral trước khi tiếp tục.

## Giai đoạn 2 — chỉ sau khi front neutral được duyệt

Từ **cùng một thiết kế đã duyệt**, dựng góc 3/4, nghiêng bên, mặt sau. Giữ tỷ lệ mắt, mỏ, má, mầm lá và ngôn ngữ lông nhất quán. Không bóp méo bản front để thuận tiện làm góc khác. Sau đó đặt pivot ở cổ, vai, gốc lá, đầu nối chân và gốc lông chuyển động.

## Giai đoạn 3 — biểu cảm và animation

Dùng **một rig**, không tạo bảy hình cú riêng: `neutral`, `happy`, `wink`, `focus`, `surprised`, `sleepy`, `confused`. Biểu cảm xuất phát từ mí, đồng tử, mỏ, nghiêng đầu, cánh và lá. `focus` không thành giận; `sleepy` không thành cau có; `wink` là đường mí cong tự nhiên. Idle chỉ gồm thở rất nhẹ (~2.5 s), chớp mắt, lá đung đưa và dịch mắt nhỏ. Chuyển động thân khoảng 1–2.5%; đầu khoảng 2°; cánh nghỉ khoảng 1–3°. Giữ nguyên độ dày nét và chồng lớp lông khi cử động.

Trước mỗi giai đoạn tiếp theo: verify Rive, render PNG, xem ảnh trực tiếp ở 500/120 px, so ảnh mẫu, sửa các đường cong còn cứng. Báo rõ phần đã cải thiện, phần còn dưới chuẩn và kết quả kiểm tra. Chỉ chuyển rig/animation khi neutral được duyệt.
