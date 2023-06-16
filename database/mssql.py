import os
import pymssql
from dotenv import load_dotenv

load_dotenv()

server = os.getenv("SERVER")
user = os.getenv("USER")
password = os.getenv("PASSWORD")
database = os.getenv("DATABASE")

conn = pymssql.connect(server, user, password, database)
cursor = conn.cursor()
