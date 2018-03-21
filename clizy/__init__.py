from argparse import ArgumentParser
from inspect import signature, Parameter
from itertools import chain
from typing import NamedTuple, Any, List


def _replace_underscores_with_dashes(string: str):
    return string.replace('_', '-')


class Option:
    def __init__(self, name, short_name, default, type):
        self.name = name
        self.short_name = short_name
        self.default = default
        self.type = type


class Argument(NamedTuple):
    name: str
    type: Any


class Interface(NamedTuple):
    name: str
    arguments: List[Argument]
    options: List[Option]


class ClizyError(Exception):
    pass


class UnsupportedTypeError(ClizyError):
    pass


class Clizy:
    _UNSUPPORTED_TYPES = (int, str, bool, float)

    def _prepare_function(self, func):
        options = []
        arguments = []

        func_signature = signature(func)
        param: Parameter

        for param_name, param in func_signature.parameters.items():
            annotation = param.annotation

            default = param.default

            annotation_is_bool = annotation is bool
            default_is_empty = default is Parameter.empty

            if annotation_is_bool and default_is_empty:
                default = False
                default_is_empty = False

            if isinstance(default, bool) and annotation is Parameter.empty:
                annotation = bool

            if annotation == Parameter.empty:
                annotation = str

            if annotation not in self._UNSUPPORTED_TYPES:
                raise UnsupportedTypeError(annotation)

            if not default_is_empty:
                option = Option(param.name, None, default, annotation)
                options.append(option)

            else:
                argument = Argument(param.name, annotation)
                arguments.append(argument)

        self._assign_short_names(options)

        name = _replace_underscores_with_dashes(func.__name__)
        return Interface(name, arguments, options)

    def _setup_parser(self, parser: ArgumentParser, interface: Interface):
        for option in interface.options:
            kwargs = {
                'default': option.default
            }

            if option.type is bool:
                kwargs['action'] = 'store_true'
            else:
                kwargs['type'] = option.type

            parser.add_argument(
                f'-{option.short_name}', f'--{option.name}', **kwargs
            )

        for argument in interface.arguments:
            parser.add_argument(
                argument.name, type=argument.type
            )

    def _assign_short_names(self, options):
        used_letters = {'h'}

        for option in options:
            for letter in chain.from_iterable(zip(option.name, option.name.upper())):
                if letter not in used_letters:
                    used_letters.add(letter)
                    option.short_name = letter
                    break

            if not option.short_name:
                raise Exception

    def run(self, *funcs, argv):
        if len(funcs) > 1:
            parser = ArgumentParser()
            subparsers = parser.add_subparsers(dest='clizy_subparser_name')
            interfaces = []

            for func in funcs:
                interface = self._prepare_function(func)

                subparser_name = _replace_underscores_with_dashes(func.__name__)
                subparser = subparsers.add_parser(subparser_name)

                self._setup_parser(subparser, interface)
                interfaces.append(interface)

            arguments = parser.parse_args(argv)

            for func in funcs:
                if func.__name__ == arguments.clizy_subparser_name:
                    kwargs = vars(arguments)
                    kwargs.pop('clizy_subparser_name')

        else:
            func = funcs[0]

            interface = self._prepare_function(func)

            parser = ArgumentParser(prog=interface.name)
            self._setup_parser(parser, interface)

            arguments = parser.parse_args(argv)
            kwargs = vars(arguments)

            return func(**kwargs)


def run(*funcs, argv=None):
    return Clizy().run(*funcs, argv=argv)


if __name__ == '__main__':
    def ls(filename, long: bool, all: bool, human_readable: bool, limit: int=None):
        print(vars())

    run(ls, argv=['--help'])
    run(ls, argv=['--all', '-H', 'file.txt'])
    run(ls, argv=['-L=42', 'file.txt'])
