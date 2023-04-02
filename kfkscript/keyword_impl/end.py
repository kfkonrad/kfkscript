from kfkscript import global_state
from kfkscript.nestState import NestState

number_of_arguments = 0


def execute(arguments):
    previous_state = global_state.nesting.pop()
    if previous_state == NestState.subroutine_definition:
        if global_state.is_keyword_definition:
            global_state.pure_keywords[
                global_state.subroutine_name
            ] = global_state.subroutine_content
            global_state.is_keyword_definition = False
        else:
            global_state.subroutines[
                global_state.subroutine_name
            ] = global_state.subroutine_content
    return global_state.ret
