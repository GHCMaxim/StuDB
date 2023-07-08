from __future__ import annotations

import sys

from option import Result, Ok, Err
from database.mssql import cursor, conn

class Login:
    username: str
    password: str
    role: str

    def set_username(self, username: str) -> Result[Login, str]:
        if username == "":
            return Err("Username cannot be empty")
        cursor.execute("SELECT * FROM Users WHERE Username = %s", (username))
        result = cursor.fetchone()
        if result is not None:
            return Err("Username already exists")
        self.username = username
        return Ok(self)

    def set_password(self, password: str) -> Result[Login, str]:
        if password == "":
            return Err("Password cannot be empty")
        self.password = password
        return Ok(self)
    
    def set_role(self, role: str) -> Result[Login, str]:
        if role == "":
            return Err("Role cannot be empty")
        if role not in ["Student", "Teacher", "Admin"]:
            return Err("Role must be either Student, Teacher or Admin")
        self.role = role
        return Ok(self)
    
    def get_username(self, username: str) -> Result[Login, str]:
        if username == "":
            return Err("Username cannot be empty")
        self.username = username
        return Ok(self)

    def get_password(self, password: str) -> Result[Login, str]:
        if password == "":
            return Err("Password cannot be empty")
        self.password = password
        return Ok(self)
    