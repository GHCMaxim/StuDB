from database.login import global_var

def have_permission(session_key: str, admin_only: bool = False) -> bool:
    valid_session_key = session_key == global_var["session_key"]
    roles = ["Admin"] if admin_only else ["Admin", "Teacher"]
    valid_role = global_var["current_user_role"] in roles
    return valid_session_key and valid_role