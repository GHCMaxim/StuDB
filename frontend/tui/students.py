import pymssql
import os
from dotenv import load_dotenv

from option import Ok, Result
from models import Student, Course, Grade, Teacher, Attendance
from helper_tui import *

load_dotenv()

server = os.getenv("SERVER")
user = os.getenv("USER")
password = os.getenv("PASSWORD")
database = os.getenv("DATABASE")

conn = pymssql.connect(server, user, password, database)
cursor = conn.cursor()

class MenuStudent:
    def start(self) -> tuple[bool, str]:
        while True:
            user_input = input("""
            Please select an option:
            [1] Add new student
            [2] Edit student
            [3] Delete student
            [4] View student
            [5] View all students
            [6] Back
            """)
            match user_input:
                case "1":
                    return self.add()
                case "2":
                    return self.edit()
                case "3":
                    return self.delete()
                case "4":
                    return self.view()
                case "5":
                    return self.view_all()
                case "6":
                    return (True, "")
    
    def add(self) -> str:
        student = Student()

        fields_data = [
            ("", student.set_id),
            ("Enter student name: ", student.set_name),
            ("Enter student date of birth (YYYY-MM-DD): ", student.set_dob),
            ("Enter student email: ", student.set_email),
            ("Enter student phone number: ", student.set_phone)
        ]
        for (field, setter) in fields_data:
            if (msg := loop_til_valid(field, setter)) != "":
                return msg

    
        cursor.execute(""" 
            INSERT INTO Students (StudentName, DateOfBirth, Email, PhoneNumber)
            VALUES (%s, %s, %s, %s)
            """, (Student.StudentName, Student.DateOfBirth, Student.Email, Student.PhoneNumber))
        conn.commit()