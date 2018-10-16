from clizy.args_parser import parse_arguments
from clizy.executor import execute_interface
from clizy.interface_builder import build_interface
from clizy.short_names_assigner import assign_short_names
from clizy.type_deducer import deduce_types


class Context:
    def __init__(self):
        self.build_interface = build_interface
        self.pipeline = [
            deduce_types,
            assign_short_names,
            parse_arguments,
        ]
        self.execute = execute_interface
        #self.overrides = {}

    def insert_after(self, *args, **kwargs):
        raise NotImplementedError

    def insert_before(self, *args, **kwargs):
        raise NotImplementedError

    def override(self, **kwargs):
        raise NotImplementedError
