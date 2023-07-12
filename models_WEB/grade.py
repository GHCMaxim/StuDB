from __future__ import annotations

from textwrap import dedent

from flask import jsonify
from flask_restful import Resource, request

from database.mssql import conn, cursor


class Grade(Resource):
    def get(self):
        data = request.get_json()
        if data is None:
            return jsonify({"message": "Bad request"}), 400
        student_id, course_id = data["student_id"], data["course_id"]
        cursor.execute(
            dedent(
                f"""
            SELECT * FROM Grades
            WHERE StudentID = '{student_id}' AND CourseID = '{course_id}'
        """
            )
        )
        row = cursor.fetchone()
        if row is None:
            return jsonify({"message": "Not found"}), 404

        return jsonify({"student_id": row[0], "course_id": row[1], "grade": row[2]}), 200

    def post(self):
        data = request.get_json()
        if data is None:
            return jsonify({"message": "Bad request"}), 400
        student_id, course_id, grade = data["student_id"], data["course_id"], data["grade"]

        cursor.execute(
            dedent(
                f"""
            INSERT INTO Grades(StudentID, CourseID, Grade)
            VALUES ('{student_id}', '{course_id}', {grade})
        """
            )
        )
        conn.commit()
        return jsonify({"message": f"Created {grade} for {student_id} in {course_id}"}), 201

    def put(self):
        data = request.get_json()
        if data is None:
            return jsonify({"message": "Bad request"}), 400
        student_id, course_id, grade = data["student_id"], data["course_id"], data["grade"]

        cursor.execute(
            dedent(
                f"""
            UPDATE Grades
            SET Grade = {grade}
            WHERE StudentID = '{student_id}' AND CourseID = '{course_id}'
        """
            )
        )
        conn.commit()
        return jsonify({"message": f"Updated {grade} for {student_id} in {course_id}"}), 200

    def delete(self):
        data = request.get_json()
        if data is None:
            return jsonify({"message": "Bad request"}), 400
        student_id, course_id = data["student_id"], data["course_id"]

        cursor.execute(
            dedent(
                f"""
            DELETE FROM Grades
            WHERE StudentID = '{student_id}' AND CourseID = '{course_id}'
        """
            )
        )
        conn.commit()
        return jsonify({"message": f"Deleted {student_id} in {course_id}"}), 200
