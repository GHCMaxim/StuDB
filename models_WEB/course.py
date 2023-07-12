from __future__ import annotations

from flask import jsonify
from flask_restful import Resource, request

from database.mssql import conn, cursor


class Course(Resource):
    def get(self):
        message_body = request.get_json()
        if (message_body == {}) or ("course_id" not in message_body.keys()):
            return jsonify({"message": "Bad Request"}), 400

        course_id = message_body["course_id"]
        cursor.execute("SELECT * FROM course WHERE course_id = %s", course_id)
        db_result = cursor.fetchone()
        if db_result is None:
            return jsonify({"message": f"Course '{course_id}' Not Found"}), 404

        return (
            jsonify(
                {
                    "message": "Success",
                    "data": {
                        "course_id": db_result[0],
                        "course_name": db_result[1],
                        "teacher_id": db_result[2],
                        "credits": db_result[3],
                    },
                }
            ),
            200,
        )

    def post(self):
        message_body = request.get_json()
        not_enough_keys = any(
            key not in message_body.keys() for key in ["course_id", "course_name", "teacher_id", "credits"]
        )
        if (message_body == {}) or not_enough_keys:
            return jsonify({"message": "Bad Request"}), 400

    def put(self):
        message_body = request.get_json()
        not_enough_keys = any(key not in message_body.keys() for key in ["course_id", "course_name", "teacher_id"])

        if (message_body is None) or not_enough_keys:
            return jsonify({"message": "Bad Request"}), 400

        course_id, course_name, teacher_id = (
            message_body["course_id"],
            message_body["course_name"],
            message_body["teacher_id"],
        )

        cursor.execute("SELECT * FROM course WHERE course_id = %s", course_id)
        db_result = cursor.fetchone()
        if db_result is None:
            cursor.execute(
                "INSERT INTO course VALUES (%s, %s, %s)",
                (course_id, course_name, teacher_id),
            )
        else:
            cursor.execute(
                "UPDATE course SET course_name = %s, teacher_id = %s WHERE course_id = %s",
                (course_name, teacher_id, course_id),
            )
        conn.commit()

        return (
            jsonify({"message": f"Course '{course_name}' {'created' if db_result is None else 'updated'}"}),
            200,
        )

    def delete(self):
        message_body = request.get_json()
        if (message_body == {}) or ("course_id" not in message_body.keys()):
            return jsonify({"message": "Bad Request"}), 400
        course_id = message_body["course_id"]

        cursor.execute(f"SELECT * FROM course WHERE course_id = {course_id}")
        db_result = cursor.fetchone()
        if db_result is None:
            return jsonify({"message": "Not Found"}), 404

        cursor.execute(f"DELETE FROM course WHERE course_id = {course_id}")
        conn.commit()

        return jsonify({"message": f"Course '{db_result[1]}' deleted"}), 200
