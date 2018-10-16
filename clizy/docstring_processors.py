from io import StringIO
import re
from itertools import chain
from typing import NamedTuple, Dict

from clizy.cli_structures import Command, Interface


SPHNIX_PARAM = re.compile('^:param (?P<name>[^:]+):[ ]+(?P<description>.*)$')


def process_docstring(interface: Command):
    return interface


class _CommandDescription(NamedTuple):
    description: str
    arguments: Dict[str, str]


def _create_described_command_from_docstring(docstring):
    docstring_stream = StringIO(docstring)
    interface_description_lines = []
    described_arguments = {}

    match = None
    for line in docstring_stream:
        match = SPHNIX_PARAM.match(line)
        if match:
            break

        interface_description_lines.append(line)

    while match:
        name = match.group('name')
        description = match.group('description')

        described_arguments[name] = description

        match = None
        for line in docstring_stream:
            match = SPHNIX_PARAM.match(line)
            # TODO: additional lines and their indent
            if match:
                break

    description = ''
    if interface_description_lines:
        description = '\n'.join(interface_description_lines)

    return _CommandDescription(description, described_arguments)


def _process_command(command: Command):
    command_description = _create_described_command_from_docstring(command.description)
    arguments_descriptions = command_description.arguments

    for arg in chain(command.arguments, command.options):
        name = arg.original_name
        description = arguments_descriptions.pop(name, None)
        if description:
            arg.description = description

    # TODO: How to handle what's left in arguments_descriptions? Raise an exception?

    command.description = command_description.description


def sphinx_docstring_processor(interface: Interface):
    for command in chain(interface.command, interface.subcommands):
        _process_command(command)

    return interface
