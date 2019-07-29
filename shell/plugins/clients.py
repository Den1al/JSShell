import argparse
from typing import List

from cmd2 import with_argparser, argparse_completer, with_category
from argparse import ArgumentParser
import tableformatter as tf

from common.models.client import Client
from shell import BasePlugin
from shell.utils.screen import available_max_width_on_screen_for_clients


class ClientsPlugin(BasePlugin):
    """ ClientsPlugin - describes the `clients` command """

    clients_plugin_parser = ArgumentParser(
        description='List and control the clients that have registered to our system')
    clients_plugin_parser_group = clients_plugin_parser.add_mutually_exclusive_group()

    clients_plugin_parser_group.add_argument('-i', '--id', help='show information for specific client by ID')
    clients_plugin_parser_group.add_argument('-k', '--kill', help='kill a client by ID')
    clients_plugin_parser_group.add_argument('-l', '--limit', help='Limit the query results', type=int, default=5)

    @with_category(BasePlugin.CATEGORY_SHELL)
    @with_argparser(clients_plugin_parser)
    def do_clients(self, args: argparse.Namespace) -> None:
        """ The main of the `clients` command """
        if args.id:
            self._client_plugin_handle_single_id(args.id)
        elif args.kill:
            self._client_plugin_handle_kill(args.kill)
        else:
            self._client_plugin_handle_show_all(limit=args.limit)

    def complete_clients(self, text: str, line: str, begin_index: int, end_index: int) -> List[str]:
        """ Handles the auto completion for this command """

        choices = dict(
            id=Client.unique_client_ids,
            kill=Client.unique_client_ids
        )

        completer = argparse_completer.AutoCompleter(
            ClientsPlugin.clients_plugin_parser,
            arg_choices=choices
        )

        tokens, _ = self.tokens_for_completion(line, begin_index, end_index)

        return completer.complete_command(tokens, text, line, begin_index, end_index)

    def _client_plugin_handle_single_id(self, client_id: str) -> None:
        """ Shows information for a specific client ID """

        client: Client = Client.objects(cid=client_id).first()

        if not client:
            self.print_error('client does not exist!')
        else:
            self.print_pairs('Client Information', {
                'ID              ': client.cid,
                'IP Address      ': client.ip,
                'Registered On   ': client.registered_on,
                'Last Seen       ': client.humanized_last_seen,
                'Num of Commands ': len(client.commands),
                'User Agent      ': client.user_agent,
            })

    def _client_plugin_handle_kill(self, client_id: str) -> None:
        """ Removes a specific client from the database """

        if client_id == '*':
            Client.delete_all_clients()
            self.print_ok('Killed all clients!')
            return

        client: Client = Client.objects(cid=client_id).first()

        if not client:
            self.print_error('client does not exist!')
        else:
            if client == self.selected_client:
                self.print_error('you cant kill the selected client!')
            else:
                client.delete_from_db()
                self.print_ok('client deleted successfully!')

    def _client_plugin_handle_show_all(self, limit: int) -> None:
        """ Shows all clients in the database """

        clients: List[Client] = list(Client.objects.order_by('-registered_on')[:limit])

        max_last_seen = 0 if not clients else max([
            len(str(client.humanized_last_seen)) for client in clients
        ])

        max_ip_length = 0 if not clients else max([
            client.ip_length_on_screen for client in clients
        ])

        max_user_agent_width = available_max_width_on_screen_for_clients(max_last_seen, max_ip_length)

        table = tf.generate_table(
            grid_style=tf.FancyGrid(),
            columns=['ID', 'IP', 'User Agent', 'Registered On', 'Last Seen'],
            rows=[
                client.to_table_list(max_user_agent_width)
                for client in clients
            ]
        )

        self.ppaged(table, chop=True)
