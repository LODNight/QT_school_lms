from database import check_login
from PyQt6.QtWidgets import  QMainWindow, QMessageBox
from PyQt6.uic import loadUi 


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

        is_success, full_name, role = check_login(username, password)

        if is_success:
            self.lblMessage_username.setText("Login successful")
            self.lblMessage_password.setText("Login successful")

            self.lblMessage_username.setStyleSheet("color: green")
            self.lblMessage_password.setStyleSheet("color: green")
            QMessageBox.information(self, "Login successful", f"username: {full_name}\nrole: {role}")

            if role == "admin":
                from windows.admin_window import AdminWindow
                self.admin_window = AdminWindow()
                self.admin_window.show()
                self.close()
            elif role == "user":
                from windows.user_window import UserWindow
                self.user_window = UserWindow()
                self.user_window.show()
                self.close()


        else:
            self.lblMessage_username.setText("Login failed")
            self.lblMessage_password.setText("Login failed")

            self.lblMessage_username.setStyleSheet("color: red")
            self.lblMessage_password.setStyleSheet("color: red")

            QMessageBox.information(self, "Login failed", "Login failed")

