from db import get_connection  # get_connection - สำหรับเชื่อมต่อฐานข้อมูล

from flask import (
    Blueprint,
    request,
    jsonify,
)  # Blueprints - สำหรับจัดกลุ่ม route request, jsonify - สำหรับจัดการ HTTP request และ response
from flask_jwt_extended import (
    create_access_token,jwt_required
)  # create_access_token - สำหรับสร้าง JWT token
import bcrypt  # bcrypt - สำหรับตรวจสอบรหัสผ่าน

auth_bp = Blueprint(
    "auth", __name__
)  # สร้าง Blueprint ชื่อ "auth" สำหรับจัดกลุ่ม route ที่เกี่ยวข้องกับการ authentication


@auth_bp.route("/login", methods=["POST"])
def login():
    # Debug information
    print("Request headers:", request.headers)
    print("Request data:", request.data)
    print("Request json:", request.json)

    # ตรวจสอบ input
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # ตรวจสอบว่ามี username และ password - ถ้าไม่มีคืน error 400
    if not username or not password:
        return {"error": "username และ password ไม่มีค่า"}, 400

    # การค้นหาผู้ใช้ในฐานข้อมูล
    try:
        conn = get_connection()
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT user_id, user_name, password FROM users WHERE user_name = %s",
                    (username,),
                )
                user = cursor.fetchone()

        if not user:
            return {"error": "ไม่มีผู้ใช้"}, 404

        user_id, user_name, hashed_password = user

        # ตรวจสอบ password (ใช้ bcrypt หรือ check_password)
        if bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
            # สร้าง JWT token
            access_token = create_access_token(
                identity=user_name,  # ใช้ user_name เป็น principal
                additional_claims={
                    "user_id": user_id
                },  # เพิ่ม user_id ใน payload ของ token
            )
            # การคืนค่า response JSON - มี access_token สำหรับใช้ในการยืนยันตัวตน
            return (
                jsonify({"access_token": access_token}),
                200,
            )  # Status code 200 - ล็อกอินสำเร็จ
        else:
            return {"error": "รหัสผ่านไม่ถูกต้อง"}, 401  # รหัสผ่านผิด

    # การจัดการข้อผิดพลาด
    except Exception as e:
        return {"error": str(e)}, 500  # ข้อผิดพลาดอื่นๆ

# INSERT USER
@auth_bp.route("/user/insert", methods=["POST"])
@jwt_required()
def insert_user():
    data = request.json
    user_name = data.get("user_name")
    email = data.get("email")
    password = data.get("password")
    status = data.get("status")
    #print("data : ", data)

    if not user_name or not email or not password or not status:
        return {"error" : "ข้อมูลไม่ครบ"}, 400
    
    try:
        conn = get_connection()
        with conn:
            with conn.cursor() as cursor:
                # 🔎 ตรวจสอบ user_name ซ้ำ
                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM users
                    WHERE user_name = %s
                    """,
                    (user_name,)
                )
                duplicate_count = cursor.fetchone()[0]

                if duplicate_count > 0:
                    return {"error": "ชื่อผู้ใช้นี้ถูกใช้งานแล้ว !!!"}, 400
                
                # 🔐 เข้ารหัสรหัสผ่าน
                hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

                # ✅ บันทึกข้อมูลใหม่
                cursor.execute(
                    """
                    INSERT INTO users (user_name, email, password, status, created_date)
                    VALUES (%s,%s,%s,%s,NOW())                
                    """,
                    (user_name, email, hashed_pw, status),
                )

        return {"message": "เพิ่มข้อมูลสำเร็จ"}, 201
    
    except Exception as e:
        #print("Error in insert user :", e)
        return {"error": str(e)}, 500

# UPDATE USER
@auth_bp.route("/user/update/<int:user_id>", methods=["PUT"])
@jwt_required()
def put_update_user(user_id):
    data = request.json
    user_name = data.get("user_name")
    email = data.get("email")
    password = data.get("password")
    status = data.get("status")

    # print("user_id : ",user_id)
    # print("data : ",data)

    if not user_name or not email or not status:
        return {"error" : "ข้อมูลไม่ครบ"}, 400
    
    try:
        conn = get_connection()
        with conn:
            with conn.cursor() as cursor:
                # 🔎 ตรวจสอบ user_name ซ้ำ (ยกเว้น user_id ที่แก้ไขอยู่)
                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM users
                    WHERE user_name = %s AND user_id != %s
                    """,
                    (user_name,user_id),
                ) 
                duplicate_count = cursor.fetchone()[0]   
                
                if duplicate_count > 0:
                    return {"error": "ชื่อผู้ใช้นี้ถูกใชเงานไปแล้ว"}, 400
                
                if password:
                # 🔐 เข้ารหัสรหัสผ่าน
                    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                    # print("เข้ารหัสรหัสผ่าน : ",hashed_pw)
                    cursor.execute(
                        """
                        UPDATE users
                        SET user_name = %s, email = %s, password = %s, status = %s, updated_date = NOW()
                        WHERE user_id = %s
                        """,
                        (user_name, email, hashed_pw, status, user_id)
                    )
                else:
                    cursor.execute(
                        """
                        UPDATE users
                        SET user_name = %s, email = %s, status = %s, updated_date = NOW()
                        WHERE user_id = %s
                        """,
                        (user_name, email, status, user_id)
                    )
                    
        return jsonify({"message": "แก้ไขข้อมูลเสร็จแล้ว"}), 200
    
    except Exception as e:
        print("Error in update_user : ", e)
        return {"error" : str(e)}, 500

# GET USER
@auth_bp.route("/user", methods=["GET"])
@jwt_required()
def get_user_info():  
    try:
        conn = get_connection()
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT user_id, user_name, email, status, created_date, updated_date
                    FROM users
                    ORDER BY user_id ASC
                    """
                )
                users = cursor.fetchall()

        user_list = []
        for u in users:
            user_list.append(
                {
                    "user_id": u[0],
                    "user_name": u[1],
                    "email": u[2],
                    "status": u[3],
                    "created_date": u[4],
                    "updated_date": u[5],
                }
            )
        return jsonify(user_list),200
            
    except Exception as e:
        return {"error": str(e)}, 500    
    
# GET STATUS
@auth_bp.route("/user_status", methods=["GET"])
def get_status_info():
    try:
        conn = get_connection()
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, status_name 
                    FROM user_status
                    ORDER BY id ASC
                    """
                )
                status = cursor.fetchall()
        
        status_list = []
        for s in status:
            status_list.append(
                {
                    "id": s[0],
                    "status_name": s[1],
                }
            )
        return jsonify(status_list),200

    except Exception as e:
        return {"error": str(e)}, 500            

# GET DELETE
@auth_bp.route("/user/delete/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    try:
        conn = get_connection()
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE user_id = %s",(user_id,))
        return {"message": "ลบข้อมูลสำเร็จแล้ว"}, 200        
    except Exception as e:
        return {"error": str(e)}, 500    