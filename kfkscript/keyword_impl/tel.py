import kfkscript.global_state as global_state

number_of_arguments = 1

def execute(arguments):
    return global_state.vars[arguments[0]]
