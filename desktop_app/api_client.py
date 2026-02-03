import requests
from dataclasses import dataclass
from http import HTTPStatus
import logging


# Địa chỉ Server (Backend đang chạy)
# api = ApiClient(os.getenv("API_BASE_URL"))
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

            if response.status_code == HTTPStatus.UNAUTHORIZED:
                return ApiResponse(False,
                    message="Token đã hết hạn hoặc không hợp lệ", 
                    status_code=response.status_code
                )

            if response.status_code == HTTPStatus.FORBIDDEN:
                return ApiResponse(
                    False, 
                    message="Bạn không có quyền truy cập", 
                    status_code=response.status_code
                )      

            if response.status_code == HTTPStatus.NOT_FOUND:
                return ApiResponse(
                    False, 
                    message="Không tìm thấy tài nguyên", 
                    status_code=response.status_code
                )

            if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
                return ApiResponse(
                    False, 
                    message="Lỗi máy chủ", 
                    status_code=response.status_code
                )

            return ApiResponse(
                False, 
                message="Lỗi không xác định", 
                status_code=response.status_code
            )

        except requests.exceptions.ConnectionError:
            return ApiResponse(
                False, 
                message = "Không thể kết nối đến Server! (Bạn đã bật Backend chưa?)", 
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR
            )

        except requests.exceptions.RequestException as e:
            return ApiResponse(False, message = f"Request Error: {e}", status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

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
        if response.success:
            self.set_token(response.data["access_token"])
            self.current_user = response.data["user"]
        return response

    # Lấy thông tin user đang đăng nhập
    def get_my_info(self):
        """
        Gọi API /users/me để lấy thông tin user đang đăng nhập (Name, Role...)
        """
        response = self.request(
            method = 'GET',
            endpoint = '/users/me',
        )
        return response.data if response.success else None

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
        