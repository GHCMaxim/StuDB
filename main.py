import sys

from option import Ok, Result

from database.mssql import conn, cursor
from frontend.helper_tui import *
from frontend.tui import *
from models import *


def menu():
    print("Welcome to the Student Management System. Please login to continue.")
    user = Login()
    fields_data = [("Enter username: ", user.get_username), ("Enter password: ", user.get_password)]
    for field, setter in fields_data:
        if (msg := loop_til_valid(field, setter)) != "":
            print(msg)
    cursor.execute(
        """
        SELECT Role FROM Users WHERE Username = %s AND Password = %s
        """,
        (user.username, user.password),
    )
    role = cursor.fetchone()
    if role is None:
        print("Invalid username or password. Please try again.")
        input("Press Enter to continue...")
        menu()

    while True:
        clrscr()
        last_msg = ""
        if last_msg:
            print(last_msg)
            last_msg = ""
        main_menu = [
            "[1] Students management",
            "[2] Courses management",
            "[3] Grades management",
            "[4] Teachers management",
            "[5] Attendance management",
            "[6] Exit",
        ]
        user_choice = get_user_option_from_menu("Main Menu", main_menu)
        respond: Result[None, str] = Ok(None)
        match user_choice:
            case 1:
                respond = MenuStudent().start()
            case 2:
                respond = MenuCourses().start()
            case 3:
                respond = MenuGrades().start()
            case 4:
                respond = MenuTeacher().start()
            case 5:
                respond = MenuAttendance().start()
            case 6:
                break
            case _:
                print("Invalid option. Please try again.")
        try:
            respond.unwrap()
        except (ValueError, TypeError) as e:
            print(e)
        input("Press Enter to continue...")


def main():
    cursor.execute(
        """
        IF OBJECT_ID('Students', 'U') IS NOT NULL
            SELECT 1
        ELSE
            SELECT 0
        """
    )
    exists = cursor.fetchone()[0]

    # if exists == 0:
    #     print("It seems like this is the first time you booted this program. Creating tables....")
    #     cursor.execute(
    #         """
    #         CREATE TABLE Logins(
    #             Username varchar(255) not null,
    #             Password varchar(255) not null,
    #             Role varchar(255) not null,
    #             PRIMARY KEY (Username)
    #         """
    #     )
    #     conn.commit()
    #     print("Please create an admin account.")
    #     user = Login()
    #     fields_data = [
    #         ("Enter username: ", user.set_username),
    #         ("Enter password: ", user.set_password),
    #         ("Enter role: ", user.set_role),
    #     ]
    #     for field, setter in fields_data:
    #         if (msg := loop_til_valid(field, setter)) != "":
    #             print(msg)

    #     cursor.execute(
    #         """
    #         INSERT INTO Logins (Username, Password, Role)
    #         VALUES (%s, %s, %s)
    #         """,
    #         (user.username, user.password, user.role),
    #     )
    #     conn.commit()
    #     print("Admin account created successfully.")
    print("Creating the rest of the tables....")
    cursor.execute(
        """
        CREATE TABLE Students(
            StudentID varchar(10) not null,
            StudentName varchar(255) not null,
            DateOfBirth date not null,
            Email varchar(255) not null,
            PhoneNumber varchar(10) not null,
            PRIMARY KEY (StudentID)
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE Teachers(
            TeacherID varchar(10) not null,
            TeacherName varchar(255) not null,
            DateOfBirth date not null,
            Email varchar(255) not null,
            PRIMARY KEY (TeacherID)
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE Courses(
            CourseID varchar(10) not null,
            CourseName varchar(255) not null,
            TeacherID varchar(10) not null,
            Credits int not null,
            PRIMARY KEY (CourseID),
            FOREIGN KEY (TeacherID) REFERENCES Teachers(TeacherID)
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE Grades(
            StudentID varchar(10) not null,
            CourseID varchar(10) not null,
            Grade int not null,
            PRIMARY KEY (StudentID, CourseID),
            FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
            FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE Attendance(
            StudentID varchar(10) not null,
            CourseID varchar(10) not null,
            AttendanceDate date not null,
            AttendanceStatus bit not null,
            PRIMARY KEY (StudentID, CourseID),
            FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
            FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
        )
        """
    )
    conn.commit()
    menu()

    if exists == 1:
        print("Loading...")
        menu()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)
