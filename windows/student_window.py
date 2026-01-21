from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.uic import loadUi
from database import get_all_classes, add_students

class StudentDialog(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("ui/student_dialog.ui", self)

        self.btn_cancel.clicked.connect(self.close)
        self.btn_save.clicked.connect(self.save_student)

        # Load danh sách lớp vào Combobox ngay khi mở
        self.load_classes_to_combo()

    def load_classes_to_combo(self):
        classes = get_all_classes()
        self.comboClass.clear()
        for cls in classes:
            self.comboClass.addItem(cls["class_name"], cls["id"])
    
    def save_student(self):
        student_id = self.txtStudentId.text()
        full_name = self.txtName.text()
        dob = self.txtDob.date().toString("yyyy-MM-dd")
        gender = self.comboGender.currentText()
        class_id = self.comboClass.currentData()

        if not student_id or not full_name:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin")
            return

        if add_students(student_id, full_name, dob, gender, class_id):
            QMessageBox.information(self, "Thành công", "Thêm sinh viên thành công")
            self.close()
        else:
            QMessageBox.warning(self, "Lỗi", "Thêm sinh viên thất bại")
