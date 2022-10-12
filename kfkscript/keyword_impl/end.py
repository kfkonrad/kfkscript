from kfkscript import global_state
from kfkscript.nestState import NestState

number_of_arguments = 0


def execute(arguments):
    previous_state = global_state.nesting.pop()
    if previous_state == NestState.subroutine_definition:
        global_state.subroutines[
            global_state.subroutine_name
        ] = global_state.subroutine_content
    return global_state.ret
