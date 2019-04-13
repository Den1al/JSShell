import argparse
from typing import List

from cmd2 import with_argparser, argparse_completer, with_category
from argparse import ArgumentParser
import tableformatter as tf

from common.models.command import Command
from shell import BasePlugin
from shell.utils.screen import available_max_width_on_screen_for_commands
from shell.utils.general import js_beautify, client_required


class CommandsPlugin(BasePlugin):
    """ CommandsPlugin - describes the `commands` command """

    commands_plugin_parser = ArgumentParser(description='Show the executed commands on the selected client')
    commands_plugin_parser.add_argument('-i', '--id', help='Show information on a specific command by ID')
    commands_plugin_parser.add_argument('-l', '--limit', help='Limit the query results', type=int, default=5)

    @with_category(BasePlugin.CATEGORY_SHELL)
    @with_argparser(commands_plugin_parser)
    def do_commands(self, args: argparse.Namespace) -> None:
        """ The main of the `commands` command """

        if args.id:
            self._commands_plugin_show_specific_id(args.id)
        else:
            self._commands_plugin_show_all(limit=args.limit)

    def complete_commands(self, text: str, line: str, begin_index: int, end_index: int) -> List[str]:
        """ Handles the auto completion for this command """

        choices = dict(id=self.selected_client.unique_commands_ids)

        completer = argparse_completer.AutoCompleter(
            CommandsPlugin.commands_plugin_parser,
            arg_choices=choices
        )

        tokens, _ = self.tokens_for_completion(line, begin_index, end_index)

        return completer.complete_command(tokens, text, line, begin_index, end_index)

    @client_required
    def _commands_plugin_show_specific_id(self, command_id: str) -> None:
        """ Shows a specific command by ID """

        cmd: Command = Command.objects(cid=command_id).first()

        if not cmd:
            self.print_error('Command ID does not exist!')
            return

        cmds_text = self.print_pairs('Command Information', body={
            'ID          ': command_id,
            'Created On  ': cmd.created_on,
            'Status      ': cmd.status,
            'Command     ': f'{ self.t.bold_white("<< command below >>") }\n{ js_beautify(cmd.text) }'
        }, just_return=True)

        cmds_text += '\n\n'

        cmds_text += self.print_pairs('Output Information', body={
            'Created On  ': cmd.output.created_on,
            'Output      ': f'{ self.t.bold_white("<< output below >>") }\n{ js_beautify(cmd.output.text) }',
        }, just_return=True)

        self.ppaged(cmds_text)

    @client_required
    def _commands_plugin_show_all(self, limit: int) -> None:
        """ Shows all commands """

        max_cmd_w, max_out_w = available_max_width_on_screen_for_commands(
            self.selected_client.max_commands_width,
            self.selected_client.max_outputs_width
        )

        table = tf.generate_table(
            grid_style=tf.FancyGrid(),
            columns=['ID', 'Status', 'Created On', 'Command', 'Output'],
            rows=[
                cmd.to_table_list(max_cmd_w, max_out_w)
                for cmd in
                self.selected_client.reversed_commands[:limit]
            ]
        )

        self.ppaged(table, chop=True)
