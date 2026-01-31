import requests

# Địa chỉ Server (Backend đang chạy)
BASE_URL = "http://127.0.0.1:8000"

# Biến toàn cục để lưu Token sau khi đăng nhập thành công
CURRENT_TOKEN = None
CURRENT_USER_INFO = None

def login(username, password):
    """
    Gửi username/pass lên API để xin Token
    """
    global CURRENT_TOKEN
    
    url = f"{BASE_URL}/token"
    # API Login yêu cầu gửi dạng Form (x-www-form-urlencoded)
    payload = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(url, data=payload)
        
        if response.status_code == 200:
            data = response.json()
            CURRENT_TOKEN = data["access_token"]
            return True, "Đăng nhập thành công!"
        elif response.status_code == 401:
            return False, "Sai tên đăng nhập hoặc mật khẩu!"
        else:
            return False, f"Lỗi Server: {response.status_code}"
            
    except requests.exceptions.ConnectionError:
        return False, "Không thể kết nối đến Server! (Bạn đã bật Backend chưa?)"
    except Exception as e:
        return False, f"Lỗi không xác định: {e}"

def get_auth_header():
    """ Hàm phụ trợ: Tạo header chứa Token để dùng cho các request sau """
    if CURRENT_TOKEN:
        return {"Authorization": f"Bearer {CURRENT_TOKEN}"}
    return {}

def get_my_info():
    """
    Gọi API /users/me để lấy thông tin user đang đăng nhập (Name, Role...)
    """
    url = f"{BASE_URL}/users/me"
    headers = get_auth_header()
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def get_current_user():
    """
    Gọi API lấy danh sách Users (Admin only)
    NOTE: Tên hàm hơi dễ nhầm lẫn, đây là lấy TOÀN BỘ user
    """
    url = f"{BASE_URL}/users"
    headers = get_auth_header() # Lấy header chứa Token
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            print(f"Token đã hết hạn hoặc không hợp lệ")
            return []
        else:
            print(f"Lỗi Server: {response.status_code}")
            return []
    except requests.exceptions.ConnectionError:
        print(f"Không thể kết nối đến Server!")
        return []
    except Exception as e:
        print(f"Lỗi kết nối: {e}")
        return []