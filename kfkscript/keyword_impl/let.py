from kfkscript import global_state

number_of_arguments = 2


def execute(arguments):
    global_state.variables[arguments[0]] = arguments[1]
    return arguments[1]
