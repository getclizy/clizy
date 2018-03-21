# clizy

Command-line interface creation for lazy people using `typing`.

## Quickstart

```python
# ls.py
from clizy import run


def ls(filename, long: bool, all: bool, human_readable: bool, limit: int=None):
    print(locals())


if __name__ == '__main__':
    run(ls)
```

When you call the script with '--help':

```console
$ python ls.py --help
usage: ls [-h] [-l] [-a] [-H] [-L LIMIT] filename

positional arguments:
  filename

optional arguments:
  -h, --help            show this help message and exit
  -l, --long
  -a, --all
  -H, --human_readable
  -L LIMIT, --limit LIMIT
```

## Why

The idea behind the library is that thanks the `typing` module it's possible to create
a non-complex command-line interface for function without too big effort.

## Todo

* support `typing.List[T]` and `list` for both optional and positional arguments
* parse docstring to get description
* optionally parse dostring format reST types and params description 
