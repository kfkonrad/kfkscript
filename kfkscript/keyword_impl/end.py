from aenum import Enum, auto, extend_enum

import kfkscript.global_state as global_state
from kfkscript.nestState import NestState
from kfkscript.keyword import Keyword

number_of_arguments = 0

def execute(arguments):
    previous_state = global_state.nesting.pop()
    if previous_state == NestState.subroutine_definition:
        global_state.subroutines[global_state.subroutine_name] = global_state.subroutine_content
    return True
