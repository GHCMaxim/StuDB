from __future__ import annotations

import re
import sys
from datetime import datetime

from flask_restful import Resource, request
from option import Err, Ok, Result

from database.mssql import conn, cursor
from frontend.helper_web.MESSAGE import ACTION_MUST_BE_CRUD, CREATE_GENERAL_MSG, MISSING_ARGS_MSG
from frontend.helper_web.validate_args import validate_args

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class StudentAPI(Resource):
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
        """Get students"""
        validate_success, message_body, missing_args = validate_args(request.get_json(silent=True), tuple(["student_id"]))
        if not validate_success:
            return {"message": MISSING_ARGS_MSG(missing_args), "data": {}}, 400
        student_id = message_body["student_id"]

        cursor.execute(f"SELECT * FROM Students WHERE StudentID = '{message_body['student_id']}'")
        db_result = cursor.fetchone()
        if db_result is None:
            return {
                "message": CREATE_GENERAL_MSG(action="not found", typeof_object="student", id=student_id),
                "data": {},
            }, 404

        return (
            {
                "message": CREATE_GENERAL_MSG(action="found", typeof_object="student", id=student_id),
                "data": {
                    "student_id": db_result[0],
                    "student_name": db_result[1],
                    "date_of_birth": datetime.strftime(db_result[2], "%Y-%m-%d"),
                    "email": db_result[3],
                    "phone_number": db_result[4],
                },
            },
            200,
        )

    def CREATE(self):
        """Add student"""
        validate_success, message_body, missing_args = validate_args(
            request.get_json(silent=True), tuple(["student_id", "student_name", "date_of_birth", "email", "phone_number"])
        )
        if not validate_success:
            return {"message": MISSING_ARGS_MSG(missing_args), "data": {}}, 400
        student_id, student_name, date_of_birth_str, email, phone_number = (
            message_body["student_id"],
            message_body["student_name"],
            message_body["date_of_birth"],
            message_body["email"],
            message_body["phone_number"],
        )

        cursor.execute(f"SELECT * FROM Students WHERE StudentID = '{student_id}'")
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
            if (res := validator(message_body[variable])).is_err:
                return {"message": res.unwrap_err()[0], "data": {}}, res.unwrap_err()[1]
        cursor.execute(
            "INSERT INTO Students (StudentID, StudentName, DateOfBirth, Email, PhoneNumber) VALUES (%s, %s, %s, %s, %s)",
            (student_id, student_name, date_of_birth_str, email, phone_number),
        )

        conn.commit()
        return (
            {
                "message": CREATE_GENERAL_MSG(action="created", typeof_object="student", id=student_id),
                "data": {
                    "student_id": student_id,
                    "student_name": student_name,
                    "date_of_birth": date_of_birth_str,
                    "email": email,
                    "phone_number": phone_number,
                },
            },
            201,
        )

    def UPDATE(self):
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

        if (res := self.validate_student_id(student_id)).is_err:
            return {"message": res.unwrap_err()[0], "data": {}}, res.unwrap_err()[1]

        cursor.execute(f"SELECT * FROM Students WHERE StudentID = '{student_id}'")
        db_result = cursor.fetchone()
        if db_result is None:
            for variable, validator in {
                "student_name": self.validate_student_name,
                "date_of_birth": self.validate_date_of_birth,
                "email": self.validate_email,
                "phone_number": self.validate_phone_number,
            }.items():
                if (res := validator(message_body[variable])).is_err():
                    return {"message": res.unwrap_err()[0], "data": {}}, res.unwrap_err[1]
            cursor.execute(
                "INSERT INTO Students (StudentID, StudentName, DateOfBirth, Email, PhoneNumber) VALUES (%s, %s, %s, %s, %s)",
                (student_id, student_name, date_of_birth, email, phone_number),
            )
        else:
            # TL;DR: if the value is empty, use the value from the database; else it must pass validation
            for variable, validator in {
                "student_name": self.validate_student_name,
                "date_of_birth": self.validate_date_of_birth,
                "email": self.validate_email,
                "phone_number": self.validate_phone_number,
            }.items():
                if message_body[variable] == "":
                    continue
                if (res := validator(message_body[variable])).is_err:
                    return {"message": res.unwrap_err()[0], "data": {}}, res.unwrap_err()[1]
            student_name = db_result[1] if student_name == "" else student_name
            date_of_birth = db_result[2] if date_of_birth == "" else date_of_birth
            email = db_result[3] if email == "" else email
            phone_number = db_result[4] if phone_number == "" else phone_number

            cursor.execute(
                "UPDATE Students SET StudentName = %s, DateOfBirth = %s, Email = %s, PhoneNumber = %s WHERE StudentID = %s",
                (student_name, date_of_birth, email, phone_number, student_id),
            )
        conn.commit()

        cursor.execute(f"SELECT * FROM Students WHERE StudentID = '{student_id}'")
        db_result = cursor.fetchone()
        return (
            {
                "message": CREATE_GENERAL_MSG(
                    action=("added" if db_result is None else "updated"), typeof_object="student", id=student_id
                ),
                "data": {
                    "student_id": db_result[0],
                    "student_name": db_result[1],
                    "date_of_birth": datetime.strftime(db_result[2], "%Y-%m-%d"),
                    "email": db_result[3],
                    "phone_number": db_result[4],
                },
            },
            201,
        )

    def DELETE(self):
        """Delete student"""
        validate_success, message_body, missing_args = validate_args(request.get_json(silent=True), tuple(["student_id"]))
        if not validate_success:
            return {"message": MISSING_ARGS_MSG(missing_args), "data": {}}, 400
        student_id = message_body["student_id"]

        cursor.execute(f"SELECT StudentID FROM Students WHERE StudentID = '{student_id}'")
        if cursor.fetchone() is None:
            return {"message": "Student not found", "data": {}}, 404

        cursor.execute(f"DELETE FROM Students WHERE StudentID = '{student_id}'")
        conn.commit()
        return {"message": CREATE_GENERAL_MSG(action="deleted", typeof_object="student", id=student_id), "data": {}}, 200

    def validate_student_id(self, student_id: str) -> Result[Self, tuple[str, int]]:
        if student_id == "":
            return Err(("Student ID cannot be empty", 400))
        if not student_id.isnumeric():
            return Err(("Student ID can only contain numbers", 400))
        if len(student_id) < 8:
            return Err(("Student ID must have at least 8 characters", 400))
        return Ok(self)

    def validate_student_name(self, name: str) -> Result[Self, tuple[str, int]]:
        if name == "":
            return Err(("Name cannot be empty", 400))
        if any(char.isdigit() for char in name):
            return Err(("Name cannot contain numbers", 400))
        return Ok(self)

    def validate_date_of_birth(self, dob: str) -> Result[Self, tuple[str, int]]:
        try:
            dob = datetime.strftime(datetime.strptime(dob, "%Y-%m-%d"), "%Y-%m-%d")
        except ValueError:
            return Err(("Invalid date format. Please try again.", 400))
        return Ok(self)

    def validate_email(self, email: str) -> Result[Self, tuple[str, int]]:
        if email == "":
            return Err(("Email cannot be empty", 400))
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            return Err(("Invalid email format. Please try again.", 400))
        return Ok(self)

    def validate_phone_number(self, phone_number: str) -> Result[Self, tuple[str, int]]:
        if phone_number == "":
            return Err(("Phone number cannot be empty", 400))
        if not phone_number.isnumeric():
            return Err(("Phone number can only contain numbers", 400))
        if len(phone_number) != 10:
            return Err(("Phone number must have 10 characters", 400))
        return Ok(self)
