from os.path import dirname, join

from tests.tests_cli.utils import stdoutify, subprocess_run_wrapper


ONE_FUNC = ("python", join(dirname(__file__), "clizy_one_func.py"))
MULTIPLE_FUNC = ("python", join(dirname(__file__), "./clizy_multiple_funcs.py"))


def test_one_func_valid_one_positional_argument():
    result = subprocess_run_wrapper(*ONE_FUNC, "1")
    assert result.returncode == 0
    assert result.stdout == stdoutify(args=[1], flag=False, optional_argument=123)


def test_one_func_valid_multiple_positional_arguments():
    result = subprocess_run_wrapper(*ONE_FUNC, "1", "2", "3")
    assert result.returncode == 0
    assert result.stdout == stdoutify(args=[1, 2, 3], flag=False, optional_argument=123)


def test_one_func_optional_provided():
    result = subprocess_run_wrapper(*ONE_FUNC, "--optional-argument", "333", "1", "2")
    assert result.returncode == 0
    assert result.stdout == stdoutify(args=[1, 2], flag=False, optional_argument=333)


def test_one_func_flag_provided():
    result = subprocess_run_wrapper(*ONE_FUNC, "--flag", "1", "2")
    assert result.returncode == 0
    assert result.stdout == stdoutify(args=[1, 2], flag=True, optional_argument=123)


def test_one_func_positional_arguments_not_provided():
    result = subprocess_run_wrapper(*ONE_FUNC)
    assert result.returncode == 2


def test_one_func_positional_arguments_have_unexpected_type():
    result = subprocess_run_wrapper(*ONE_FUNC, "asd")
    assert result.returncode == 2


def test_one_func_optional_argument_have_unexpected_type():
    result = subprocess_run_wrapper(*ONE_FUNC, "--optional-argument", "asd", "1", "2")
    assert result.returncode == 2


def test_multiple_funcs_optional_provided():
    result = subprocess_run_wrapper(*MULTIPLE_FUNC, "first", "--foptional-argument", "333", "1", "2")
    assert result.returncode == 0
    assert result.stdout == stdoutify(fargs=[1, 2], fflag=False, foptional_argument=333)
