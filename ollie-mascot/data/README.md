# Dữ liệu build Ollie

Đây là dữ liệu được công cụ build sử dụng. Tài liệu cú pháp Rive nằm riêng ở `../docs/rive-cli/`.

| Nguồn chỉnh sửa | Vai trò | Đầu ra |
|---|---|---|
| `model.json` | Tên/ID artboard, machine, View Model, enum, property và giá trị mặc định | `../data.rml`, `../build/data/contract.json` |
| `presets.json` | 29 bộ giá trị và chuỗi advance/click để chạy thử | `../build/data/presets.json`, `tools/preview.py` |
| `expressions.json` | 19 cảnh mới: tên, nhóm, ô mẫu, thời lượng, nét mặt, đạo cụ và chuyển động | Playground, `../dist/data/expressions.json` |
| `features.json` | Tính năng Ollie dùng preset/nhóm thoại nào; đạo cụ nào còn thiếu | `../dist/data/features.json` |
| `../speech/lines.vi.json` | 20 câu tiếng Việt, placeholder, mood/gesture, điểm neo và thời gian hiển thị | `../dist/speech/lines.vi.json`, playground |

Chạy từ thư mục `ollie-mascot`:

```powershell
python tools/build_kit.py
python tools/preview.py --list
python tools/preview.py happy
python tools/preview.py wake --capture
```

`preview.py` dùng runtime đã dựng gần nhất. Nếu vừa sửa model/rig, chạy build trước. Preset `wake` bắt đầu ngủ: preview tương tác cần chạm vào Ollie, còn `--capture` phát lại cả chuỗi chạm đã định nghĩa.

Các quy tắc dữ liệu:

- `mood` có 26 giá trị: giữ nguyên 7 giá trị đầu và nối thêm 19 cảnh. ID/thứ tự cũ được bảo toàn; mọi giá trị mới có animation và transition tương ứng.
- `isAsleep` dùng boolean JSON thật `true`/`false`, không phải chuỗi.
- `wave` là trigger: đặt trong mảng `triggers`, không đặt vào `values` như một trạng thái bật/tắt.
- `capture_steps.advance` là số frame ở 60 FPS. `click` là tọa độ artboard, không phải tọa độ màn hình.
- Placeholder thoại phải khai báo, và ứng dụng phải cung cấp dữ liệu thật. Playground bỏ qua câu thiếu dữ liệu để không hiện `{minutes}` hoặc tự điền số liệu giả.
- Lời thoại do ứng dụng vẽ bên ngoài `.riv`; không nhúng font/chuỗi vào vector.
- `mood_only`, nếu được dùng trong features, nghĩa là chỉ có biểu cảm phù hợp và đạo cụ ghi trong `pending_prop` chưa được dựng. Các ánh xạ hiện tại dùng cảnh có sẵn; xem `expressions.json` để biết đúng đạo cụ của từng cảnh.

`python tools/build_data.py --check` chỉ kiểm tra, không ghi đè model. Sau khi sửa model, dùng `python tools/build_ollie.py` hoặc full build để sinh lại runtime; khi chưa dựng lại, kiểm tra sẽ báo dữ liệu nhúng khác nguồn.

`build/data/rig-map.json` được trích từ runtime thực tế: 15 node chính cùng pivot cục bộ và 37 timeline. Ba Solo bổ sung chứa đạo cụ, nét mặt phụ và hiệu ứng nền. Không sửa file này làm nguồn; sửa generator/scaffold rồi dựng lại.
