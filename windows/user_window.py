from database import check_login
from PyQt6.QtWidgets import  QMainWindow, QMessageBox
from PyQt6.uic import loadUi 

class UserWindow(QMainWindow):
    def __init__(self):
        super(UserWindow, self).__init__()
        loadUi("ui/user.ui", self)