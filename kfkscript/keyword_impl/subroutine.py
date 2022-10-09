import kfkscript.global_state as global_state
from kfkscript.nestState import NestState

number_of_arguments = 1

def execute(arguments):
    if len(global_state.nesting) > 0 and NestState.subroutine_definition in global_state.nesting:
        print(f"Nested subroutine definition in line {global_state.line_number} not allowed, exiting")
        exit(1)
    global_state.nesting.append(NestState.subroutine_definition)
    global_state.subroutine_name = arguments[0]
    global_state.subroutine_content = []
