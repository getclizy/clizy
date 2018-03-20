from argparse import ArgumentParser
from inspect import signature, Parameter
import sys
from itertools import chain


_Empty = object()


class ArgParseArgumentBuilder:
    def __init__(self, parser: ArgumentParser):
        self._parser = parser

        self.type = _Empty
        self.default = _Empty
        self.name: str = _Empty

    def build(self):
        args = []
        kwargs = {}

        if self.default is not _Empty:
            dashed_name = self.name.replace('_', '-')
            args.append(f'--{dashed_name}')

        if self.type is not _Empty:
            kwargs['type'] = self.type

        self._parser.add_argument(*args, **kwargs)


class Clizy:
    def __init__(self):
        self._argparse = ArgumentParser()

    def add_func(self, func):
        func_signature = signature(func)

        used_short_options = set()

        for param in func_signature.parameters:
            param: Parameter

            name: str = param.name
            annotation = param.annotation
            default = param.default

            if annotation == Parameter.empty:
                param_type = str
            else:
                param_type = annotation

            # argument
            if default == Parameter.empty:
                short_option = None
                for char in chain(name, (c.upper() for c in name)):
                    if char in used_short_options:
                        continue

                    short_option = char

    def run(self, argv=None):
        if not argv:
            argv = sys.argv

        self._argparse.parse_args(argv)

