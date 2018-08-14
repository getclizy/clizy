from argparse import ArgumentParser
from inspect import signature, Parameter, cleandoc

from itertools import chain
from typing import List, Iterable, Callable, Union

from clizy._cli_structures import _Option, _Argument, _Interface, _Undefined
from clizy.docstring_processors import sphinx_docstring_processor


def _replace_underscores_with_dashes(string: str):
    return string.replace('_', '-')


class ClizyError(Exception):
    pass


class UnsupportedTypeError(ClizyError):
    pass


class _InterfaceBuilder:
    _SUPPORTED_TYPES = {int, str, bool, float}
    _SUPPORTED_COMPLEX_TYPES = {list, List[int], List[float], List[str]}

    def __init__(self, docstring_processor):
        self._docstring_processor = docstring_processor

    def _assign_short_names(self, options):
        used_letters = {'h', '-'}

        for option in options:
            for letter in chain.from_iterable(zip(option.name, option.name.upper())):
                if letter not in used_letters:
                    used_letters.add(letter)
                    option.short_name = letter
                    break

            if not option.short_name:
                raise Exception

    def _process_docstring(self, docstring, interface: _Interface):
        if docstring is None:
            return

        cleaned_docstring = cleandoc(docstring)
        return self._docstring_processor(cleaned_docstring, interface)

    def build(self, func: Callable):
        options = {}
        arguments = {}

        func_signature = signature(func)
        param: Parameter

        for param in func_signature.parameters.values():
            original_name = param.name
            name = _replace_underscores_with_dashes(original_name)
            expected_type = param.annotation

            default = param.default

            if default is Parameter.empty:
                default = _Undefined

            if expected_type is list:
                expected_type = List[str]

            if isinstance(default, bool) and expected_type is Parameter.empty:
                expected_type = bool

            if expected_type == Parameter.empty:
                expected_type = str

            is_container = expected_type in self._SUPPORTED_COMPLEX_TYPES

            if expected_type not in self._SUPPORTED_TYPES and not is_container:
                raise UnsupportedTypeError(expected_type)

            if param.kind is Parameter.KEYWORD_ONLY:
                option = _Option(original_name, name, None, default, expected_type, is_container, None)
                options[original_name] = option

            else:
                argument = _Argument(name, expected_type, is_container, default, None)
                arguments[original_name] = argument

        self._assign_short_names(options.values())

        func_name = _replace_underscores_with_dashes(func.__name__)

        interface = _Interface(func_name, None, arguments, options, func)
        self._process_docstring(func.__doc__, interface)

        return interface

    def build_multiple(self, funcs):
        interfaces = []
        for func in funcs:
            interface = self.build(func)
            interfaces.append(interface)
        return interfaces


class _InterfaceExecutor:
    def __init__(self):
        pass

    def execute(self, interface: _Interface, args=None):
        parser = ArgumentParser()
        self._setup_parser(parser, interface)

        arguments = parser.parse_args(args)
        kwargs = vars(arguments)

        return interface.func(**kwargs)

    def execute_multiple(self, interfaces: List[_Interface], args=None):
        parser = ArgumentParser()
        subparsers = parser.add_subparsers(dest='clizy_subparser_name')

        for interface in interfaces:
            subparser_name = interface.name
            subparser = subparsers.add_parser(subparser_name)

            self._setup_parser(subparser, interface)

        arguments = parser.parse_args(args)
        kwargs = vars(arguments)
        func_name = kwargs.pop('clizy_subparser_name')

        for interface in interfaces:
            if interface.name == func_name:
                interface.func(**kwargs)

    def _setup_arguments(self, parser: ArgumentParser, interface: _Interface):
        complex_type_count = 0
        for argument in interface.arguments.values():
            kwargs = {
                # dest is first argument for positional arguments, can't be set
                # 'dest': argument.original_name
            }

            argument_type = argument.type
            if argument.is_container:
                if complex_type_count > 1:
                    raise RuntimeError("Cannot handle multiple arguments of List type")

                complex_type_count += 1

                # TODO: make it nicer and less error prone
                argument_type = argument_type.__args__[0]
                if argument.default is None:
                    kwargs['nargs'] = '*'
                else:
                    kwargs['nargs'] = '+'
            else:
                if argument.default is not _Undefined:
                    kwargs['default'] = argument.default
                    kwargs['nargs'] = '?'

            kwargs['type'] = argument_type

            if argument.description:
                kwargs['help'] = argument.description

            parser.add_argument(
                argument.name, **kwargs
            )

    def _setup_options(self, parser: ArgumentParser, interface: _Interface):
        for option in interface.options.values():
            kwargs = {
                'dest': option.original_name
            }

            option_type = option.type

            if option.is_container:
                kwargs['nargs'] = '*'
                # TODO: make it nicer and less error prone
                option_type = option.type.__args__[0]
                kwargs['type'] = option_type
            else:
                if option_type is bool:
                    kwargs['action'] = 'store_true'
                else:
                    kwargs['type'] = option_type

            if option.description:
                kwargs['help'] = option.description

            if option.default is _Undefined:
                # it's very weird to have an option required, but.. whatever
                kwargs['required'] = True
            else:
                kwargs['default'] = option.default

            parser.add_argument(
                f'-{option.short_name}', f'--{option.name}', **kwargs
            )

    def _setup_parser(self, parser: ArgumentParser, interface: _Interface):
        self._setup_options(parser, interface)
        self._setup_arguments(parser, interface)


def run_func(func: Callable, args=None):
    docstring_processor = sphinx_docstring_processor
    interface_builder = _InterfaceBuilder(docstring_processor)
    interface_executor = _InterfaceExecutor()

    interface = interface_builder.build(func)

    return interface_executor.execute(interface, args)


def run_funcs(funcs: Iterable, args=None):
    docstring_processor = sphinx_docstring_processor
    interface_builder = _InterfaceBuilder(docstring_processor)
    interface_executor = _InterfaceExecutor()

    interfaces = interface_builder.build_multiple(funcs)

    return interface_executor.execute_multiple(interfaces, args)


def run(funcs: Union[Iterable, Callable], args=None):
    if isinstance(funcs, Iterable):
        return run_funcs(funcs, args=args)
    else:
        return run_func(funcs, args=args)
