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
        cursor.execute("""
            CREATE TABLE Students(
                StudentID int not null,
                StudentName varchar(255) not null,
                DateOfBirth date not null,
                PRIMARY KEY (StudentID)
                FOREIGN KEY (StudentID) REFERENCES Students(StudentID) 
            )
            """)
    if exists == 1:
        cursor.execute("""
            DROP TABLE Students
            """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)