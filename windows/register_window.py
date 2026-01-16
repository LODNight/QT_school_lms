from database import check_login
from PyQt6.QtWidgets import  QMainWindow, QMessageBox
from PyQt6.uic import loadUi 


class RegisterWindow(QMainWindow):
    def __init__(self):
        super(RegisterWindow, self).__init__()
        loadUi("ui/register.ui", self)

        self.btnLogin.clicked.connect(self.show_login_window)
    
    def show_login_window(self):
        from windows.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def register(self):
        username = self.lineUsername.text()
        password = self.linePassword.text()
        confirm_password = self.lineConfirmPassword.text()

        # if password == confirm_password:
