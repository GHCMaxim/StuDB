from __future__ import annotations

from flask_restful import Resource, request

from database.mssql import conn, cursor
from frontend.helper_web.MESSAGE import ACTION_MUST_BE_CRUD, CREATE_GENERAL_MSG, MISSING_ARGS_MSG
from frontend.helper_web.validate_args import validate_args


class CourseAPI(Resource):
    def post(self):
        validate_success, message_body, missing_args = validate_args(request.get_json(silent=True), tuple(["action"]))
        if not validate_success:
            return {"message": MISSING_ARGS_MSG(missing_args), "data": {}}, 400
        match message_body["action"].lower():
            case "read":
                return self.READ()
            case "create":
                return self.CREATE()
            case "update":
                return self.UPDATE()
            case "delete":
                return self.DELETE()
            case _:
                return {"message": ACTION_MUST_BE_CRUD, "data": {}}, 400

    def READ(self):
        validate_success, message_body, missing_args = validate_args(request.get_json(silent=True), tuple(["course_id"]))
        if not validate_success:
            return {"message": MISSING_ARGS_MSG(missing_args), "data": {}}, 400
        course_id = message_body["course_id"]
        if course_id == "":
            return {"message": "Course ID cannot be empty", "data": {}}, 400

        cursor.execute(f"SELECT * FROM Courses WHERE CourseID = '{course_id}'")
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
            },
            200,
        )

    def CREATE(self):
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
        if (course_id == "") or (course_name == "") or (teacher_id == "") or (credits == ""):
            return {"message": "Course ID, Course Name, Teacher ID, Credits cannot be empty", "data": {}}, 400

        cursor.execute(f"SELECT * FROM Courses WHERE CourseID = '{course_id}'")
        db_result = cursor.fetchone()
        if db_result is not None:
            return (
                {
                    "message": CREATE_GENERAL_MSG(action="already exists", typeof_object="Course", id=course_id),
                    "data": {
                        "course_id": db_result[0],
                        "course_name": db_result[1],
                        "teacher_id": db_result[2],
                        "credits": db_result[3],
                    },
                },
                409,
            )

        cursor.execute(
            "INSERT INTO Courses VALUES (%s, %s, %s, %s)",
            (course_id, course_name, teacher_id, credits),
        )
        conn.commit()

        return {
            "message": CREATE_GENERAL_MSG(action="created", typeof_object="Course", id=course_id),
            "data": {
                "course_id": course_id,
                "course_name": course_name,
                "teacher_id": teacher_id,
                "credits": credits,
            },
        }, 201

    def UPDATE(self):
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
        if (course_id == "") and (course_name == "") and (teacher_id == "") and (credits == ""):
            return {"message": "Course unchanged", "data": {}}, 200

        cursor.execute(f"SELECT * FROM Courses WHERE CourseID = '{course_id}'")
        db_result = cursor.fetchone()
        if db_result is None:
            if (course_name == "") or (teacher_id == "") or (credits == ""):
                return {"message": "Course Name, Teacher ID, Credits cannot be empty", "data": {}}, 400
            cursor.execute(
                "INSERT INTO Courses VALUES (%s, %s, %s, %s)",
                (course_id, course_name, teacher_id, credits),
            )
        else:
            course_name = db_result[1] if course_name == "" else course_name
            teacher_id = db_result[2] if teacher_id == "" else teacher_id
            credits = db_result[3] if credits == "" else credits
            cursor.execute(
                "UPDATE Courses SET CourseName = %s, TeacherID = %s, Credits = %s WHERE CourseID = %s",
                (course_name, teacher_id, credits, course_id),
            )
        conn.commit()
        return {
            "message": CREATE_GENERAL_MSG(
                action=("created" if db_result is None else "updated"), typeof_object="Course", id=course_id
            ),
            "data": {
                "course_id": course_id,
                "course_name": course_name,
                "teacher_id": teacher_id,
                "credits": credits,
            },
        }, 200

    def DELETE(self):
        validate_success, message_body, missing_args = validate_args(request.get_json(silent=True), tuple(["course_id"]))
        if not validate_success:
            return {"message": MISSING_ARGS_MSG(missing_args), "data": {}}, 400
        course_id = message_body["course_id"]
        if course_id == "":
            return {"message": "Course ID cannot be empty", "data": {}}, 400

        cursor.execute(f"SELECT * FROM Courses WHERE CourseID = '{course_id}'")
        db_result = cursor.fetchone()
        if db_result is None:
            return {"message": CREATE_GENERAL_MSG(action="not found", typeof_object="Course", id=course_id), "data": {}}, 404

        cursor.execute(f"DELETE FROM Courses WHERE CourseID = '{course_id}'")
        conn.commit()

        return {"message": CREATE_GENERAL_MSG(action="deleted", typeof_object="Course", id=course_id), "data": {}}, 200
