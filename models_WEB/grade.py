from __future__ import annotations

from textwrap import dedent

from flask import jsonify
from flask_restful import Resource, request

from database.mssql import conn, cursor
from frontend.helper_web.MESSAGE import CREATE_GRADE_MSG, MISSING_ARGS_MSG
from frontend.helper_web.validate_args import validate_args


class Grade(Resource):
    def get(self):
        validate_success, message_body, missing_args = validate_args(
            request.get_json(silent=True), tuple(["student_id", "course_id"])
        )
        if not validate_success:
            return jsonify({"message": MISSING_ARGS_MSG(missing_args)}), 400
        student_id, course_id = message_body["student_id"], message_body["course_id"]

        cursor.execute(
            dedent(
                f"""
            SELECT * FROM Grades
            WHERE StudentID = '{student_id}' AND CourseID = '{course_id}'
        """
            )
        )
        db_result = cursor.fetchone()
        if db_result is None:
            return (
                jsonify({"message": CREATE_GRADE_MSG(action="not found", student_id=student_id, course_id=course_id)}),
                404,
            )

        return jsonify({"student_id": db_result[0], "course_id": db_result[1], "grade": db_result[2]}), 200

    def post(self):
        validate_success, message_body, missing_args = validate_args(
            request.get_json(silent=True), tuple(["student_id", "course_id", "grade"])
        )
        if not validate_success:
            return jsonify({"message": MISSING_ARGS_MSG(missing_args)}), 400
        student_id, course_id, grade = message_body["student_id"], message_body["course_id"], message_body["grade"]

        cursor.execute(
            dedent(
                f"""
            INSERT INTO Grades(StudentID, CourseID, Grade)
            VALUES ('{student_id}', '{course_id}', {grade})
        """
            )
        )
        conn.commit()
        return jsonify({"message": CREATE_GRADE_MSG(action="created", student_id=student_id, course_id=course_id)}), 201

    def put(self):
        validate_success, message_body, missing_args = validate_args(
            request.get_json(silent=True), tuple(["student_id", "course_id", "grade"])
        )
        if not validate_success:
            return jsonify({"message": MISSING_ARGS_MSG(missing_args)}), 400
        student_id, course_id, grade = message_body["student_id"], message_body["course_id"], message_body["grade"]

        cursor.execute(
            dedent(
                f"""
            SELECT * FROM Grades
            WHERE StudentID = '{student_id}' AND CourseID = '{course_id}'
        """
            )
        )
        db_result = cursor.fetchone()
        if db_result is None:
            cursor.execute(
                dedent(
                    f"""
                INSERT INTO Grades(StudentID, CourseID, Grade)
                VALUES ('{student_id}', '{course_id}', {grade})
            """
                )
            )
        else:
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
        return (
            jsonify(
                {
                    "message": CREATE_GRADE_MSG(
                        action=("updated" if db_result is not None else "created"),
                        student_id=student_id,
                        course_id=course_id,
                    )
                }
            ),
            200,
        )

    def delete(self):
        validate_success, message_body, missing_args = validate_args(
            request.get_json(silent=True), tuple(["student_id", "course_id"])
        )
        if not validate_success:
            return jsonify({"message": MISSING_ARGS_MSG(missing_args)}), 400
        student_id, course_id = message_body["student_id"], message_body["course_id"]

        cursor.execute(
            dedent(
                f"""
            SELECT * FROM Grades
            WHERE StudentID = '{student_id}' AND CourseID = '{course_id}'
        """
            )
        )
        db_result = cursor.fetchone()
        if db_result is None:
            return jsonify({"message": f"Grade not found for {student_id} in {course_id}"}), 404

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
