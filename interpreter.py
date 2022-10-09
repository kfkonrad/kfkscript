import functools
import logging
import sys

from kfkscript.keyword import Keyword

logging.TRACE = 5
logging.addLevelName(logging.TRACE, "TRACE")
logging.Logger.trace = functools.partialmethod(logging.Logger.log, logging.TRACE)
logging.trace = functools.partial(logging.log, logging.TRACE)

# logging.getLogger().setLevel(logging.DEBUG)
# logging.getLogger().setLevel(logging.TRACE)

vars = {}
line_number = 0

def parse_keyword(line):
    logging.trace(f"parse_keyword({line})")
    first_space = line.find(" ")
    raw_keyword = line[:first_space]
    try:
        keyword = Keyword[raw_keyword]
    except KeyError:
        print(f'Invalid Keyword {raw_keyword} in line {line_number}, exiting')
        exit(1)
    else:
        rest_of_line = line[first_space + 1 :]
        return keyword, rest_of_line


def parse_argument(line):
    logging.trace(f"parse_argument({line})")
    if line[0] == "$":
        return parse_dollar_string(line)
    elif line[0] == "'":
        return parse_single_quote_string(line)
    else:
        return execute_line(line)


def execute_line(line):
    logging.trace(f"execute_line({line})")
    if line == "" or line[0] == "#":
        return None
    keyword, rest_of_line = parse_keyword(line)
    arguments = []
    for i in range(keyword.number_of_arguments):
        new_arg, rest_of_line = parse_argument(rest_of_line)
        arguments.append(new_arg)
    return execute_keyword(keyword, arguments), rest_of_line


def parse_single_quote_string(line):
    logging.trace(f"parse_single_quote_string({line})")
    end = line.find('"')
    if line[0] != "'":
        raise ValueError(f"invalid string literal: {line}")
    if end == -1:
        return line[1:], ""
    return line[1:end], line[end + 2 :]


def parse_dollar_string(line):
    logging.trace(f"parse_dollar_string({line})")
    if line[0] != "$":
        raise ValueError(f"invalid variable name: {line}")
    end = line.find(" ")
    if end == -1:
        return line[1:], ""
    return line[1:end], line[end + 1 :]


def execute_keyword(keyword, arguments):
    logging.trace(f"execute_keyword({keyword}, {arguments})")
    logging.debug(f"Keyword: {keyword}, Arguments: {arguments}")
    if keyword == Keyword.print:
        print(arguments[0], end="")
        return arguments[0]
    if keyword == Keyword.println:
        print(arguments[0])
        return arguments[0]
    elif keyword == Keyword.let:
        vars[arguments[0]] = arguments[1]
        return arguments[1]
    elif keyword == Keyword.tel:
        return vars[arguments[0]]
    elif keyword == Keyword.strunescape:
        return bytes(arguments[0], "utf-8").decode("unicode_escape")
    elif keyword == Keyword.plus:
        return arguments[0] + arguments[1]
    raise NotImplementedError(keyword)


def main():
    global line_number
    logging.trace("main")
    filename = sys.argv[1]
    # arguments = sys.argv[:1]
    kfkscript = open(filename, "r").readlines()


    for line_number, line in enumerate(kfkscript, 1):
        execute_line(line[:-1])


main()
