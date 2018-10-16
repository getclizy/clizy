from typing import Union, List, Callable


class _UndefinedType:
    def __bool__(self):
        return False

    def __repr__(self):
        return 'Undefined'


Undefined = _UndefinedType()


class Argument:
    def __init__(self, original_name, name, value, type, description, required):
        self.original_name = original_name
        self.name = name
        self.value = value
        self.type = type
        self.description = description
        self.required = required


class OptionalArgument(Argument):
    def __init__(self, original_name, name, short_name, value, type, description, required):
        super().__init__(original_name, name, value, type, description, required)

        self.short_name = short_name


class PositionalArgument(Argument):
    pass


class Command:
    def __init__(self, func: Callable, name: str, normalized_name: str, description: Union[str, None],
                 arguments: List[Argument], options: List[OptionalArgument]):
        if func is None:
            raise ValueError("func cannot be None")

        self.func = func
        self.original_name = name
        self.name = normalized_name
        self.description = description
        self.arguments = arguments
        self.options = options


class Interface:
    description: str
    command: Command
    subcommands: List[Command]
    selected_subcommands: List[str]

    def __init__(self, description, command, subcommands):
        if command is None:
            raise ValueError("command cannot be None")

        self.description = description
        self.command = command
        self.subcommands = subcommands
        self.selected_subcommands = []
