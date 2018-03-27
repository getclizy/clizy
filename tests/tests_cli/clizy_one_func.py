#!/usr/bin/env python
from typing import List
from clizy import run
from tests.tests_cli.utils import cli_print_dict


def func(args: List[int], flag: bool, optional_argument: int=123):
    cli_print_dict(locals())


if __name__ == '__main__':
    run(func)
