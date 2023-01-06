number_of_arguments = 1


def execute(arguments):
    print(*arguments, sep="")
    return arguments[0]
