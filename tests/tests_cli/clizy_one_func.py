#!/usr/bin/env python
from typing import List
from clizy import run
from tests.utils import cli_print_dict


def func(args: List[int], *, flag=False, optional_argument: int=123):
    cli_print_dict(locals())


def func_with_optional_list(arg, *, items: List[int]=None):
    cli_print_dict(locals())


def func_with_optional_args(arg1, arg2, arg3=None, *, option1=None):
    cli_print_dict(locals())


if __name__ == '__main__':
    run(func)
