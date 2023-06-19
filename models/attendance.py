from __future__ import annotations
import re
import sys
import textwrap
from datetime import datetime
from option import Result, Ok, Err
from database.mssql import cursor, conn
import itertools


if sys.version_info < (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

class Attendance:
    StudentID: int
    CourseID: str
    AttendanceDate: str
    AttendanceStatus: int

    def set_student_id(self, id: str) -> Result[Self, str]:
        if id == "":
            return Err("ID cannot be empty")
        if not id.isnumeric():
            return Err("ID must be a number")
        cursor.execute("SELECT * FROM Students WHERE StudentID = %s", (id))
        result = cursor.fetchone()
        if result is None:
            return Err("StudentID does not exist")
        self.StudentID = int(id)
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