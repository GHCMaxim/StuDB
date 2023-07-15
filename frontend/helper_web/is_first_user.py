from database.mssql import cursor

def is_first_user() -> bool:
    cursor.execute(f"SELECT * FROM Users")
    db_result = cursor.fetchone()
    if db_result is None:
        return True
    else:
        return False