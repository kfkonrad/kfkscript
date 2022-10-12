from kfkscript import global_state
from kfkscript.nestState import NestState

number_of_arguments = 0


def execute(arguments):
    if len(global_state.nesting) > 0:
        if global_state.nesting[-1] == NestState["else"]:
            global_state.nesting[-1] = NestState["if"]
        elif global_state.nesting[-1] == NestState["if"]:
            global_state.nesting[-1] = NestState["else"]
    return True
