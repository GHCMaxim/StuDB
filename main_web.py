from flask import Flask, render_template
from flask_restful import Api

from models_WEB import Attendance, Course, Grade, Student, Teacher

app = Flask(__name__)
api = Api(app)


@app.route("/attendance")
def attendance():
    return render_template("attendance.html")


@app.route("/course")
def course():
    return render_template("course.html")


@app.route("/student")
def student():
    return render_template("student.html")


@app.route("/teacher")
def teacher():
    return render_template("teacher.html")


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/grade")
def grade():
    return render_template("grade.html")


@app.route("/home")
def home():
    return render_template("home.html")


api.add_resource(AttendanceAPI, "/api/attendance")
api.add_resource(CourseAPI, "/api/course")
api.add_resource(StudentAPI, "/api/student")
api.add_resource(TeacherAPI, "/api/teacher")
api.add_resource(GradeAPI, "/api/grade")
api.add_resource(UserAPI, "/api/user")


if __name__ == "__main__":
    app.run()
