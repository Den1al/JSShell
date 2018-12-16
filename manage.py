from argparse import ArgumentParser
from web import start_api_server
from shell import start_shell

parser = ArgumentParser()
parser.add_argument('mode', help='which mode to start', choices=['web', 'shell'])


if __name__ == '__main__':
    args = parser.parse_args()

    dict(
        web=start_api_server,
        shell=start_shell
    ).get(args.mode)()
