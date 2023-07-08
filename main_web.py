import sys

from option import Ok, Result
from frontend.helper_tui import *
from database.mssql import cursor, conn
from frontend.tui import *
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/attendance')
def attendance():
    return render_template('attendance.html')

@app.route('/course')
def course():
    return render_template('course.html')

@app.route('/student')
def student():
    return render_template('student.html')

@app.route('/teacher')
def teacher():
    return render_template('teacher.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/grade')
def grade():
    return render_template('grade.html')

@app.route('/home')
def home():
    return render_template('home.html')



