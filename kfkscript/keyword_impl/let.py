import kfkscript.global_state as global_state

number_of_arguments = 2

def execute(arguments):
    global_state.vars[arguments[0]] = arguments[1]
    return arguments[1]
