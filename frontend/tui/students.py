import pymssql
import os
from dotenv import load_dotenv

from option import Ok, Result
from models import Student
from ..helper_tui import *
from database.mssql import cursor, conn

class MenuStudent:
    def start(self) -> Result[None,str]:
        last_msg = ""
        while True:
            last_msg = refresh(last_msg)
            student_menu = [
                "[1] Add student",
                "[2] Edit student",
                "[3] Delete student",
                "[4] View student",
                "[5] View all students",
                "[6] Back"
            ]
            choice = get_user_option_from_menu("Student Management",student_menu)
            
            match choice:
                case 1:
                    last_msg = self.__add()
                case 2:
                    last_msg = self.__edit()
                case 3:
                    last_msg =  self.__delete()
                case 4:
                    last_msg = self.__view()
                case 5:
                    last_msg = self.__view_all()
                case 6:
                    return Ok(None)
                case _:
                    last_msg = "Invalid option. Please try again."
    
    def __add(self) -> str:
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
            INSERT INTO Students (StudentID, StudentName, DateOfBirth, Email, PhoneNumber)
            VALUES (%s, %s, %s, %s, %s)
            """, (student.StudentID, student.StudentName, student.DateOfBirth, student.Email, student.PhoneNumber))
        conn.commit()
        return "Student added successfully."
    
    def __edit(self) -> str:
        student = Student()
        if (msg := loop_til_valid("Enter student ID: ", student.set_id)) != "":
            return msg

        fields_data = [
            ("Enter student name: ", student.set_name),
            ("Enter student date of birth (YYYY-MM-DD): ", student.set_dob),
            ("Enter student email: ", student.set_email),
            ("Enter student phone number: ", student.set_phone)
        ]
        for (field, setter) in fields_data:
            if (msg := loop_til_valid(field, setter)) != "":
                return msg

        cursor.execute("""
            UPDATE Students
            SET StudentName = %s, DateOfBirth = %s, Email = %s, PhoneNumber = %s
            WHERE StudentID = %s
            """, (student.StudentName, student.DateOfBirth, student.Email, student.PhoneNumber, student.StudentID))
        conn.commit()
        return "Student updated successfully."
    
    def __delete(self) -> str:
        student = Student()
        if (msg := loop_til_valid("Enter student ID: ", student.set_id)) != "":
            return msg

        cursor.execute("""
            DELETE FROM Students
            WHERE StudentID = %s
            """, (student.StudentID))
        conn.commit()
        return ""
    
    def __view(self) -> str:
        student = Student()
        if (msg := loop_til_valid("Enter student ID: ", student.set_id)) != "":
            return msg

        cursor.execute("""
            SELECT * FROM Students
            WHERE StudentID = %s
            """, (student.StudentID))
        row = cursor.fetchone()
        print(row)
        return ""
    
    def __view_all(self) -> str:
        cursor.execute("""
            SELECT * FROM Students
            """)
        for row in cursor:
            print('row = %r' % (row,))
        return ""
    