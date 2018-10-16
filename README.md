# Clizy - command-line interface for lazy people 

## ⚠ `master` branch refers to an alpha version of version 2!

`master` version now refers to an alpha version of a complete overhaul with new features and customizations.

## Why clizy?

Clizy simplifies command line interface creation by using mainly features available in Python 3.5 and higher - type
hints and keyword only arguments.

No unnecessary clutter, complexity and overwhelming documentation. Keep it simple, stupid. Ideal for lazy developers.

Let's take a look at this example:

```python
# installer.py
from clizy import run


class Installer:
    def __init__(self, *, index_url='https://default/'):
        self._index_url = index_url

    def install(self, packages: list):
        print(f"Install '{name}' from '{self._index_url}'")

    def search(self, pattern):
        print(f"Searching for '{pattern}' in '{self._index_url}'")

if __name__ == '__main__':
    run(Installer)
```

Before any explanation, let's take a look on how a very similar command-line interface is created using click:

```python
# package_installer.py
import click


@click.group()
@click.option('--index-url', default='http://default.com/')
@click.pass_context
def cli(ctx, index_url):
    ctx.obj['index_url'] = index_url


@cli.command()
@click.pass_context
@click.argument('packages', nargs=-1)
def install(ctx, packages):
    print(f"Install '{name}' from '{ctx.obj['index_url']}'")


@cli.command()
@click.pass_context
@click.argument('pattern')
def search(ctx, pattern):
    print(f"Searching for '{name}' in '{ctx.obj['index_url']}'")


if __name__ == '__main__':
    cli(obj={})
```

Quite a difference in verbosity and readability, isn't it?

Now for a very short explanation - clizy processes the class, its methods and their arguments into this
command line interface: 

```text
installer.py --index-url https://custom/ install flask requests
               ^                         ^       ^     ^
               |                         |       two positional arguments
               |                         command based on a method
               keyword only becomes an optional argument
```

Such command line invocation using clizy will basically translates into a predictable function call like this:

```python
Installer(index_url='https://custom/').install(['flask', 'requests'])
```

Interested? See the [docs](docs/docs.md).
