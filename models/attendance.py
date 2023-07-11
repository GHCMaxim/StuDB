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
    StudentID: str
    CourseID: str
    AttendanceDate: str
    AttendanceStatus: int

    def get(self):
        """Get attendance"""
        data = request.get_json()
        student_id = data["student_id"]
        course_id = data["course_id"]
        date = data["date"]

        if student_id == "" and course_id == "" and date == "":
            cursor.execute("SELECT * FROM Attendance")
            result = cursor.fetchall()

            # {
            #     <student_id>: {
            #         <course_id>: {
            #             <date>: <status>
            #             ...
            #         }
            #         <course_id>: {
            #             ...
            #         }
            #         ...
            #     }
            #     <student_id>: {
            #         ...
            #     }
            #     ...
            # }
            return_result = {}
            for row in result:
                if row[0] not in return_result:
                    return_result[row[0]] = {}
                if row[1] not in return_result[row[0]]:
                    return_result[row[0]][row[1]] = {}
                return_result[row[0]][row[1]][row[2]] = row[3]

            return jsonify(return_result), 200

        if student_id != "":
            if not student_id.isnumeric():
                return jsonify({"message": "StudentID must be a number"}), 400
            cursor.execute("SELECT * FROM Attendance WHERE StudentID = %s ORDER BY CourseID, AttendanceDate", (student_id))
            result = cursor.fetchall()
            if result is None:
                return jsonify({"message": "StudentID not found"}), 404

            # STUDENT_ID    COURSE_ID       DATE         STATUS
            #  123              MATH        2021-10-10    1

            # {
            #     <course_id>: {
            #         <date>: <status>
            #         <date>: <status>
            #     }
            #     <course_id>: {
            #         <date>: <status>
            #         <date>: <status>
            #     }
            # }

            return_data = {}
            for row in result:
                if row[1] not in return_data:
                    return_data[row[1]] = {}
                return_data[row[1]][row[2]] = row[3]
            return jsonify(return_data), 200

        if course_id != "":
            cursor.execute("SELECT * FROM Attendance WHERE CourseID = %s ORDER BY StudentID, AttendanceDate", (course_id))
            result = cursor.fetchone()
            if result is None:
                return jsonify({"message": "CourseID not found"}), 404

            # {
            #     <student_id>: {
            #         <date>: <status>
            #         <date>: <status>
            #     }
            #     <student_id>: {
            #         <date>: <status>
            #         <date>: <status>
            #     }
            # }

            return_data = {}
            for row in result:
                if row[0] not in return_data:
                    return_data[row[0]] = {}
                return_data[row[0]][row[2]] = row[3]
            return jsonify(return_data), 200

        if date != "":
            try:
                date = datetime.strftime(datetime.strptime(date, "%Y-%m-%d"), "%Y-%m-%d")
                cursor.execute("SELECT * FROM Attendance WHERE Date = %s ORDER BY CourseID, StudentID", (date))
                result = cursor.fetchall()
                if result is None:
                    return jsonify({"message": "Date not found"}), 404
            except ValueError:
                return jsonify({"message": "Invalid date format. Must be YYYY-MM-DD"}), 400

            # {
            #     <student_id>: {
            #         <course_id>: <status>
            #         <course_id>: <status>
            #     }
            #     <student_id>: {
            #         <course_id>: <status>
            #         <course_id>: <status>
            #     }
            # }

            return_data = {}
            for row in result:
                if row[0] not in return_data:
                    return_data[row[0]] = {}
                return_data[row[0]][row[1]] = row[3]
            return jsonify(return_data), 200

    def post(self):
        """Create attendance"""
        data = request.get_json()
        student_id = data["student_id"]
        course_id = data["course_id"]
        date = data["date"]
        status = data["status"]

        for variable, validator in {
            "student_id": self.validate_student_id,
            "course_id": self.validate_course_id,
            "date": self.validate_date,
            "status": self.validate_status,
        }.items():
            if (res := validator(data[variable])).is_err:
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
        data = request.get_json()

        for variable, validator in {
            "student_id": self.validate_student_id,
            "course_id": self.validate_course_id,
            "date": self.validate_date,
            "status": self.validate_status,
        }.items():
            if (res := validator(data[variable])).is_err:
                return jsonify({"message": res.unwrap_err()[0]}), res.unwrap_err()[1]

        cursor.execute(
            "UPDATE Attendance SET AttendanceStatus = %s WHERE StudentID = %s AND CourseID = %s AND AttendanceDate = %s",
            (data["status"], data["student_id"], data["course_id"], data["date"]),
        )
        conn.commit()
        return jsonify({"message": "Attendance replaced successfully"}), 200

    def validate_student_id(self, id: str) -> Result[Self, tuple[str, int]]:
        if id == "":
            return Err(("ID cannot be empty", 400))
        if not id.isnumeric():
            return Err(("ID must be a number", 400))
        cursor.execute("SELECT * FROM Students WHERE StudentID = %s", (id))
        result = cursor.fetchone()
        if result is None:
            return Err(("StudentID does not exist", 404))
        return Ok(self)

    def validate_course_id(self, id: str) -> Result[Self, tuple[str, int]]:
        if id == "":
            return Err(("ID cannot be empty", 400))
        cursor.execute("SELECT * FROM Courses WHERE CourseID = %s", (id))
        result = cursor.fetchone()
        if result is None:
            return Err(("CourseID does not exist", 404))
        return Ok(self)

    def validate_date(self, date: str) -> Result[Self, tuple[str, int]]:
        try:
            date = datetime.strftime(datetime.strptime(date, "%Y-%m-%d"), "%Y-%m-%d")
        except ValueError:
            return Err(("Invalid date format. Must be YYYY-MM-DD", 400))
        return Ok(self)

    def validate_status(self, status: str) -> Result[Self, tuple[str, int]]:
        if status not in (0, 1):
            return Err(("Status must be 0 or 1", 400))
        return Ok(self)

    def set_student_id(self, id: str) -> Result[Self, str]:
        if id == "":
            return Err("ID cannot be empty")
        if not id.isnumeric():
            return Err("ID must be a number")
        cursor.execute("SELECT * FROM Students WHERE StudentID = %s", (id))
        result = cursor.fetchone()
        if result is None:
            return Err("StudentID does not exist")
        self.StudentID = id
        return Ok(self)

    def set_course_id(self, id: str) -> Result[Self, str]:
        if id == "":
            return Err("ID cannot be empty")
        cursor.execute("SELECT * FROM Courses WHERE CourseID = %s", (id))
        result = cursor.fetchone()
        if result is None:
            return Err("CourseID does not exist")
        self.CourseID = id
        return Ok(self)

    def set_date(self, date: str) -> Result[Self, str]:
        try:
            date = datetime.strftime(datetime.strptime(date, "%Y-%m-%d"), "%Y-%m-%d")
        except ValueError:
            return Err("Invalid date format. Please try again.")
        self.AttendanceDate = date
        return Ok(self)

    def set_status(self, status: str) -> Result[Self, str]:
        if status == "":
            return Err("Status cannot be empty")
        if not status.isnumeric():
            return Err("Status must be a number")
        if int(status) < 0 or int(status) > 1:
            return Err("Status must be either 0 or 1")
        self.AttendanceStatus = int(status)
        return Ok(self)
