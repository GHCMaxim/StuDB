from __future__ import annotations

import sys

from flask import jsonify
from flask_restful import Resource, request
from option import Err, Ok, Result

from database.mssql import conn, cursor

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class CoursesAPI(Resource):
    def get(self):
        cursor.execute("SELECT * FROM Courses")
        result = cursor.fetchall()

        # course_id
        #   - course_name: course_name
        #   - teacher_id: teacher_id
        #   - credits: credits
        # ...

        return_data = {}
        for course in result:
            return_data[course[0]] = {"course_name": course[1], "teacher_id": course[2], "credits": course[3]}
        return jsonify(result), 200

    def post(self):
        data = request.get_json()
        course_id, course_name, teacher_id, credits = (
            data["course_id"],
            data["course_name"],
            data["teacher_id"],
            data["credits"],
        )

        # write to the database, no need for Course class
        cursor.execute(
            "INSERT INTO Courses (CourseID, CourseName, TeacherID, Credits) VALUES (%s, %s, %s, %s)",
            (course_id, course_name, teacher_id, credits),
        )
        conn.commit()

        return jsonify({"message": "Course added successfully"}), 201


class Courses:
    CourseID: str
    CourseName: str
    TeacherID: int
    Credits: int

    def set_id(self, id: str) -> Result[Self, str]:
        if id == "":
            return Err("ID cannot be empty")
        cursor.execute("SELECT * FROM Courses WHERE CourseID = %s", (id))
        result = cursor.fetchone()
        if result is not None:
            return Err("CourseID already exists")
        self.CourseID = id
        return Ok(self)

    def get_id(self, id: str) -> Result[Self, str]:
        if id == "":
            return Err("ID cannot be empty")
        cursor.execute("SELECT * FROM Courses WHERE CourseID = %s", (id))
        result = cursor.fetchone()
        if result is None:
            return Err("CourseID does not exist")
        self.CourseID = id
        return Ok(self)

    def set_name(self, name: str) -> Result[Self, str]:
        if name == "":
            return Err("Name cannot be empty")
        if any(char.isdigit() for char in name):
            return Err("Name cannot contain numbers")
        self.CourseName = name
        return Ok(self)

    def set_teacher_id(self, id: str) -> Result[Self, str]:
        if id == "":
            return Err("ID cannot be empty")
        if not id.isnumeric():
            return Err("ID must be a number")
        cursor.execute("SELECT * FROM Teachers WHERE TeacherID = %s", (id))
        result = cursor.fetchone()
        if result is None:
            return Err("TeacherID does not exist")
        self.TeacherID = int(id)
        return Ok(self)

    def set_credits(self, credits: str) -> Result[Self, str]:
        if credits == "":
            return Err("Credits cannot be empty")
        if not credits.isnumeric():
            return Err("Credits must be a number")
        if int(credits) < 0 or int(credits) > 5:
            return Err("Credits must be in range [0, 5]")
        self.Credits = int(credits)
        return Ok(self)
