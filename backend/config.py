import os
from dotenv import load_dotenv

load_dotenv() # โหลดค่า .env ถ้ามี

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") #คือ คีย์ลับ (Secret Key) ที่ใช้ในการเข้ารหัสและถอดรหัส JWT (JSON Web Token)