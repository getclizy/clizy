from clizy.cli_structures import Interface, Command, OptionalArgument, Undefined
from clizy.short_names_assigner import assign_short_names


def dummy():
    pass


def test_assign_short_names_assigns_short_name_to_one_command():
    option = OptionalArgument('option', 'option', None, Undefined, Undefined, '', False)
    interface = Interface("", Command(
        dummy, 'dummy', 'dummy', '', [],
        [
            option
        ]), [])
    assign_short_names(interface)

    assert option.short_name == 'o'


def test_assign_short_names_assigns_short_names_to_subcommands_too():
    option1 = OptionalArgument('option_first', 'option-first', None, Undefined, Undefined, '', False)
    option2 = OptionalArgument('option_second', 'option-second', None, Undefined, Undefined, '', False)
    suboption1 = OptionalArgument('option_first', 'option-first', None, Undefined, Undefined, '', False)
    suboption2 = OptionalArgument('option_second', 'option-second', None, Undefined, Undefined, '', False)
    # TODO: rename these to something more reasonable
    suboption3 = OptionalArgument('option_first', 'option-first', None, Undefined, Undefined, '', False)
    suboption4 = OptionalArgument('option_second', 'option-second', None, Undefined, Undefined, '', False)

    interface = Interface(
        "", Command(
            dummy, 'dummy', 'dummy', '', [],
            [
                option1, option2
            ]
        ),
        [
            Command(
                dummy, 'subdummy1', 'subdummy1', '', [],
                [
                    suboption1, suboption2
                ]
            ),
            Command(
                dummy, 'subdummy2', 'subdummy2', '', [],
                [
                    suboption3, suboption4
                ]
            )
        ]
    )
    assign_short_names(interface)

    assert option1.short_name == 'o'
    assert option2.short_name == 'O'

    assert suboption1.short_name == 'p'
    assert suboption2.short_name == 'P'

    assert suboption3.short_name == 'p'
    assert suboption4.short_name == 'P'
