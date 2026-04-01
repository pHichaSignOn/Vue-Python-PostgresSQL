# locations.py
from flask import Blueprint, jsonify, request
from db import get_connection

locations_bp = Blueprint("locations", __name__)


# ---------------- INSERT LOCATIONS----------------
@locations_bp.route("/locations/insert", methods=["POST"])
def insert_locations():
    data = request.get_json()

    if not data:
        return jsonify({"error": "ไม่พบข้อมูลที่ส่งมา"}), 400

    name = data.get("name")
    description = data.get("default")
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if not name or not description or latitude is None or longitude is None:
        return jsonify({"error": "ข้อมูลไม่ครบ"}), 400

    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
                INSERT INTO locations (name, description, latitude, longitude, status)
                VALUES (%s, %s, %s, %s, %s)
            """,
            (name, description, latitude, longitude, 1),
        )

        conn.commit()
        return jsonify({"message": "บันทึกข้อมูลสำเร็จ"}), 200

    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        if conn:
            conn.close()
        if cur:
            cur.close()


# ---------------- READ LOCATIONS ----------------
@locations_bp.route("/locations/read", methods=["GET"])
def get_locations():
    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT id, name, description, latitude, longitude
            FROM locations
            WHERE status = 1
            ORDER BY id DESC
            """
        )
        rows = cur.fetchall()

        data = [
            {
                "id": r[0],
                "name": r[1],
                "description": r[2],
                "latitude": float(r[3]),
                "longitude": float(r[4]),
            }
            for r in rows
        ]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# ---------------- UPDATE LOCATIONS ----------------
@locations_bp.route("/locations/update/<int:id>", methods=["PUT"])
def update_locations(id):
    data = request.json

    name = data.get("name")
    description = data.get("default")
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE locations
            SET name=%s, description=%s, latitude=%s, longitude=%s
            WHERE id=%s
            """,
            (name, description, latitude, longitude, id),
        )
        conn.commit()

        return jsonify({"message": "แก้ไขสำเร็จ"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()


# ---------------- DELETE LOCATIONS ----------------
@locations_bp.route("/locations/delete/<int:id>", methods=["DELETE"])
def delete_locations(id):

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM locations WHERE id=%s", (id,))
        conn.commit()

        return jsonify({"message": "ลบสำเร็จ"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()
