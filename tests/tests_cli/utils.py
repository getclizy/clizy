import subprocess


def dict_as_string_ordered(dictionary):
    return '{' + ", ".join(f"{repr(key)}: {repr(value)}" for key, value in sorted(dictionary.items())) + '}'


def stdoutify(**kwargs):
    return bytes(dict_as_string_ordered(kwargs) + '\n', 'utf-8')


def cli_print_dict(dictionary):
    string = dict_as_string_ordered(dictionary)
    print(string)


def subprocess_run_wrapper(*args):
    return subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
