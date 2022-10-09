import kfkscript.global_state as global_state

number_of_arguments = 1

def execute(arguments):
    global_state.ret = arguments[0]
    return global_state.ret
