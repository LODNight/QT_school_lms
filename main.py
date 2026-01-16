from database import create_connection,check_login
from PyQt6.uic.properties import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
from PyQt6.uic import loadUi 

# print("-- KIEM TRA HE THONG KET NOI --")

# # 1. Test ket noi 
# print("\n[B1]: Dang ket noi thu toi xampp...")
# conn = create_connection()
# if conn is not None:
#     print("\nKet noi thanh cong")
#     print("\nThong tin server:", conn.get_server_info())
#     conn.close()
# else:
#     print("\nKet noi that bai")


# # 2. Test Truy van
# print("\n[B2]: Thu ket noi dang nhap voi username 'admin'...")
# is_success, full_name, role = check_login('admin', '123456')


# if is_success: 
#     print("\nDang nhap thanh cong")
#     print(f"\nHo ten: {full_name}")
#     print(f"\nVai tro: {role}")
# else:
#     print("\nDang nhap that bai")
# print("\n -- KET THUC --")

class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        loadUi("ui/login.ui", self)

        self.btnRegister.clicked.connect(self.show_register_window)
        self.btnLogin.clicked.connect(self.login)

        
    def show_register_window(self):
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

        is_success, full_name, role = check_login(username, password)

        if is_success:
            self.lblMessage_username.setText("Login successful")
            self.lblMessage_password.setText("Login successful")

            self.lblMessage_username.setStyleSheet("color: green")
            self.lblMessage_password.setStyleSheet("color: green")
            QMessageBox.information(self, "Login successful", f"username: {full_name}\nrole: {role}")

            if role == "admin":
                self.admin_window = AdminWindow()
                self.admin_window.show()
                self.close()
            elif role == "user":
                self.user_window = UserWindow()
                self.user_window.show()
                self.close()


        else:
            self.lblMessage_username.setText("Login failed")
            self.lblMessage_password.setText("Login failed")

            self.lblMessage_username.setStyleSheet("color: red")
            self.lblMessage_password.setStyleSheet("color: red")

            QMessageBox.information(self, "Login failed", "Login failed")


class RegisterWindow(QMainWindow):
    def __init__(self):
        super(RegisterWindow, self).__init__()
        loadUi("ui/register.ui", self)

        self.btnLogin.clicked.connect(self.show_login_window)
    
    def show_login_window(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def register(self):
        username = self.lineUsername.text()
        password = self.linePassword.text()
        confirm_password = self.lineConfirmPassword.text()

        # if password == confirm_password:



app = QApplication(sys.argv)
window = LoginWindow()
window.show()
app.exec()