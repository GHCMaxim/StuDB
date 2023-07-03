from option import Ok, Result
from models import Grades
from ..helper_tui import *
from database.mssql import cursor, conn

class MenuGrades:
    def start(self) -> Result[None, str]:
        last_msg = ""
        while True:
            last_msg = refresh(last_msg)
            grades_menu = [
                "[1] Add a grade",
                "[2] Edit a grade",
                "[3] Delete a grade",
                "[4] View a grade",
                "[5] View all grades for a student",
                "[6] View all grades for a course",
                "[7] Back"
            ]
            choice = get_user_option_from_menu("Grades Management", grades_menu)

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
                    last_msg = self.__view_all_for_student()
                case 6:
                    last_msg = self.__view_all_for_course()
                case 7:
                    return Ok(None)
                case _:
                    last_msg = "Invalid option. Please try again."
                
    def __add(self) -> str:
        grade = Grades()

        fields_data = [
            ("Enter student ID: ", grade.set_student_id),
            ("Enter course ID: ", grade.set_course_id),
            ("Enter grade: ", grade.set_grade)
        ]
        for (field, setter) in fields_data:
            if (msg := loop_til_valid(field, setter)) != "":
                return msg

        cursor.execute(""" 
            INSERT INTO Grades (GradeID, StudentID, CourseID, Grade)
            VALUES (%s, %s, %s)
            """, (grade.StudentID, grade.CourseID, grade.Grade))
        conn.commit()
        print("Grade added successfully.")
        return ""
    
    def __edit(self) -> str:
        grade = Grades()

        fields_data = [
            ("Enter student ID: ", grade.set_student_id),
            ("Enter course ID: ", grade.set_course_id),
            ("Enter grade: ", grade.set_grade)
        ]
        for (field, setter) in fields_data:
            if (msg := loop_til_valid(field, setter)) != "":
                return msg

        cursor.execute(""" 
            UPDATE Grades
            SET Grade = %s
            WHERE StudentID = %s AND CourseID = %s
            """, (grade.Grade, grade.StudentID, grade.CourseID))
        conn.commit()
        print("Grade updated successfully.")
        return ""
    
    def __delete(self) -> str:
        grade = Grades()

        fields_data = [
            ("Enter student ID: ", grade.set_student_id),
            ("Enter course ID: ", grade.set_course_id)
        ]
        for (field, setter) in fields_data:
            if (msg := loop_til_valid(field, setter)) != "":
                return msg

        cursor.execute(""" 
            DELETE FROM Grades
            WHERE StudentID = %s AND CourseID = %s
            """, (grade.StudentID, grade.CourseID))
        conn.commit()
        print("Grade deleted successfully.")
        return ""
    
    def __view(self) -> str:
        grade = Grades()

        fields_data = [
            ("Enter student ID: ", grade.set_student_id),
            ("Enter course ID: ", grade.set_course_id)
        ]
        for (field, setter) in fields_data:
            if (msg := loop_til_valid(field, setter)) != "":
                return msg

        cursor.execute(""" 
            SELECT * FROM Grades
            WHERE StudentID = %s AND CourseID = %s
            """, (grade.StudentID, grade.CourseID))
        result = cursor.fetchone()
        if result is None:
            print("No such grade exists.")
            return ""
        else:
            print(f"Grade: {result[2]}")
            return ""
    
    def __view_all_for_student(self) -> str:
        grade = Grades()

        fields_data = [
            ("Enter student ID: ", grade.set_student_id)
        ]
        for (field, setter) in fields_data:
            if (msg := loop_til_valid(field, setter)) != "":
                return msg

        cursor.execute(""" 
            SELECT * FROM Grades
            WHERE StudentID = %s
            """, (grade.StudentID))
        result = cursor.fetchall()
        if result is None:
            print("No grades for this student exists.")
            return ""
        else:
            for row in result:
                print(f"Grade: {row[2]}")
            return ""
        
    def __view_all_for_course(self) -> str:
        grade = Grades()

        fields_data = [
            ("Enter course ID: ", grade.set_course_id)
        ]
        for (field, setter) in fields_data:
            if (msg := loop_til_valid(field, setter)) != "":
                return msg

        cursor.execute(""" 
            SELECT * FROM Grades
            WHERE CourseID = %s
            """, (grade.CourseID))
        result = cursor.fetchall()
        if result is None:
            print("No grades for this course exists.")
            return ""
        else:
            for row in result:
                print('row = %r' % (row,))
            return ""
    
    