import os
import subprocess
from typing import NamedTuple
from unittest.mock import patch

from io import StringIO


def dict_as_string_ordered(dictionary):
    return '{' + ", ".join(f"{repr(key)}: {repr(value)}" for key, value in sorted(dictionary.items())) + '}'


def stdoutify(**kwargs):
    # TODO: why the hell it works on Windows with '\n' instead of os.linesep ('\r\n')?
    return dict_as_string_ordered(kwargs) + '\n'


def cli_print_dict(dictionary):
    string = dict_as_string_ordered(dictionary)
    print(string)


def subprocess_run_wrapper(*args):
    return subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


class Output(NamedTuple):
    returncode: int
    stdout: str
    stderr: str


def run_clizy_wrapper(clizy_func, *args, **kwargs):
    code = 0
    stdout = StringIO()
    stderr = StringIO()
    with patch.multiple('sys', stdout=stdout, stderr=stderr):
        try:
            clizy_func(*args, **kwargs)
        except SystemExit as e:
            code = e.code

        return Output(code, stdout.getvalue(), stderr.getvalue())
