from multiprocessing import Process, Queue
from queue import Empty
from typing import NamedTuple


def stdoutify(**kwargs):
    # TODO: why the hell it works on Windows with '\n' instead of os.linesep ('\r\n')?
    return dict_as_string_ordered(kwargs) + '\n'


class Output(NamedTuple):
    returncode: int
    stdout: str
    stderr: str


def target(function, args, kwargs, queue: Queue):
    import sys
    from io import StringIO

    stdout_stream = StringIO()
    sys.stdout = stdout_stream

    stderr_stream = StringIO()
    sys.stderr = stderr_stream

    try:
        function(*args, **kwargs)
    except SystemExit:
        queue.put(stdout_stream.getvalue())
        queue.put(stderr_stream.getvalue())
        queue.put(None)
        raise
    except BaseException as e:
        queue.put(stdout_stream.getvalue())
        queue.put(stderr_stream.getvalue())
        queue.put(e)
    else:
        queue.put(stdout_stream.getvalue())
        queue.put(stderr_stream.getvalue())
        queue.put(None)
    finally:
        queue.close()


def run_in_process(func, *args, **kwargs):
    """
    Wrapper for multiprocessing.
    """
    queue = Queue()

    process = Process(
        target=target, kwargs={
            'function': func, 'args': args, 'kwargs': kwargs,
            'queue': queue}
    )

    process.start()

    process.join()

    items = []

    while True:
        try:
            item = queue.get_nowait()
            items.append(item)
        except Empty:
            break

    queue.close()

    if len(items) != 3:
        raise RuntimeError("Well, that's unexpected.")

    exc: Exception
    stdout, stderr, exc = items

    if exc:
        raise exc.with_traceback(exc.__traceback__)

    return Output(process.exitcode, stdout, stderr)


def dict_as_string_ordered(dictionary):
    return '{' + ", ".join(f"{repr(key)}: {repr(value)}" for key, value in sorted(dictionary.items())) + '}'


def cli_print_dict(dictionary):
    string = dict_as_string_ordered(dictionary)
    print(string)
