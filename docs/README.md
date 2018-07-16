![clizy](https://media.githubusercontent.com/media/prokopst/clizy/master/docs/clizy.gif)

Command-line interface creation for lazy people using type hints.

## Quickstart

This code snippet:

```python
# ls.py
def ls(filename, *, long=False, all=False, human_readable=False, limit: int=None):
    """
    Fake command for listing.

    :param filename: filename, what else did you expect?
    :param long: long listing or something
    :param all: all, like including hidden files dude
    :param human_readable: show human readable stats
    :param limit: limit the number of files printed
    """
    ...
```

generates this command line interface:

```console
$ python ls.py --help
usage: ls [-h] [-l] [-a] [-H] [-L LIMIT] filename

Fake command for listing.

positional arguments:
  filename              filename, what else did you expect?

optional arguments:
  -h, --help            show this help message and exit
  -l, --long            long listing or something
  -a, --all             all, like including hidden files dude
  -H, --human-readable  show human readable stats
  -L LIMIT, --limit LIMIT
                        limit the number of files printed
```

Clizy simplifies command line interface creation by using things we all use, know and love -
arguments names, default values, docstrings and type hints - without unnecessary complexities
and overwhelming documentation.

Interested? See [docs](docs.md) and [comparison](comparison.md) with other libraries.
