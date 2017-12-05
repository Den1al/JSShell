import datetime
import jsbeautifier
import json
import shutil


def get_date():
    """ Gets the current time """
    return datetime.datetime.now()


def datetime_to_text(dt):
    """ Formats a datetime object to a human readable time """
    return dt.strftime('%H:%M:%S %Y-%m-%d')


def dict_to_beautified_json(d):
    """ Serializes & Beautifies a dictionary"""
    return jsbeautifier.beautify(json.dumps(d))


class More(object):
    """ Simulate the `more` binary from unix """

    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'

    def __init__(self, num_lines=shutil.get_terminal_size().lines):
        self.num_lines = num_lines

    def __ror__(self, other):
        s = str(other).split("\n")
        length = len(s)

        for i in range(0, length, self.num_lines):
            print(*s[i: i + self.num_lines], sep="\n")

            if i + self.num_lines >= length:
                return

            res = input("{colors.bg.white}{colors.fg.black}--More--({pctg:2.1%}){colors.reset}".format(pctg=i/length, colors=Colors))
            print(More.ERASE_LINE + More.CURSOR_UP_ONE, end="")

            if res == 'q':
                break

        print(More.ERASE_LINE , end="")


class Colors:
    """ Colors class:
    reset all colors with colors.reset two subclasses fg for foreground and bg for background.
    use as colors.subclass.colorname.
    i.e. colors.fg.red or colors.bg.green
    also, the generic bold, disable, underline, reverse, strikethrough,
    and invisible work with the main class
    i.e. colors.bold
    """

    reset='\033[0m'
    bold='\033[01m'
    disable='\033[02m'
    underline='\033[04m'
    reverse='\033[07m'
    strikethrough='\033[09m'
    invisible='\033[08m'
    italics='\033[3m'

    class fg:
        white='\033[37m'
        black='\033[30m'
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        yellow='\033[93m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan='\033[96m'

    class bg:
        white='\033[47m'
        black='\033[40m'
        red='\033[41m'
        green='\033[42m'
        orange='\033[43m'
        blue='\033[44m'
        purple='\033[45m'
        cyan='\033[46m'
        lightgrey='\033[47m'
