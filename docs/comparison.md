![clizy](https://media.githubusercontent.com/media/prokopst/clizy/master/docs/clizy.gif)

As mentioned several times in the documentation, clizy aims to be as simple as possible, uses only things available
in Python. No need to read several pages of documentation or hit.

Clizy simplifies command line interface creation by using things we all use, know and love -
arguments names, default values, docstrings and type hints - without unnecessary complexities
and overwhelming documentation.

Developers should spent time on programming, not learning libraries and reading piles of documentation.

## Comparison to other libraries

Let's compare clizy to other libraries.

### [argparse](https://docs.python.org/3/library/argparse.html)

argparse from the standard library is quite verbose and magical,
its [gentle introduction](https://docs.python.org/3/howto/argparse.html) beats you with 14 pages. I don't really
think that's really gentle.

### [docopt](http://docopt.org/)

docopt has introduced its own, command-line interface description language. For example:

```text
Naval Fate.

Usage:
  naval_fate ship new <name>...
  naval_fate ship <name> move <x> <y> [--speed=<kn>]
  naval_fate ship shoot <x> <y>
  naval_fate mine (set|remove) <x> <y> [--moored|--drifting]
  naval_fate -h | --help
  naval_fate --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --speed=<kn>  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.
```

The first issue with this is, obviously, that you don't really use Python, but you have to learn this description
language first with all its caveats. It's relatively easy to read, but not that easy to remember.
The second issue is that it does not do even simple type validation or conversion. It's possible to use
a different library for it, but the complexity grows and things are suddenly specified on two places.

### [Click](http://click.pocoo.org/)

Click is highly popular library to create command line interface, so let's take a bit deeper look at the library.
Consider this example from the official documentation:

```python
import click

@click.group()
def cli():
    pass

@cli.command()
def initdb():
    click.echo('Initialized the database')

@cli.command()
def dropdb():
    click.echo('Dropped the database')

if __name__ == '__main__':
    cli()
```

From the readability point of view it overuses decorators and uses strange constructs (notice how a dummy cli function
is used for grouping).

In another example:

```python
@click.command()
@click.option('--arg', default=0, type=int)
def function(arg):
    ...
```

Notice how the library forces developers to use `@click.option` even for information
which can be potentially retrieved from the function itself using pure Python language:

```python
def function(arg: int=0):
    ...
```

### [clize](https://github.com/epsy/clize)

clize, while very similar in name, differs in many points - clizy has a different philosophy, is Python 3 only
and uses what's already available in Python, no additional constructs.

### [defopt](https://github.com/evanunderscore/defopt)

defopt is very similar in nature, but it is under the viral GPL v3, So when you use it your software **must
be** GPL too. That's no-go for many developers.