import datetime
import uuid
from typing import Any, Sequence

import arrow


def now() -> datetime:
    """ Returns the current time """

    return datetime.datetime.utcnow()


def new_uuid() -> str:
    """ Created a new UUID string """

    return str(uuid.uuid4()).replace('-', '')


def first(collection: Sequence) -> Any:
    """ Retrieves the first element of a collection """

    if len(collection) == 0:
        return None

    return collection[0]


def to_humanized_date(date: datetime) -> str:
    """ Converts a date to a human readable format """

    return arrow.get(date).humanize()


def concat_url_path(url: str, path: str) -> str:
    """ Safely concatenating the start of a url string and a path """

    if url.endswith('/'):
        url = url[:-1]

    if path.startswith('/'):
        path = path[1:]

    return url + '/' + path
