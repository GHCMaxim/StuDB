from __future__ import annotations

import re
import sys
from datetime import datetime
from textwrap import dedent

from flask import jsonify
from flask_restful import Resource, request
from option import Err, Ok, Result

from database.mssql import conn, cursor

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class Student(Resource):
    def get(self):
        """Get students"""
        data = request.get_json()
        student_id = data["student_id"]

        if (res := self.get_student_id(student_id)).is_err:
            return jsonify({"message": res.unwrap_err()[0]}), res.unwrap_err()[1]

        cursor.execute(
            """
            SELECT * FROM Students
            WHERE StudentID = %s
            """,
            (student_id),
        )
        student = cursor.fetchone()

        return jsonify(
            {
                "student_id": student[0],
                "student_name": student[1],
                "date_of_birth": student[2],
                "email": student[3],
                "phone_number": student[4],
            }
        )

    def post(self):
        """Add student"""
        data = request.get_json()
        student_id, student_name, date_of_birth, email, phone_number = (
            data["student_id"],
            data["student_name"],
            data["date_of_birth"],
            data["email"],
            data["phone_number"],
        )

        for variable, validator in {
            "student_id": self.validate_student_id,
            "student_name": self.validate_student_name,
            "date_of_birth": self.validate_date_of_birth,
            "email": self.validate_email,
            "phone_number": self.validate_phone_number,
        }.items():
            if (res := validator(data[variable])).is_err():
                return jsonify({"message": res.unwrap_err()[0]}), res.unwrap_err()[1]

        # fmt: off
        cursor.execute(dedent(
            """
           INSERT INTO Students(StudentID, StudentName, DateOfBirth, Email, PhoneNumber)
           VALUES (:student_id, :student_name, :date_of_birth, :email, :phone_number)
           """), {
               "student_id": student_id,
               "student_name": student_name,
               "date_of_birth": date_of_birth,
               "email": email,
               "phone_number": phone_number
            })
        # fmt: on

        conn.commit()
        return jsonify({"message": f"Student {student_name} added successfully"}), 201

    def put(self):
        """Update student"""
        data = request.get_json()
        student_id, student_name, date_of_birth, email, phone_number = (
            data["student_id"],
            data["student_name"],
            data["date_of_birth"],
            data["email"],
            data["phone_number"],
        )

        for variable, validator in {
            "student_id": self.get_student_id,
            "student_name": self.validate_student_name,
            "date_of_birth": self.validate_date_of_birth,
            "email": self.validate_email,
            "phone_number": self.validate_phone_number,
        }.items():
            if (res := validator(data[variable])).is_err():
                return jsonify({"message": res.unwrap_err()[0]}), res.unwrap_err()[1]

        # fmt: off
        cursor.execute(dedent(
            """
            UPDATE Students
            SET StudentName = :student_name, DateOfBirth = :date_of_birth, Email = :email, PhoneNumber = :phone_number
            WHERE StudentID = :student_id
            """),
            {
                "student_id": student_id,
                "student_name": student_name,
                "date_of_birth": date_of_birth,
                "email": email,
                "phone_number": phone_number
            })
        # fmt: on

        conn.commit()
        return jsonify({"message": f"Student {student_name} updated successfully"}), 200

    def delete(self):
        """Delete student"""
        data = request.get_json()
        student_id = data["student_id"]
        if (res := self.get_student_id(student_id)).is_err:
            return jsonify({"message": res.unwrap_err()[0]}), res.unwrap_err()[1]
        cursor.execute("DELETE FROM Students WHERE StudentID = %s", (student_id))
        conn.commit()
        return jsonify({"message": f"Student {student_id} deleted successfully"}), 200

    def validate_student_id(self, student_id: str) -> Result[Self, tuple[str, int]]:
        if student_id == "":
            return Err(("Student ID cannot be empty", 400))
        if not student_id.isnumeric():
            return Err(("Student ID can only contain numbers", 400))
        if len(student_id) < 8:
            return Err(("Student ID must have at least 8 characters", 400))
        cursor.execute(
            """
            SELECT StudentID FROM Students
            WHERE StudentID = %s
            """,
            (student_id),
        )
        if cursor.fetchone() is not None:
            return Err(("Student ID already exists", 400))
        self.StudentID = int(student_id)
        return Ok(self)

    def get_student_id(self, student_id: str) -> Result[Self, tuple[str, int]]:
        if student_id == "":
            return Err(("Student ID cannot be empty", 400))
        if not student_id.isnumeric():
            return Err(("Student ID can only contain numbers", 400))
        if len(student_id) < 8:
            return Err(("Student ID must have at least 8 characters", 400))
        cursor.execute(
            """
            SELECT StudentID FROM Students
            WHERE StudentID = %s
            """,
            (student_id),
        )
        if cursor.fetchone() is None:
            return Err(("Student ID does not exist", 400))
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
