import kfkscript.global_state as global_state
from kfkscript.execution import run
number_of_arguments = 1

def execute(arguments):
    subroutine_name = arguments[0]
    run(global_state.subroutines[subroutine_name])
