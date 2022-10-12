import kfkscript.global_state as global_state

number_of_arguments = 0


def execute(arguments):
    ret = global_state.ret
    global_state.scopes.append(
        {
            "vars": global_state.vars,
            "ret": ret,
        }
    )
    global_state.vars = {}
    return ret
