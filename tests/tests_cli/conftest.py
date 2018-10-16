import pytest


class ClizyOutput:
    def __init__(self, capsys):
        self._capsys = capsys
        self._code = None
        self._out = None
        self._err = None

    def __enter__(self):
        # throws away previous output
        self._capsys.readouterr()

    def __exit__(self, exc_type, exc_val, exc_tb):
        captured = self._capsys.readouterr()
        self._out = captured.out
        self._err = captured.err

        if isinstance(exc_val, SystemExit):
            self._code = exc_val.code
            return True

        if exc_val is None:
            self._code = 0
        else:
            self._code = 1

    @property
    def out(self):
        if self._out is None:
            raise Exception
        return self._out

    @property
    def err(self):
        if self._err is None:
            raise Exception
        return self._err

    @property
    def code(self):
        if self._code is None:
            raise Exception
        return self._code


@pytest.fixture()
def clizy_output(capsys):
    return ClizyOutput(capsys)
