from cmd2 import with_argparser, with_category
from argparse import ArgumentParser

from shell import BasePlugin
from shell.utils.general import client_required


class BackPlugin(BasePlugin):
    """ BackPlugin - describes the `back` command"""

    back_parser = ArgumentParser(description='Un-select the current selected client')

    @with_category(BasePlugin.CATEGORY_SHELL)
    @with_argparser(back_parser)
    def do_back(self, _) -> None:
        """ The main of the `back` command """

        self._back_plugin_handle_back()

    @client_required
    def _back_plugin_handle_back(self) -> None:
        """ Simply set the current client to `None` """

        self.select_client(None)
