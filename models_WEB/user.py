from __future__ import annotations

import uuid

from flask_restful import Resource, request

from database.login import global_var
from database.mssql import conn, cursor
from frontend.helper_web.is_first_user import is_first_user
from frontend.helper_web.MESSAGE import CREATE_USER_MSG, INVALID_ROLE, INVALID_SESSION, MISSING_ARGS_MSG
from frontend.helper_web.validate_args import validate_args


class LoginAPI(Resource):
    def post(self):
        """User login"""
        validate_success, message, missing_args = validate_args(
            request.get_json(silent=True), tuple(["username", "password"])
        )
        if not validate_success:
            return {"message": MISSING_ARGS_MSG(missing_args), "data": {}}, 400
        username, password = message["username"], message["password"]

        cursor.execute(f"SELECT * FROM Users WHERE Username='{username}' AND Password='{password}'")
        db_result = cursor.fetchone()
        if db_result is None:
            return {"message": "Wrong username or password"}, 400

        global_var["current_user"] = db_result[0]
        global_var["current_user_role"] = db_result[2].capitalize()
        global_var["session_key"] = str(uuid.uuid4())

        return (
            {"message": CREATE_USER_MSG("logged in", username), "data": {"session_key": global_var["session_key"]}},
            200,
        )


class LogoutAPI(Resource):
    def post(self):
        """User logout"""
        validate_success, message, missing_args = validate_args(request.get_json(silent=True), tuple(["session_key"]))
        if not validate_success:
            return {"message": MISSING_ARGS_MSG(missing_args)}, 400
        session_key = message["session_key"]

        if session_key != global_var["session_key"]:
            return {"message": INVALID_SESSION}, 400

        global_var["current_user"] = ""
        global_var["current_user_role"] = ""
        global_var["session_key"] = ""

        return {"message": "Logged out"}, 200


class RegisterAPI(Resource):
    def get(self):
        if is_first_user():
            return {"message": True}, 200
        else:
            return {"message": False}, 200

    def post(self):
        """User register"""
        validate_success, message_body, missing_args = validate_args(
            request.get_json(silent=True), tuple(["username", "password", "session_key", "role"])
        )
        if not validate_success:
            return {"message": MISSING_ARGS_MSG(missing_args)}, 400
        username, password, session_key, role = (
            message_body["username"],
            message_body["password"],
            message_body["session_key"],
            message_body["role"].capitalize(),
        )

        role = "Student" if role == "" else role
        if username == "" or password == "":
            return {"message": "Username or password cannot be empty"}, 400

        if is_first_user():
            cursor.execute(f"INSERT INTO Users VALUES ('{username}', '{password}', 'Admin')")
            conn.commit()
            return {"message": CREATE_USER_MSG("created", username)}, 200
        else:
            if session_key != global_var["session_key"]:
                return {"message": INVALID_SESSION}, 400
            if global_var["current_user_role"] != "Admin":
                return {"message": INVALID_ROLE}, 400

        cursor.execute(f"SELECT * FROM Users WHERE Username='{username}'")
        db_result = cursor.fetchone()
        if db_result is not None:
            return {"message": CREATE_USER_MSG("already exists", username)}, 400

        cursor.execute(f"INSERT INTO Users VALUES ('{username}', '{password}', '{role}')")
        conn.commit()

        return {"message": CREATE_USER_MSG("created", username)}, 200


class ValidateSessionAPI(Resource):
    def post(self):
        """Validate session"""
        validate_success, message_body, missing_args = validate_args(request.get_json(silent=True), tuple(["session_key"]))
        if not validate_success:
            return {"message": MISSING_ARGS_MSG(missing_args)}, 400
        session_key = message_body["session_key"]

        if session_key != global_var["session_key"]:
            return {"message": INVALID_SESSION}, 400

        return (
            {
                "message": "Valid session",
                "data": {"role": global_var["current_user_role"], "username": global_var["current_user"]},
            },
            200,
        )
