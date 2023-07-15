from __future__ import annotations

from flask_restful import Resource, request

from database.mssql import conn, cursor
from frontend.helper_web.MESSAGE import CREATE_GENERAL_MSG, MISSING_ARGS_MSG
from frontend.helper_web.validate_args import validate_args


class CourseAPI(Resource):
    def get(self):
        validate_success, message_body, missing_args = validate_args(request.get_json(silent=True), tuple(["course_id"]))
        if not validate_success:
            return {"message": MISSING_ARGS_MSG(missing_args), "data": {}}, 400
        course_id = message_body["course_id"]
        if (course_id == ""):
            return {"message": "Course ID cannot be empty", "data": {}}, 400

        cursor.execute("SELECT * FROM course WHERE course_id = %s", course_id)
        db_result = cursor.fetchone()
        if db_result is None:
            return {"message": CREATE_GENERAL_MSG(action="not found", typeof_object="Course", id=course_id), "data": {}}, 404

        return (
                {
                    "message": "Success",
                    "data": {
                        "course_id": db_result[0],
                        "course_name": db_result[1],
                        "teacher_id": db_result[2],
                        "credits": db_result[3],
                    },
                }
            ,
            200,
        )

    def post(self):
        validate_success, message_body, missing_args = validate_args(
            request.get_json(silent=True), tuple(["course_id", "course_name", "teacher_id", "credits"])
        )
        if not validate_success:
            return {"message": MISSING_ARGS_MSG(missing_args), "data": {}}, 400

        course_id, course_name, teacher_id, credits = (
            message_body["course_id"],
            message_body["course_name"],
            message_body["teacher_id"],
            message_body["credits"],
        )

        cursor.execute("SELECT * FROM course WHERE course_id = %s", course_id)
        db_result = cursor.fetchone()
        if db_result is not None:
            return (
                {"message": CREATE_GENERAL_MSG(action="already exists", typeof_object="Course", id=course_id), "data": {}},
                409,
            )

        cursor.execute(
            "INSERT INTO course VALUES (%s, %s, %s, %s)",
            (course_id, course_name, teacher_id, credits),
        )
        conn.commit()

        return {"message": CREATE_GENERAL_MSG(action="created", typeof_object="Course", id=course_id), "data": {}}, 201

    def put(self):
        validate_success, message_body, missing_args = validate_args(
            request.get_json(silent=True), tuple(["course_id", "course_name", "teacher_id", "credits"])
        )
        if not validate_success:
            return {"message": MISSING_ARGS_MSG(missing_args), "data": {}}, 400

        course_id, course_name, teacher_id, credits = (
            message_body["course_id"],
            message_body["course_name"],
            message_body["teacher_id"],
            message_body["credits"],
        )

        cursor.execute("SELECT * FROM course WHERE course_id = %s", course_id)
        db_result = cursor.fetchone()
        if db_result is None:
            cursor.execute(
                "INSERT INTO course VALUES (%s, %s, %s)",
                (course_id, course_name, teacher_id),
            )
            conn.commit()
            return {"message": CREATE_GENERAL_MSG(action="created", typeof_object="Course", id=course_id), "data": {}}, 201
        else:
            cursor.execute(
                "UPDATE course SET course_name = %s, teacher_id = %s WHERE course_id = %s",
                (course_name, teacher_id, course_id),
            )
            conn.commit()
            return {"message": CREATE_GENERAL_MSG(action="updated", typeof_object="Course", id=course_id), "data": {}}, 200

    def delete(self):
        validate_success, message_body, missing_args = validate_args(request.get_json(silent=True), tuple(["course_id"]))
        if not validate_success:
            return {"message": MISSING_ARGS_MSG(missing_args), "data": {}}, 400
        course_id = message_body["course_id"]

        cursor.execute(f"SELECT * FROM course WHERE course_id = {course_id}")
        db_result = cursor.fetchone()
        if db_result is None:
            return {"message": CREATE_GENERAL_MSG(action="not found", typeof_object="Course", id=course_id), "data": {}}, 404

        cursor.execute(f"DELETE FROM course WHERE course_id = {course_id}")
        conn.commit()

        return {"message": CREATE_GENERAL_MSG(action="deleted", typeof_object="Course", id=course_id), "data": {}}, 200
