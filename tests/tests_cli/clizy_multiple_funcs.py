#!/usr/bin/env python
from typing import List
from clizy import run_funcs
from tests.tests_cli.utils import cli_print_dict


def one(args: List[int], flag: bool, optional_argument: int=123):
    cli_print_dict(locals())


def two(args: List[int], flag: bool, optional_argument: int=123):
    cli_print_dict(locals())


def three(args: List[int], flag: bool, optional_argument: int=123):
    cli_print_dict(locals())


if __name__ == '__main__':
    run_funcs(one, two, three)
