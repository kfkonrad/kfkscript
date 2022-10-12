from kfkscript import global_state
from kfkscript.nestState import NestState

number_of_arguments = 1


def execute(arguments):
    if arguments[0] is True:
        global_state.nesting.append(NestState["if"])
    elif arguments[0] is False:
        global_state.nesting.append(NestState["else"])
    else:
        print(
            f"Argument of if in line {global_state.line_number} must be bool, was {arguments[0]}"
        )
        exit(1)
    return arguments[0]
