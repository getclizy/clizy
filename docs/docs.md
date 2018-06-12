![clizy](https://media.githubusercontent.com/media/prokopst/clizy/master/docs/clizy.gif)

Command-line interface creation for lazy people using type hints.

## Documentation

The rules for a function signature arguments are described in this table. The first column shows the function signature
and the second shows an interface generated using

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


## FAQ

**How can I make optional argument mandatory/required?**

Required optional arguments don't make any sense in the first place.

**How can I echo?**

Just use the `print` function.

**How can I echo in colors?**

Use [colorama](https://pypi.org/project/colorama/).

**How can I get user's input?**

Use builtin `input` (🔗) or `getpass.getpass` (🔗) from the standard library within a function.

**How can I create mutually exclusive functions?**

This situation can be handled within a function: 

```python
def function(argument1, argument2):
    if argument1 and argument2:
        raise ValueError("argument1 and argument2 are mutually exclusive")
```

But note that mutually exclusive optional arguments should be rarely used.

**How to select a letter for short options?**

Letter selection for short options is not possible, it's chosen automatically based on name and available letter.

**How to extend clizy to understand custom types?**

Types are limited to what you can pass through a command line interface. You can handle more complex types
within a function.  

**How to use global options for several functions?**

Global options are not supported. They have to be always explicit for each function.
