from kfkscript import global_state

number_of_arguments = 1


def execute(arguments):
    return global_state.variables[arguments[0]]
