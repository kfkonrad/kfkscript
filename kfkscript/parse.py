import logging

from kfkscript import global_state
from kfkscript.keyword import Keyword
from kfkscript.invocation import Invocation


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
        print(
            f"Invalid Keyword {raw_keyword} in line {global_state.line_number}, exiting"
        )
        exit(1)
    else:
        if first_space != -1:
            rest_of_line = line[first_space + 1 :]
        else:
            rest_of_line = ""
        return keyword, rest_of_line


def parse_argument(line):
    logging.trace(f"parse_argument({line})")
    if line[0] == "$":
        return parse_dollar_string(line)
    if line[0] == "'":
        return parse_single_quote_string(line)
    if line[0] in "-0123456789." and  (line[0] != "-" or (len(line) > 1 and line[1] != " ")):
            return parse_number(line)
    return parse_remaining_line(line)


def parse_number(line):
    logging.trace(f"parse_number({line})")
    if line[0] not in "-0123456789.":
        raise ValueError(f"invalid number: {line}")
    end = line.find(" ")
    if end == -1:
        return convert_to_number(line[:]), ""
    return convert_to_number(line[:end]), line[end + 1 :]


def convert_to_number(number_string):
    try:
        if "." in number_string:
            return float(number_string)
        return int(number_string)
    except Exception:
        print(f"Invalid number: {number_string}")
        exit(1)


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
    while line is not None:
        inv, line = parse_remaining_line(line)
        yield inv


def parse_remaining_line(line):
    logging.trace(f"parse_line({line})")
    try:
        line = line.strip()
    except Exception:
        pass
    if line is None or line == "" or line[0] == "#":
        return None, None
    if len(line) >= 4 and line[:3] == "..." and line[3] in "0123456789":
        global_state.variadic_number, rest_of_line = parse_number(line[3:])
        global_state.variadic_number = int(global_state.variadic_number) - 1
    else:
        rest_of_line = line

    keyword, rest_of_line = parse_keyword(rest_of_line)
    rest_of_line = rest_of_line.strip()
    arguments = []
    for _ in range(global_state.variadic_number + keyword.number_of_arguments):
        new_arg, rest_of_line = parse_argument(rest_of_line)
        rest_of_line = rest_of_line.strip()
        arguments.append(new_arg)
    return Invocation(keyword, arguments), rest_of_line
