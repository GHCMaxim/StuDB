from __future__ import annotations

import sys
from datetime import datetime

from flask import jsonify
from flask_restful import Resource, request
from option import Err, Ok, Result

from database.mssql import conn, cursor

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class Attendance(Resource):
    def get(self):
        """Get attendance"""
        message_body = request.get_json()
        not_enough_keys = any(keys not in message_body for keys in ("student_id", "course_id", "date"))
        if (message_body == {}) or not_enough_keys:
            return jsonify({"message": "Missing required fields"}), 400
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
        if db_result is None:
            return jsonify({"message": "No attendance found"}), 404

        # course
        #   student
        #      date: status
        #      ...
        #   ...
        # ...

        results = {}
        for result in db_result:
            student_id, course_id, date, status = result
            if course_id not in results:
                results[course_id] = {}
            if student_id not in results[course_id]:
                results[course_id][student_id] = {}
            results[course_id][student_id][date] = status

        return jsonify({"message": "Attendance found", "data": results}), 200

    def post(self):
        """Create attendance"""
        message_body = request.get_json()
        not_enough_keys = any(keys not in message_body for keys in ("student_id", "course_id", "date", "status"))
        if (message_body == {}) or not_enough_keys:
            return jsonify({"message": "Missing required fields"}), 400

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
                return jsonify({"message": res.unwrap_err()[0]}), res.unwrap_err()[1]

        cursor.execute(
            "SELECT * FROM Attendance WHERE StudentID = %s AND CourseID = %s AND AttendanceDate = %s",
            (student_id, course_id, date),
        )
        if cursor.fetchone() is not None:
            return jsonify({"message": "Attendance already exists"}), 400

        cursor.execute(
            "INSERT INTO Attendance (StudentID, CourseID, AttendanceDate, AttendanceStatus) VALUES (%s, %s, %s, %s)",
            (student_id, course_id, date, status),
        )
        conn.commit()
        return jsonify({"message": "Attendance created successfully"}), 201

    def put(self):
        """Replace attendance"""
        message_body = request.get_json()
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
                return jsonify({"message": res.unwrap_err()[0]}), res.unwrap_err()[1]

        cursor.execute(
            "SELECT * FROM Attendance WHERE StudentID = %s AND CourseID = %s AND AttendanceDate = %s",
            (student_id, course_id, date),
        )
        db_result = cursor.fetchone()
        if db_result is None:
            cursor.execute(
                "INSERT INTO Attendance (StudentID, CourseID, AttendanceDate, AttendanceStatus) VALUES (%s, %s, %s, %s)",
                (student_id, course_id, date, status),
            )
            conn.commit()
            return jsonify({"message": "Attendance created successfully"}), 201

        status = 1 - int(db_result[3])
        cursor.execute(
            "UPDATE Attendance SET AttendanceStatus = %s WHERE StudentID = %s AND CourseID = %s AND AttendanceDate = %s",
            (status, student_id, course_id, date),
        )
        conn.commit()
        return jsonify({"message": "Attendance replaced successfully"}), 200

    def delete(self):
        """Delete attendance"""
        message_body = request.get_json()
        not_enough_keys = any(keys not in message_body for keys in ("student_id", "course_id", "date"))
        if (message_body == {}) or not_enough_keys:
            return jsonify({"message": "Missing required fields"}), 400

        student_id, course_id, date = (message_body["student_id"], message_body["course_id"], message_body["date"])

        for variable, validator in {
            "student_id": self.validate_student_id,
            "course_id": self.validate_course_id,
            "date": self.validate_date,
        }.items():
            if (res := validator(message_body[variable])).is_err:
                return jsonify({"message": res.unwrap_err()[0]}), res.unwrap_err()[1]

        cursor.execute(
            "SELECT * FROM Attendance WHERE StudentID = %s AND CourseID = %s AND AttendanceDate = %s",
            (student_id, course_id, date),
        )
        if cursor.fetchone() is None:
            return jsonify({"message": "Attendance does not exist"}), 404

        cursor.execute(
            "DELETE FROM Attendance WHERE StudentID = %s AND CourseID = %s AND AttendanceDate = %s",
            (student_id, course_id, date),
        )
        conn.commit()
        return jsonify({"message": "Attendance deleted successfully"}), 200

    def validate_student_id(self, id: str) -> Result[Self, tuple[str, int]]:
        if id == "":
            return Err(("ID cannot be empty", 400))
        if not id.isnumeric():
            return Err(("ID must be a number", 400))
        cursor.execute("SELECT * FROM Students WHERE StudentID = %s", (id))
        db_result = cursor.fetchone()
        if db_result is None:
            return Err(("StudentID does not exist", 404))
        return Ok(self)

    def validate_course_id(self, id: str) -> Result[Self, tuple[str, int]]:
        if id == "":
            return Err(("ID cannot be empty", 400))
        cursor.execute("SELECT * FROM Courses WHERE CourseID = %s", (id))
        db_result = cursor.fetchone()
        if db_result is None:
            return Err(("CourseID does not exist", 404))
        return Ok(self)

    def validate_date(self, date: str) -> Result[Self, tuple[str, int]]:
        try:
            date = datetime.strftime(datetime.strptime(date, "%Y-%m-%d"), "%Y-%m-%d")
        except ValueError:
            return Err(("Invalid date format. Must be YYYY-MM-DD", 400))
        return Ok(self)

    def validate_status(self, status: str) -> Result[Self, tuple[str, int]]:
        if status not in ("0", "1", ""):
            return Err(("Status must be 0 or 1", 400))
        return Ok(self)
