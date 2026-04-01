import os #ใช้สำหรับเข้าถึง environment variables ของระบบ
import psycopg2 #library หลักสำหรับเชื่อมต่อกับ PostgreSQL database
from dotenv import load_dotenv #ใช้สำหรับโหลดค่าจากไฟล์ .env

load_dotenv() #โหลดค่าจากไฟล์ .env ใน directory

def get_connection(): #ฟังก์ชัน get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )