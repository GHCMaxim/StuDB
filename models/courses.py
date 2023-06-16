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

class Courses:
    CourseID: str
    CourseName: str
    TeacherID: int

    def set_id(self, id: str) -> Result[Self, str]:
        if id == "":
            return Err("ID cannot be empty")
        cursor.execute("SELECT * FROM Courses WHERE CourseID = %s", (id))
        result = cursor.fetchone()
        if result is not None:
            return Err("CourseID already exists")
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