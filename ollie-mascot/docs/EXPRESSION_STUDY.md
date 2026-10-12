# Ollie — phân tích biểu cảm và thư viện chuyển động 01

**Cập nhật cánh 04:** đã vẽ lại đường bao và bảy lớp lông cho 15 tư thế cánh chuyển động, gồm một dáng ôm đạo cụ riêng theo ảnh mẫu. Bốn cảnh còn lại giữ cánh front gốc. Xem [phân tích cấu tạo](WING_STUDY.md) và [bảng 95 khung của cả 19 cảnh](../playground/wing-review.html).

Ngày dựng: 09/10/2026. Tham chiếu: bảng sticker 4 hàng × 5 cột người dùng gửi trong cuộc trò chuyện. Artwork front hiện tại vẫn là chuẩn nhận diện; bảng sticker cung cấp ý tưởng biểu cảm, tư thế và đạo cụ, không thay thế tỉ lệ nhân vật.

## Đọc bộ mẫu

Đầu lớn, mặt kem, mắt xanh, chỏm lông ba tầng, chồi lá và chân vàng là sáu dấu hiệu cần giữ. Khi gắn đạo cụ, vẫn phải đọc được mặt, dáng cú và ít nhất một phần ngực. Với các cảnh như laptop hoặc ôm tim, đạo cụ che huy hiệu là có chủ đích.

Mỗi hình gồm bốn lớp. **Nét mặt** truyền cảm xúc; **tư thế cánh và thân** truyền hành động; **đạo cụ** nói rõ ngữ cảnh; **hiệu ứng phụ** nhấn cường độ. Chỉ đổi mắt sẽ khó phân biệt “đang học”, “quản lý tiền” và “chuẩn bị tập luyện”. Chỉ thêm đạo cụ lên tư thế đứng cũ cũng chưa tạo thành một hành động.

- Mắt cười khép + má hồng: yêu thương, khích lệ, ăn mừng. Phân biệt bằng tư thế ôm, dang cánh hoặc nâng cúp.
- Mí nặng + vai rủ: mệt. Mày nâng ở giữa + giọt nước mắt: buồn. Mắt mở rộng + mồ hôi + cánh chạm má: lo lắng. Ba trạng thái này có nhịp riêng.
- Mắt nhắm + thân ổn định: thư giãn hoặc trân trọng. Mũ ngủ/cánh che mỏ chuyển nghĩa sang buồn ngủ; tay mở thấp và chân thu vào chuyển nghĩa sang thiền.
- Cánh luân phiên + bước chân + vệt phía sau: chạy. Cánh giữ thanh tạ cùng nâng/hạ: tập sức mạnh. Hào quang và ánh mắt sáng là năng lượng, không thay thế hai động tác vận động.
- Ví, heo đất, checklist, đồng hồ và laptop phải đọc được ở cỡ nhỏ. Chi tiết nhỏ chỉ bổ trợ; hình khối chính và màu sắc làm nhiệm vụ nhận diện.

## Đối chiếu đủ 20 ô

Tọa độ “hàng.cột” tính từ góc trên trái. Thời lượng tính ở 60 fps. Các cảnh mới được dựng nhìn thẳng/ba phần tư nhẹ bằng rig front; cảnh chạy không phải một rig quay nghiêng hoàn chỉnh.

| Ô | Cảnh / key | Tư thế và đạo cụ | Nhịp / thời lượng |
|---|---|---|---|
| 1.1 | Vẫy chào / `wave` | Cánh vẫy bên đầu, mỏ cười; giữ cử chỉ đã có | Một lần rồi trả về mood |
| 1.2 | Nảy ý tưởng / `idea` | Cánh ở cằm, đầu nghiêng, bóng đèn bên đầu | Nghĩ → sáng lên → gật, 3 s |
| 1.3 | Ôm yêu thương / `love` | Mắt cười, má hồng, hai cánh ôm tim | Tim và cánh nhún nhẹ, 2,67 s |
| 1.4 | Ăn lành mạnh / `nutrition` | Nháy mắt, nâng bát rau, cà chua và cà rốt | Nâng bát mời rồi hạ, 3 s |
| 1.5 | Chạy bộ / `running` | Thân nghiêng, cánh và chân luân phiên, vệt tốc độ | Bước trái/phải, 0,8 s |
| 2.1 | Mệt rồi / `tired` | Mí nặng, quầng mắt nhẹ, đầu và cánh rủ | Thở và cúi đầu chậm, 4 s |
| 2.2 | Hơi lo lắng / `worried` | Mày nâng giữa, mỏ tròn, cánh chạm má, mồ hôi | Lắc rất nhẹ, giọt trượt/tan, 2 s |
| 2.3 | Vào guồng / `pomodoro` | Tai nghe, laptop có hình cà chua, cánh gõ | Gõ luân phiên, gật đầu, 2,4 s |
| 2.4 | Đến giờ nghỉ / `bedtime` | Mũ ngủ, mắt nhắm, cánh che mỏ, chữ Z | Ngáp/gật chậm, 4 s |
| 2.5 | Bạn làm được / `cheer` | Mắt cười, giơ cả hai cánh, tia sáng | Nhún và mở cánh, 1,67 s |
| 3.1 | Cần cân đối lại / `sad` | Mày buồn, giọt nước mắt, ví rỗng nứt minh họa | Nhìn xuống và thở ra, 3,5 s |
| 3.2 | Quản lý chi tiêu / `wallet` | Nâng ví có tiền và xu | Ví và tờ tiền nâng nhẹ, 3 s |
| 3.3 | Tiết kiệm nhỏ / `saving` | Ôm heo đất; xu ở phía trên khe | Xu hạ vào khe, heo nhún, 3 s |
| 3.4 | Xong một việc / `checklist` | Nháy mắt, bảng công việc và dấu tích lớn | Nâng bảng, dấu tích bật/ổn định, 2,5 s |
| 3.5 | Ăn mừng / `celebrate` | Cúp một bên, cánh kia mở, giấy màu | Nâng cúp và nhún, 2 s |
| 4.1 | Nhắc giờ nhẹ / `alarm` | Hai cánh giữ đồng hồ chuông | Rung hai nhịp rồi nghỉ, 2 s |
| 4.2 | Tập một chút / `workout` | Hai cánh cùng giữ thanh tạ, mồ hôi | Nâng → giữ → hạ có kiểm soát, 2,5 s |
| 4.3 | Hít thở chậm / `meditate` | Mắt nhắm, cánh mở thấp, chân thu, vòng thở | Vòng mở/thu và thân nâng/hạ, 6 s |
| 4.4 | Gửi lời cảm ơn / `letter` | Mắt nhắm dịu, nâng phong thư có dấu tim | Nâng thư và nghiêng đầu, 3,33 s |
| 4.5 | Đầy năng lượng / `energized` | Mắt ánh sao, cánh mở nhẹ, hào quang lá | Hào quang nở và thân nhún, 2 s |

