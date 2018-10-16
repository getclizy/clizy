from typing import List

import pytest

from clizy.cli_structures import Argument, Undefined, Interface, Command
from clizy.type_deducer import deduce_types


def dummy():
    pass


@pytest.mark.parametrize("value,type,expected_value,expected_type", [
    (Undefined, Undefined, Undefined, str),
    (Undefined, list, Undefined, List[str]),
    (Undefined, List, Undefined, List[str]),
    (1337, Undefined, 1337, int),
    (False, Undefined, False, bool),
    (Undefined, bool, False, bool),
])
def test_deduce_types(value, type, expected_value, expected_type):
    argument = Argument(None, None, value, type, None, None)

    interface = Interface(
        "", Command(dummy, None, None, None, [argument], []), []
    )

    deduce_types(interface)

    assert argument.value == expected_value
    assert argument.type == expected_type
