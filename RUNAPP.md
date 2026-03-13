# Hướng dẫn Chạy Dự án (Run App)

Dự án này bao gồm hai thành phần hoạt động song song: **Backend** và ứng dụng **Desktop**. Bạn cần phải chạy Backend lên trước để Desktop App có thể kết nối với cơ sở dữ liệu thông qua API.

---

## 1. Môi trường Yêu cầu
- Đã cài đặt [Python 3.8+](https://www.python.org/downloads/)
- Bạn nên sử dụng môi trường ảo (virtual environment) để tránh xung đột thư viện.

---

## 2. Khởi chạy Backend (FastAPI)

Kéo Terminal / Command Prompt hoặc tab Terminal trong VSCode, trỏ vào thư mục `backend`:

```bash
cd backend
```

**(Tùy chọn) Cài đặt các thư viện cần thiết nếu chưa có:**
```bash
pip install fastapi uvicorn sqlalchemy pydantic passlib bcrypt
```

**Chạy Server Backend:**
```bash
uvicorn main:app --reload
```
*Ghi chú: `--reload` giúp server tự động cập nhật nếu bạn có chỉnh sửa code backend.*
*Server sẽ chạy thành công tại địa chỉ: `http://127.0.0.1:8000`*

---

## 3. Khởi chạy Desktop App (PyQt6)

**Mở một tab Terminal / Command Prompt MỚI**, chuyển thư mục vào `desktop_app`:

```bash
cd desktop_app
```

**(Tùy chọn) Cài đặt các thư viện cần thiết nếu chưa có:**
```bash
pip install PyQt6 requests
```

**Chạy ứng dụng Desktop:**
```bash
python main.py
```
*Ứng dụng giao diện sẽ bật lên ngay sau đó với màn hình Đăng nhập.*

---

## 💡 Lưu ý Xử lý Sự Cố Thông Thường
1. **Lỗi không tìm thấy module khi import:** Hãy kiểm tra xem bạn đã cài đúng các thư viện bằng lệnh `pip install` ở trên chưa.
2. **Lỗi Desktop App không đăng nhập được/Không thấy data:** Có thể bạn quên chạy nền Backend hoặc Backend đang bị lỗi. Hãy xem cửa sổ Terminal của Backend xem có cảnh báo lỗi (Error) nào không.
3. **Lỗi chặn Script Powershell (tại Windows):** Nếu bạn gặp lỗi *"... cannot be loaded because running scripts is disabled on this system."*, hãy chạy lệnh Desktop/Backend trực tiếp bằng CMD (Command Prompt) thay vì Powershell, hoặc chỉ gõ thủ công từng lệnh `uvicorn...` thay vì chạy script.