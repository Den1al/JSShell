import json
from typing import List

from cmd2 import with_argparser, with_category, argparse_completer
from argparse import ArgumentParser

from common.models.command import Command
from shell import BasePlugin
from shell.utils.general import client_required, js_beautify


class DumpPlugin(BasePlugin):

    dump_parser = ArgumentParser(description='Dumps a command to the disk')
    dump_parser.add_argument('id', help='the command ID to dump')
    dump_parser.add_argument('-f', '--file', help='the filename of the dumped command')
    dump_parser.add_argument('-t', '--type',
                             help='the file type to save',
                             choices=['txt', 'json'],
                             default='txt')

    @with_category(BasePlugin.CATEGORY_SHELL)
    @with_argparser(dump_parser)
    def do_dump(self, args):
        """ The main of the `dump` command """

        self._dump_parser_handle_dumping(args.id, args.file, args.type)

    def complete_dump(self, text: str, line: str, begin_index: int, end_index: int) -> List[str]:
        """ Handles the auto completion for this command """

        choices = dict(id=self.selected_client.unique_commands_ids)

        completer = argparse_completer.AutoCompleter(
            DumpPlugin.dump_parser,
            arg_choices=choices
        )

        tokens, _ = self.tokens_for_completion(line, begin_index, end_index)

        return completer.complete_command(tokens, text, line, begin_index, end_index)

    @client_required
    def _dump_parser_handle_dumping(self, command_id: str, file_name: str, file_type: str) -> None:
        cmd = Command.objects(cid=command_id).first()

        if not cmd:
            self.print_error('Command not found!')
            return

        if not file_name:
            file_name = f'{cmd.cid}.{file_type}'

        if file_type == 'txt':
            self._dump_parser_handle_dumping_txt(cmd, file_name)
        elif file_type == 'json':
            self._dump_parser_handle_dumping_json(cmd, file_name)

        self.print_ok('Command dumped successfully!')

    def _dump_parser_handle_dumping_txt(self, cmd: Command, file_name: str) -> None:
        cmds_text = self.print_pairs('Command Information', body={
            'ID          ': cmd.cid,
            'Created On  ': cmd.created_on,
            'Status      ': cmd.status,
            'Command     ': f'<< command below >>\n{ js_beautify(cmd.text, colors=False) }'
        }, just_return=True, colors=False)

        if cmd.output:
            cmds_text += '\n\n' + self.print_pairs('Output Information', body={
                'Created On  ': cmd.output.created_on,
                'Output      ': f'"<< output below >>" \n{ js_beautify(cmd.output.text, colors=False) }',
            }, just_return=True, colors=False)

        with open(file_name, 'w') as f:
            f.write(cmds_text)

    # noinspection PyMethodMayBeStatic
    def _dump_parser_handle_dumping_json(self, cmd: Command, file_name: str) -> None:
        with open(file_name, 'w') as f:
            json.dump({
                'command': cmd.to_dict(),
                'output': cmd.output.to_dict() if cmd.output else {}
            }, f)
