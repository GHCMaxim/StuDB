def MISSING_ARGS_MSG(missing_args: tuple[str]) -> str:
    return f"Missing arguments: {', '.join(missing_args)}."


ATTENDANCE_FOUND = "Attendance found."
ATTENDANCE_NOT_FOUND = "Attendance not found."
ATTENDANCE_EXISTS = "Attendance already exists."
ATTENDANCE_CREATED = "Attendance created."


def CREATE_USER_MSG(action: str, username: str) -> str:
    return f"User with username '{username}' {action.lower()}."


def ATTENDANCE_UPDATED_MSG(old: str, new: str) -> str:
    return f"Attendance updated from {old} to {new}."


def CREATE_GRADE_MSG(action: str, student_id: str, course_id: str) -> str:
    return f"Grade for student {student_id} in course {course_id} {action.lower()}."


def CREATE_GENERAL_MSG(action: str, typeof_object: str, name: str = "", id: str = "") -> str:
    typeof_object = typeof_object.capitalize()
    action = action.lower()
    return f"{typeof_object} with {'name' if name else 'id'} '{name if name else id}' {action}."
