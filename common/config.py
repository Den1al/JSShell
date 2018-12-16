import json
from typing import Dict, List


def read_config() -> Dict:
    """ Returns the parsed configuration file from disk """

    with open('resources/config.json', 'r') as f:
        return json.load(f)


def read_pre_flight() -> List:
    """ Returns the parsed pre-flight scripts file from disk """

    with open('resources/preflight.json', 'r') as f:
        return json.load(f)
