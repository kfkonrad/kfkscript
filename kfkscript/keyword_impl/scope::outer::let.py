from kfkscript import global_state

number_of_arguments = 2


def execute(arguments):
    name = arguments[0]
    value = arguments[1]
    if len(global_state.scopes) > 0:
        global_state.scopes[-1]["variables"][name] = value
    else:
        global_state.variables[name] = value
    return value
