import kfkscript.global_state as global_state

number_of_arguments = 0


def execute(arguments):
    ctx = global_state.scopes.pop()
    ret = global_state.ret
    global_state.ret = ctx["ret"]
    global_state.vars = ctx["vars"]
    return ret
