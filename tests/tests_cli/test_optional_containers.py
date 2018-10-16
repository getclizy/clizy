import sys
from typing import Tuple, List

import pytest

from clizy import run
from tests.utils import stdoutify, cli_print_dict


@pytest.mark.parametrize("type_hint, value, expected_output", [
    (Tuple[int, int], ['1', '2'], stdoutify(values=[1, 2])),
    (Tuple[str, str], ['a', 'b'], stdoutify(values=['a', 'b'])),
    (Tuple[int, ...], ['1', '2', '3', '4', '5', '6'], stdoutify(values=[1, 2, 3, 4, 5, 6])),
])
def test_tuple(monkeypatch, clizy_output, type_hint, value, expected_output):
    monkeypatch.setattr(sys, 'argv', ['run', '--values', *value])

    def func(*, values: type_hint):
        cli_print_dict(locals())

    with clizy_output:
        run(func)

    assert clizy_output.code == 0
    assert clizy_output.err == ''
    assert clizy_output.out == expected_output


@pytest.mark.parametrize("type_hint, value, expected_output", [
    (List[int], ['--values', '1', '--values', '2'], stdoutify(values=[1, 2])),
    (List[str], ['--values', 'a', '--values', 'b'], stdoutify(values=['a', 'b'])),
])
def test_list(monkeypatch, clizy_output, type_hint, value, expected_output):
    monkeypatch.setattr(sys, 'argv', ['run', *value])

    def func(*, values: type_hint):
        cli_print_dict(locals())

    with clizy_output:
        run(func)

    assert clizy_output.code == 0
    assert clizy_output.err == ''
    assert clizy_output.out == expected_output
