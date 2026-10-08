# Tài liệu Rive CLI cục bộ

Các file tại đây được trích bằng `rive docs` và `rive schema --all --json` từ CLI đang cài. Xem `index.json` để biết phiên bản, lệnh nguồn và hash. Các bản tiện mở theo cách Nez dùng nằm ở `build/doc_data.txt`, `doc_draw.txt`, `doc_ease.txt`, `doc_rig.txt`, `doc_sm.txt`, `doc_workflow.txt`, `doc_format.txt`.

| Khi cần | Đọc |
|---|---|
| View Model, giá trị mặc định, enum, data binding | [data.md](data.md) |
| Shape, path, fill/stroke, gradient | [drawing.md](drawing.md) |
| Keyframe và easing | [easing.md](easing.md) |
| Rig, constraint, Solo | [rigging.md](rigging.md) |
| State/transition/condition/listener | [state-machines.md](state-machines.md) |
| Quy trình verify/inspect/render | [workflow.md](workflow.md) |
| Cấu trúc RML và kiểu thuộc tính | [format.md](format.md) |

`schema/` chứa 14 loại liên quan tới data và binding, gồm cả thuộc tính editor-only như `exports` và `defaultInstanceId`. Đây là tài liệu tham chiếu; nguồn dữ liệu Ollie nằm ở `../../data/`.

Tái tạo: `python tools/sync_cli_docs.py --refresh` từ gốc Ollie. Full build tự kiểm tra phiên bản/hash và phục hồi alias trong build, kể cả sau khi xóa thư mục build.
