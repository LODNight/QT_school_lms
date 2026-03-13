import requests
from dataclasses import dataclass
from http import HTTPStatus
import logging


# Địa chỉ Server (Backend đang chạy)
BASE_URL = "http://127.0.0.1:8000"

@dataclass
class ApiResponse:
    success: bool
    data: any = None
    message: str = ""
    status_code: int = None

class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None
        self.current_user = None
        self.session = requests.Session()

    def set_token(self, token):
        self.token = token
        self.session.headers.update({
            "Authorization": f"Bearer {token}"
        })
        
    def request(self, method, endpoint, **kwargs):
        try: 
            response = self.session.request(
                method,
                f"{self.base_url}{endpoint}",
                timeout=5,
                **kwargs
            )

            if response.ok:
                return ApiResponse(True, response.json(), status_code=response.status_code)

            message = {
                HTTPStatus.UNAUTHORIZED: "Token hết hạn",
                HTTPStatus.FORBIDDEN: "Không có quyền",
                HTTPStatus.NOT_FOUND: "Không tìm thấy tài nguyên",
                HTTPStatus.INTERNAL_SERVER_ERROR: "Lỗi máy chủ"
            }

            return ApiResponse(
                False,
                message = message.get(response.status_code, f"Lỗi: {response.status_code}"),
                status_code = response.status_code
            )

        except requests.exceptions.RequestException as e:
            return ApiResponse(False, message = f"Lỗi kết nối: {str(e)}")

    # Đăng nhập để nhận Token
    def login(self, username, password):
        """
        Gửi username/pass lên API để xin Token
        """
        response = self.request(
            method="POST", 
            endpoint="/token", 
            data={
                "username": username,
                "password": password
            }
        )
        if not response.success:
            return response
        
        # Chỉ set token
        self.set_token(response.data["access_token"])
        
        # Gọi API lấy user
        user_response = self.request(
            method="GET",
            endpoint="/users/me"
        )

        if not user_response.success:
            return ApiClient(
                False,
                message = "Đăng nhập thành công nhưng không lấy được thông tin user"
            )
        
        self.current_user = user_response.data
        return response


    # Lấy danh sách Users (Admin only)
    def get_all_users(self):
        """
        Gọi API lấy danh sách Users (Admin only)
        """
        response = self.request(
            method = 'GET',
            endpoint = '/users',
        )
        return response.data if response.success else []
        
    # Lấy danh sách Lớp
    def get_all_classes(self):
        """ Gọi API lấy danh sách Lớp """
        response = self.request(
            method = 'GET',
            endpoint = '/classes',
        )
        return response.data if response.success else []
        
    # Lấy danh sách khóa học
    def get_all_course(self):
        """ Gọi API lấy danh sách khóa học """
        response = self.request(
            method = 'GET',
            endpoint = '/courses',
        )
        return response.data if response.success else []

    def get_grade_board(self, class_id):
        """ Gọi API lấy bảng điểm của 1 lớp """
        return self.request(
            method = 'GET',
            endpoint = f'/classes/{class_id}/grade-board',
        )

    def save_grades(self, grades_list):
        """ Gọi API cập nhật điểm số """
        return self.request(
            method = 'POST',
            endpoint = '/grades/update',
            json = grades_list
        )


# --- SINGLETON INSTANCE ---
client = ApiClient(BASE_URL)
