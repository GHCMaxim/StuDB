from __future__ import annotations

import sys
from datetime import datetime

from flask_restful import Resource, request
from option import Err, Ok, Result

from database.mssql import conn, cursor
from frontend.helper_web.MESSAGE import (
    ACTION_MUST_BE_CRUD,
    ATTENDANCE_CREATED,
    ATTENDANCE_DELETED,
    ATTENDANCE_EXISTS,
    ATTENDANCE_FOUND,
    ATTENDANCE_NOT_FOUND,
    ATTENDANCE_UPDATED_MSG,
    CREATE_GENERAL_MSG,
    MISSING_ARGS_MSG,
)
from frontend.helper_web.validate_args import validate_args

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class AttendanceAPI(Resource):
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

    def CREATE(self):
        validate_success, message_body, missing_args = validate_args(
            request.get_json(silent=True), tuple(["student_id", "course_id", "date", "status"])
        )
        if not validate_success:
            return {"message": MISSING_ARGS_MSG(missing_args), "data": {}}, 400

        student_id, course_id, date, status = (
            message_body["student_id"],
            message_body["course_id"],
            message_body["date"],
            message_body["status"],
        )

        for variable, validator in {
            "student_id": self.validate_student_id,
            "course_id": self.validate_course_id,
            "date": self.validate_date,
            "status": self.validate_status,
        }.items():
            if (res := validator(message_body[variable])).is_err:
                return {"message": res.unwrap_err()[0], "data": {}}, res.unwrap_err()[1]

        cursor.execute(
            "SELECT * FROM Attendance WHERE StudentID = %s AND CourseID = %s AND AttendanceDate = %s",
            (student_id, course_id, date),
        )
        if cursor.fetchone() is not None:
            return {
                "message": ATTENDANCE_EXISTS,
                "data": {
                    "student_id": student_id,
                    "course_id": course_id,
                    "date": date,
                    "status": status,
                },
            }, 400

        cursor.execute(
            "INSERT INTO Attendance (StudentID, CourseID, AttendanceDate, AttendanceStatus) VALUES (%s, %s, %s, %s)",
            (student_id, course_id, date, status),
        )
        conn.commit()
        return {
            "message": ATTENDANCE_CREATED,
            "data": {
                "student_id": student_id,
                "course_id": course_id,
                "date": date,
                "status": status,
            },
        }, 201

    def READ(self):
        """Get attendance"""
        validate_success, message_body, missing_args = validate_args(
            request.get_json(silent=True), tuple(["student_id", "course_id", "date"])
        )
        if not validate_success:
            return {"message": MISSING_ARGS_MSG(missing_args), "data": {}}, 400
        student_id, course_id, date = (
            message_body["student_id"],
            message_body["course_id"],
            message_body["date"],
        )
        queries = {
            "000": ("SELECT * FROM Attendance ORDER BY CourseID, StudentID, AttendanceDate", ()),
            "111": (
                "SELECT * FROM Attendance WHERE StudentID = %s AND CourseID = %s AND AttendanceDate = %s ORDER BY AttendanceDate",
                (student_id, course_id, date),
            ),
            "100": ("SELECT * FROM Attendance WHERE StudentID = %s ORDER BY CourseID, AttendanceDate", (student_id)),
            "010": ("SELECT * FROM Attendance WHERE CourseID = %s ORDER BY StudentID, AttendanceDate", (course_id)),
            "001": ("SELECT * FROM Attendance WHERE AttendanceDate = %s ORDER BY CourseID, StudentID", (date)),
            "110": (
                "SELECT * FROM Attendance WHERE StudentID = %s AND CourseID = %s ORDER BY AttendanceDate",
                (student_id, course_id),
            ),
            "101": (
                "SELECT * FROM Attendance WHERE StudentID = %s AND AttendanceDate = %s ORDER BY CourseID",
                (student_id, date),
            ),
            "011": (
                "SELECT * FROM Attendance WHERE CourseID = %s AND AttendanceDate = %s ORDER BY StudentID",
                (course_id, date),
            ),
        }

        query_key = ""
        query_key += "1" if student_id != "" else "0"
        query_key += "1" if course_id != "" else "0"
        query_key += "1" if date != "" else "0"

        cursor.execute(queries[query_key][0], queries[query_key][1])
        db_result = cursor.fetchall()
        if len(db_result) == 0:
            return {"message": ATTENDANCE_NOT_FOUND, "data": {}}, 404

        # course
        #   student
        #      date: status
        #      ...
        #   ...
        # ...

        results = {}
        for result in db_result:
            print(result)
            student_id, course_id, date, status = (
                result[0],
                result[1],
                result[2].strftime("%Y-%m-%d"),
                result[3],
            )
            if course_id not in results:
                results[course_id] = {}
            if student_id not in results[course_id]:
                results[course_id][student_id] = {}
            results[course_id][student_id][date] = status

        return {"message": ATTENDANCE_FOUND, "data": results}, 200

    def UPDATE(self):
        """Replace attendance"""
        validate_success, message_body, missing_args = validate_args(
            request.get_json(silent=True), tuple(["student_id", "course_id", "date", "status"])
        )
        if not validate_success:
            return {"message": MISSING_ARGS_MSG(missing_args), "data": {}}, 400

        student_id, course_id, date, status = (
            message_body["student_id"],
            message_body["course_id"],
            message_body["date"],
            message_body["status"],
        )

        for variable, validator in {
            "student_id": self.validate_student_id,
            "course_id": self.validate_course_id,
            "date": self.validate_date,
            "status": self.validate_status,
        }.items():
            if (res := validator(message_body[variable])).is_err:
                return {"message": res.unwrap_err()[0], "data": {}}, res.unwrap_err()[1]

        cursor.execute(
            "SELECT * FROM Attendance WHERE StudentID = %s AND CourseID = %s AND AttendanceDate = %s",
            (student_id, course_id, date),
        )
        db_result = cursor.fetchone()
        if db_result is None:
            cursor.execute(
                "INSERT INTO Attendance (StudentID, CourseID, AttendanceDate, AttendanceStatus) VALUES (%s, %s, %s, %s)",
                (student_id, course_id, date, 1),
            )
        else:
            status = 1 - int(db_result[3])
            cursor.execute(
                "UPDATE Attendance SET AttendanceStatus = %s WHERE StudentID = %s AND CourseID = %s AND AttendanceDate = %s",
                (status, student_id, course_id, date),
            )
        conn.commit()
        return {
            "message": ATTENDANCE_CREATED if db_result is None else ATTENDANCE_UPDATED_MSG(str(1 - status), str(status)),
            "data": {
                "student_id": student_id,
                "course_id": course_id,
                "date": date,
                "status": status,
            },
        }, 201

    def DELETE(self):
        """Delete attendance"""
        validate_success, message_body, missing_args = validate_args(
            request.get_json(silent=True), tuple(["student_id", "course_id", "date"])
        )
        if not validate_success:
            return {"message": MISSING_ARGS_MSG(missing_args), "data": {}}, 400

        student_id, course_id, date = (message_body["student_id"], message_body["course_id"], message_body["date"])

        for variable, validator in {
            "student_id": self.validate_student_id,
            "course_id": self.validate_course_id,
            "date": self.validate_date,
        }.items():
            if (res := validator(message_body[variable])).is_err:
                return {"message": res.unwrap_err()[0], "data": {}}, res.unwrap_err()[1]

        cursor.execute(
            "SELECT * FROM Attendance WHERE StudentID = %s AND CourseID = %s AND AttendanceDate = %s",
            (student_id, course_id, date),
        )
        if cursor.fetchone() is None:
            return {"message": ATTENDANCE_NOT_FOUND, "data": {}}, 404

        cursor.execute(
            "DELETE FROM Attendance WHERE StudentID = %s AND CourseID = %s AND AttendanceDate = %s",
            (student_id, course_id, date),
        )
        conn.commit()
        return {"message": ATTENDANCE_DELETED, "data": {}}, 200

    def validate_student_id(self, id: str) -> Result[Self, tuple[str, int]]:
        if id == "":
            return Err(("ID cannot be empty", 400))
        if not id.isnumeric():
            return Err(("ID must be a number", 400))
        cursor.execute("SELECT * FROM Students WHERE StudentID = %s", (id))
        db_result = cursor.fetchone()
        if db_result is None:
            return Err((CREATE_GENERAL_MSG(action="not found", typeof_object="Student", id=id), 404))
        return Ok(self)

    def validate_course_id(self, id: str) -> Result[Self, tuple[str, int]]:
        if id == "":
            return Err(("ID cannot be empty", 400))
        cursor.execute("SELECT * FROM Courses WHERE CourseID = %s", (id))
        db_result = cursor.fetchone()
        if db_result is None:
            return Err((CREATE_GENERAL_MSG(action="not found", typeof_object="Course", id=id), 404))
        return Ok(self)

    def validate_date(self, date: str) -> Result[Self, tuple[str, int]]:
        try:
            date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            return Err(("Invalid date format. Must be YYYY-MM-DD", 400))
        return Ok(self)

    def validate_status(self, status: str) -> Result[Self, tuple[str, int]]:
        if status not in ("0", "1", ""):
            return Err(("Status must be 0, 1 or empty", 400))
        return Ok(self)
