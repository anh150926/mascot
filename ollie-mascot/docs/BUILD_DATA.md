# Phân tích Nez và phần bổ sung cho Ollie

Kiểm tra trực tiếp các thư mục `nez-mascot/`, data.rml, speech, tests, tools, tài liệu build và năm file doc_*.txt. Các file của Nez giữ nguyên.

## Phân biệt tài liệu với dữ liệu chạy

Nez hiện **không có thư mục nguồn `data/`**; nguồn View Model là file `data.rml` ở gốc. File người dùng đang mở `build/doc_data.txt` là bản lưu của `rive docs data` — giải thích View Model, enum và data binding, không phải file input được Rive compile.

| Trong Nez | Vai trò thực tế | Bổ sung/tương ứng trong Ollie |
|---|---|---|
| `build/doc_data.txt` | tài liệu data binding | cùng tên, sinh từ CLI đang cài; nguồn bền ở `docs/rive-cli/data.md` |
| `doc_draw.txt`, `doc_ease.txt`, `doc_rig.txt`, `doc_sm.txt` | cú pháp hình, easing, rigging, state machine | đủ 5 alias tương ứng, thêm workflow/format |
| `data.rml` | Mood + Mascot/Default + mood/isAsleep/wave | `data/model.json` sinh `data.rml`, giữ tên, enum và ID hiện có |
| Không có metadata phiên bản cho doc cache | khó biết tài liệu thuộc CLI nào | `docs/rive-cli/index.json`: phiên bản, lệnh nguồn, SHA-256; 14 schema JSON |
| `speech/lines.vi.json` | câu thoại app đọc, mood/gesture, điểm neo | 20 câu riêng của Ollie, 10 nhóm theo planning/wellness, không sao chép câu về robot/tai nghe/phòng học |
| Preset nằm rải trong lệnh và probe | dữ liệu chạy thử | `data/presets.json`: 10 preset dùng trực tiếp bởi `tools/preview.py` |
| MASCOT_BRIEF + TUNING | nhận diện và cách chỉnh | MASCOT_BRIEF + MODEL_BRIEF + TUNING + tài liệu này |
| `tests/t1..t10*.json` | kiểm theo giai đoạn và vùng màu của Nez | Ollie giữ 28 capture riêng, thêm 5 kiểm thử lỗi dữ liệu; không dùng vùng pixel xanh dương của Nez |
| `build/moods`, `rv`, `trace` | output xem biểu cảm/rig/chồng ảnh | đã có từ bộ mẫu; thêm `build/data` cho contract, rig map, báo cáo |
| `.superpowers`, docs/superpowers/plans | lịch sử công cụ/kế hoạch của Nez | không phải dữ liệu build; không đưa vào runtime Ollie |
| `rive.yaml` có push projectId/fileId | đích tài khoản riêng của Nez | không chuyển sang Ollie; Ollie tiếp tục xuất cục bộ |

## Luồng build hiện tại

```text
data/model.json ── build_data.py ── data.rml ─┐
artwork/build_artwork.py ── artwork/front.rml ├─ build_ollie.py ── runtime.rml
tools/scaffold/runtime.rml ──────────────────┘
data/presets.json + features.json + speech/lines.vi.json
                         └─ kiểm tra kiểu, tham chiếu, placeholder ─┐
runtime.rml ── kiểm tra binding/ID/default/mood/layer ─────────────┤
            ── rive verify + inspect + 28 capture ────────────────┤
            ── export .riv + data/speech cho ứng dụng ◀──────────┘

rive docs/schema ── docs/rive-cli/ + build/doc_*.txt
```

`tools/build_kit.py` là lệnh chung. Tài liệu/schema được làm mới khi CLI đổi phiên bản hoặc khi gọi `sync_cli_docs.py --refresh`; build không cần tải tài liệu từ mạng. `data/`, `speech/` và tài liệu bị exclude khỏi compile, nhưng data.rml được nhúng có chủ đích trong runtime.rml. Đầu ra ứng dụng gồm:

```text
dist/
  ollie.riv
  ollie-front.png / ollie-front.svg
  data/
    contract.json       API tên/kiểu/default, không cần hiểu ID nội bộ
    presets.json        giá trị cùng argv preview/capture
    features.json       ánh xạ tính năng và đạo cụ còn thiếu
    rig-map.json        node/pivot và thời lượng timeline thực tế
    validation.json     kết quả kiểm tra + hash nguồn
  speech/lines.vi.json
```

## Những lỗi bị chặn trước khi xuất

- ID trùng hoặc sai dạng; giá trị enum mặc định không tồn tại.
- Preset dùng mood/trigger không có, boolean viết thành chuỗi, tọa độ click ngoài artboard.
- Câu thoại dùng mood/gesture sai, placeholder chưa khai báo, ID câu trùng.
- Ánh xạ tính năng trỏ vào preset/nhóm thoại không tồn tại.
- Runtime sai liên kết Artboard → Main → Mascot/Default; data nhúng không khớp model.
- Property không có binding, mood thiếu timeline/transition, thứ tự layer thay đổi.
- Ảnh bitmap tham chiếu hoặc nền Fill lọt vào runtime sản xuất.

Kiểm tra dữ liệu không đánh giá độ giống nghệ thuật. 28 probe tiếp tục kiểm tra render và hành vi; bảng đối chiếu ảnh vẫn là nơi kiểm tra hình dáng. Các góc nghiêng/sau và đạo cụ chưa có đủ reference tiếp tục để trạng thái chờ.

## Kiểm tra riêng

```powershell
python tools/build_data.py --check
python -m unittest discover -s tests -p test_data.py -v
python tools/check.py tests/poses.json
python tools/preview.py sleep --capture
```

Lệnh đầu báo lỗi nếu model vừa đổi mà runtime chưa được dựng lại. Full build sẽ thực hiện theo đúng thứ tự. Không chỉnh file trong build/data hoặc dist/data rồi kỳ vọng thay đổi đi ngược vào nguồn.
