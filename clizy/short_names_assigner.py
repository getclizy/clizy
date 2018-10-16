from itertools import chain
from typing import List
import copy

from clizy.cli_structures import Interface, OptionalArgument


def _assign_short_names(options: List[OptionalArgument], used_letters):
    if not options:
        return

    for option in options:
        for letter in chain.from_iterable(zip(option.name, option.name.upper())):
            if letter not in used_letters:
                used_letters.add(letter)
                option.short_name = letter
                break

        if not option.short_name:
            raise Exception


def assign_short_names(interface: Interface) -> Interface:
    used_letters = {'h', '-', '_'}

    command = interface.command
    subcommands = interface.subcommands

    _assign_short_names(command.options, used_letters)

    if subcommands:
        for subcommand in subcommands:
            if subcommand.options:
                used_letters_copy = copy.copy(used_letters)
                _assign_short_names(subcommand.options, used_letters_copy)

    return interface
