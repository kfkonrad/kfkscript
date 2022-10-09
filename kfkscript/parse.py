import logging

import kfkscript.global_state as global_state
from kfkscript.keyword import Keyword
from kfkscript.execution import Execution


def parse_keyword(line):
    logging.trace(f"parse_keyword({line})")
    first_space = line.find(" ")
    if first_space != -1:
        raw_keyword = line[:first_space]
    else:
        raw_keyword = line
    try:
        keyword = Keyword[raw_keyword]
    except KeyError:
        print(f"Invalid Keyword {raw_keyword} in line {global_state.line_number}, exiting")
        exit(1)
    else:
        if first_space != -1:
            rest_of_line = line[first_space + 1 :]
        else:
            rest_of_line = ''
        return keyword, rest_of_line


def parse_argument(line):
    logging.trace(f"parse_argument({line})")
    if line[0] == "$":
        return parse_dollar_string(line)
    elif line[0] == "'":
        return parse_single_quote_string(line)
    else:
        return parse_remaining_line(line)


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

def parse_line(line):
    executions = []
    while line != None:
        exe, line = parse_remaining_line(line)
        executions.append(exe)
    return executions

def parse_remaining_line(line):
    logging.trace(f"parse_line({line})")
    try:
        line = line.strip()
    except Exception:
        pass
    if line is None or line == "" or line[0] == "#":
        return None, None
    keyword, rest_of_line = parse_keyword(line)
    rest_of_line = rest_of_line.strip()
    arguments = []
    for i in range(keyword.number_of_arguments):
        new_arg, rest_of_line = parse_argument(rest_of_line)
        rest_of_line = rest_of_line.strip()
        arguments.append(new_arg)
    return Execution(keyword, arguments), rest_of_line
