from common.models import db
from common.utils import now


class Output(db.Document):
    """ Output Model - describes a executed command"""

    text = db.StringField(default='-')
    created_on = db.DateTimeField(default=now)

    meta = {
        'indexes': [
            'created_on'
        ]
    }

    def to_dict(self):
        """ Converts the class instance into a dict """

        return {
            'text': self.text,
            'created_on': str(self.created_on)
        }

    def __repr__(self):
        """ Returns the string representation of this `Output` instance """

        return f'<Output' \
               f'text={self.text[:25]}' \
               f'created_on="{self.created_on}"' \
               f'>'
