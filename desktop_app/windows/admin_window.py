# from database import check_login
from PyQt6.QtWidgets import  QMainWindow, QMessageBox, QHeaderView, QTableWidgetItem, QVBoxLayout, QWidget, QFileDialog
from PyQt6.QtCore import Qt
from database import get_all_students, delete_student, get_all_classes, get_scores_by_class, search_students
from PyQt6.uic import loadUi 
from windows.student_dialog import StudentDialog
import pandas as pd
import api_client

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class AdminWindow(QMainWindow):
    def __init__(self):
        super(AdminWindow, self).__init__()
        loadUi("ui/admin.ui", self)

        # Kết nối các button tab Home
        self.btnHome.clicked.connect(lambda: self.mainStack.setCurrentIndex(0))
        self.btnStudent.clicked.connect(self.show_student_page)
        self.btnLogout.clicked.connect(self.handle_logout)

        # Kết nối các button Student 
        self.btnAddStudent.clicked.connect(self.open_add_dialog)
        self.btnEditStudent.clicked.connect(self.open_edit_dialog)
        self.btnDeleteStudent.clicked.connect(self.handle_delete)

        # Setup trang điểm số
        self.btnScore.clicked.connect(lambda: self.mainStack.setCurrentIndex(2))
        self.load_classes_for_score_page()
        self.btnLoadScores.clicked.connect(self.load_scores_table)
        self.btnSaveScore.clicked.connect(self.save_scores_data)
        self.btnExportExcel.clicked.connect(self.export_excel)

        self.btnSearch.clicked.connect(self.handle_search)
        self.txtSearch.returnPressed.connect(self.handle_search)

        # Setup Bảng (Table)
        self.setup_table()

        # Setup Chart
        self.setup_chart_area()

        # Load data ngay khi mở
        self.load_data()

        # Load data bằng API
        self.load_data_by_api() # Load Users
        self.load_classes_combo()   # Load Classes

    # Hàm load dữ liệu từ API
    def load_data_by_api(self):
        """Load dữ liệu từ API và hiển thị lên bảng."""
        # 1. Gọi API lấy danh sách users
        users = api_client.client.get_all_users()

        # 2. Reset bảng
        self.tablesStudent.setRowCount(0)

        if not users:
            return

        # 3. Cập nhật dữ liệu vào bảng
        self.tablesStudent.setRowCount(len(users))
        
        # Danh sách các key tương ứng với từng cột (0 -> 4)
        column_keys = ["id", "username", "full_name", "email", "role"]

        for row_idx, user in enumerate(users):
            for col_idx, key in enumerate(column_keys):
                # Lấy giá trị an toàn bằng .get(), chuyển về string
                value = str(user.get(key, ""))
                item = QTableWidgetItem(value)
                self.tablesStudent.setItem(row_idx, col_idx, item)

    def load_classes_combo(self):
        """ Load danh sách lớp vào combobox """
        classes = api_client.client.get_all_classes()

        if not classes:
            return
        if hasattr(self, 'cboClassSelect'):
            self.cboClassSelect.clear()
            for cls in classes:
                display_name = f"{cls['name']} ({cls['course']['name']})"
                self.cboClassSelect.addItem(display_name, cls['id'])

    # Hàm setup khu vực vẽ biểu đồ
    def setup_chart_area(self):
        """ Chuẩn bị khu vực để vẽ biểu đồ """
        self.chart_layout = QVBoxLayout(self.widgetChart)

        # Tạo một cái khung tranh (Figure) của Matplotlib
        self.chart_figure = plt.figure()
        self.chart_canvas = FigureCanvas(self.chart_figure)
        
        # Nhét khung tranh vào layout
        self.chart_layout.addWidget(self.chart_canvas)

    # Hàm vẽ biểu đồ
    def draw_chart(self, df):
        """ Vẽ biểu đồ """
        # 1. Xóa biểu đồ cũ đi để vẽ cái mới
        self.chart_figure.clear()

        # 2. Tính toán dữ liệu: Đếm số lượng Đậu (>=5) và Rớt (<5)
        # Logic: df['Average'] là cột điểm TB mình đã tính ở bước trước
        count_pass = len(df[df['Average'] >= 5.0])
        count_fail = len(df[df['Average'] < 5.0])
        
        # Nếu chưa có dữ liệu thì thôi
        if count_pass == 0 and count_fail == 0:
            self.chart_canvas.draw()
            return

        # 3. Vẽ biểu đồ tròn (Pie Chart)
        ax = self.chart_figure.add_subplot(111) # Tạo trục vẽ
        labels = ['Đậu', 'Rớt']
        sizes = [count_pass, count_fail]
        colors = ['#4CAF50', '#F44336'] # Xanh lá và Đỏ
        
        # Vẽ
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.axis('equal') # Để biểu đồ tròn vo
        ax.set_title(f"Tỷ lệ Đậu/Rớt (Tổng: {count_pass + count_fail} HS)")

        # 4. Cập nhật hiển thị
        self.chart_canvas.draw()

    # Hàm load lớp vào tab điểm số
    def load_classes_for_score_page(self):
        """ Load các lớp vào combobox """
        classes = get_all_classes()
        self.cboClassSelect.clear()
        for c_id, c_name in classes:
            self.cboClassSelect.addItem(c_name, c_id)     

    # Hàm load bảng điểm
    def load_scores_table(self):
        class_id = self.cboClassSelect.currentData()
        if not class_id:
            return

        response = api_client.client.get_grade_board(class_id)
        if not response.success:
            self.tableScores.setRowCount(0)
            self.tableScores.setColumnCount(0)
            return

        data = response.data
        columns_info = data["columns"]
        rows_info = data["rows"]

        total_cols = 2 + len(columns_info)
        self.tableScores.setColumnCount(total_cols)

        headers = ["ID", "Họ Tên"]
        self.column_map = {}

        for idx, col in enumerate(columns_info):
            headers.append(f"{col['name']} ({col['weight']})")
            self.column_map[idx + 2] = col["id"]

        self.tableScores.setHorizontalHeaderLabels(headers)
        self.tableScores.hideColumn(0)
        self.tableScores.setRowCount(len(rows_info))

        for r, row in enumerate(rows_info):
            enrollment_item = QTableWidgetItem(str(row["enrollment_id"]))
            enrollment_item.setFlags(enrollment_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.tableScores.setItem(r, 0, enrollment_item)

            name_item = QTableWidgetItem(row["full_name"])
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.tableScores.setItem(r, 1, name_item)

            scores = row["scores"]

        for c in range(2, total_cols):
            category_id = self.column_map[c]
            value = scores.get(category_id, "")
            self.tableScores.setItem(r, c, QTableWidgetItem(str(value)))

    def save_scores_data(self):
        updates = []

        for r in range(self.tableScores.rowCount()):
            try:
                enrollment_id = int(self.tableScores.item(r, 0).text())
            except:
                continue

        for c in range(2, self.tableScores.columnCount()):
            item = self.tableScores.item(r, c)
            if not item or not item.text().strip():
                 continue

            try:
                updates.append({
                    "enrollment_id": enrollment_id,
                    "category_id": self.column_map[c],
                    "value": float(item.text())
                })
            except ValueError:
                QMessageBox.warning(
                    self, "Lỗi",
                    f"Dòng {r+1} cột {c+1} nhập sai định dạng!"
                )
                return

        if not updates:
            QMessageBox.information(self, "Thông tin", "Không có dữ liệu để lưu!")
            return

        response = api_client.client.save_grades(updates)
        if response.success:
            QMessageBox.information(self, "Thành công", response.data["message"])
            self.load_scores_table()
        else:
            QMessageBox.critical(self, "Lỗi", response.message)

    # Hàm lấy thông tin học sinh được chọn
    def get_selected_student_infor(self):
        """ Lấy thông tin học sinh được chọn """
        current_row = self.tablesStudent.currentRow()
        if current_row < 0:
            return None
        
        student_id = self.tablesStudent.item(current_row, 0).text()
        student_name = self.tablesStudent.item(current_row, 1).text()
        student_dob = self.tablesStudent.item(current_row, 2).text()
        student_gender = self.tablesStudent.item(current_row, 3).text()
        student_class = self.tablesStudent.item(current_row, 4).text()
        
        return {
            "student_id": student_id, "student_name": student_name, "student_dob": student_dob,
            "student_gender": student_gender, "student_class": student_class
            }

    # Hàm xử lý khi nhấn nút Thêm
    def open_add_dialog(self):
        """ Mở dialog thêm học sinh """
        self.student_dialog = StudentDialog()
        # exec() sẽ dừng màn hình chính lại chờ Dialog đóng
        if self.student_dialog.exec():
            # Nếu người dùng bấm Lưu (accept) thì load lại bảng
            self.load_data()

    # Hàm xử lý khi nhấn nút Sửa
    def open_edit_dialog(self):
        """ Mở dialog sửa học sinh """
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
        """ Xóa học sinh """
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
        """ Hiển thị trang Student """
        self.mainStack.setCurrentIndex(1)   # Chuyển sang trang Student
        self.load_data()    # load lại dữ liệu 

    # Hàm setup Bảng (Table)
    def setup_table(self):
        """ Setup Bảng (Table) """
        self.tablesStudent.setColumnCount(5) # 5 trường dữ liệu
        self.tablesStudent.setHorizontalHeaderLabels([
            "ID",
            "Họ và Tên",
            "Ngày sinh",
            "Giới tính",
            "Lớp"
        ])

        # Tự động co giãn cột cho lớp
        header = self.tablesStudent.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    # Hàm load dữ liệu vào bảng
    def load_data(self):
        """ Load dữ liệu vào bảng """
        data = get_all_students()
        self.update_student_table(data)

    # Hàm tìm kiếm
    def handle_search(self):
        keyword = self.txtSearch.text().strip()
        
        if not keyword:
            # Nếu ô tìm kiếm rỗng thì load lại toàn bộ danh sách
            self.load_data() 
            return

        # Gọi DB tìm kiếm
        results = search_students(keyword)
        
        self.update_student_table(results) # Gợi ý: Viết hàm update_student_table

    # Hàm update bảng học sinh
    def update_student_table(self, data):
        """ Hàm phụ trợ để đỡ viết lặp code hiển thị """
        self.tablesStudent.setRowCount(len(data))
        for row_index, row_data in enumerate(data):
            raw_dob = row_data[2]
            if raw_dob:
                dob = raw_dob.strftime("%d/%m/%Y")
            else:
                dob = ""

            self.tablesStudent.setItem(row_index, 0, QTableWidgetItem(row_data[0]))
            self.tablesStudent.setItem(row_index, 1, QTableWidgetItem(row_data[1]))
            self.tablesStudent.setItem(row_index, 2, QTableWidgetItem(dob))
            self.tablesStudent.setItem(row_index, 3, QTableWidgetItem(row_data[3]))
            self.tablesStudent.setItem(row_index, 4, QTableWidgetItem(row_data[4]))

    # Hàm xuất bảng điểm ra file Excel
    def export_excel(self):
        """ Xuất bảng điểm hiện tại ra file Excel """
        # 1. Kiểm tra xem đã có dữ liệu chưa
        # Lấy lại dữ liệu từ DB (giống hàm load_score) hoặc lấy từ TableWidget (phức tạp hơn)
        # Cách nhanh nhất: Gọi lại hàm lấy dữ liệu để tạo DataFrame sạch
        class_id = self.cboClassSelect.currentData()
        if not class_id:
             QMessageBox.warning(self, "Lỗi", "Vui lòng chọn lớp trước!")
             return

        raw_data = get_scores_by_class(class_id)
        if not raw_data:
             QMessageBox.warning(self, "Lỗi", "Lớp này chưa có dữ liệu để xuất!")
             return

        # Tạo DataFrame
        df = pd.DataFrame(raw_data, columns=['ID', 'Name', '15m', '45m', 'Final'])
        df.fillna(0, inplace=True)
        df['Average'] = (df['15m'] + df['45m']*2 + df['Final']*3) / 6
        df['Average'] = df['Average'].round(2)

        # 2. Mở hộp thoại chọn nơi lưu file
        # Trả về đường dẫn file người dùng chọn
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Lưu file Excel", 
            "", 
            "Excel Files (*.xlsx);;All Files (*)"
        )

        # 3. Lưu file
        if file_path:
            try:
                # Nếu người dùng quên gõ đuôi .xlsx thì tự thêm vào
                if not file_path.endswith('.xlsx'):
                    file_path += '.xlsx'
                
                # Hàm thần thánh của Pandas
                df.to_excel(file_path, index=False, sheet_name='BangDiem')
                
                QMessageBox.information(self, "Thành công", f"Đã xuất file tại:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể ghi file: {e}")

    # Hàm xử lý khi nhấn nút Đăng xuất
    def handle_logout(self):
        """ Xử lý khi nhấn nút Đăng xuất """
        from windows.login_window import LoginWindow
        self.login = LoginWindow()
        self.login.show()
        self.close()