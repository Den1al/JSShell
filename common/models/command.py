from typing import List

from common.models import db
from common.models.output import Output
from common.utils import now, new_uuid

NOT_YET_SERVED = 'queued'
SERVED_BUT_NOT_COMPLETE = 'served'
COMPLETE = 'complete'


class Command(db.Document):
    """ Command Model - describes a executed command"""

    cid = db.StringField(required=True, primary_key=True, default=new_uuid)
    text = db.StringField(required=True)
    created_on = db.DateTimeField(default=now)
    is_served = db.BooleanField(default=False)
    is_complete = db.BooleanField(default=False)
    output = db.ReferenceField(Output)

    meta = {
        'indexes': [
            'created_on',
            'is_served'
        ]
    }

    @property
    def status(self) -> str:
        """ Returns a human friendly status """

        status = NOT_YET_SERVED

        if self.is_served:
            status = SERVED_BUT_NOT_COMPLETE

        if self.is_complete:
            status = COMPLETE

        return status

    @property
    def colored_status(self) -> str:
        """ Returns a human friendly colored status """

        reset = '\033[0m'
        blue = '\033[34m'
        yellow = '\033[93m'
        green = '\033[32m'

        return {
            NOT_YET_SERVED: yellow,
            SERVED_BUT_NOT_COMPLETE: blue,
            COMPLETE: green
        }.get(self.status, '') + self.status + reset

    def _generate_shortened_command_text(self, max_cmd_width: int) -> str:
        """ Generated a shortened command based on the longest
            command the selected client holds """

        if not self.text:
            return '-'

        if len(self.text) <= max_cmd_width:
            return self.text

        return self.text[:max_cmd_width - 3] + '...'

    def _generate_shortened_output_text(self, max_cmd_width: int) -> str:
        """ Generated a shortened output based on the longest
            output the selected client holds """

        if not (self.output and self.output.text):
            return '-'

        if len(self.output.text) <= max_cmd_width:
            return self.output.text

        return self.output.text[:max_cmd_width - 3] + '...'

    def set_served(self) -> None:
        """ Handles all the needed operations to set the `is_served` status """

        self.is_served = True
        self.save()

    def set_output(self, output: Output) -> None:
        """ Handles all the needed operations to set the `output` status """

        self.is_complete = True
        self.output = output
        self.save()

    def to_table_list(self, max_cmd_width: int, max_out_width: int) -> List[str]:
        """ Converts this `Command` instance to a `tableformatter` list """

        return [
            self.cid,
            self.colored_status,
            self.created_on,
            self._generate_shortened_command_text(max_cmd_width),
            self._generate_shortened_output_text(max_out_width)
        ]

    def to_dict(self):
        """ Converts the class instance into a dict """

        return {
            'id': self.cid,
            'status': self.status,
            'created_on': str(self.created_on),
            'text': self.text
        }

    def __repr__(self):
        """ Returns the string representation of this `Command` instance """

        return f'<Command ' \
               f'cid="{self.cid}" ' \
               f'text="{self.text[:25]}" ' \
               f'is_served={self.is_served} ' \
               f'is_complete={self.is_complete} ' \
               f'output={self.output} ' \
               f'>'
