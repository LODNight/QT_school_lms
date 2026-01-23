import mysql.connector
from mysql.connector import Error

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='school_lms_db'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def check_login(username, password):
    conn = create_connection()
    cursor = None
    if conn:
        try:
            cursor = conn.cursor(dictionary = True)
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))

            user = cursor.fetchone()

            if user:
                return True, user['full_name'], user['role']
            else:
                return False, None, None
        except Error as e:
            print(f"Error: {e}")
        finally:
            if conn.is_connected():
                if cursor:
                    cursor.close()
                conn.close()
    return False, None, None


# Get Student         
def get_all_students():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            querry = """
                SELECT s.student_id, s.full_name, s.dob, s.gender, c.class_name
                FROM students s
                LEFT JOIN classes c ON c.class_id = s.class_id 
            """
            cursor.execute(querry) 
            result = cursor.fetchall() # Lấy về list các tuple
            return result
        except Error as e:
            print(f"Error: {e}")
        finally:
            if conn.is_connected():
                if cursor:
                    cursor.close()
                conn.close()
    return []

# Add Student 
def add_students(student_id, full_name, dob, gender, class_id):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            querry = """
                INSERT INTO students (student_id, full_name, dob, gender, class_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(querry, (student_id, full_name, dob, gender, class_id))
            conn.commit()
            return True
        except Error as e:
            print(f"Error: {e}")
        finally:
            if conn.is_connected():
                if cursor:
                    cursor.close()
                conn.close()
    return False

# Update Student
def update_student(student_id, full_name, dob, gender, class_id):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()

            # Câu lệnh Querry
            querry = """
                UPDATE students
                SET full_name = %s, dob = %s, gender = %s, class_id = %s
                WHERE student_id = %s
            """
            # Thuc hien cau lenh querry
            cursor.execute(querry, (full_name, dob, gender,class_id, student_id))

            # Luu thay doi vao database
            conn.commit()

            return True
        except Error as e:
            print(f"ERROR: {e}")
        finally:
            if conn.is_connected():
                if cursor:
                    cursor.close()
                conn.close()
    return False

def delete_student(student_id):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            querry = """
                DELETE FROM students
                WHERE student_id = %s
            """
            cursor.execute(querry, (student_id,))
            conn.commit()
            return True
        except Error as e:
            print(f"ERROR: {e}")
        finally:
            if conn.is_connected():
                if cursor:
                    cursor.close()
                conn.close()
    return False



# Classes 
def get_all_classes():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            querry = """
                SELECT class_id, class_name 
                FROM classes
                """
            cursor.execute(querry) 
            result = cursor.fetchall() # Lấy về list các tuple
            return result
        except Error as e:
            print(f"Error: {e}")
        finally:
            if conn.is_connected():
                if cursor:
                    cursor.close()
                conn.close()
    return []



# Get Score List
def get_scores_by_class(class_id):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            querry = """
                SELECT s.student_id, s.full_name,
                       sc.score_15m, sc.score_45m, sc.score_final
                FROM students s
                LEFT JOIN scores sc ON sc.student_id = s.student_id AND subject_name = 'Toán'
                WHERE s.class_id = %s
            """
            cursor.execute(querry, (class_id,))
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Error: {e}")
        finally:
            if conn.is_connected():
                if cursor:
                    cursor.close()
                conn.close()
    return []

# Save Score List
def save_score_list(data_list):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Cú pháp UPSERT của MySQL
            querry = """
                INSERT INTO scores (student_id, subject_name, score_15m, score_45m, score_final)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                score_15m = VALUES(score_15m),
                score_45m = VALUES(score_45m),
                score_final = VALUES(score_final)
            """
            # data_list chứa nhiều dòng, dùng executemany cho nhanh
            cursor.executemany(querry, data_list)
            conn.commit()
            return True
        except Error as e:
            print(f"Error: {e}")
        finally:
            if conn.is_connected():
                if cursor:
                    cursor.close()
                conn.close()
    return False