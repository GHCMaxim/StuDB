from __future__ import annotations
import re
import sys
import textwrap
from datetime import datetime
from option import Result, Ok, Err
import itertools


if sys.version_info < (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

class Teacher:
    TeacherID: int
    TeacherName: str
    DateOfBirth: str
    Email: str

    @classmethod
    def count(cls):
        try:
            with open('te_count_data.txt') as fin:
                i = int(fin.read())
        except IOError:
            i = 0
        i+=1
        cls.id_iter = itertools.count(i)
        with open('count_data', 'w') as fout:
            fout.write(str(i))
    
    def set_id(self) -> Result[Self, int]:
        self.TeacherID = next(Teacher.id_iter)
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