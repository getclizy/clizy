from os.path import dirname, join

from clizy import run, run_funcs
from tests.utils import run_in_process, stdoutify
from tests.tests_cli.clizy_multiple_funcs import first, second, third
from tests.tests_cli.clizy_one_func import func, func_with_optional_list, func_with_optional_args

ONE_FUNC = ("python", join(dirname(__file__), "clizy_one_func.py"))
MULTIPLE_FUNC = ("python", join(dirname(__file__), "./clizy_multiple_funcs.py"))


def test_one_func_valid_one_positional_argument():
    result = run_in_process(run, func, argv=["1"])
    assert result.returncode == 0
    assert result.stdout == stdoutify(args=[1], flag=False, optional_argument=123)


def test_one_func_valid_multiple_positional_arguments():
    result = run_in_process(run, func, argv=["1", "2", "3"])
    assert result.returncode == 0
    assert result.stdout == stdoutify(args=[1, 2, 3], flag=False, optional_argument=123)


def test_one_func_optional_provided():
    result = run_in_process(run, func, argv=["--optional-argument", "333", "1", "2"])
    assert result.returncode == 0
    assert result.stdout == stdoutify(args=[1, 2], flag=False, optional_argument=333)


def test_one_func_flag_provided():
    result = run_in_process(run, func, argv=["--flag", "1", "2"])
    assert result.returncode == 0
    assert result.stdout == stdoutify(args=[1, 2], flag=True, optional_argument=123)


def test_one_func_positional_arguments_not_provided():
    result = run_in_process(run, func, argv=[])
    assert result.returncode == 2


def test_one_func_positional_arguments_have_unexpected_type():
    result = run_in_process(run, func, argv=["asd"])
    assert result.returncode == 2


def test_one_func_optional_argument_have_unexpected_type():
    result = run_in_process(run, func, argv=["--optional-argument", "asd", "1", "2"])
    assert result.returncode == 2


def test_multiple_funcs_optional_provided():
    result = run_in_process(run_funcs, first, second, third, argv=["first", "--foptional-argument", "333", "1", "2"])
    assert result.returncode == 0
    assert result.stdout == stdoutify(fargs=[1, 2], fflag=False, foptional_argument=333)


def test_func_with_optional_list():
    result = run_in_process(run, func_with_optional_list, argv=["xxx", "--items", "333", "1", "2"])
    assert result.returncode == 0
    assert result.stdout == stdoutify(arg="xxx", items=[333, 1, 2])


def test_func_with_optional_args():
    result = run_in_process(run, func_with_optional_args, argv=["x1", "x2", "--option1", "o"])
    assert result.returncode == 0
    assert result.stdout == stdoutify(arg1='x1', arg2='x2', arg3=None, option1='o')
