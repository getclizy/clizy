from typing import Text, Union


class _SecretText(Text):
    pass


class _InputText(Text):
    pass


# TODO: explanation
SecretText = Union[Text, _SecretText]
InputText = Union[Text, _InputText]
