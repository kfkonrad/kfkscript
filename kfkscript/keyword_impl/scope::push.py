from kfkscript import global_state

number_of_arguments = 0


def execute(arguments):
    ret = global_state.ret
    global_state.scopes.append(
        {
            "variables": global_state.variables,
            "ret": ret,
        }
    )
    global_state.variables = {}
    return ret
