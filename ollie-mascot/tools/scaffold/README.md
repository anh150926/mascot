# Snapshot scaffold

`runtime.rml` là snapshot kiến trúc animation Nez được Ollie sử dụng và retarget. Chỉ generator Ollie đọc bản local này; không cần sửa dự án Nez.

`data.rml` ở đây được giữ làm lịch sử lúc chụp scaffold, không còn là nguồn dữ liệu build. Nguồn hiện tại là `../../data/model.json`; `../build_data.py` sinh `../../data.rml` rồi `../build_ollie.py` nhúng vào runtime.
