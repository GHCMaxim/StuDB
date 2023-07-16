from __future__ import annotations

from datetime import datetime

from flask_restful import Resource, request

from database.mssql import conn, cursor
from frontend.helper_web.have_permission import have_permission
from frontend.helper_web.MESSAGE import ACTION_MUST_BE_CRUD, CREATE_GENERAL_MSG, INVALID_ROLE, MISSING_ARGS_MSG
from frontend.helper_web.validate_args import validate_args


class TeacherAPI(Resource):
    def post(self):
        validate_success, message_body, missing_args = validate_args(request.get_json(silent=True), tuple(["action"]))
        if not validate_success:
            return {"message": MISSING_ARGS_MSG(missing_args), "data": {}}, 400
        match message_body["action"].lower():
            case "create":
                return self.CREATE()
            case "read":
                return self.READ()
            case "update":
                return self.UPDATE()
            case "delete":
                return self.DELETE()
            case _:
                return {"message": ACTION_MUST_BE_CRUD, "data": {}}, 400

    def READ(self):
        validate_success, message_body, missing_args = validate_args(request.get_json(silent=True), tuple(["teacher_id"]))
        if not validate_success:
            return {"message": MISSING_ARGS_MSG(missing_args), "data": {}}, 400
        teacher_id = message_body["teacher_id"]
        if teacher_id == "":
            return {"message": "teacher_id cannot be empty", "data": {}}, 400

        cursor.execute(f"SELECT * FROM Teachers WHERE TeacherID = '{teacher_id}'")
        row = cursor.fetchone()
        if row is None:
            return {
                "message": CREATE_GENERAL_MSG(action="not found", typeof_object="teacher", id=teacher_id),
                "data": {},
            }, 404

        return (
            {
                "message": CREATE_GENERAL_MSG(action="found", typeof_object="teacher", id=teacher_id),
                "data": {
                    "teacher_id": row[0],
                    "teacher_name": row[1],
                    "date_of_birth": datetime.strftime(row[2], "%Y-%m-%d"),
                    "email": row[3],
                },
            },
            200,
        )

    def CREATE(self):
        validate_success, message_body, missing_args = validate_args(
            request.get_json(silent=True), tuple(["teacher_id", "teacher_name", "date_of_birth", "email", "session_key"])
        )
        if not validate_success:
            return {"message": MISSING_ARGS_MSG(missing_args), "data": {}}, 400
        teacher_id, teacher_name, date_of_birth_str, email, session_key = (
            message_body["teacher_id"],
            message_body["teacher_name"],
            message_body["date_of_birth"],
            message_body["email"],
            message_body["session_key"],
        )
        if not have_permission(session_key, admin_only=True):
            return {"message": INVALID_ROLE, "data": {}}, 403

        if (teacher_id == "") or (teacher_name == "") or (date_of_birth_str == "") or (email == ""):
            return {"message": "all fields cannot be empty", "data": {}}, 400

        cursor.execute(f"SELECT * FROM Teachers WHERE TeacherID = '{teacher_id}'")
        db_result = cursor.fetchone()
        if db_result is not None:
            return (
                {"message": CREATE_GENERAL_MSG(action="already exists", typeof_object="teacher", id=teacher_id), "data": {}},
                409,
            )

        cursor.execute(f"INSERT INTO Teachers VALUES ('{teacher_id}', '{teacher_name}', '{date_of_birth_str}', '{email}')")
        conn.commit()

        return {
            "message": CREATE_GENERAL_MSG(action="added", typeof_object="teacher", id=teacher_id),
            "data": {
                "teacher_id": teacher_id,
                "teacher_name": teacher_name,
                "date_of_birth": date_of_birth_str,
                "email": email,
            },
        }, 201

    def UPDATE(self):
        validate_success, message_body, missing_args = validate_args(
            request.get_json(silent=True), tuple(["teacher_id", "teacher_name", "date_of_birth", "email", "session_key"])
        )
        if not validate_success:
            return {"message": MISSING_ARGS_MSG(missing_args), "data": {}}, 400
        teacher_id, teacher_name, date_of_birth, email, session_key = (
            message_body["teacher_id"],
            message_body["teacher_name"],
            message_body["date_of_birth"],
            message_body["email"],
            message_body["session_key"],
        )
        if not have_permission(session_key, admin_only=True):
            return {"message": INVALID_ROLE, "data": {}}, 403

        if teacher_id == "":
            return {"message": "teacher_id cannot be empty", "data": {}}, 400

        cursor.execute(f"SELECT * FROM Teachers WHERE TeacherID = '{teacher_id}'")
        db_result = cursor.fetchone()
        if db_result is None:
            if (teacher_name == "") or (date_of_birth == "") or (email == ""):
                return {"message": "all fields cannot be empty", "data": {}}, 400
            cursor.execute(f"INSERT INTO Teachers VALUES ('{teacher_id}', '{teacher_name}', '{date_of_birth}', '{email}')")
        else:
            cursor.execute(
                "UPDATE Teachers SET TeacherName = %s, DateOfBirth = %s, Email = %s WHERE TeacherID = %s",
                (teacher_name, date_of_birth, email, teacher_id),
            )

        return (
            {
                "message": CREATE_GENERAL_MSG(
                    action=("added" if db_result is None else "updated"), typeof_object="teacher", id=teacher_id
                ),
                "data": {
                    "teacher_id": teacher_id,
                    "teacher_name": teacher_name,
                    "date_of_birth": date_of_birth,
                    "email": email,
                },
            },
            200,
        )

    def DELETE(self):
        validate_success, message_body, missing_args = validate_args(
            request.get_json(silent=True), tuple(["teacher_id", "session_key"])
        )
        if not validate_success:
            return {"message": MISSING_ARGS_MSG(missing_args), "data": {}}, 400
        teacher_id, session_key = message_body["teacher_id"], message_body["session_key"]
        if not have_permission(session_key, admin_only=True):
            return {"message": INVALID_ROLE, "data": {}}, 403

        cursor.execute(f"DELETE FROM Teachers WHERE TeacherID = '{teacher_id}'")
        conn.commit()

        return {"message": CREATE_GENERAL_MSG(action="deleted", typeof_object="teacher", id=teacher_id), "data": {}}, 200
