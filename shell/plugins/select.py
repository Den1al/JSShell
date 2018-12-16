import argparse
from typing import List

from cmd2 import with_argparser, argparse_completer, with_category
from argparse import ArgumentParser

from common.models.client import Client
from shell import BasePlugin


class SelectPlugin(BasePlugin):
    """ SelectPlugin - describes the `select` command """

    select_parser = ArgumentParser(description='Select a client as the current client')
    select_parser.add_argument('id', help='The client\'s ID (from the "clients" command)')

    @with_category(BasePlugin.CATEGORY_SHELL)
    @with_argparser(select_parser)
    def do_select(self, args: argparse.Namespace) -> None:
        """ The main of the `select` command """

        self._select_plugin_handle_select(args.id)

    def complete_select(self, text: str, line: str, begin_index: int, end_index: int) -> List[str]:
        """ Handles the auto completion for this command """

        choices = dict(id=Client.unique_client_ids())

        completer = argparse_completer.AutoCompleter(SelectPlugin.select_parser, arg_choices=choices)
        tokens, _ = self.tokens_for_completion(line, begin_index, end_index)
        
        return completer.complete_command(tokens, text, line, begin_index, end_index)

    def _select_plugin_handle_select(self, client_id: str) -> None:
        """ Selected a client as the selected client by ID """

        client = Client.objects(cid=client_id).first()

        if not client:
            self.print_error('client does not exist!')
            return

        self.select_client(client)
