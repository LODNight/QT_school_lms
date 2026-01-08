from database import create_connection,check_login

print("-- KIEM TRA HE THONG KET NOI --")

# 1. Test ket noi 
print("\n[B1]: Dang ket noi thu toi xampp...")
conn = create_connection()
if conn is not None:
    print("\nKet noi thanh cong")
    print("\nThong tin server:", conn.get_server_info())
    conn.close()
else:
    print("\nKet noi that bai")


# 2. Test Truy van
print("\n[B2]: Thu ket noi dang nhap voi username 'admin'...")
is_success, full_name, role = check_login('admin', '123456')


if is_success: 
    print("\nDang nhap thanh cong")
    print(f"\nHo ten: {full_name}")
    print(f"\nVai tro: {role}")
else:
    print("\nDang nhap that bai")
print("\n -- KET THUC --")