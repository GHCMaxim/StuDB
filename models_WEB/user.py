from __future__ import annotations


from flask_restful import Resource, request

from database.login import global_var
from database.mssql import conn, cursor
from frontend.helper_web.MESSAGE import CREATE_USER_MSG, MISSING_ARGS_MSG
from frontend.helper_web.validate_args import validate_args


class UserAPI(Resource):
    def post(self):
        """User login"""
        validate_success, message_body, missing_args = validate_args(
            request.get_json(silent=True), tuple(["username", "password"])
        )
        if not validate_success:
            return {"message": MISSING_ARGS_MSG(missing_args), "data": {}}, 400
        username, password = message["username"], message["password"]

        cursor.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
        db_result = cursor.fetchone()
        if db_result is None:
            return {"message": "Wrong username or password"}, 400

        cursor.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
        conn.commit()
        return jsonify({"message": CREATE_USER_MSG("created", username)}), 201

    def put(self):
        """User register"""
        validate_success, message_body, missing_args = validate_args(
            request.get_json(silent=True), tuple(["username", "password"])
        )
        if not validate_success:
        username, password = message_body["username"], message_body["password"]
            return {"message": MISSING_ARGS_MSG(missing_args)}, 400

        cursor.execute(f"SELECT * FROM users WHERE Username='{username}' AND Password='{password}'")
        db_result = cursor.fetchone()
        if db_result is None:
            return {"message": CREATE_USER_MSG("already exists", username)}, 400

        global_var["current_user"] = db_result[0]
        global_var["current_user_role"] = db_result[3]
        return jsonify({"message": CREATE_USER_MSG("logged in", username)}), 201
