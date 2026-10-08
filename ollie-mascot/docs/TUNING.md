# Chỉnh Ollie và tái tạo bộ mẫu

| Muốn sửa | Sửa ở đâu | Kiểm tra chính |
|---|---|---|
| Tỉ lệ/nét/màu front | `artwork/build_artwork.py` | front-compare, onion, grid |
| Điểm xoay/gắn bộ phận | `tools/build_ollie.py` | neutral so với front, wave-strip, sleep-strip |
| Mắt/mỏ của mood | `tools/build_ollie.py`: add_eye, add_beak | contact sheet + blink probes |
| Thời gian chuyển động | `tools/scaffold/runtime.rml` hoặc bước retarget có ghi chú | đầu, giữa, cuối vòng và trở về |
| Dữ liệu ứng dụng | `data/model.json`, binding trong scaffold | `build/data/validation.json`, JSON probe |
| Preset và lời thoại | `data/presets.json`, `speech/lines.vi.json` | `tools/build_data.py --check`, playground |
| Kịch bản kiểm tra | `tests/poses.json`, `tools/check.py` | check-report.json |
| Ảnh chuẩn mới | `reference/` + manifest | canvas, góc nhìn, mốc neo, ưu tiên |

Không sửa trực tiếp runtime.rml, data.rml, artwork/front.rml hoặc artwork/parts.json: chúng được sinh lại. SVG cũng là đầu ra; nếu chỉnh SVG bằng công cụ ngoài, đưa thay đổi về path trong nguồn trước khi build. Tài liệu data/schema đúng phiên bản CLI nằm trong `docs/rive-cli/`; xem [BUILD_DATA.md](BUILD_DATA.md) để theo luồng build.

Sau khi chỉnh chạy `python tools/build_kit.py`. CLI phải verify không lỗi; inspect phải có đủ thành phần; xem ảnh lớn, ảnh nhỏ, mood bị ảnh hưởng và chuyển động nối vòng. Không chỉ dựa vào việc file .riv mở được.

Probe kiểm tra: dữ liệu mood/ngủ thật, chớp mắt có thay đổi vùng mắt, thở có thay đổi, wave khác dáng nghỉ và trở về nghỉ, wave bị chặn khi ngủ, chạm đánh thức đổi isAsleep=false, neutral rig giữ dáng front, nhân vật/effect không chạm biên viewport tại frame được chọn. Đây là kiểm tra mốc mẫu, không chứng minh mọi frame ở mọi tổ hợp đều hoàn hảo.

Screenshot CLI có nền preview #1D1D1D; ảnh *-alpha.png chỉ loại nền nối với mép ảnh để bảo toàn đồng tử và mi đen. Rive artboard và SVG vốn trong suốt. Ảnh front gốc được bảo toàn; bản 500 px không crop.

Rive compile loại web-pet/ và playground/: các thư mục này không phải nguồn RML, riêng node_modules gây quét/đóng gói chậm. build/rv là snapshot runtime tối giản; build/trace là project chồng ảnh tĩnh. Các stages bị loại khỏi compile của project review cha.

Scaffold chụp từ dự án Nez có sẵn trong workspace ngày 08/10/2026. Nez giữ nguyên; Ollie có scaffold độc lập. Nếu thay scaffold, giữ/retarget ID cố định và chạy lại probe.
