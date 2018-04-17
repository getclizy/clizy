from io import StringIO
import re

from clizy.cli_structures import Interface


def simple_docstring_processor(docstring, interface: Interface):
    interface.description = docstring


SPHNIX_PARAM = re.compile('^:param (?P<name>[^:]+):[ ]+(?P<description>.*)$')


def _process_match(match, interface):
    name = match.group('name')
    description = match.group('description')

    if not description:
        return

    argument = interface.arguments.get(name, None)
    if argument:
        argument.description = description
        return

    option = interface.options.get(name, None)
    if option:
        option.description = description
        return


def sphinx_docstring_processor(docstring: str, interface: Interface):
    interface_description_lines = []

    docstring_stream = StringIO(docstring)

    for line in docstring_stream:
        match = SPHNIX_PARAM.match(line)
        if match:
            _process_match(match, interface)
            break

        interface_description_lines.append(line)

    for line in StringIO(docstring):
        match = SPHNIX_PARAM.match(line)
        if match:
            _process_match(match, interface)

    if interface_description_lines:
        interface.description = '\n'.join(interface_description_lines)
