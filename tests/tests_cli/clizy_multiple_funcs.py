#!/usr/bin/env python
from typing import List
from clizy import run_funcs
from tests.utils import cli_print_dict


def first(fargs: List[int], *, fflag=False, foptional_argument: int=123):
    cli_print_dict(locals())


def second(sargs: List[int], *, sflag=False, soptional_argument: int=123):
    cli_print_dict(locals())


def third(targs: List[int], *, tflag=False, toptional_argument: int=123):
    cli_print_dict(locals())


if __name__ == '__main__':
    run_funcs(first, second, third)
