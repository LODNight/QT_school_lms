# from database import check_login
from PyQt6.QtWidgets import  QMainWindow, QMessageBox
from PyQt6.uic import loadUi 

class AdminWindow(QMainWindow):
    def __init__(self):
        super(AdminWindow, self).__init__()
        loadUi("ui/admin.ui", self)


        self.btnHome.clicked.connect(lambda: self.mainStack.setCurrentIndex(0))
        self.btnStudent.clicked.connect(lambda: self.mainStack.setCurrentIndex(1))
        self.btnScore.clicked.connect(lambda: self.mainStack.setCurrentIndex(2))
        self.btnLogout.clicked.connect(self.handle_logout)

    def handle_logout(self):
        from windows.login_window import LoginWindow
        self.login = LoginWindow()
        self.login.show()
        self.close()