# NezFocus Mascot Repository 🌟

Repository chứa toàn bộ tài nguyên, thiết kế, mô hình animation Rive và công cụ chạy thử (playground) cho linh vật trong hệ sinh thái **NezFocus**.

---

## 📁 Cấu Trúc Dự Án

```
mascot/
├── ollie-mascot/          # Linh vật Ollie (Thiết kế mới nhất: Chibi, Vector, Rive runtime, Web-pet)
├── nez-mascot/            # Linh vật Nez (Mô hình Rive runtime chuẩn, state machine, moods & gestures)
├── mascot-playground/     # Giao diện web chạy thử tương tác (Mood, Chat bubble, Gestures)
└── README.md
```

---

## 🎨 1. Ollie Mascot (`ollie-mascot/`)
- **Mô tả:** Bản vẽ vector và mô hình animation Rive mới nhất cho chú gấu/chibi Ollie lá xanh.
- **Tài nguyên chính:**
  - `dist/ollie.riv`: File Rive runtime tối ưu hóa xuất cho ứng dụng.
  - `dist/ollie-front.svg`, `dist/ollie-front.png`: Tài nguyên vector & hình ảnh sắc nét.
  - `review.html`: Trang kiểm tra trực quan so sánh bản vẽ và runtime.
  - `playground/`: Môi trường kiểm thử tương tác riêng cho Ollie.
  - `web-pet/`: Demo tương tác web thời gian thực (Pixi.js & Vite).

---

## 🤖 2. Nez Mascot (`nez-mascot/`)
- **Mô tả:** Linh vật Nez ban đầu của NezFocus với đầy đủ hệ thống State Machine, Voice Lines và cử chỉ cảm xúc.
- **Tính năng State Machine:**
  - `mood`: `neutral`, `happy`, `wink`, `focus`, `surprised`, `sleepy`, `confused`
  - `isAsleep`: Chế độ ngủ với bong bóng zZ, đánh thức bằng thao tác click/chạm.
  - `wave`: Cử chỉ vẫy tay chào người dùng.
- **Tài nguyên chính:**
  - `dist/runtime.riv`: File Rive runtime chính thức tích hợp vào Mobile App (React Native).
  - `speech/lines.vi.json`: Lời thoại tiếng Việt theo từng bối cảnh.

---

## 🎮 3. Mascot Playground (`mascot-playground/`)
Môi trường web kiểm thử nhanh các cử chỉ, trạng thái và khung thoại mà không cần chạy toàn bộ ứng dụng mobile.

### Cách chạy kiểm thử:
```bash
# Khởi chạy một local web server tại thư mục gốc:
python -m http.server 8080
```
Sau đó truy cập: [http://localhost:8080/mascot-playground/](http://localhost:8080/mascot-playground/) hoặc mở `ollie-mascot/review.html`.
