"""

The structure of a plugin is as follows:

from cmd2 import with_argparser
from argparse import ArgumentParser

from shell import BasePlugin


class ExamplePlugin(BasePlugin):

    example_parser = ArgumentParser(description='...')

    @with_argparser(example_parser)
    def do_example(self, args):
        pass
"""