## Chuyển động và cách dùng

Ưu tiên một hành động chính trong mỗi cảnh. Đạo cụ chuyển động chậm hơn các tín hiệu ngắn như dấu tích, đồng xu hoặc chuông để mắt người xem biết nhìn vào đâu. Các keyframe đầu/cuối của từng vòng quay về cùng tư thế. Chớp mắt chỉ được thêm vào các cảnh mở mắt; các đường mắt cười/nhắm không cần chớp thêm.

Cả 19 cảnh giữ tỉ lệ nhân vật bằng bảy mood gốc; khoảng trống cho đạo cụ và hiệu ứng được bố trí quanh Ollie. Dấu hỏi đã chỉnh của `confused` giữ nguyên. Các cảnh ôm/cầm dùng tư thế uốn từ bảy lớp cánh gốc; chỉ cánh tham gia động tác được thay thế. Khi chuyển về mood gốc, ngủ hoặc vẫy, các lớp mới được xóa bằng Solo, cánh và khớp chân trở lại giá trị phù hợp.

`bedtime` là biểu cảm chuẩn bị nghỉ, không tự đặt `isAsleep`. `isAsleep=true` vẫn ưu tiên tư thế ngủ thật, ẩn đạo cụ và chặn cử chỉ vẫy như rig cũ. Chạm Ollie ghi `isAsleep=false`, chạy giật mình rồi trở lại mood được chọn.

Các vòng `running`, `alarm`, `workout` có nhiều năng lượng, nên dùng trong vùng minh họa hoặc khi người dùng chọn xem. Với thông báo kéo dài, có thể dừng ở tư thế đại diện. “Buồn vì ví rỗng” là một lựa chọn minh họa; ứng dụng nên dùng lời nhắc trung tính khi nói về số dư thật, tránh tạo cảm giác phán xét.

## Cấu trúc và tái tạo

- `data/expressions.json`: tên, nhóm, đối chiếu ô mẫu, thời lượng, mô tả mặt/đạo cụ/chuyển động/cách dùng.
- `tools/expression_library.py`: hình vector và keyframe của 19 cảnh. Ba lớp Solo là `SceneProps`, `SceneFace`, `SceneBackdrop`.
- `data/model.json`: nối thêm 19 giá trị vào cuối `Mood`. Bảy giá trị đầu giữ nguyên tên, thứ tự và ID `0:601`–`0:607`. `Mascot`, `Default`, `Main`, `mood`, `isAsleep`, `wave` giữ nguyên tên và kiểu.
- `data/presets.json`: 19 preset mới; `data/features.json` chỉ đánh dấu đạo cụ đã dựng là có sẵn.
- `playground/index.html`: chọn cảnh, lọc nhóm, xem mô tả, thử trực tiếp; PNG fallback được xuất từ rig.
- `build/expressions/`: ảnh từng cảnh, strip đầu/giữa/cuối vòng và báo cáo kiểm tra. `playground/frames/expressions-contact.png` là bảng tổng hợp có thể chia sẻ.

```powershell
python tools/build_ollie.py
rive . --verify
rive inspect . --summary
python tools/build_expressions.py
rive . --once
Copy-Item build/ollie-mascot.riv dist/ollie.riv
python tools/build_data.py --check --package
```

`python tools/build_kit.py` thực hiện cả luồng, bao gồm kiểm tra hành vi cũ và bộ cảnh mới. Các đạo cụ là vector cách điệu theo bảng mẫu, không phải bản trace chính xác từng sticker. Bản dựng cần được xem và điều chỉnh theo phản hồi thẩm mỹ tiếp theo.
