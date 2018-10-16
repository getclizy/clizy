import inspect
from inspect import signature, Parameter
from typing import Callable, List

from clizy.cli_structures import OptionalArgument, Undefined, Command, Interface, PositionalArgument

_IGNORED_ARG_NAMES = {'self', 'cls'}


def _replace_underscores_with_dashes(string: str):
    return string.lower().replace('_', '-')


def build_interface(obj) -> Interface:
    if inspect.isclass(obj):
        return _build_from_class(obj)

    if inspect.isfunction(obj):
        return _build_from_func(obj)

    if isinstance(obj, (list, tuple)):
        return _build_from_multiple_funcs(obj)

    # TODO: better error
    raise NotImplementedError


def _build_from_class(klass):
    command = _build_command_from_init(klass)
    subcommands = []

    names = dir(klass)

    for name in names:
        if name.startswith('_'):
            continue

        func = getattr(klass, name)
        if not inspect.isfunction(func):
            continue

        subcommand = _build_command_from_function(func)
        subcommands.append(subcommand)

    if not subcommands:
        # TODO: better error
        raise Exception

    return Interface(inspect.getdoc(klass), command, subcommands)


def _build_from_func(func):
    command = _build_command_from_function(func)
    return Interface(inspect.getdoc(func), command, [])


def _build_from_multiple_funcs(funcs: List[Callable]):
    # This creates a fake class to be passed to _build_from_class
    class Dummy:
        pass

    for func in funcs:
        setattr(Dummy, func.__name__, staticmethod(func))

    return _build_from_class(Dummy)


def _build_command_from_init(klass):
    name = klass.__name__
    normalized_name = _replace_underscores_with_dashes(name)

    command = Command(klass, name, normalized_name, None, [], [])

    # This is a class actually, so let's take __init__ docstrings.
    # Note inspect.signature somewhere above returns what we expect.
    func_init = getattr(klass, '__init__')
    is_default_init = func_init is object.__init__
    if not is_default_init:
        command.description = inspect.getdoc(func_init)
        init_signature = signature(klass.__init__)
        _set_command_args_from_signature(command, init_signature)

    return command


def _build_command_from_function(func: Callable) -> Command:
    name = func.__name__
    normalized_name = _replace_underscores_with_dashes(name)
    command = Command(func, name, normalized_name, None, [], [])

    description = inspect.getdoc(func)
    command.description = description

    func_signature = signature(func)
    _set_command_args_from_signature(command, func_signature)

    return command


def _set_command_args_from_signature(command: Command, func_signature):
    options = []
    arguments = []

    param: Parameter
    for param in func_signature.parameters.values():
        original_name = param.name

        if original_name in _IGNORED_ARG_NAMES:
            continue

        name = _replace_underscores_with_dashes(original_name)
        expected_type = param.annotation
        required = False

        default = param.default

        if default is Parameter.empty:
            default = Undefined
            required = True

        if expected_type == Parameter.empty:
            expected_type = Undefined

        if param.kind is Parameter.KEYWORD_ONLY:
            option = OptionalArgument(original_name, name, None, default, expected_type, None, required)
            options.append(option)

        else:
            argument = PositionalArgument(original_name, name, default, expected_type, None, required)
            arguments.append(argument)

    command.options = options
    command.arguments = arguments
