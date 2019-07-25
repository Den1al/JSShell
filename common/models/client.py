from typing import List, Union

from common.models import db
from common.models.command import Command
from common.utils import now, new_uuid, first, to_humanized_date

CommandsList = List[Union[None, Command]]


class Client(db.Document):
    """ Client Model - describes a connected client"""

    cid = db.StringField(required=True, primary_key=True, default=new_uuid)
    user_agent = db.StringField(default='-')
    ip = db.StringField(default='-')
    registered_on = db.DateTimeField(default=now)
    last_seen = db.DateTimeField(default=now)
    commands = db.ListField(
        db.ReferenceField(Command)
    )

    @property
    def ip_length_on_screen(self):
        """ Return the length of the IP address + padding """
        return len(self.ip) + 3

    @property
    def reversed_commands(self) -> CommandsList:
        """ The commands ListField on reversed order (by the creation date) """
        return sorted(self.commands, key=lambda cmd: cmd.created_on, reverse=True)

    @property
    def max_commands_width(self) -> int:
        """ The longest command width from the commands ListField """

        not_empty_commands_length = [
            len(c.text) for c
            in self.commands
            if c.text
        ]

        if len(not_empty_commands_length) == 0:
            return 0

        return max(not_empty_commands_length)

    @property
    def max_outputs_width(self) -> int:
        """ The longest output width from the commands ListField """

        outputs_length = [
            len(c.output.text) for c
            in self.commands
            if c.output and c.output.text
        ]

        if len(outputs_length) == 0:
            return 0

        return max(outputs_length)

    def unique_commands_ids(self) -> List[str]:
        """ Generates a list of all commands unique ID's """

        return [str(cmd.cid) for cmd in self.commands]

    @property
    def humanized_last_seen(self) -> str:
        """ Converts the last seen to a human readable format """

        return to_humanized_date(self.last_seen)

    @staticmethod
    def unique_client_ids() -> List[str]:
        """ Generates a list of all unique client ID's """

        return [str(client.cid) for client in Client.objects] + ['*']

    @staticmethod
    def delete_all_clients() -> None:
        for client in Client.objects:
            client.delete_from_db()

    def delete_from_db(self):
        for cmd in self.commands:
            cmd.delete_from_db(save=False)

        self.delete()
        self.save()

    def _generate_shortened_user_agent(self, max_user_agent_width: int) -> int:
        """ Generates a shortened user agent string according to the
            longest user agent string in the database """

        if len(self.user_agent) <= max_user_agent_width:
            return self.user_agent

        return self.user_agent[:max_user_agent_width - 4] + ' ...'

    def update_last_seen(self) -> None:
        """ Handles all the needed operations to update the last seen date """

        self.last_seen = now()
        self.save()

    def get_first_not_served_command(self) -> Command:
        """ Returns the first not served command """

        not_served_commands = [
            c for c in
            self.commands
            if not c.is_served
        ]

        return first(not_served_commands)

    def run_command(self, command_string: str) -> None:
        """ Handles all the needed operations to run a command """

        cmd = Command(text=command_string)
        cmd.save()

        self.commands.append(cmd)
        self.save()

    def to_table_list(self, max_user_agent_width: int) -> List[Union[str, int]]:
        """ Converts this `Client` instance to a `tableformatter` list """

        return [
            self.cid,
            self.ip,
            self._generate_shortened_user_agent(max_user_agent_width),
            self.registered_on,
            self.humanized_last_seen
        ]

    def __repr__(self):
        """ Returns the string representation of this `Client` instance """

        return f'<Client: ' \
               f'cid="{self.cid}", ' \
               f'ip="{self.ip}", ' \
               f'user_agent="{self.user_agent}", ' \
               f'registered_on="{self.registered_on}",' \
               f' last_seen="{self.last_seen}"' \
               f'>'
