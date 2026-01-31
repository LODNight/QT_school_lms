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
        username = self.lineUsername.text()
        password = self.linePassword.text()

        if not username or not password:
            self.lblMessage_username.setText("Username is required")
            self.lblMessage_password.setText("Password is required")

            self.lblMessage_username.setStyleSheet("color: red")
            self.lblMessage_password.setStyleSheet("color: red")

        is_success, message = api_client.login(username, password)
        
        if is_success:
            # Lấy thông tin user sau khi login thành công
            user_info = api_client.get_my_info()
            
            if not user_info:
                 QMessageBox.critical(self, "Lỗi", "Không thể lấy thông tin người dùng!")
                 return

            full_name = user_info.get("full_name", "")
            role = user_info.get("role", "")

            self.lblMessage_username.setText("Login successful")
            self.lblMessage_password.setText("Login successful")

            self.lblMessage_username.setStyleSheet("color: green")
            self.lblMessage_password.setStyleSheet("color: green")
            QMessageBox.information(self, "Login successful", f"Xin chào: {full_name}\nVai trò: {role}")

            if role == "admin":
                from windows.admin_window import AdminWindow
                self.admin_window = AdminWindow()
                self.admin_window.show()
                self.close()
            elif role == "user" or role == "student":
                from windows.user_window import UserWindow
                self.user_window = UserWindow()
                self.user_window.show()
                self.close()
            else:
                 QMessageBox.warning(self, "Lỗi", f"Vai trò không hợp lệ: {role}")
        else:
            self.lblMessage_username.setText(message)
            self.lblMessage_password.setText(message)

            self.lblMessage_username.setStyleSheet("color: red")
            self.lblMessage_password.setStyleSheet("color: red")

            QMessageBox.warning(self, "Login failed", message)

