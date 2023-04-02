from kfkscript import global_state

number_of_arguments = 1


def execute(arguments):
    global_state.variadic_number = arguments[0] - 1
    return global_state.variadic_number
