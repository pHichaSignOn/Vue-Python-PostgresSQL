from db import get_connection #นำเข้าฟังก์ชัน get_connection() จาก module db สำหรับการเชื่อมต่อฐานข้อมูล
from password_utils import hash_password #นำเข้าฟังก์ชัน hash_password() จาก module password_utils สำหรับเข้าระหัส

def add_user(user_nmae: str, plain_password: str, email: str):
    hashed_pw = hash_password(plain_password)

    conn = get_connection()

    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO users (user_name, password, email, created_date)
                    VALUES (%s, %s, %s, NOW())
                    RETURNING user_id
                """,
                    (user_nmae,hashed_pw,email)
                )
                user_id = cursor.fetchone()[0]
        print(f"เพิ่ม user สำเร็จ user_id = {user_id}")

    #การจัดการข้อผิดพลาด   
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")

    #การปิด connection  
    finally:
        conn.close()    

#การรันโดยตรง
if __name__=="__main__":
    # ใส่ plain password ตรงนี้ได้เลย
    add_user("admin02","admin123","admin02@gmail.com")