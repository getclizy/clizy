from typing import List

import pytest

from clizy.args_parser import parse_sys_arguments
from clizy.cli_structures import Interface, Command, Argument, Undefined, OptionalArgument


def dummy():
    pass


@pytest.mark.parametrize("default,type,value,expected_value", [
    (123, int, ["1337"], 1337),
    (Undefined, List[float], ["1337", "1", "2"], [1337.0, 1.0, 2.0]),
    (123, int, ["1337"], 1337),
])
def test_parse_sys_args(default, type, value, expected_value):
    arg = Argument('arg', 'arg', default, type, "whatever", False)
    interface = Interface("interface", Command(dummy, 'dummy', 'dummy', "", [arg], []), [])

    parse_sys_arguments(interface, value)

    assert arg.value == expected_value


@pytest.mark.parametrize("default,type,value,expected_value", [
    (123, int, ["--arg", "1337"], 1337),
    (Undefined, List[float], ["--arg", "1337", "1", "2"], [1337.0, 1.0, 2.0]),
    (True, bool, ["--arg"], True),
    (False, bool, ["--arg"], True),
    (False, bool, [], False),
])
def test_parse_sys_args_options(default, type, value, expected_value):
    option = OptionalArgument('arg', 'arg', 'a', default, type, "whatever", False)
    interface = Interface("interface", Command(dummy, 'dummy', 'dummy', "", [], [option]), [])

    parse_sys_arguments(interface, value)

    assert option.value == expected_value
