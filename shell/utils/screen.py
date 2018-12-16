import os
from shutil import get_terminal_size
from typing import Tuple

from blessings import Terminal


def banner():
    """ Returns the banner """

    t = Terminal()

    return t.bright_blue('''\
     ╦╔═╗┌─┐┬ ┬┌─┐┬  ┬  
     ║╚═╗└─┐├─┤├┤ │  │  
    ╚╝╚═╝└─┘┴ ┴└─┘┴─┘┴─┘ 2.0 \
    ''') + f'''
        {t.underline_bright_cyan("by @Daniel_Abeles")}
    '''


def available_max_width_on_screen_for_commands(max_command_length: int, max_output_length: int) -> Tuple[int, int]:
    """ Returns the longest available width for the commands plugin.
        Due to the fact we have constant values in the table, we can
        calculate the remaining available width for the rest of the
        columns. This is due `tableformatter` tables width overflow behaviour.
    """

    id_length = 32
    max_status_length = 8
    date_length = 26
    table_buffer = 16

    width, _ = get_terminal_size()

    space_left = width - table_buffer - date_length - max_status_length - id_length
    half_space_left = int(space_left / 2)

    if max_command_length > half_space_left and max_output_length > half_space_left:
        return half_space_left, half_space_left

    if max_command_length < half_space_left:
        return max_command_length, space_left - max_command_length

    if max_output_length < half_space_left:
        return space_left - max_output_length, max_output_length


def available_max_width_on_screen_for_clients(max_last_seen_length: int) -> int:
    """ Returns the longest available width for the clients plugin.
        Due to the fact we have constant values in the table, we can
        calculate the remaining available width for the rest of the
        columns. This is due `tableformatter` tables width overflow behaviour.
    """

    id_length = 32
    date_length = 26
    table_buffer = 14

    width, _ = get_terminal_size()
    space_left = width - table_buffer - date_length - id_length

    return space_left - max_last_seen_length


def clear_screen() -> None:
    """ Clears the screen """

    os.system('cls' if os.name == 'nt' else 'clear')


def to_bold_cyan(title: str) -> str:
    return '\033[01m\033[36m' + title + '\033[0m'
