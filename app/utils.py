import datetime
import jsbeautifier
import json


def get_date():
    """ Gets the current time """
    return datetime.datetime.now()


def datetime_to_text(dt):
    """ Formats a datetime object to a human readable time """
    return dt.strftime('%H:%M:%S %Y-%m-%d')


def dict_to_beautified_json(d):
    """ Serializes & Beautifies a dictionary"""
    return jsbeautifier.beautify(json.dumps(d))