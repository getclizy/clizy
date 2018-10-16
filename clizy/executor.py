from itertools import chain

from clizy.cli_structures import Interface, Undefined


def _call(func, command):
    kwargs = {}
    for argument in chain(command.arguments, command.options):
        if argument.value is not Undefined:
            kwargs[argument.original_name] = argument.value

    return func(**kwargs)


def execute_interface(interface: Interface):
    command = interface.command

    func = command.func

    result = _call(func, command)

    selected_commands = set(interface.selected_subcommands)
    subcommands = interface.subcommands

    for subcommand in subcommands:
        if subcommand.name not in selected_commands:
            continue

        func = getattr(result, subcommand.original_name)
        _call(func, subcommand)

    return result
