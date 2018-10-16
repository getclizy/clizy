from typing import Union, Callable, ClassVar

from clizy.context import Context


DEFAULT_CONTEXT = Context()


def run(obj, *, context: Context=DEFAULT_CONTEXT):
    interface = context.build_interface(obj)

    for filter in context.pipeline:
        filter(interface)

    context.execute(interface)
