from __future__ import annotations

from flask import jsonify
from flask_restful import Resource, request

from database.mssql import conn, cursor
from frontend.helper_web.MESSAGE import CREATE_GENERAL_MSG, MISSING_ARGS_MSG
from frontend.helper_web.validate_args import validate_args


class TeacherAPI(Resource):
    def get(self):
        validate_success, message_body, missing_args = validate_args(request.get_json(silent=True), tuple(["teacher_id"]))
        if not validate_success:
            return jsonify({"message": MISSING_ARGS_MSG(missing_args)}), 400
        teacher_id = message_body["teacher_id"]

        cursor.execute(f"SELECT * FROM teacher WHERE TeacherID = '{teacher_id}'")
        row = cursor.fetchone()
        if row is None:
            return jsonify({"message": CREATE_GENERAL_MSG(action="not found", typeof_object="teacher", id=teacher_id)}), 404

        return (
            jsonify(
                {
                    "message": CREATE_GENERAL_MSG(action="found", typeof_object="teacher", id=teacher_id),
                    "data": {
                        "teacher_id": row[0],
                        "teacher_name": row[1],
                        "date_of_birth": row[2],
                        "email": row[3],
                    },
                }
            ),
            200,
        )

    def post(self):
        validate_success, message_body, missing_args = validate_args(
            request.get_json(silent=True), tuple(["teacher_id", "teacher_name", "date_of_birth", "email"])
        )
        if not validate_success:
            return jsonify({"message": MISSING_ARGS_MSG(missing_args)}), 400
        teacher_id, teacher_name, date_of_birth, email = (
            message_body["teacher_id"],
            message_body["teacher_name"],
            message_body["date_of_birth"],
            message_body["email"],
        )

        cursor.execute(f"SELECT * FROM teacher WHERE TeacherID = '{teacher_id}'")
        db_result = cursor.fetchone()
        if db_result is not None:
            return (
                jsonify({"message": CREATE_GENERAL_MSG(action="already exists", typeof_object="teacher", id=teacher_id)}),
                409,
            )

        cursor.execute(f"INSERT INTO teacher VALUES ('{teacher_id}', '{teacher_name}', '{date_of_birth}', '{email}')")
        conn.commit()

        return jsonify({"message": CREATE_GENERAL_MSG(action="added", typeof_object="teacher", id=teacher_id)}), 201

    def put(self):
        validate_success, message_body, missing_args = validate_args(
            request.get_json(silent=True), tuple(["teacher_id", "teacher_name", "date_of_birth", "email"])
        )
        if not validate_success:
            return jsonify({"message": MISSING_ARGS_MSG(missing_args)}), 400
        teacher_id, teacher_name, date_of_birth, email = (
            message_body["teacher_id"],
            message_body["teacher_name"],
            message_body["date_of_birth"],
            message_body["email"],
        )

        cursor.execute(f"SELECT * FROM teacher WHERE TeacherID = '{teacher_id}'")
        db_result = cursor.fetchone()
        if db_result is None:
            cursor.execute(f"INSERT INTO teacher VALUES ('{teacher_id}', '{teacher_name}', '{date_of_birth}', '{email}')")
        else:
            cursor.execute(
                f"UPDATE teacher SET TeacherName = '{teacher_name}', DateOfBirth = '{date_of_birth}', Email = '{email}' WHERE TeacherID = '{teacher_id}'"
            )

        return (
            jsonify(
                {
                    "message": CREATE_GENERAL_MSG(
                        action=("added" if db_result is None else "updated"), typeof_object="teacher", id=teacher_id
                    )
                }
            ),
            200,
        )

    def delete(self):
        validate_success, message_body, missing_args = validate_args(request.get_json(silent=True), tuple(["teacher_id"]))
        if not validate_success:
            return jsonify({"message": MISSING_ARGS_MSG(missing_args)}), 400
        teacher_id = message_body["teacher_id"]

        cursor.execute(f"DELETE FROM teacher WHERE TeacherID = '{teacher_id}'")
        conn.commit()

        return jsonify({"message": CREATE_GENERAL_MSG(action="deleted", typeof_object="teacher", id=teacher_id)}), 200
