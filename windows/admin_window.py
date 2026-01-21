# from database import check_login
from PyQt6.QtWidgets import  QMainWindow, QMessageBox, QHeaderView, QTableWidgetItem
from database import get_all_students
from PyQt6.uic import loadUi 
from windows.student_window import StudentDialog

class AdminWindow(QMainWindow):
    def __init__(self):
        super(AdminWindow, self).__init__()
        loadUi("ui/admin.ui", self)


        self.btnHome.clicked.connect(lambda: self.mainStack.setCurrentIndex(0))
        self.btnStudent.clicked.connect(self.show_student_page)
        self.btnScore.clicked.connect(lambda: self.mainStack.setCurrentIndex(2))
        self.btnLogout.clicked.connect(self.handle_logout)

        self.btnAddStudent.clicked.connect(self.add_dialog)

        # Setup Bảng (Table)
        self.setup_table()

        # Load data ngay khi mở
        self.load_data()

    def add_dialog(self):
        self.student_dialog = StudentDialog()
        # exec() sẽ dừng màn hình chính lại chờ Dialog đóng
        if self.student_dialog.exec():
            # Nếu người dùng bấm Lưu (accept) thì load lại bảng
            self.load_data()

    def show_student_page(self):
        self.mainStack.setCurrentIndex(1)   # Chuyển sang trang Student
        self.load_data()    # load lại dữ liệu 

    def setup_table(self):
        self.tableStudent.setColumnCount(5) # 5 trường dữ liệu
        self.tableStudent.setHorizontalHeaderLabels([
            "ID",
            "Họ và Tên",
            "Ngày sinh",
            "Giới tính",
            "Lớp"
        ])

        # Tự động co giãn cột cho lớp
        header = self.tableStudent.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def load_data(self):
        data = get_all_students()

        # 1. Set số dòng cho bảng bằng số bản ghi lấy được
        self.tableStudent.setRowCount(len(data))

        # 2. Duyệt qua từng dòng dữ liệu
        for row, student in enumerate(data):
            # row_data là tuple: ('HS001', 'Nguyen Van A', ...)
            raw_dob = student[2]
            if raw_dob:
                dob = raw_dob.strftime("%d/%m/%Y")
            else:
                dob = ""

            self.tableStudent.setItem(row, 0, QTableWidgetItem(student[0]))
            self.tableStudent.setItem(row, 1, QTableWidgetItem(student[1]))
            self.tableStudent.setItem(row, 2, QTableWidgetItem(dob))
            self.tableStudent.setItem(row, 3, QTableWidgetItem(student[3]))
            self.tableStudent.setItem(row, 4, QTableWidgetItem(student[4]))


    def handle_logout(self):
        from windows.login_window import LoginWindow
        self.login = LoginWindow()
        self.login.show()
        self.close()