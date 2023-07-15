from __future__ import annotations

import re
import sys
from datetime import datetime
from textwrap import dedent

from flask_restful import Resource, request
from option import Err, Ok, Result

from database.mssql import conn, cursor
from frontend.helper_web.MESSAGE import CREATE_GENERAL_MSG, MISSING_ARGS_MSG
from frontend.helper_web.validate_args import validate_args

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class StudentAPI(Resource):
    def get(self):
        """Get students"""
        validate_success, message_body, missing_args = validate_args(request.get_json(silent=True), tuple(["student_id"]))
        if not validate_success:
            return {"message": MISSING_ARGS_MSG(missing_args), "data": {}}, 400
        student_id = message_body["student_id"]

        cursor.execute(f"SELECT * FROM Students WHERE StudentID = {message_body['student_id']}")
        db_result = cursor.fetchone()
        if db_result is None:
            return {"message": CREATE_GENERAL_MSG(action="not found", typeof_object="student", id=student_id), "data": {}}, 404

        return (
                {
                    "message": CREATE_GENERAL_MSG(action="found", typeof_object="student", id=student_id),
                    "data": {
                        "student_id": db_result[0],
                        "student_name": db_result[1],
                        "date_of_birth": db_result[2],
                        "email": db_result[3],
                        "phone_number": db_result[4],
                    },
                }
            ,
            200,
        )

    def post(self):
        """Add student"""
        validate_success, message_body, missing_args = validate_args(
            request.get_json(silent=True), tuple(["student_id", "student_name", "date_of_birth", "email", "phone_number"])
        )
        if not validate_success:
            return {"message": MISSING_ARGS_MSG(missing_args), "data": {}}, 400
        student_id, student_name, date_of_birth, email, phone_number = (
            message_body["student_id"],
            message_body["student_name"],
            message_body["date_of_birth"],
            message_body["email"],
            message_body["phone_number"],
        )

        cursor.execute(f"SELECT StudentID FROM Students WHERE StudentID = {student_id}")
        if cursor.fetchone() is not None:
            return (
                {"message": CREATE_GENERAL_MSG(action="already exists", typeof_object="student", id=student_id), "data": {}},
                409,
            )

        for variable, validator in {
            "student_id": self.validate_student_id,
            "student_name": self.validate_student_name,
            "date_of_birth": self.validate_date_of_birth,
            "email": self.validate_email,
            "phone_number": self.validate_phone_number,
        }.items():
            if (res := validator(message_body[variable])).is_err():
                return {"message": res.unwrap_err()[0], "data": {}}, res.unwrap_err[1]

        cursor.execute(
            dedent(
                f"""
            INSERT INTO Students (StudentID, StudentName, DateOfBirth, Email, PhoneNumber)
            VALUES ({student_id}, '{student_name}', '{date_of_birth}', '{email}', '{phone_number}')
            """
            )
        )

        conn.commit()
        return {"message": CREATE_GENERAL_MSG(action="added", typeof_object="student", id=student_id), "data": {}}, 201

    def put(self):
        """Update student"""
        validate_success, message_body, missing_args = validate_args(
            request.get_json(silent=True), tuple(["student_id", "student_name", "date_of_birth", "email", "phone_number"])
        )
        if not validate_success:
            return {"message": MISSING_ARGS_MSG(missing_args), "data": {}}, 400
        student_id, student_name, date_of_birth, email, phone_number = (
            message_body["student_id"],
            message_body["student_name"],
            message_body["date_of_birth"],
            message_body["email"],
            message_body["phone_number"],
        )

        for variable, validator in {
            "student_id": self.validate_student_id,
            "student_name": self.validate_student_name,
            "date_of_birth": self.validate_date_of_birth,
            "email": self.validate_email,
            "phone_number": self.validate_phone_number,
        }.items():
            if (res := validator(message_body[variable])).is_err():
                return jsonify({"message": res.unwrap_err()[0]}), res.unwrap_err()[1]

        # if student not exists, create new student, else update student
        cursor.execute(f"SELECT StudentID FROM Students WHERE StudentID = {student_id}")
        db_result = cursor.fetchone()
        if db_result is None:
            cursor.execute(
                dedent(
                    f"""
                INSERT INTO Students (StudentID, StudentName, DateOfBirth, Email, PhoneNumber)
                VALUES ({student_id}, '{student_name}', '{date_of_birth}', '{email}', '{phone_number}')
                """
                )
            )
        else:
            cursor.execute(
                dedent(
                    f"""
                UPDATE Students
                SET StudentName = '{student_name}', DateOfBirth = '{date_of_birth}', Email = '{email}', PhoneNumber = '{phone_number}'
                WHERE StudentID = {student_id}
                """
                )
            )
        conn.commit()
        return (

                {
                    "message": CREATE_GENERAL_MSG(
                        action=("added" if db_result is None else "updated"), typeof_object="student", id=student_id
                    ), "data": {}
                }
            ,
            201,
        )

    def delete(self):
        """Delete student"""
        validate_success, message_body, missing_args = validate_args(request.get_json(silent=True), tuple(["student_id"]))
        if not validate_success:
            return {"message": MISSING_ARGS_MSG(missing_args), "data": {}}, 400
        student_id = message_body["student_id"]

        cursor.execute(f"SELECT StudentID FROM Students WHERE StudentID = {student_id}")
        if cursor.fetchone() is None:
            return {"message": "Student not found", "data": {}}, 404

        cursor.execute(f"DELETE FROM Students WHERE StudentID = {student_id}")
        conn.commit()
        return {"message": CREATE_GENERAL_MSG(action="deleted", typeof_object="student", id=student_id), "data": {}}, 200

    def validate_student_id(self, student_id: str) -> Result[Self, tuple[str, int]]:
        if student_id == "":
            return Err(("Student ID cannot be empty", 400))
        if not student_id.isnumeric():
            return Err(("Student ID can only contain numbers", 400))
        if len(student_id) < 8:
            return Err(("Student ID must have at least 8 characters", 400))
        cursor.execute(f"SELECT StudentID FROM Students WHERE StudentID = {student_id}")
        if cursor.fetchone() is not None:
            return Err((CREATE_GENERAL_MSG(action="already exists", typeof_object="student", id=student_id), 400))
        self.StudentID = int(student_id)
        return Ok(self)

    def validate_student_name(self, name: str) -> Result[Self, tuple[str, int]]:
        if name == "":
            return Err(("Name cannot be empty", 400))
        if any(char.isdigit() for char in name):
            return Err(("Name cannot contain numbers", 400))
        self.StudentName = name
        return Ok(self)

    def validate_date_of_birth(self, dob: str) -> Result[Self, tuple[str, int]]:
        try:
            dob = datetime.strftime(datetime.strptime(dob, "%Y-%m-%d"), "%Y-%m-%d")
        except ValueError:
            return Err(("Invalid date format. Please try again.", 400))
        self.DateOfBirth = dob
        return Ok(self)

    def validate_email(self, email: str) -> Result[Self, tuple[str, int]]:
        if email == "":
            return Err(("Email cannot be empty", 400))
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            return Err(("Invalid email format. Please try again.", 400))
        self.Email = email
        return Ok(self)

    def validate_phone_number(self, phone_number: str) -> Result[Self, tuple[str, int]]:
        if phone_number == "":
            return Err(("Phone number cannot be empty", 400))
        if not phone_number.isnumeric():
            return Err(("Phone number can only contain numbers", 400))
        if len(phone_number) < 10:
            return Err(("Phone number must have at least 10 characters", 400))
        self.PhoneNumber = phone_number
        return Ok(self)
