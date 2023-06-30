import pymssql
import os
from dotenv import load_dotenv

from option import Ok, Result
from models import Attendance
from ..helper_tui import *
from database.mssql import cursor, conn

class MenuAttendance:
    def start(self) -> Result[None,str]:
        last_msg = ""
        while True:
            last_msg = refresh(last_msg)
            attendance_menu = [
                "[1] Add attendance",
                "[2] Edit attendance (By switching status via input.)",
                "[3] Delete attendance",
                "[4] View attendance",
                "[5] View all attendance",
                "[6] Back"
            ]
            choice = get_user_option_from_menu("Attendance Management",attendance_menu)

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
        attendance = Attendance()

        fields_data = [
            ("Enter student id: ", attendance.set_student_id),
            ("Enter course id: ", attendance.set_course_id),
            ("Enter date (YYYY-MM-DD): ", attendance.set_date),
            ("Enter attendance status: ", attendance.set_status)
        ]
        for (field, setter) in fields_data:
            if (msg := loop_til_valid(field, setter)) != "":
                return msg
        
        cursor.execute("""
            INSERT INTO Attendance (StudentID, CourseID, Date, Status)
            VALUES (%s, %s, %s, %s)
            """, (attendance.StudentID, attendance.CourseID, attendance.AttendanceDate, attendance.AttendanceStatus))
        conn.commit()
        return "Attendance added successfully."
    
    def __edit(self) -> str:
        attendance = Attendance()

        fields_data = [
            ("Enter student id: ", attendance.set_student_id),
            ("Enter course id: ", attendance.set_course_id),
            ("Enter date (YYYY-MM-DD): ", attendance.set_date),
        ]
        for (field, setter) in fields_data:
            if (msg := loop_til_valid(field, setter)) != "":
                return msg
        
        cursor.execute("""
            SELECT * FROM Attendance
            WHERE StudentID = %s AND CourseID = %s AND Date = %s
            IF STATUS = 1
                UPDATE Attendance SET Status = 0
            ELSE
                UPDATE Attendance SET Status = 1
            """, (attendance.StudentID, attendance.CourseID, attendance.AttendanceDate))
        conn.commit()
        return "Attendance edited successfully."
    
    def __delete(self) -> str:
        attendance = Attendance()

        fields_data = [
            ("Enter student id: ", attendance.set_student_id),
            ("Enter course id: ", attendance.set_course_id),
            ("Enter date (YYYY-MM-DD): ", attendance.set_date),
        ]
        for (field, setter) in fields_data:
            if (msg := loop_til_valid(field, setter)) != "":
                return msg
        
        cursor.execute("""
            DELETE FROM Attendance
            WHERE StudentID = %s AND CourseID = %s AND Date = %s
            """, (attendance.StudentID, attendance.CourseID, attendance.AttendanceDate))
        conn.commit()
        return "Attendance deleted successfully."
    
    def __view(self) -> str:
        attendance = Attendance()

        fields_data = [
            ("Enter student id: ", attendance.set_student_id),
            ("Enter course id: ", attendance.set_course_id),
            ("Enter date (YYYY-MM-DD): ", attendance.set_date),
        ]
        for (field, setter) in fields_data:
            if (msg := loop_til_valid(field, setter)) != "":
                return msg
        
        cursor.execute("""
            SELECT * FROM Attendance
            WHERE StudentID = %s AND CourseID = %s AND Date = %s
            """, (attendance.StudentID, attendance.CourseID, attendance.AttendanceDate))
        result = cursor.fetchall()
        if result is None:
            return "Attendance not found."
        else:
            print(f"StudentID\tCourseID\tDate\tStatus")
            for row in result:  
                print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}")
            return ""

        
    def __view_all(self) -> str:
        cursor.execute("""
            SELECT * FROM Attendance
            """)
        result = cursor.fetchall()
        if result is None:
            return "No attendance found."
        else:
            print(f"StudentID\tCourseID\tDate\tStatus")
            for row in result:
                print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}")
            return ""
