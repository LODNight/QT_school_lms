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

