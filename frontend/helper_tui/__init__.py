from .clrscr import clrscr
from .clustering import clustering
from .COLORS import BCOLORS, FCOLORS
from .get_user_option_from_list import get_user_option_from_list
from .get_user_option_from_menu import get_user_option_from_menu
from .listing import listing
from .loop_til_valid import loop_til_valid 
from .refresh import refresh


def styling(x: str | int | float, y: str | int | float) -> str:
    return f"- {FCOLORS.CYAN}{x}{FCOLORS.END} {FCOLORS.GREEN}{y}{FCOLORS.END}"


def __error_msg(x: str) -> str:
    return FCOLORS.RED + x + FCOLORS.END


ENTER_TO_CONTINUE_MSG: str = FCOLORS.PURPLE + "Press Enter to continue..." + FCOLORS.END


__all__ = [
    "clrscr",
    "clustering",
    "BCOLORS",
    "FCOLORS",
    "get_user_option_from_list",
    "get_user_option_from_menu",
    "listing",
    "loop_til_valid",
    "styling",
    "refresh",
    "ENTER_TO_CONTINUE_MSG",
]
