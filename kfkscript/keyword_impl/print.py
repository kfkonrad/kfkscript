number_of_arguments = 1


def execute(arguments):
    print(*arguments, end="", sep="")
    return arguments[0]
