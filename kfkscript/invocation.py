import logging

from kfkscript import global_state
from kfkscript.keyword import Keyword
from kfkscript.nestState import NestState


class Invocation:
    def __init__(self, keyword, arguments):
        self.keyword = keyword
        self.arguments = arguments

    def __repr__(self):
        return f"Invocation(keyword: {self.keyword}, arguments: {self.arguments})"


def execute(inv):
    logging.trace(f"execute({inv})")
    if inv is None:
        return None
    if (
        len(global_state.nesting) > 0
        and NestState.subroutine_definition in global_state.nesting
    ):
        if inv.keyword == Keyword["if"]:
            global_state.nesting.append(NestState["ignore"])
        if inv.keyword == Keyword["end"]:
            previous_nest_state = global_state.nesting[-1]
            inv.keyword.execute([])
            if previous_nest_state == NestState.subroutine_definition:
                return None
        global_state.subroutine_content.append(inv)
        return None
    plain_arguments = []
    for arg in inv.arguments:
        if isinstance(arg, Invocation):
            plain_arguments.append(execute(arg))
        else:
            plain_arguments.append(arg)
    # this means no invocation is currently supposed to take place
    # this means were in the unentered part of an if/else clause
    # we still need to explicitly skip this because the parser can't
    # know when/if it should skip certain branches
    if (
        len(global_state.nesting) > 0
        and global_state.nesting[-1] in (NestState["else"], NestState["ignore"])
        and inv.keyword not in (Keyword["end"], Keyword["else"])
    ):
        if inv.keyword == Keyword["if"]:
            # the ignore state helps keeping a valid NestState when the
            # above if-clause inevitably ends. Otherwise the above
            # skipping mechanism would wrongly execute nested ifs in
            # skipped branches
            global_state.nesting.append(NestState["ignore"])
        return None
    return inv.keyword.execute(plain_arguments)
