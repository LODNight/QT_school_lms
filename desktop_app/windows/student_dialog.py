from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtCore import QDate
from PyQt6.uic import loadUi
from database import get_all_classes, add_students, update_student

class StudentDialog(QDialog):
    def __init__(self, student_data=None):
        super().__init__()
        loadUi("ui/student_dialog.ui", self)

        self.student_data = student_data
        self.comboGender.addItems(["Nam", "Nữ", "Khác"])

        # Load danh sách lớp vào Combobox ngay khi mở
        self.load_classes_to_combo()

        if self.student_data:
            self.setWindowTitle("Cập nhật thông tin sinh viên")
            self.labelTitle.setText("Cập nhật thông tin sinh viên")
            self.setup_edit_mode()
        else:
            self.setWindowTitle("Thêm thông tin sinh viên")
            self.labelTitle.setText("Thêm thông tin sinh viên")

        self.btnCancel.clicked.connect(self.close)
        self.btnSave.clicked.connect(self.save_student)

    def load_classes_to_combo(self):
        classes = get_all_classes()
        self.comboClass.clear()
        for cls in classes:
            self.comboClass.addItem(cls[1], cls[0])

    def setup_edit_mode(self):
        # student_data dạng: (id, name, dob_string, gender, class_name)

        # 1. Điền ID và khóa lại (Không cho sửa ID)
        self.txtStudentId.setText(self.student_data['student_id'])
        self.txtStudentId.setReadOnly(True)

        # 2. Điền tên
        self.txtName.setText(self.student_data['student_name'])

        # 3. Điền ngày sinh
        self.txtDob.setDate(QDate.fromString(self.student_data['student_dob'], "dd/MM/yyyy"))

        # 4. Điền giới tính
        self.comboGender.setCurrentText(self.student_data['student_gender'])
        
        # 5. Điền lớp
        # Tìm text trong combo và set index
        index = self.comboClass.findText(self.student_data['student_class'])
        if index >= 0:
            self.comboClass.setCurrentIndex(index)

    
    def save_student(self):
        student_id = self.txtStudentId.text()
        full_name = self.txtName.text()
        dob = self.txtDob.date().toString("yyyy-MM-dd")
        gender = self.comboGender.currentText()
        class_id = self.comboClass.currentData()

        if not student_id or not full_name:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin")
            return

        # LOGIC QUYẾT ĐỊNH: THÊM hay SỬA?
        if self.student_data:
            # SỬA
            if update_student(student_id, full_name, dob, gender, class_id):
                QMessageBox.information(self, "Thành công", "Cập nhật thông tin sinh viên thành công")
                self.accept()
            else:
                QMessageBox.warning(self, "Lỗi", "Cập nhật thông tin sinh viên thất bại")
        else:
            # THÊM
            if add_students(student_id, full_name, dob, gender, class_id):
                QMessageBox.information(self, "Thành công", "Thêm sinh viên thành công")
                self.accept()
            else:
                QMessageBox.warning(self, "Lỗi", "Thêm sinh viên thất bại")
