from __future__ import annotations

from option import Err, Ok, Result
from typing_extensions import Self

from database.mssql import cursor


class Grades:
    StudentID: str
    CourseID: str
    Grade: int

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

    def set_grade(self, grade: str) -> Result[Self, str]:
        if grade == "":
            return Err("Grade cannot be empty")
        if not grade.isnumeric():
            return Err("Grade must be a number")
        if int(grade) < 0 or int(grade) > 10:
            return Err("Grade must be in range [0, 10]")
        self.Grade = int(grade)
        return Ok(self)
