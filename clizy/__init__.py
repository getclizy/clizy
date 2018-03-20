from argparse import ArgumentParser
from inspect import signature, Parameter


_Empty = object()


def _normalize_string(string: str):
    return string.replace('_', '-')


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
            dashed_name = _normalize_string(self.name)
            args.append(f'--{dashed_name}')

            kwargs['default'] = self.default

        if self.type is not _Empty:
            kwargs['type'] = self.type

        # short_option = None
        # for char in chain(name, (c.upper() for c in name)):
        #     if char in used_short_options:
        #         continue
        #
        #     short_option = char

        self._parser.add_argument(*args, **kwargs)


class Clizy:
    def __init__(self):
        pass

    def _prepare_function(self, parser: ArgumentParser, func):
        func_signature = signature(func)
        param: Parameter

        for param in func_signature.parameters:
            argument_builder = ArgParseArgumentBuilder(parser)

            argument_builder.name = param.name

            default = param.default
            if default is not Parameter.empty:
                argument_builder.default = default

            annotation = param.annotation
            if annotation == Parameter.empty:
                argument_builder.type = annotation

            argument_builder.build()

    def run(self, *funcs):
        parser = ArgumentParser()

        if len(funcs) > 1:
            subparsers = parser.add_subparsers()
            for func in funcs:
                subparser_name = _normalize_string(func.__name__)
                subparser = subparsers.add_parser(subparser_name)
                self._prepare_function(subparser, func)
        else:
            func = funcs[0]
            self._prepare_function(parser, func)
