![clizy](https://media.githubusercontent.com/media/prokopst/clizy/master/docs/clizy.gif)

Command-line interface creation for lazy people using type hints.

## Quickstart

This code snippet:

```python
# ls.py
import clizy

def ls(filename, long: bool, all: bool, human_readable: bool, limit: int=None):
    """
    Fake command for listing.
    """
    ...

if __name__ == '__main__':
    clizy.run(ls)
```

generates this command line interface:

```console
$ python ls.py --help
usage: ls [-h] [-l] [-a] [-H] [-L LIMIT] filename

Fake command for listing.

positional arguments:
  filename

optional arguments:
  -h, --help            show this help message and exit
  -l, --long
  -a, --all
  -H, --human-readable
  -L LIMIT, --limit LIMIT
```

Clizy simplifies command line interface creation by using things we all use, know and love -
arguments names, default values, docstrings and type hints - without unnecessary complexities
and overwhelming documentation.

Interested? See [docs](docs.md) and [comparison](comparison.md) with other libraries.
