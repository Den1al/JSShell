import argparse
from typing import List

from cmd2 import with_argparser, with_category
from argparse import ArgumentParser

from shell import BasePlugin
from shell.utils.general import client_required


class ExecutePlugin(BasePlugin):
    """ ExecutePlugin - describes the `execute` command """

    execute_plugin_parser = ArgumentParser(description='Execute commands on the selected client')
    execute_plugin_parser.add_argument('cmd', nargs='+', type=str, help='The command to run')

    @with_category(BasePlugin.CATEGORY_SHELL)
    @with_argparser(execute_plugin_parser)
    def do_execute(self, args: argparse.Namespace) -> None:
        """ The main of the `execute` plugin """

        self._execute_plugin_handle_execute(args.cmd)

    @client_required
    def _execute_plugin_handle_execute(self, cmd: List) -> None:
        """ Executes the command on the selected client """

        self.selected_client.run_command(' '.join(cmd))
        self.print_ok('Executed command successfully')
