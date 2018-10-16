from typing import List, Any

from clizy.cli_structures import Undefined
from clizy.interface_builder import build_interface


def test_build_interface_builds_from_func():
    def this_is_function(argument_first, argument_second: List[int]=None, *,
                         option_first=1, option_second: str="second"):
        """
        This is docstring.
        """
        raise NotImplementedError

    interface = build_interface(this_is_function)

    assert interface.description == "This is docstring."

    command = interface.command
    assert command is not None
    assert command.func is this_is_function
    assert command.original_name == 'this_is_function'
    assert command.name == 'this-is-function'

    arguments = command.arguments
    assert arguments
    assert len(arguments) == 2

    argument_first = arguments[0]
    assert argument_first.name == "argument-first"
    assert argument_first.original_name == "argument_first"
    assert argument_first.value is Undefined
    assert argument_first.type is Undefined
    assert argument_first.description is None
    assert argument_first.required is True

    argument_second = arguments[1]
    assert argument_second.name == "argument-second"
    assert argument_second.original_name == "argument_second"
    assert argument_second.value is None
    assert argument_second.type is List[int]
    assert argument_second.description is None
    assert argument_second.required is False

    options = command.options
    assert options
    assert len(options) == 2

    option_first = options[0]
    assert option_first.name == "option-first"
    assert option_first.original_name == "option_first"
    assert option_first.short_name is None
    assert option_first.value is 1
    assert option_first.type is Undefined
    assert option_first.description is None
    assert option_first.required is False

    option_second = options[1]
    assert option_second.name == "option-second"
    assert option_second.original_name == "option_second"
    assert option_second.short_name is None
    assert option_second.value == "second"
    assert option_second.type is str
    assert option_second.description is None
    assert option_second.required is False


def test_build_interface_builds_from_empty_func():
    def empty_function():
        pass

    interface = build_interface(empty_function)

    assert interface.description is None
    assert not interface.subcommands

    command = interface.command
    assert command

    assert command.description is None
    assert command.original_name == 'empty_function'
    assert command.name == 'empty-function'
    assert command.func is empty_function
    assert not command.arguments
    assert not command.options
