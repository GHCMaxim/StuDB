import pymssql
import os
from dotenv import load_dotenv

from option import Ok, Result
from models import Teacher
from ..helper_tui import *
from database.mssql import cursor, conn

class MenuTeacher:
    def start(self) -> Result[None, str]:
        last_msg = ""
        while True:
            last_msg = refresh(last_msg)
            teacher_menu = [
                "[1] Add teacher",
                "[2] Edit teacher",
                "[3] Delete teacher",
                "[4] View teacher",
                "[5] View all teachers",
                "[6] Back"
            ]
            choice = get_user_option_from_menu("Teacher Management", teacher_menu)
            
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
        teacher = Teacher()

        fields_data = [
            ("Enter teacher id: ", teacher.set_id),
            ("Enter teacher name: ", teacher.set_name),
            ("Enter teacher's date of birth: ", teacher.set_dob),
            ("Enter teacher email: ", teacher.set_email),
        ]
        for (field, setter) in fields_data:
            if (msg := loop_til_valid(field, setter)) != "":
                return msg


        cursor.execute(""" 
            INSERT INTO Teacher (TeacherID, TeacherName, DateOfBirth, TeacherEmail)
            VALUES (%s, %s, %s, %s)
            """, (teacher.TeacherID, teacher.TeacherName, teacher.DateOfBirth, teacher.Email))
        conn.commit()
        return "Teacher added successfully."
    
    def __edit(self) -> str:
        teacher = Teacher()
        if (msg := loop_til_valid("Enter teacher id: ", teacher.set_id)) != "":
            return msg
        
        fields_data = [
            ("Enter teacher name: ", teacher.set_name),
            ("Enter teacher's date of birth: ", teacher.set_dob),
            ("Enter teacher email: ", teacher.set_email),
        ]
        for (field, setter) in fields_data:
            if (msg := loop_til_valid(field, setter)) != "":
                return msg
        cursor.execute("""
            UPDATE Teacher
            SET TeacherName = %s, DateOfBirth = %s, TeacherEmail = %s
            WHERE TeacherID = %s
            """, (teacher.TeacherName, teacher.DateOfBirth, teacher.Email, teacher.TeacherID))
        conn.commit()
        return "Teacher edited successfully."
    
    def __delete(self) -> str:
        teacher = Teacher()
        if (msg := loop_til_valid("Enter teacher id: ", teacher.set_id)) != "":
            return msg
        cursor.execute("""
            DELETE FROM Teacher
            WHERE TeacherID = %s
            """, (teacher.TeacherID))
        conn.commit()
        return "Teacher deleted successfully."
    
    def __view(self) -> str:
        teacher = Teacher()
        if (msg := loop_til_valid("Enter teacher id: ", teacher.set_id)) != "":
            return msg
        cursor.execute("""
            SELECT * FROM Teacher
            WHERE TeacherID = %s
            """, (teacher.TeacherID))
        result = cursor.fetchone()
        if result == None:
            return "Teacher not found."
        else:
            for row in result:
                print('row = %r' % (row,))
            return ""
    
    def __view_all(self) -> str:
        cursor.execute("""
            SELECT * FROM Teacher
            """)
        result = cursor.fetchall()
        if result == None:
            return "No teachers found."
        else:
            for row in result:
                print('row = %r' % (row,))
            return ""
