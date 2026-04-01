import bcrypt #ใช้สำหรับการเข้ารหัสรหัสผ่านและตรวจสอบรหัสผ่านด้วย library bcrypt บีคริปต์

def hash_password(plain_password: str) ->str:
    salt = bcrypt.gensalt() #สร้าง salt เรียก method gensalt สุ่มค่าความปลอดภัย
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"),salt) #เข้ารหัสรหัสพร้อมกับ salt

    return hashed.decode("utf-8") # แปลงผลลัพธ์ที่เข้ารหัสแล้วกลับเป็น string สำหรับเก็บใน database

def check_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), #ตรวจว่ารหัสผ่านที่ให้มาตรงกับที่เข้ารหัสไว้หรือไม่
        hashed_password.encode("utf-8"), # แปลงรหัสผ่านที่เก็บใน database กลับเป็น bytes
    )