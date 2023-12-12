from dataclasses import dataclass
import logging
from typing import Any

from kfkscript import global_state
from kfkscript.keyword import Keyword
from kfkscript.invocation import Invocation


def __first_whitespace(string):
    return next((i for i, char in enumerate(string) if char.isspace()), -1)

def __strip_with_linecount(string):
    remaining_string = string
    while remaining_string[0].isspace():
        if remaining_string[0] == "\n":
            global_state.line_number += 1
            # print("_LN", global_state.line_number)
        remaining_string = remaining_string[1:]
    return remaining_string

def parse_keyword(script):
    logging.trace(f"parse_keyword({script[:3]})")
    remaining_script = __strip_with_linecount(script)
    first_space = __first_whitespace(remaining_script)
    if first_space != -1:
        raw_keyword = remaining_script[:first_space]
    else:
        raw_keyword = remaining_script
    try:
        keyword = Keyword[raw_keyword]
    except KeyError:
        print(
            f"Invalid Keyword {raw_keyword} in line {global_state.line_number}, exiting"
        )
        exit(1)
    else:
        if first_space != -1:
            remaining_script = remaining_script[first_space:]
        else:
            remaining_script = ""
        return keyword, remaining_script


def parse_argument(script: str):
    logging.trace(f"parse_argument({script[:3]})")
    remaining_script = __strip_with_linecount(script)
    if remaining_script[0] == "$":
        return parse_dollar_string(remaining_script)
    if remaining_script[0] == "'":
        return parse_single_quote_string(remaining_script)
    if remaining_script[0] in "-0123456789." and  (remaining_script[0] != "-" or (len(remaining_script) > 1 and remaining_script[1] != " ")):
            return parse_number(remaining_script)
    return parse_remaining_script(remaining_script)


def parse_number(script):
    logging.trace(f"parse_number({script[:3]})")
    if script[0] not in "-0123456789.":
        raise ValueError(f"invalid number on line {global_state.line_number}: {script}")
    end = __first_whitespace(script)
    if end == -1:
        return convert_to_number(script[:]), ""
    return convert_to_number(script[:end]), script[end:]


def convert_to_number(number_string):
    try:
        if "." in number_string:
            return float(number_string)
        return int(number_string)
    except Exception:
        print(f"Invalid number: {repr(number_string)}")
        exit(1)


def parse_single_quote_string(script):
    logging.trace(f"parse_single_quote_string({script[:3]})")
    end = script.find('"')
    if script[0] != "'":
        raise ValueError(f"invalid string literal: {script[:3]}")
    if end == -1:
        return script[1:], ""
    return script[1:end], script[end + 1 :]


def parse_dollar_string(script):
    logging.trace(f"parse_dollar_string({script[:3]})")
    if script[0] != "$":
        raise ValueError(f"invalid variable name: {script[:3]}")
    end = __first_whitespace(script)
    if end == -1:
        return script[1:], ""
    return script[1:end], script[end:]


# TODO: potentiell obsolet weil duplikat zu parse_remaining_script
def parse_next_invocation(script):
    inv, remaining_script = parse_remaining_script(script)
    return inv, remaining_script



def parse_remaining_script(script):
    logging.trace(f"parse_line({script[:3]})")

    if script is None or script == "" or script[0] == "#":
        return None, None
    if len(script) >= 4 and script[:3] == "..." and script[3] in "0123456789":
        global_state.variadic_number, remaining_script = parse_number(script[3:])
        global_state.variadic_number = int(global_state.variadic_number) - 1
    else:
        remaining_script = script

    keyword, remaining_script = parse_keyword(remaining_script)
    arguments = []
    current_variadic_number = global_state.variadic_number + keyword.number_of_arguments
    # reset variadic number to parse arguments which themselves may be variadic
    # we can safely reset it here because will no longer be accessed for the current invocation
    global_state.variadic_number = 0
    for i in range(current_variadic_number):
        new_arg, remaining_script = parse_argument(remaining_script)
        arguments.append(new_arg)
    if remaining_script == "" or remaining_script == "\n":
        remaining_script = None
    return Invocation(keyword, arguments), remaining_script
