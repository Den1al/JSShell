from app import app, db
from app.models import Client, Command
from prettytable import PrettyTable
from time import sleep
from jsbeautifier import beautify


class InteractiveShell(object):
    """ An interactive shell for the JSShell Project """
    def __init__(self):
        self.stay = True
        self.prompt = '>> '
        self.current_client_id = 0

    def error(self, text):
        """ Error print statement """
        print('Error:',text)

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
        for c in Client.query.all():
           t.add_row([c.id, c.client_id, c.user_agent, c.ip, c.last_beaconed])
        print(t)

    def help_menu(self):
        """ Prints a pretty help menu """
        t = PrettyTable(['command', 'description'])
        t.align = 'l'
        t.add_row(['list', 'Lists all the clients registered'])
        t.add_row(['help', 'self.help()'])
        t.add_row(['select <id>', 'Selected a specific client from the list'])
        t.add_row(['<command>', 'Executes a command to the current selected client'])
        t.add_row(['back', 'Detaches from the current client'])
        t.add_row(['exit', 'Exists this interactive shell'])
        t.add_row(['coms', 'Displays the commands and output for the current client'])
        t.add_row(['com <id>', 'Displays a specific command and output for the current client'])
        t.add_row(['comk', 'Kills a command ("*" for all)'])
        t.add_row(['clik', 'Kills a client ("*" for all)'])
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

        self.prompt = '(Client {}) >> '.format(i)
        self.current_client_id = i

    def back(self):
        """ Detaches from a client """
        self.prompt = '>> '
        self.current_client_id = 0

    @client_required
    def execute_command(self, cmd):
        """ Executes a command on a client """
        client = Client.query.filter_by(id=self.current_client_id).first()
        c = Command(cmd)
        client.commands.append(c)
        db.session.add(c)
        db.session.commit()
        print('Added task successfully.')


    @client_required
    def display_commands(self, com_id = None):
        """ Displays all the commands executed on a client """
        if com_id:
            client = Client.query.filter_by(id=self.current_client_id).first()
            if not com_id in [str(i.id) for i in client.commands]:
                self.error('Selected client does not have this command ID.')
                return

            com = Command.query.filter_by(id=com_id).first()
            print('(Command {}) : \n{}'.format(com.id, beautify(com.cmd)))
            print('(Output  {}) : \n{}'.format(com.id, beautify(com.output)))

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

            status = "waiting"

            if com.is_served:
                status = "served"

            if com.is_returned:
                status = "complete"

            t.add_row([com.id, status, command, output])

        print(t)

    def watch_for_commands(self):
        """ A thread that will watch for incoming commands and print them """
        while True:
            if not self.current_client_id:
                continue

            client = Client.query.filter_by(id=self.current_client_id).first()
            if not client:
                continue

            com = client.get_printable()
            if not com:
                continue

            print('(Command {}) >> {}'.format(com.id, com.output))
            com.is_printed = True
            db.session.commit()
            sleep(1)

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

    def loop(self):
        """ The main loop for the class """

        print("""
  ╦╔═╗╔═╗┬ ┬┌─┐┬  ┬
  ║╚═╗╚═╗├─┤├┤ │  │
 ╚╝╚═╝╚═╝┴ ┴└─┘┴─┘┴─┘
  By @Daniel_Abeles
        """)

        while self.stay:
            op,_,tail = input(self.prompt).strip().partition(' ')

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

            elif op == 'coms':
                self.display_commands()

            elif op == 'comk':
                self.command_kill(tail)

            elif op == 'clik':
                self.client_kill(tail)

            elif op == '':
                continue

            else:
                self.execute_command(' '.join([op, tail]))


if __name__ == "__main__":

    ints = InteractiveShell()
    ints.loop()
