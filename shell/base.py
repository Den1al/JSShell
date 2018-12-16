from threading import Thread
from time import sleep
from typing import Dict, Union

from cmd2 import Cmd, categorize
from cmd2.plugin import PostparsingData
from blessings import Terminal

from common.config import read_config
from common.models.client import Client
from shell.utils.screen import banner, to_bold_cyan
from shell.utils.general import get_prompt


class BasePlugin(Cmd):
    """ BasePlugin - the base class which all of our plugins should inherit from.
        It is meant to define all the necessary base functions for plugins. """

    prompt = '>> '
    ruler = '-'
    intro = banner()
    terminators = []

    CATEGORY_SHELL = to_bold_cyan('Shell Based Operations')
    CATEGORY_GENERAL = to_bold_cyan('General Commands')

    def __init__(self):
        Cmd.__init__(self,
                     startup_script=read_config().get('STARTUP_SCRIPT', ''),
                     use_ipython=True)

        self.aliases.update({'exit': 'quit', 'help': 'help -v'})
        self.hidden_commands.extend(['load', 'pyscript', 'set', 'shortcuts', 'alias', 'unalias', 'shell', 'macro'])

        self.t = Terminal()
        self.selected_client = None

        self.prompt = self.get_prompt()
        self.allow_cli_args = False

        # Alerts Thread
        self._stop_thread = False
        self._seen_clients = set(Client.unique_client_ids())
        self._alert_thread = Thread()

        # Register the hook functions
        self.register_preloop_hook(self._alert_thread_preloop_hook)
        self.register_postloop_hook(self._alert_thread_postloop_hook)

        # Set the window title
        self.set_window_title('<< JSShell 2.0 >>')

        categorize([
            BasePlugin.do_help,
            BasePlugin.do_quit,
            BasePlugin.do_py,
            BasePlugin.do_ipy,
            BasePlugin.do_history,
            BasePlugin.do_edit
        ], BasePlugin.CATEGORY_GENERAL)

        self.register_postparsing_hook(self._refresh_client_data_post_parse_hook)

    def _alert_thread_preloop_hook(self) -> None:
        """ Start the alerter thread """

        self._stop_thread = False
        self._alert_thread = Thread(name='alerter', target=self._alert_function)
        self._alert_thread.start()

    def _alert_thread_postloop_hook(self) -> None:
        """ Stops the alerter thread """

        self._stop_thread = True

        if self._alert_thread.is_alive():
            self._alert_thread.join()

    def _alert_function(self) -> None:
        """ When the client list is larger than the one we know of
            alert the user that a new client has registered """

        while not self._stop_thread:
            if self.terminal_lock.acquire(blocking=False):
                current_clients = set(Client.unique_client_ids())
                delta = current_clients - self._seen_clients

                if len(delta) > 0:
                    self.async_alert(self.t.bold_blue(' << new client registered >>'), self.prompt)

                self._seen_clients = current_clients
                self.terminal_lock.release()

            sleep(0.5)

    def print_error(self, text: str, end: str ='\n', start: str='') -> None:
        """ Prints a formatted error message """

        self.poutput(start + self.t.bold_red('[-]') + ' ' + self.t.red(text), end=end)

    def print_info(self, text: str, end: str='\n', start: str='') -> None:
        """ Prints a formatted informational message """

        self.poutput(start + self.t.bold_yellow('[!]') + ' ' + self.t.yellow(text), end=end)

    def print_ok(self, text: str, end: str='\n', start: str='') -> None:
        """ Prints a formatted success message """

        self.poutput(start + self.t.bold_green('[+]') + ' ' + self.t.green(text), end=end)

    def print_pairs(self, title: str, body: Dict[str, str],
                    just_return: bool=False, colors: bool=True) -> Union[str, None]:
        """ Prints pairs of values with a certain title """

        if colors:
            data = [self.t.bold_white_underline(title)]
        else:
            data = [title]

        for key, value in body.items():
            k = key + ':'
            if colors:
                data.append(f' - {self.t.bold(k)} {value}')
            else:
                data.append(f' - {k} {value}')

        if just_return:
            return '\n'.join(data)

        self.ppaged('\n'.join(data))

    def select_client(self, client: Client) -> None:
        """ Handles the operation of selecting a new client """

        self.selected_client = client
        self.update_prompt()

    def _refresh_client_data_post_parse_hook(self, params: PostparsingData) -> PostparsingData:
        """ Refreshes the selected client data from the database. We do that because
            of `mongoengine`s behaviour, where if we set the current client, we do not track
            for modifications. This way, before every command is parsed we re-select the client """

        if self.selected_client:
            cid = self.selected_client.cid
            self.select_client(Client.objects(cid=cid).first())

        return params

    def get_prompt(self) -> str:
        """ Handles the operations of getting the prompt string """

        prompt = self.t.bold_cyan('>> ')

        if self.selected_client:
            client_id = self.t.bold_red(self.selected_client.cid)
            prompt = self.t.cyan(f"[Client #{client_id}]") + ' ' + prompt

        return prompt

    def update_prompt(self) -> None:
        """ Handles what is needed when updating the prompt """

        self.prompt = get_prompt(self)
