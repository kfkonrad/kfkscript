import logging
from kfkscript import global_state
from kfkscript import invocation

number_of_arguments = 1


def execute(arguments):
    subroutine_name = arguments[0]
    return invocation.execute(global_state.subroutines[subroutine_name])
