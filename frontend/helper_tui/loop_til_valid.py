def loop_til_valid(prompt: str, validator: callable) -> str:
    user_input = input(f"{prompt}, leave blank to cancel: ")
    if user_input == "":
        return "Cancelled"
    while True:
        try:
            validator(user_input).unwrap()
            break
        except (ValueError, TypeError) as e:
            user_input = input(f"{e}, please try again: ")
    return ""