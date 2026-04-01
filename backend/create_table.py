from db import (
    get_connection,
)  # นำเข้าฟังก์ชัน get_connection() จาก module db สำหรับการเชื่อมต่อฐานข้อมูล


def create_users_table():
    conn = get_connection()

    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        user_id SERIAL PRIMARY KEY,
                        user_name VARCHAR(100) UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        email VARCHAR(100) UNIQUE,
                        created_date TIMESTAMP DEFAULT NOW()
                    )                
                """
                )
        print("สร้างตาราง users เสร็จแล้ว")
    except Exception as e:
        print(f"เกิดข้อผิดพลาf: {e}")

    finally:
        conn.close()


def create_locations_table():
    """สร้างตาราง locations"""
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cursor:
                # สร้างตาราง locations
                cursor.execute(
                    """
                    CREATE TABLE locations (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100),
                        description VARCHAR(200),
                        latitude DOUBLE PRECISION,
                        longitude DOUBLE PRECISION,
                        status INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );  
                    """
                )
                print("ตรวจสอบ/สร้างตาราง locations สำเร็จแล้ว")

    except Exception as e:
        print(f"เกิดข้อผิดพลาด location: {e}")

    finally:
        conn.close()


# การรันโดยตรง
if __name__ == "__main__":
    # ถ้ารันไฟล์นี้โดยตรง จะเรียกฟังก์ชันสร้างตาราง
    create_users_table()
    create_locations_table()
