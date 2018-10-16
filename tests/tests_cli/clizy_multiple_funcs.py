#!/usr/bin/env python
from typing import List
from tests.utils import cli_print_dict


class Application:
    def first(self, fargs: List[int], *, fflag=False, foptional_argument: int=123):
        cli_print_dict(locals())

    def second(self, sargs: List[int], *, sflag=False, soptional_argument: int=123):
        cli_print_dict(locals())

    def third(self, targs: List[int], *, tflag=False, toptional_argument: int=123):
        cli_print_dict(locals())
