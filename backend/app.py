from flask import Flask
from flask_jwt_extended import JWTManager # สำหรับจัดการ JWT
from flask_cors import CORS # เพิ่ม import นี้สำหรับแก้ไข CORS
from config import JWT_SECRET_KEY # นำค่า secret key จาก config
from auth import auth_bp # นำเข้า auth blueprint
from locations import locations_bp # นำเข้า locations blueprint
from datetime import timedelta # นำเข้า datetime

# สร้าง Flask application
app = Flask(__name__)

# ตั้งค่า CORS - สำคัญมากสำหรับให้ frontend เรียก API ได้
CORS(app) # อนุญาตทุก origin (สำหรับ development)

# ตั้งค่า JWT secret key สำหรับการเข้ารหัสและถอดรหัส tokens
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

# ตั้งค่าเวลา jwt
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)

# Initialize JWTManager กับ app
jwt = JWTManager(app)

# ลงทะเบียน Blueprint
app.register_blueprint(auth_bp)

# insert data ลง database
app.register_blueprint(locations_bp)

# Route พื้นฐาน
# จัดการ favicon เพื่อป้องกัน error 404
@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")    

# Route หลักที่คืนค่า JSON response พื้นฐาน
@app.route("/")
def root():
    return {"Hello": "World"}

# การรัน application
if __name__ =="__main__":
    app.run(debug=False, host='0.0.0.0', port=5000) # เปลี่ยน host และ port