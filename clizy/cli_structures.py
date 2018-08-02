from typing import Dict, Union

Undefined = object()


class Option:
    def __init__(self, original_name, name, short_name, default, type, is_container, description):
        self.original_name = original_name
        self.name = name
        self.short_name = short_name
        self.default = default
        self.type = type
        self.is_container = is_container
        self.description = description


class Argument:
    def __init__(self, name, type, is_container, default, description):
        self.name = name
        self.type = type
        self.default = default
        self.is_container = is_container
        self.description = description


class Interface:
    def __init__(self, name: str, description: Union[str, None], arguments: Dict[str, Argument], options: Dict[str, Option], func):
        self.name = name
        self.description = description
        self.arguments = arguments
        self.options = options
        self.func = func
