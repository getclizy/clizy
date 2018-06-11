![clizy](clizy.gif)

Command-line interface creation for lazy people using type hints.

Quickstart
----------

Such normal Python function with sphinx docstring:

```python
  # ls.py
  import clizy

  def ls(filename, long: bool, all: bool, human_readable: bool, limit: int=None):
      """
      Fake command for listing.

      :param filename: filename, what else did you expect?
      :param long: long listing or something
      :param all: all, like including hidden files dude
      :param human_readable: show human readable stats
      :param limit: limit the number of files printed
      """
      print(locals())

  if __name__ == '__main__':
      clizy.run(ls)
```

Creates a command line interface. When you call the script with :code:`--help`, you can see what was generated:

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
Why
---

Why to use clizy over `argparse <https://docs.python.org/3/library/argparse.html>`_, 
`docopt <http://docopt.org/>`_ and `Click <http://click.pocoo.org/>`_?

`argparse <https://docs.python.org/3/library/argparse.html>`_ is quite verbose and magical, its `gentle introduction <https://docs.python.org/3/howto/argparse.html>`_ is
literally 14 pages long.

`docopt <http://docopt.org/>`_ introduced its own, very strict, documentation language which you have to learn first.

`Click <http://click.pocoo.org/>`_ makes developers use decorators even for information available in the function itself (variable names, type hints, default values).

`clize <https://github.com/prokopst/clizy>`_, while very similar in name, differs in many points - clizy has a different philosophy, is Python 3 only and uses what's already available in Python.

`defopt <https://github.com/evanunderscore/defopt>`_ is very similar in nature, but it is under the viral GPL v3, so when you use it your software must be GPL too. That's a no-go for many people.

**Clizy simplifies command line interface creation by using things we all use, know and love - type hints, arguments names, default values and docstrings - without unnecessary complexities and overwhelming documentation.**
**Spent time on programming, not learning libraries and reading a pile of documentation.**

Rules
-----

The rules for function arguments are simple and sane enough:

* Command line argument names are chosen automatically based on function argument names.
* No default value, no type hint - positional argument :code:`str`.
* No default value, type hint :code:`List[?]` - positional arguments with one or more values.
* Default value, no type hint - optional argument, type :code:`str`.
* Default value, type hint :code:`bool` - optional argument without any value. If present on the command line.
  function receives :code:`True`, if not function receives :code:`False`.
* Type hint :code:`int`, :code:`float` or :code:`str` - value is expected to have used type.


<table>
  <tr>
    <th>Function signature</th>
    <th>Generated interface</th>
  </tr>
  <tr>
    <td>
      <code>function(arg)</code>
    </td>
    <td rowspan="5">
      <code>function arg</code><br/>
      exactly one positional argument as expected type (<code>str</code> when no provided)
    </td>
  </tr>
  <tr>
    <td>
      <code>function(arg: int)</code>
    </td>
  </tr>
  <tr>
    <td>
      <code>function(arg: float)</code>
    </td>
  </tr>
  <tr>
    <td>
      <code>function(arg: str)</code>
    </td>
  </tr>
  <tr>
    <td>
      <code>function(arg)</code>
    </td>
  </tr>
  <tr>
    <td>
      <code>function(arg: list)</code>
    </td>
    <td rowspan="5">
      <code>function arg [arg ...]</code><br/>
      one or more positional arguments as expected type (by default <code>str</code>)
    </td>
  </tr>
  <tr>
    <td>
      <code>function(arg: typing.List)</code>
    </td>
  </tr>
  <tr>
    <td>
      <code>function(arg: typing.List[int])</code>
    </td>
  </tr>
  <tr>
    <td>
      <code>function(arg: typing.List[float])</code>
    </td>
  </tr>
  <tr>
    <td>
      <code>function(arg: typing.List[str])</code>
    </td>
  </tr>
 <tr>
    <td>
      <code>function(arg=None)</code>
    </td>
    <td rowspan="3">
      <code>function -a, --arg ARG</code><br/>
      optional argument with provided value as <code>str</code>.
    </td>
  </tr>
  <tr>
    <td>
      <code>function(arg: str=None)</code>
    </td>
  </tr>
  <tr>
    <td>
      <code>function(arg: str="default")</code>
    </td>
  </tr>
  <tr>
    <td>
      <code>function(arg: float=None)</code>
    </td>
    <td rowspan="3">
      <code>function -a, --arg ARG</code><br/>
      optional argument with provided value as <code>float</code>
    </td>
  </tr>
  <tr>
    <td>
      <code>function(arg: float=0)</code>
    </td>
  </tr>
  <tr>
    <td>
      <code>function(arg=0.0)</code>
    </td>
  </tr>
  <tr>
    <td>
      <code>function(arg: int=0)</code>
    </td>
    <td rowspan="2">
      <code>function -a, --arg ARG</code><br/>
      optional argument with provided value as <code>int</code>
    </td>
  </tr>
  <tr>
    <td>
      <code>function(arg: int=None)</code>
    </td>
  </tr>
  <tr>
    <td>
      <code>function(arg=0)</code>
    </td>
  </tr>
  <tr>
    <td>
      <code>function(arg=True)</code>
    </td>
    <td rowspan="2">
      <code>function -a, --arg</code><br/>
      optional argument without any value. When provided it's True, when not it's False.
    </td>
  </tr>
  <tr>
    <td>
      <code>function(arg: bool)</code>
    </td>
  </tr>
</table>


Limitations
-----------

Simplification comes at cost of flexibility, you should consider these limitations when choosing this library:

* select a letter for short options is not possible, it's chosen automatically based on name and available letter

* global options are not supported for multiple functions

  * they have to be always explicit for each function
    
* optional arguments cannot be required

  * actually both required and optional does not make sense in the first place
    
* types are limited to primitives

* there is no support for a choice

  * you can still do :code:`if value not in ['A', 'B']: raise ValueError`
    
* there is no support for a user input

  * you can still use :code:`input` for normal input and :code:`getpass.getpass` for passwords
    
* mutually exclusive options are not supported

  * you can still use :code:`if value1 and value2: raise ValueError`
