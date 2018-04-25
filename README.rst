clizy
=====

Command-line interface creation for lazy people using type hints.

.. image:: clizy.gif

Quickstart
----------

Such normal Python function with sphinx docstring:

.. code:: python

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


Creates a command line interface. When you call the script with :code:`--help`, you can see what was generated:

.. code::

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

Why
---

Why to use clizy over `argparse <https://docs.python.org/3/library/argparse.html>`_, 
`docopt <http://docopt.org/>`_ and `Click <http://click.pocoo.org/>`_?

`argparse <https://docs.python.org/3/library/argparse.html>`_ is quite verbose and magical, its `gentle introduction <https://docs.python.org/3/howto/argparse.html>`_ is
literally 14 pages long.

`docopt <http://docopt.org/>`_ introduced its own, very strict, documentation language which you have to learn first.

`Click <http://click.pocoo.org/>`_ makes developers use decorators even for information available in the function itself (variable names, type hints, default values).

Clizy simplifies command line interface creation by using things we all use and know - type hints, arguments names, default values and docstrings.

Rules
-----

The rules for function arguments are simple and sane enough:

* names are chosen automatically based on names.
* No default value, no type hint - positional argument :code:`str`.
* No default value, type hint :code:`List[?]` - positional arguments with one or more values.
* Default value, no type hint - optional argument, type :code:`str`.
* Default value, type hint :code:`bool` - optional argument without any value. If present on the command line.
  function receives :code:`True`, if not function receives :code:`False`.
* Type hint :code:`int`, :code:`float` or :code:`str` - value is expected to have used type.

Limitations
-----------

Simplification comes at cost of flexibility, you should consider if these limitations when choosing this library:

* select a letter for short options is not possible, it's chosen automatically

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
