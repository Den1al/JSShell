from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('mode', help='which mode to start', choices=['web', 'shell'])


def handle_web():
    from web import start_api_server
    start_api_server()


def handle_shell():
    from shell import start_shell
    start_shell()


if __name__ == '__main__':
    args = parser.parse_args()

    dict(
        web=handle_web,
        shell=handle_shell
    ).get(args.mode)()
