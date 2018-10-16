from itertools import chain
from typing import List, Tuple

from clizy.cli_structures import Interface, Argument, Undefined, PositionalArgument

_TYPE_CONVERSION_TABLE = {
    list: List[str],
    List: List[str],
}


def deduce_types(interface: Interface):
    for command in chain([interface.command], interface.subcommands):
        for argument in chain(command.arguments, command.options):
            _deduce_type(argument)


def _deduce_type(argument: Argument):
    if argument.type is Undefined:
        if argument.value in (Undefined, None):
            argument.type = str
        else:
            argument.type = type(argument.value)

    argument.type = _TYPE_CONVERSION_TABLE.get(argument.type, argument.type)

    if argument.type is bool:
        # with verbose=True and --verbose, verbose=False? That makes no sense
        if argument.value is True:
            # TODO: better error
            raise Exception("True is not supported")
        # do bool positional arguments make any sense?
        if isinstance(argument, PositionalArgument):
            # TODO: better error
            raise Exception("bool is not supported for positional arguments")
        if argument.value is Undefined:
            argument.value = False
