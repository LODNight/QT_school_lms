from database import create_connection,check_login
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
from PyQt6.uic import loadUi 
from windows.login_window import LoginWindow
from windows.admin_window import AdminWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    # window = AdminWindow()
    window.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print("Đã đóng ứng dụng")