# from database import check_login
from PyQt6.QtWidgets import  QMainWindow, QMessageBox, QHeaderView, QTableWidgetItem
from database import get_all_students, delete_student
from PyQt6.uic import loadUi 
from windows.student_dialog import StudentDialog

class AdminWindow(QMainWindow):
    def __init__(self):
        super(AdminWindow, self).__init__()
        loadUi("ui/admin.ui", self)

        # Kết nối các button tab Home
        self.btnHome.clicked.connect(lambda: self.mainStack.setCurrentIndex(0))
        self.btnStudent.clicked.connect(self.show_student_page)
        self.btnScore.clicked.connect(lambda: self.mainStack.setCurrentIndex(2))
        self.btnLogout.clicked.connect(self.handle_logout)

        # Kết nối các button Student 
        self.btnAddStudent.clicked.connect(self.open_add_dialog)
        self.btnEditStudent.clicked.connect(self.open_edit_dialog)
        self.btnDeleteStudent.clicked.connect(self.handle_delete)

        # Setup Bảng (Table)
        self.setup_table()

        # Load data ngay khi mở
        self.load_data()

    # Hàm lấy thông tin học sinh được chọn
    def get_selected_student_infor(self):
        current_row = self.tableStudent.currentRow()
        if current_row < 0:
            return None
        
        student_id = self.tableStudent.item(current_row, 0).text()
        student_name = self.tableStudent.item(current_row, 1).text()
        student_dob = self.tableStudent.item(current_row, 2).text()
        student_gender = self.tableStudent.item(current_row, 3).text()
        student_class = self.tableStudent.item(current_row, 4).text()
        
        return {
            "student_id": student_id, "student_name": student_name, "student_dob": student_dob,
            "student_gender": student_gender, "student_class": student_class
            }

    # Hàm xử lý khi nhấn nút Thêm
    def open_add_dialog(self):
        self.student_dialog = StudentDialog()
        # exec() sẽ dừng màn hình chính lại chờ Dialog đóng
        if self.student_dialog.exec():
            # Nếu người dùng bấm Lưu (accept) thì load lại bảng
            self.load_data()

    # Hàm xử lý khi nhấn nút Sửa
    def open_edit_dialog(self):
        # 1. Kiểm tra xem có chọn dòng nào chưa
        selected_student = self.get_selected_student_infor()
        if not selected_student:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một sinh viên để sửa")
            return
        
        # 2. Mở dialog và TRUYỀN DỮ LIỆU VÀO -> Chế độ Sửa
        dialog = StudentDialog(student_data = selected_student)
        if dialog.exec():
            self.load_data()

    # Hàm xử lý khi nhấn nút Xóa
    def handle_delete(self):
        # 1. Kiểm tra chọn dòng
        student_selected = self.get_selected_student_infor()
        if not student_selected:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một học sinh để xóa")
            return

        # 2. Hỏi xác nhận 
        confirm = QMessageBox.question(self, "Xác nhận", f"Bạn có chắc chắn muốn xóa học sinh '{student_selected['student_name']}' này không?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            # 3. Gọi DB Xóa
            if delete_student(student_selected['student_id']):
                QMessageBox.information(self, "Thành công", "Xóa học sinh thành công")
                self.load_data()
            else:
                QMessageBox.warning(self, "Lỗi", "Xóa học sinh thất bại")
        
    # Hàm hiển thị trang Student
    def show_student_page(self):
        self.mainStack.setCurrentIndex(1)   # Chuyển sang trang Student
        self.load_data()    # load lại dữ liệu 

    # Hàm setup Bảng (Table)
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

    # Hàm load dữ liệu vào bảng
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

    # Hàm xử lý khi nhấn nút Đăng xuất
    def handle_logout(self):
        from windows.login_window import LoginWindow
        self.login = LoginWindow()
        self.login.show()
        self.close()