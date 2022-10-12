from kfkscript import global_state

number_of_arguments = 1


def execute(arguments):
    search_variable = arguments[0]
    for scope in reversed(global_state.scopes):
        if search_variable in scope["variables"]:
            return scope["variables"][search_variable]
    print(
        f"Variable {search_variable} not foud in line {global_state.line_number}, exiting"
    )
    exit(1)
