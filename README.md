# clizy

Command-line interface creation for lazy people using `typing`.

## Quickstart

```python
# ls.py
from clizy import run

def ls(filename, long: bool=False, all: bool=False, human_readable: bool=False):
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


## Todo

* support `typing.List[T]` and `list`
* parse docstring