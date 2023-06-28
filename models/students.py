from __future__ import annotations
import re
import sys
import textwrap
from datetime import datetime
from option import Result, Ok, Err
import itertools
from database.mssql import cursor, conn


if sys.version_info < (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


class Student:
    StudentID: int
    StudentName: str
    DateOfBirth: str
    Email: str
    PhoneNumber: str

    def set_id(self, id: str) -> Result[Self, str]:
        if id == "":
            return Err("Student ID cannot be empty")
        if not id.isnumeric():
            return Err("Student ID can only contain numbers")
        cursor.execute("""
            SELECT StudentID FROM Students
            WHERE StudentID = %s
            """, (id))
        if cursor.fetchone() is not None:
            return Err("Student ID already exists")
        self.StudentID = int(id)
        return Ok(self)
    
    def get_id(self, id: str) -> Result[Self, str]:
        if id == "":
            return Err("Student ID cannot be empty")
        if not id.isnumeric():
            return Err("Student ID can only contain numbers")
        cursor.execute("""
            SELECT StudentID FROM Students
            WHERE StudentID = %s
            """, (id))
        if cursor.fetchone() is None:
            return Err("Student ID doesn't exist. Please try again.")
        self.StudentID = int(id)
        return Ok(self)
        

    def set_name(self, name: str) -> Result[Self, str]:
        if name == "":
            return Err("Name cannot be empty")
        if any(char.isdigit() for char in name):
            return Err("Name cannot contain numbers")
        self.StudentName = name
        return Ok(self)
    
    def set_dob(self, dob: str) -> Result[Self, str]:
        try:
            dob = datetime.strftime(datetime.strptime(dob, "%Y-%m-%d"), "%Y-%m-%d")
        except ValueError:
            return Err("Invalid date format. Please try again.")
        self.DateOfBirth = dob
        return Ok(self)
    
    def set_email(self, email: str) -> Result[Self, str]:
        if email == "":
            return Err("Email cannot be empty")
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            return Err("Invalid email format. Please try again.")
        self.Email = email
        return Ok(self)
    
    def set_phone(self, phone: str) -> Result[Self, str]:
        if phone == "":
            return Err("Phone number cannot be empty")
        if not phone.isnumeric():
            return Err("Phone number can only contain numbers")
        if len(phone) < 10 or len(phone) > 11:
            return Err("Phone number must have 10 or 11 digits")
        self.PhoneNumber = phone
        return Ok(self)
    
    def __str__(self) -> str:
        return textwrap.dedent(f"""
        Student ID: {self.StudentID}
        Student Name: {self.StudentName}
        Date of birth: {self.DateOfBirth}
        Email: {self.Email}
        Phone number: {self.PhoneNumber}
        """)
    
