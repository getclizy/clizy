import sys

import pytest

from clizy import run
from tests.utils import stdoutify
from tests.tests_cli.clizy_multiple_funcs import Application
from tests.tests_cli.clizy_one_func import func, func_with_optional_list, func_with_optional_args


def test_one_func_valid_one_positional_argument(monkeypatch, clizy_output):
    monkeypatch.setattr(sys, 'argv', ["run", "1"])

    with clizy_output:
        run(func)

    assert clizy_output.code == 0
    assert clizy_output.out == stdoutify(args=[1], flag=False, optional_argument=123)
    assert clizy_output.err == ''


def test_one_func_valid_multiple_positional_arguments(monkeypatch, clizy_output):
    monkeypatch.setattr(sys, 'argv', ["func", "1", "2", "3"])

    with clizy_output:
        run(func)

    assert clizy_output.code == 0
    assert clizy_output.out == stdoutify(args=[1, 2, 3], flag=False, optional_argument=123)


def test_one_func_optional_provided(monkeypatch, clizy_output):
    monkeypatch.setattr(sys, 'argv', ["func", "--optional-argument", "333", "1", "2"])

    with clizy_output:
        run(func)

    assert clizy_output.code == 0
    assert clizy_output.out == stdoutify(args=[1, 2], flag=False, optional_argument=333)


def test_one_func_flag_provided(monkeypatch, clizy_output):
    monkeypatch.setattr(sys, 'argv', ["func", "--flag", "1", "2"])

    with clizy_output:
        run(func)

    assert clizy_output.code == 0
    assert clizy_output.out == stdoutify(args=[1, 2], flag=True, optional_argument=123)


def test_one_func_positional_arguments_not_provided(monkeypatch, clizy_output):
    monkeypatch.setattr(sys, 'argv', ["func"])

    with clizy_output:
        run(func)
    assert clizy_output.code == 2


def test_one_func_positional_arguments_have_unexpected_type(monkeypatch, clizy_output):
    monkeypatch.setattr(sys, 'argv', ["func", "asd"])

    with clizy_output:
        run(func)
    assert clizy_output.code == 2


def test_one_func_optional_argument_have_unexpected_type(monkeypatch, clizy_output):
    monkeypatch.setattr(sys, 'argv', ["func", "--optional-argument", "asd", "1", "2"])

    with clizy_output:
        run(func)
    assert clizy_output.code == 2


@pytest.mark.parametrize("args, expected_result", [
    (["func", "first", "--foptional-argument", "333", "1", "2"], stdoutify(fargs=[1, 2], fflag=False, foptional_argument=333)),
    (["func", "second", "--soptional-argument", "333", "1", "2"], stdoutify(sargs=[1, 2], sflag=False, soptional_argument=333)),
    (["func", "third", "--toptional-argument", "333", "1", "2"], stdoutify(targs=[1, 2], tflag=False, toptional_argument=333)),

])
def test_multiple_funcs_optional_provided(monkeypatch, clizy_output, args, expected_result):
    monkeypatch.setattr(sys, 'argv', args)

    with clizy_output:
        run(Application)
    assert clizy_output.code == 0
    assert clizy_output.out == expected_result


def test_func_with_optional_list(monkeypatch, clizy_output):
    monkeypatch.setattr(sys, 'argv', ["func", "xxx", "--items", "333", "1", "2"])

    with clizy_output:
        run(func_with_optional_list)
    assert clizy_output.code == 0
    assert clizy_output.out == stdoutify(arg="xxx", items=[333, 1, 2])


def test_func_with_optional_args(monkeypatch, clizy_output):
    monkeypatch.setattr(sys, 'argv', ["func", "x1", "x2", "--option1", "o"])

    with clizy_output:
        run(func_with_optional_args)
    assert clizy_output.code == 0
    assert clizy_output.out == stdoutify(arg1='x1', arg2='x2', arg3=None, option1='o')
