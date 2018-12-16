import importlib
import pkgutil
from typing import List

from shell.base import BasePlugin
from shell.utils.screen import clear_screen


def get_all_plugins() -> List:
    """ Returns all the available plugins inside the plugin
        directory. We need to import the plugins before using
        the `__subclasses__()` function. """

    for _, name, _ in pkgutil.iter_modules(['shell/plugins']):
        importlib.import_module('shell.plugins.' + name, __package__)

    return BasePlugin.__subclasses__()


class JSShell(*get_all_plugins(), BasePlugin):
    """ The JSShell class. We inherit from all the plugins
        to simulate the notion of mixins. Basically every plugin
        contributes their functions, so in the sum up we have all
        of their abilities joined.

        to run the command loop:
        >>> JSShell.cmdloop()
        """


def start_shell() -> None:
    """ Handles all the operations needed to start
        JSShell command line interface """

    clear_screen()
    JSShell().cmdloop()
