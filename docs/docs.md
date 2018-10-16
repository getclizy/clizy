# clizy: CLI for lazy people

Clizy is a Python library for creation of effortless, intuitive and elegant command line interfaces.

## User's guide

This guide will guide you through several examples to help you grab the concepts of the library.

Clizy is based on features available in pure Python - in most cases the code will look the same way as an ordinary
Python code - no special constructs like decorators to create user interfaces.

### Positional and optional arguments

For positional and optional arguments Clizy makes use of arguments and keyword-only arguments.

Keyword-only arguments were introduced in Python 3.0 by [PEP 3102](https://www.python.org/dev/peps/pep-3102/). The
snippet bellow includes a keyword only argument called `arg3`. As the name suggests, the only way to specify the
argument is to use an explicit keyword argument usage using `arg3=value`:

```python
def func(arg1, arg2, *, arg3=None):
    ...
    
func("aaa", "bbb", arg3="ccc")

# raises TypeError: func() takes 2 positional arguments but 3 were given
func("aaa", "bbb", "ccc")
```

Now let's take a look on how Clizy operates with them:

```python
from clizy import run


def func(positional_argument, *, optional_argument=None):
    pass


if __name__ == '__main__':
    run(func)
```

In this example clizy interprets `positional_argument` as a positional argument and `optional_argument` as an optional
option `--optional-argument` with an automatic short option `-o`.

When the script is invoked with `--help`, it shows this help message:

```console
$ python example.py --help
usage: example.py [-h] [-o OPTIONAL_ARGUMENT] positional-argument

positional arguments:
  positional-argument

optional arguments:
  -h, --help            show this help message and exit
  -o OPTIONAL_ARGUMENT, --optional-argument OPTIONAL_ARGUMENT
```

Technically this function call:

```python
func('positional value', optional_argument='optional value')
```

and this command line call:

```console
$ example.py --optional-argument 'optional value' 'positional value'
```

are equal.

### Types

Types are automatically deduced from a default argument value or an argument type hint (
[PEP 3107](https://www.python.org/dev/peps/pep-3107/) and [PEP 484](https://www.python.org/dev/peps/pep-0484/)).

Clizy supports several Python types ouf of the box, the rest of this section provides explanation for all supported
types.

#### No type

If no type hint is, clizy considers an argument as `str` - technically the only type which command line can pass to
a command line application.

```python
from clizy import run


def func(string, *, another_string):
    print(string, type(string))
    print(another_string, type(another_string))

if __name__ == '__main__':
    run(func)
```


```console
$ python example.py --another-string yyy xxx
xxx <class 'str'>
yyy <class 'str'>
$ python example.py --help
usage: example.py [-h] -a ANOTHER_STRING string

positional arguments:
  string

optional arguments:
  -h, --help            show this help message and exit
  -a ANOTHER_STRING, --another-string ANOTHER_STRING
```

#### `str`, `int` and `float`

Behavior of the basic types is obvious - the type hint means a type into which is command line argument converted.

In the example bellow `string` is a positional argument of type `str`. `integer` of type `int` and `real_number` of
type `float` are optional arguments.

```python
from clizy import run


def func(string: str, *, integeter: int, real_number: float):
    print(locals())

if __name__ == '__main__':
    run(func)
```

How usage looks:

```console
$ python example.py --help
usage: example.py [-h] -i INTEGETER -r REAL_NUMBER string

positional arguments:
  string

optional arguments:
  -h, --help            show this help message and exit
  -i INTEGETER, --integeter INTEGETER
  -r REAL_NUMBER, --real-number REAL_NUMBER
$ python example.py --integer 123 --real-number 1.23 value
{'real_number': 1.23, 'integer': 123, 'string': 'value'}
```

#### `bool`

For optional arguments indicates their presence - `True` is set if an optional argument is present.

In the example `flag1` and `flag2` are interpreted by clizy in the same way - as an optional flag which is `False` by
default.

```python
from clizy import run


def func(*, flag1: bool, flag2=False):
    print(locals())

if __name__ == '__main__':
    run(func)
```

How usage looks:

```console
$ example.py --help
usage: example.py [-h] [-f] [-F]

optional arguments:
  -h, --help   show this help message and exit
  -f, --flag1
  -F, --flag2
$ python example.py --flag2
{'flag2': True, 'flag1': False}
```

#### Optional `typing.Tuple`

Behavior of `typing.Tuple` is based on the [typing module](https://docs.python.org/3/library/typing.html#typing.Tuple).
with a specific number of elements.

```python
from typing import Tuple
from clizy import run


def func(*, position: Tuple[int, int]):
    x, y = position
    print("x=", x, ", y=", y)

if __name__ == '__main__':
    run(func)
```

TODO: 

#### `typing.Tuple[str, ...]` (tuples with ellipsis)

#### Positional `list`, `typing.List` and `typing.Tuple`

A positional argument with such type is interpreted by clizy as a multi value argument. Behavior of `list` is
equal to `typing.List[str]`. 

All `typing.List` expects a virtually unlimited number of items (as long as your computer can handle it). `typing.Tuple`
expects a specific number of elements, for example `typing.Tuple[int, int, int]` expects three elements
of type int. The only exception is `Tuple[str, ...]` - a tuple with unknown number of elements - which behaves in a
similar way of as `typing.List`. 

```python
from clizy import run
from typing import List, Tuple


def func(tuple_values: Tuple[str, str, str], list_values: List[int]):
    print('tuple_values:', tuple_values)
    print('list_values:', list_values)


if __name__ == '__main__':
    run(func)
```

How it looks like:

```console
$ python example.py a b c 1 2 3 4 5 6
tuple_values: ['a', 'b', 'c']
list_values: [1, 2, 3, 4, 5, 6]
```

#### Optional `typing.Tuple`

Optional tuples are optional arguments with a specific number of elements, for example:

```python
from clizy import run
from typing import Tuple


def func(*, position: Tuple[int, int]=(0, 0)):
    x, y = position
    print('x:', x, 'y:', y)


if __name__ == '__main__':
    run(func)
```

How it looks like:

```console
$ python example.py --help
usage: example.py [-h] -p POSITION POSITION

optional arguments:
  -h, --help            show this help message and exit
  -p POSITION POSITION, --position POSITION POSITION
$ python example.py --pos 1 1
x: 1 y: 1
```

A special case is a tuple with ellisis (`...`), e.g. `typing.Tuple[int, ...]`. It's called
[a variable-length tuple of homogeneous type](https://docs.python.org/3/library/typing.html#typing.Tuple)) and clizy
support it as well:

 

#### Optional `list`, `typing.List[str]`, `typing.List[int]` and `typing.List[float]`

### Multiple commands

Multiple commands are supported passing a list of callables:

```python
def command1():
    pass
    
def command2():
    pass
```

How help message looks like:

```console
$ python example.py --help
usage: example.py [-h] {command1,command2} ...

positional arguments:
  {command1,command2}

optional arguments:
  -h, --help           show this help message and exit

$ python example.py command2 --help
usage: example.py command2 [-h] arg1 arg2

positional arguments:
  arg1
  arg2

optional arguments:
  -h, --help  show this help message and exit
```

Alternatively a class can be used:

```python
class CommandLine:
    def command1(self):
        pass
        
    def command2(self):
        pass
```

Using a class has a benefit of providing shared optional arguments for all subcommands by using the `__init__` method:

```python
from clizy import run


class Example:
    def __init__(self, *, optional=None):
        self.optional = optional

    def command1(self, arg1):
        print(f"optional: {self.optional}, arg1: {arg1}")

    def command2(self, arg1, arg2):
        print(f"optional: {self.optional}, arg1: {arg1}, arg2: {arg2}")

if __name__ == '__main__':
    run(Example)
```

How it looks:

```console
$ python example.py --help
usage: example.py [-h] [-o OPTIONAL] {command1,command2} ...

positional arguments:
  {command1,command2}

optional arguments:
  -h, --help            show this help message and exit
  -o OPTIONAL, --optional OPTIONAL

$ python example.py command2 --help
usage: example.py command2 [-h] arg1 arg2

positional arguments:
  arg1
  arg2

optional arguments:
  -h, --help  show this help message and exit

$ python example.py --optional x command2 y z
optional: x, arg1: y, arg2: z
```

## FAQ

**How can I make optional argument mandatory/required?**

You can just use a keyword only argument without a default value:

```
def function(*, arg):
    pass
```

But note required optional arguments don't make sense in the first place. 


**How can I  make users interaction more interactive?**

Unlike for example click, clizy does not support any user interactions like colorful echoing and progress bars. On the
other hand there are specialized libraries which can the job (sometimes subjectively even better than click):

* [print](https://docs.python.org/3.7/library/functions.html#print) builtin function for echoing
* [colorama](https://pypi.org/project/colorama/) library for colorized output
* [input](https://docs.python.org/3.7/library/functions.html#input) builtin function for input
* [getpass](https://docs.python.org/3/library/getpass.html) module to ask users for their password
* [tqdm](https://github.com/tqdm/tqdm) library for powerful and simple progress bars

**How can I create mutually exclusive optional arguments?**

This situation can be handled within a function: 

```python
def function(*, argument1=None, argument2=None):
    if argument1 and argument2:
        raise ValueError("argument1 and argument2 are mutually exclusive")
```

But note that mutually exclusive optional arguments should be rarely used.
