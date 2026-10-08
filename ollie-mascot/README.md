# Bộ mẫu Ollie

Bản dựng ngày 08/10/2026 dùng **“Cú lá xanh chibi đáng yêu.png”** làm chuẩn front mới. Nét vẽ được dựng lại bằng đường Bézier có tay nắm độc lập: đầu lớn, chỏm ba tầng, mắt rộng, mỏ cười, cánh lá và huy hiệu tròn. Đây là bản để đối chiếu và tiếp tục chỉnh sửa theo ảnh người dùng bổ sung, chưa phải thiết kế đã duyệt.

Mở **[review.html](review.html)** để xem ảnh gốc cạnh vector, kéo thanh chồng nét, xem từng bộ phận, biểu cảm và chuỗi chuyển động. **[Playground](playground/index.html)** dùng để thử mood, vẫy, ngủ và chạm đánh thức. Khi runtime web không tải được, playground dùng các frame được xuất từ chính Rive.

## Các file chính

| Mục | Vị trí |
|---|---|
| Ảnh front nguyên gốc | `reference/ollie-front-master.png` |
| Nguồn gốc, hash, quy tắc ưu tiên, góc còn thiếu | `reference/manifest.json` |
| Phân tích hình dáng & mốc neo | [docs/MODEL_BRIEF.md](docs/MODEL_BRIEF.md) |
| Nguồn nét vẽ, chia bộ phận | `artwork/build_artwork.py` |
| Vector SVG | `artwork/ollie-front.svg` |
| RML front tĩnh, sinh tự động | `artwork/front.rml` |
| Bộ dựng rig | `tools/build_ollie.py` |
| Runtime hoàn chỉnh, sinh tự động | `runtime.rml` |
| Nguồn dữ liệu có thể chỉnh | `data/model.json` → sinh `data.rml` |
| Preset / ánh xạ tính năng | `data/presets.json`, `data/features.json` |
| Lời thoại tiếng Việt | `speech/lines.vi.json` |
| Phân tích cấu trúc data/build so với Nez | [docs/BUILD_DATA.md](docs/BUILD_DATA.md) |
| Tài liệu CLI lưu cục bộ | `docs/rive-cli/`, bản tiện mở `build/doc_*.txt` |
| Kịch bản 28 probe | `tests/poses.json` |
| Kết quả kiểm tra | `build/check-report.json` |
| Xuất cho ứng dụng | `dist/ollie.riv`, `dist/ollie-front.svg`, `dist/ollie-front.png` |

## Dựng lại trên Windows

Chạy từ thư mục `ollie-mascot`. Cần Python có Pillow và Rive CLI; công cụ tự tìm rive trong PATH hoặc thư mục .rive/bin của người dùng.

```powershell
python tools/build_kit.py
```

Lệnh này dựng artwork, ghép rig, verify, inspect, chụp probe thật từ state machine, kiểm tra hành vi, tạo ảnh đối chiếu, cập nhật playground và xuất .riv unsigned cục bộ. Không đăng tải lên tài khoản Rive.

Build đồng thời đồng bộ tài liệu đúng phiên bản CLI, kiểm tra data/preset/lời thoại và đóng gói `dist/data/` + `dist/speech/` cho ứng dụng. Đổi tên property hoặc ID sẽ bị kiểm tra với binding của rig trước khi xuất. Chi tiết: [data/README.md](data/README.md).

```powershell
# Rive tương tác; giữ tỉ lệ khi đổi kích thước cửa sổ
& "$env:USERPROFILE\.rive\bin\rive.exe" . --fit=contain

# Chạy lại probe
python tools/check.py tests/poses.json

# Chồng ảnh chuẩn và nét vector; cập nhật khi front.rml thay đổi
python tools/trace.py --watch

# Tạo lại ảnh so sánh tĩnh
python tools/overlay.py

# Chạy preset từ data/presets.json; --capture xuất ảnh + dữ liệu thật
python tools/preview.py sleep --capture

# Kiểm tra nguồn dữ liệu và liên kết runtime hiện tại
python tools/build_data.py --check

# Làm mới bộ tài liệu CLI và schema đã lưu
python tools/sync_cli_docs.py --refresh
```

## Cấu trúc build tương tự Nez

```text
build/
  ollie-mascot.riv         runtime unsigned
  problems.log, rive.log   chẩn đoán Rive
  manifest.json           danh sách đầu ra
  check-report.json       kết quả hành vi + 28 captures
  inspect-summary.json    cấu trúc rig đã resolve
  front.png               hình tĩnh render bằng Rive
  front-alpha.png         ảnh bỏ nền preview
  construction.png        từng bước dựng
  parts.png               15 ô bộ phận
  moods/                  bảy biểu cảm + ngủ + contact sheet
  rv/                     project review độc lập; stages/ chứa từng bước
  trace/                  ảnh chuẩn, overlay, lưới, landmarks, project trace
  probe-t*.png/.json      frame và View Model tương ứng
  idle-strip.png          thở, đầu/cuối vòng, chớp mắt
  wave-strip.png          nghỉ, vẫy, trở về
  sleep-strip.png         thức, ngủ, giật mình, thức lại
  size-*.png              80 / 120 / 240 / 500 px
```

V2/V3 được giữ làm lịch sử. Nguồn hiện tại là artwork/, không phải visual-v3/. Thư mục web-pet/ là bản web riêng, không nằm trong gói Rive và chưa được chuyển sang artwork mới này.

## Dữ liệu runtime

Artboard Runtime, 500×500, nền trong suốt. State machine Main; View Model Mascot, instance Default.

| Thuộc tính | Kiểu | Giá trị |
|---|---|---|
| mood | enum | neutral, happy, wink, focus, surprised, sleepy, confused |
| isAsleep | bool | ngủ/thức; chạm nhân vật đặt về false |
| wave | trigger | vẫy cánh khi đang thức |

Rig có 7 layer, 17 timeline. Kiến trúc animation được lấy từ Nez, lưu snapshot riêng trong tools/scaffold/, rồi thay hình nhân vật bằng Ollie và chỉnh điểm xoay/biên độ. Build Ollie không phụ thuộc các sửa đổi tương lai của Nez và không chỉnh file của Nez. `data/model.json` là nguồn chính; `tools/build_data.py` sinh `data.rml`, sau đó nhúng vào runtime. File data.rml riêng bị loại khỏi compile trực tiếp để tránh khai báo trùng.

## Thêm ảnh để chỉnh tiếp

Đặt ảnh bổ sung trong reference/incoming/ và ghi rõ góc nhìn hoặc biểu cảm. Ảnh front mới là chuẩn nhận diện; bảng thiết kế cũ chỉ cung cấp hướng biểu cảm, màu và bối cảnh. Khi ảnh mâu thuẫn, ghi lại quyết định trong reference/manifest.json trước khi thay nét. Xem [docs/TUNING.md](docs/TUNING.md) để biết sửa file nào.

Hiện chỉ có front đủ rõ để dựng chính xác. Chưa có bộ vector nghiêng/sau hoặc đạo cụ được xác nhận; các mục đó được đánh dấu chờ ảnh. Kiểm tra tự động xác nhận hành vi và tránh cắt hình ở các frame chọn trước; độ giống nghệ thuật vẫn cần xem ảnh đối chiếu và phản hồi của người dùng.
