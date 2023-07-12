from __future__ import annotations

from flask import jsonify
from flask_restful import Resource, request

from database.mssql import conn, cursor


class Teacher(Resource):
    def get(self):
        data = request.get_json()
        if data is None or data["teacher_id"] is None:
            return jsonify({"message": "No input data provided"}), 400
        teacher_id = data["teacher_id"]

        cursor.execute(f"SELECT * FROM teacher WHERE TeacherID = '{teacher_id}'")
        row = cursor.fetchone()
        if row is None:
            return jsonify({"message": "Teacher not found"}), 404

        return jsonify({"TeacherID": row[0], "TeacherName": row[1], "DateOfBirth": row[2], "Email": row[3]}), 200

    def post(self):
        data = request.get_json()
        if data is None:
            return jsonify({"message": "No input data provided"}), 400
        teacher_id = data["teacher_id"]
        teacher_name = data["teacher_name"]
        date_of_birth = data["date_of_birth"]
        email = data["email"]

        cursor.execute(f"SELECT * FROM teacher WHERE TeacherID = '{teacher_id}'")
        row = cursor.fetchone()
        if row is not None:
            return jsonify({"message": "Teacher already exists"}), 400

        cursor.execute(f"INSERT INTO teacher VALUES ('{teacher_id}', '{teacher_name}', '{date_of_birth}', '{email}')")
        conn.commit()

        return jsonify({"message": f"Teacher {teacher_id} added successfully"}), 201

    def put(self):
        data = request.get_json()
        if data is None:
            return jsonify({"message": "No input data provided"}), 400
        teacher_id = data["teacher_id"]
        teacher_name = data["teacher_name"]
        date_of_birth = data["date_of_birth"]
        email = data["email"]

        cursor.execute(
            f"UPDATE teacher SET TeacherName = '{teacher_name}', DateOfBirth = '{date_of_birth}', Email = '{email}' WHERE TeacherID = '{teacher_id}'"
        )
        conn.commit()

        return jsonify({"message": f"Teacher {teacher_id} updated successfully"}), 200

    def delete(self):
        data = request.get_json()
        if data is None or data["teacher_id"] is None:
            return jsonify({"message": "No input data provided"}), 400
        teacher_id = data["teacher_id"]

        cursor.execute(f"DELETE FROM teacher WHERE TeacherID = '{teacher_id}'")
        conn.commit()

        return jsonify({"message": f"Teacher {teacher_id} deleted successfully"}), 200
