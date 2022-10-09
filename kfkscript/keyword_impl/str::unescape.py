number_of_arguments = 1

def execute(arguments):
    return bytes(arguments[0], "utf-8").decode("unicode_escape")
