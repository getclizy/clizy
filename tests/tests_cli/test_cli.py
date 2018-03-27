from tests.tests_cli.utils import stdoutify, subprocess_run_wrapper


def test_x_stuff_valid_one_positional_argument():
    result = subprocess_run_wrapper("./clizy_one_func.py", "1")
    assert result.stdout == stdoutify(args=[1], flag=False, optional_argument=123)


def test_x_stuff_valid_multiple_positional_arguments():
    result = subprocess_run_wrapper("./clizy_one_func.py", "1", "2", "3")
    assert result.stdout == stdoutify(args=[1, 2, 3], flag=False, optional_argument=123)


def test_x_stuff_optional_provided():
    result = subprocess_run_wrapper("./clizy_one_func.py", "--optional-argument", "333", "1", "2")
    assert result.stdout == stdoutify(args=[1, 2], flag=False, optional_argument=333)


def test_x_stuff_flag_provided():
    result = subprocess_run_wrapper("./clizy_one_func.py", "--flag", "1", "2")
    assert result.stdout == stdoutify(args=[1, 2], flag=True, optional_argument=123)


def test_x_stuff_positional_arguments_not_provided():
    result = subprocess_run_wrapper("./clizy_one_func.py")
    assert result.returncode == 2


def test_x_stuff_positional_arguments_have_unexpected_type():
    result = subprocess_run_wrapper("./clizy_one_func.py", "asd")
    assert result.returncode == 2


def test_x_stuff_optional_argument_have_unexpected_type():
    result = subprocess_run_wrapper("./clizy_one_func.py", "--optional-argument", "asd", "1", "2")
    assert result.returncode == 2
