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
        self.load_data_by_api()

    # Hàm load dữ liệu từ API
    def load_data_by_api(self):
        """Load dữ liệu từ API và hiển thị lên bảng."""
        # 1. Gọi API lấy danh sách users
        users = api_client.get_current_user()

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
        """ Load bảng điểm """
        class_id = self.cboClassSelect.currentIndex()
        raw_data = get_scores_by_class(class_id)
        # --- SỨC MẠNH CỦA PANDAS ---
        # 1. Tạo DataFrame từ dữ liệu thô
        df = pd.DataFrame(raw_data, columns=['ID', 'Name', '15m', '45m', 'Final'])

        # 2. Chuyển đổi dữ liệu sang số (float) để tránh lỗi object/Decimal
        cols = ['15m', '45m', 'Final']
        for col in cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # 3. Xử lý dữ liệu (Điền số 0 vào ô trống để tính toán không lỗi)
        df.fillna(0, inplace=True)
        
        # 3. Tính điểm trung bình (Ví dụ: 15p hệ số 1, 45p hs 2, Thi hs 3)
        df['Average'] = (df['15m'] + df['45m']*2 + df['Final']*3) / 6
        df['Average'] = df['Average'].round(2) # Làm tròn 2 số

        # 4. Đổ DataFrame lên QTableWidget
        self.tableScores.setRowCount(len(df))
        
        for row in range(len(df)):
            # Cột 0: ID (Không cho sửa)
            item_id = QTableWidgetItem(str(df.iloc[row]['ID']))
            item_id.setFlags(item_id.flags() & ~Qt.ItemFlag.ItemIsEditable) # Disable edit
            self.tableScores.setItem(row, 0, item_id)
            
            # Cột 1: Tên (Không cho sửa)
            item_name = QTableWidgetItem(str(df.iloc[row]['Name']))
            item_name.setFlags(item_name.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.tableScores.setItem(row, 1, item_name)
            
            # Cột 2, 3, 4: Điểm (Cho phép sửa bình thường)
            self.tableScores.setItem(row, 2, QTableWidgetItem(str(df.iloc[row]['15m'])))
            self.tableScores.setItem(row, 3, QTableWidgetItem(str(df.iloc[row]['45m'])))
            self.tableScores.setItem(row, 4, QTableWidgetItem(str(df.iloc[row]['Final'])))
            
            # Cột 5: Điểm TB (Không cho sửa)
            self.tableScores.setItem(row, 5, QTableWidgetItem(str(df.iloc[row]['Average'])))
            
        self.draw_chart(df)

    # Hàm lưu điểm
    def save_scores_data(self):
        """ Quét dữ liệu trên bảng và lưu vào DB """
        data_to_save = []
        rows = self.tableScores.rowCount()
        
        for row in range(rows):
            s_id = self.tableScores.item(row, 0).text()
            
            # Lấy điểm, nếu user xóa trắng thì coi là 0
            try:
                sc_15 = float(self.tableScores.item(row, 2).text())
            except: sc_15 = 0.0
            
            try:
                sc_45 = float(self.tableScores.item(row, 3).text())
            except: sc_45 = 0.0
                
            try:
                sc_final = float(self.tableScores.item(row, 4).text())
            except: sc_final = 0.0
            
            data_to_save.append((s_id, sc_15, sc_45, sc_final))
            
        if save_score_list(data_to_save):
            QMessageBox.information(self, "Thành công", "Đã lưu bảng điểm!")
            self.load_score_table() # Load lại để Pandas tính lại điểm TB mới nhất
        else:
            QMessageBox.critical(self, "Lỗi", "Lưu thất bại.")

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