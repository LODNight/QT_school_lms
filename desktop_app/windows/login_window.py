from database import check_login
from PyQt6.QtWidgets import  QMainWindow, QMessageBox
from PyQt6.uic import loadUi 

import api_client


class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        loadUi("ui/login.ui", self)

        self.btnRegister.clicked.connect(self.show_register_window)
        self.btnLogin.clicked.connect(self.login)

        
    def show_register_window(self):
        from windows.register_window import RegisterWindow
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()

    def login(self):
        username = self.lineUsername.text().strip()
        password = self.linePassword.text().strip()

        self.lblMessage_username.clear()
        self.lblMessage_password.clear()

        if not username or not password:
           self._show_error("Username và password không được để trống")
           return

        # Gọi API Login thông qua Singleton client
        response = api_client.client.login(username, password)
        
        if not response.success:
            self._show_error(response.message)
            QMessageBox.warning(self, "Đăng nhập thất bại", response.message)
            return

        # Lấy User từ client state
        user_infor = api_client.client.current_user
        if not user_infor:
            QMessageBox.warning(self, "Đăng nhập thất bại", "Không tìm thấy thông tin người dùng")
            return

        full_name = user_infor.get("full_name", "")
        role = user_infor.get("role", "")

        self._show_success("Đăng nhập thành công")
        QMessageBox.information(
            self, 
            "Đăng nhập thành công", 
            f"Xin chào: {full_name}\nVai trò: {role}"
        )

        self._open_main_window(role)

    # ===== Helper methods (UI only) =====
    def _show_error(self, message):
        self.lblMessage_username.setText(message)
        self.lblMessage_password.setText(message)
        self.lblMessage_username.setStyleSheet("color: red")
        self.lblMessage_password.setStyleSheet("color: red")

    def _show_success(self, message):
        self.lblMessage_username.setText(message)
        self.lblMessage_password.setText(message)
        self.lblMessage_username.setStyleSheet("color: green")
        self.lblMessage_password.setStyleSheet("color: green")

    def _open_main_window(self, role):
        if role == "admin":
            from windows.admin_window import AdminWindow
            self.window = AdminWindow()
        elif role in ("user", "student"):
            from windows.user_window import UserWindow
            self.window = UserWindow()
        else:
            QMessageBox.warning(self, "Lỗi", f"Vai trò không hợp lệ: {role}")
            return

        self.window.show()
        self.close()