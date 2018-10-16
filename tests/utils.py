from multiprocessing import Process, Queue
from queue import Empty
from typing import NamedTuple


def stdoutify(**kwargs):
    # TODO: why the hell it works on Windows with '\n' instead of os.linesep ('\r\n')?
    return dict_as_string_ordered(kwargs) + '\n'


class Output(NamedTuple):
    returncode: int
    stdout: str
    stderr: str


def dict_as_string_ordered(dictionary):
    return '{' + ", ".join(f"{repr(key)}: {repr(value)}" for key, value in sorted(dictionary.items())) + '}'


def cli_print_dict(dictionary):
    dictionary.pop('self', None)
    dictionary.pop('cls', None)
    string = dict_as_string_ordered(dictionary)
    print(string)
