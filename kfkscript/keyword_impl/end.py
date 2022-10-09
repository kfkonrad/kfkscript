import kfkscript.global_state as global_state

number_of_arguments = 0

def execute(arguments):
    global_state.nesting.pop()
    return True
