from __future__ import annotations
import re
import sys
import textwrap
from datetime import datetime
from option import Result, Ok, Err
from database.mssql import cursor, conn
import itertools


from typing_extensions import Self

class Teacher:
    TeacherID: int
    TeacherName: str
    DateOfBirth: str
    Email: str

    def set_id(self, id: str) -> Result[Self, str]:
        if id == "":
            return Err("Teacher ID cannot be empty")
        if not id.isnumeric():
            return Err("Teacher ID can only contain numbers")
        if len(id) < 8:
            return Err("Teacher ID must have at least 8 characters")
        cursor.execute("""
            SELECT TeacherID FROM Teachers
            WHERE TeacherID = %s
            """, (id))
        if cursor.fetchone() is not None:
            return Err("Teacher ID already exists")
        self.TeacherID = int(id)
        return Ok(self)
    
    def get_id(self, id: str) -> Result[Self, str]:
        if id == "":
            return Err("Teacher ID cannot be empty")
        if not id.isnumeric():
            return Err("Teacher ID can only contain numbers")
        if len(id) < 8:
            return Err("Teacher ID must have at least 8 characters")
        cursor.execute("""
            SELECT TeacherID FROM Teachers
            WHERE TeacherID = %s
            """, (id))
        if cursor.fetchone() is None:
            return Err("Teacher ID doesn't exist. Please try again.")
        self.TeacherID = int(id)
        return Ok(self)

    def set_name(self, name: str) -> Result[Self, str]:
        if name == "":
            return Err("Name cannot be empty")
        if any(char.isdigit() for char in name):
            return Err("Name cannot contain numbers")
        self.TeacherName = name
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
    
    def __str__(self) -> str:
        return textwrap.dedent(f"""\
            TeacherID: {self.TeacherID}
            TeacherName: {self.TeacherName}
            DateOfBirth: {self.DateOfBirth}
            Email: {self.Email}
            """)