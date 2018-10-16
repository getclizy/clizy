from argparse import ArgumentParser
from itertools import chain
from typing import List, Tuple

from clizy.cli_structures import Interface, Command, Undefined, Argument

_SUBPARSER_TOKEN = 'clizy_subparser_name'


# TODO: the whole type handling is far from ideal. Converter's API has to be introduced.


def parse_sys_arguments(interface: Interface, args=None):
    command = interface.command
    subcommands = interface.subcommands

    parser = ArgumentParser()
    _setup_parser(parser, interface.command)

    if subcommands:
        # TODO: rename clizy_subparser_name to _clizy_subparser_name if it's allowed
        # it sounds bit safer
        subparsers = parser.add_subparsers(dest=_SUBPARSER_TOKEN)

        for subcommand in subcommands:
            subparser_name = subcommand.name
            subparser = subparsers.add_parser(subparser_name)

            _setup_parser(subparser, subcommand)

    # TODO: support multiple commands
    arguments = parser.parse_args(args)
    kwarguments = vars(arguments)
    selected_subcommand_name = kwarguments.pop(_SUBPARSER_TOKEN, None)

    _assign_values_from_kwarguments(command, kwarguments)

    if selected_subcommand_name is not None:
        # O(n), but given the fact that number of subcommands is usually very low...
        # ¯\_(ツ)_/¯
        found = False
        for subcommand in subcommands:
            subcommand_name = subcommand.name
            if subcommand_name == selected_subcommand_name:
                interface.selected_subcommands.append(subcommand_name)
                _assign_values_from_kwarguments(subcommand, kwarguments)
                found = True
                break

        # No, I'm not going to use hard to understand else after for, it sucks!
        if not found:
            # TODO: error message + exception class
            raise Exception

    return interface


def _assign_values_from_kwarguments(command, kwargs):
    for argument in chain(command.arguments, command.options):
        value = kwargs.pop(argument.original_name, Undefined)
        if value is not Undefined:
            argument.value = value


def _is_tuple(obj):
    try:
        return issubclass(obj, Tuple)
    # Handle: TypeError: issubclass() arg 1 must be a class
    except TypeError:
        return False


def _is_list(obj):
    try:
        return issubclass(obj, List)
    # Handle: TypeError: issubclass() arg 1 must be a class
    except TypeError:
        return False


def _setup_positional_arguments(parser: ArgumentParser, command: Command):
    complex_type_count = 0
    argument: Argument
    for argument in command.arguments:
        kwargs = {
            # dest is first argument for positional arguments, can't be set
            # 'dest': argument.original_name
        }

        argument_type = argument.type

        if _is_list(argument_type):
            if complex_type_count > 1:
                raise RuntimeError("Cannot handle multiple arguments of List type")

            complex_type_count += 1

            # TODO: make it nicer and less error prone
            argument_type = argument_type.__args__[0]
            if argument.value is Undefined:
                kwargs['nargs'] = '+'
            else:
                kwargs['nargs'] = '*'
                kwargs['default'] = argument.value

        elif _is_tuple(argument_type):
            tuple_args = getattr(argument_type, '__args__', (str, ...))
            count = len(tuple_args)
            if count == 2 and tuple_args[1] is ...:
                if argument.value is not Undefined:
                    kwargs['nargs'] = '*'
                else:
                    kwargs['nargs'] = '+'
            else:
                kwargs['nargs'] = count

            if argument.value is not Undefined:
                kwargs['default'] = argument.value
                kwargs['required'] = False

            # TODO: handle different tuple types
            argument_type = tuple_args[0]
        else:
            if argument.value is not Undefined:
                kwargs['default'] = argument.value
                kwargs['nargs'] = '?'

        kwargs['type'] = argument_type

        if argument.description:
            kwargs['help'] = argument.description

        parser.add_argument(
            argument.original_name, **kwargs
        )


def _setup_optional_arguments(parser: ArgumentParser, command: Command):
    for option in command.options:
        kwargs = {
            'dest': option.original_name
        }

        option_type = option.type

        if _is_list(option_type):
            kwargs['action'] = 'append'
            # TODO: make it nicer and less error prone
            option_type = option_type.__args__[0]
            kwargs['type'] = option_type
        elif _is_tuple(option_type):
            tuple_args = getattr(option_type, '__args__', (str, ...))

            if len(tuple_args) == 2 and tuple_args[1] is ...:
                kwargs['nargs'] = '+'
            else:
                kwargs['nargs'] = len(tuple_args)
            # TODO: make it nicer and less error prone
            option_type = tuple_args[0]
            kwargs['type'] = option_type
        else:
            if option_type is bool:
                kwargs['action'] = 'store_true'
            else:
                kwargs['type'] = option_type

        if option.description:
            kwargs['help'] = option.description

        if option.value is Undefined:
            # it's very weird to have an option required, but.. whatever
            kwargs['required'] = True
        else:
            kwargs['default'] = option.value

        parser.add_argument(
            f'-{option.short_name}', f'--{option.name}', **kwargs
        )


def _setup_parser(parser: ArgumentParser, command: Command):
    _setup_optional_arguments(parser, command)
    _setup_positional_arguments(parser, command)


parse_arguments = parse_sys_arguments
