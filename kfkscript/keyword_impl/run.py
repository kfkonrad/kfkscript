import kfkscript.global_state as global_state
from kfkscript.execution import run
from copy import deepcopy

number_of_arguments = 1

def execute(arguments):
    subroutine_name = arguments[0]
    #print(global_state.nesting)
    return run(global_state.subroutines[subroutine_name])
