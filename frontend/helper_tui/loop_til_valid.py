from __future__ import annotations

import sys

if sys.version_info >= (3, 11):
    from typing import Callable
else:
    from typing_extensions import Callable


def loop_til_valid(prompt: str, validator: Callable) -> str:
    user_input = input(f"{prompt}, leave blank to cancel: ")
    if user_input == "":
        confirm = input("Are you sure you want to cancel? (y/n): ")
        if confirm.lower() == "y":
            return "Cancelled"
        user_input = input(f"{prompt}, leave blank to cancel: ")
    while True:
        try:
            validator(user_input).unwrap()
            break
        except (ValueError, TypeError) as e:
            user_input = input(f"{e}, please try again: ")
    return ""
