from models import Courses
from option import Ok, Result

from database.mssql import conn, cursor

from ..helper_tui import *


class MenuCourses:
    def start(self) -> Result[None, str]:
        last_msg = ""
        while True:
            last_msg = refresh(last_msg)
            courses_menu = [
                "[1] Add course",
                "[2] Edit course",
                "[3] Delete course",
                "[4] View course",
                "[5] View all courses",
                "[6] Back",
            ]
            choice = get_user_option_from_menu("Course Management", courses_menu)

            match choice:
                case 1:
                    last_msg = self.__add()
                case 2:
                    last_msg = self.__edit()
                case 3:
                    last_msg = self.__delete()
                case 4:
                    last_msg = self.__view()
                case 5:
                    last_msg = self.__view_all()
                case 6:
                    return Ok(None)
                case _:
                    last_msg = "Invalid option. Please try again."

    def __add(self) -> str:
        course = Courses()

        fields_data = [
            ("Enter course id: ", course.set_id),
            ("Enter course name: ", course.set_name),
            ("Enter teacher id: ", course.set_teacher_id),
            ("Enter course credits: ", course.set_credits),
        ]
        for field, setter in fields_data:
            if (msg := loop_til_valid(field, setter)) != "":
                return msg

        cursor.execute(
            """ 
            INSERT INTO Courses (CourseID, CourseName, CourseDescription, Credits)
            VALUES (%s, %s, %s, %s)
            """,
            (course.CourseID, course.CourseName, course.TeacherID, course.Credits),
        )
        conn.commit()

        return "Course added successfully."

    def __edit(self) -> str:
        course = Courses()
        if (msg := loop_til_valid("Enter course id: ", course.get_id)) != "":
            return msg

        fields_data = [
            ("Enter course name: ", course.set_name),
            ("Enter teacher id: ", course.set_teacher_id),
            ("Enter course credits: ", course.set_credits),
        ]
        for field, setter in fields_data:
            if (msg := loop_til_valid(field, setter)) != "":
                return msg

        cursor.execute(
            """
            UPDATE Courses
            SET CourseName = %s, TeacherID = %s, Credits = %s
            WHERE CourseID = %s
            """,
            (course.CourseName, course.TeacherID, course.Credits, course.CourseID),
        )
        conn.commit()
        return "Course edited successfully."

    def __delete(self) -> str:
        course = Courses()
        if (msg := loop_til_valid("Enter course id: ", course.get_id)) != "":
            return msg

        cursor.execute(
            """
            DELETE FROM Courses
            WHERE CourseID = %s
            """,
            (course.CourseID),
        )
        conn.commit()
        return "Course deleted successfully."

    def __view(self) -> str:
        course = Courses()
        if (msg := loop_til_valid("Enter course id: ", course.get_id)) != "":
            return msg

        cursor.execute(
            """
            SELECT * FROM Courses
            WHERE CourseID = %s
            """,
            (course.CourseID),
        )
        result = cursor.fetchone()
        if result is None:
            return "Course not found."
        else:
            print("CourseID\tCourseName\tTeacherID\tCredits")
            print(f"{result[0]}\t{result[1]}\t{result[2]}\t{result[3]}")
        return ""

    def __view_all(self) -> str:
        cursor.execute(
            """
            SELECT * FROM Courses
            """
        )
        result = cursor.fetchall()
        if result is None:
            return "No courses found."
        else:
            print("CourseID\tCourseName\tTeacherID\tCredits")
            for row in result:
                print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}")
        return ""
