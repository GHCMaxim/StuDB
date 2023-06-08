import pymssql
import os
import sys

from dotenv import load_dotenv

load_dotenv()

server = os.getenv("SERVER")
user = os.getenv("USER")
password = os.getenv("PASSWORD")
database = os.getenv("DATABASE")

def main():
    conn = pymssql.connect(server, user, password, database)
    cursor = conn.cursor()
    exists = cursor.execute("""
        IF OBJECT_ID('Students', 'U') IS NOT NULL
            SELECT 1
        ELSE
            SELECT 0
        """)

    if exists == 0:
        print("It seems like you don't have a database yet. Creating tables....")
        cursor.execute("""
            CREATE TABLE Students(
                StudentID int not null,
                StudentName varchar(255) not null,
                DateOfBirth date not null,
                PRIMARY KEY (StudentID) 
            )
            """)
        cursor.execute("""
            CREATE TABLE Courses(
                CourseID int not null,
                CourseName varchar(255) not null,
                PRIMARY KEY (CourseID)
                FOREIGN KEY (TeacherID) REFERENCES Teachers(TeacherID)
            )
            """)
        cursor.execute("""
            CREATE TABLE Grades(
                StudentID int not null,
                CourseID int not null,
                Grade int not null,
                PRIMARY KEY (StudentID, CourseID),
                FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
                FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
            )
            """)
        cursor.execute("""
            CREATE TABLE Teachers(
                TeacherID int not null,
                TeacherName varchar(255) not null,
                PRIMARY KEY (TeacherID)
            )
            """)
        cursor.execute("""
            CREATE TABLE Attendance(
                StudentID int not null,
                CourseID int not null,
                AttendanceDate date not null,
                AttendanceStatus bit not null,
                PRIMARY KEY (StudentID, CourseID),
                FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
                FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
            )
            """)
        cursor.commit()

    if exists == 1:
        print("Loading...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)