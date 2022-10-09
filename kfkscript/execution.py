import logging

import kfkscript.global_state as global_state
from kfkscript.keyword import Keyword
from kfkscript.nestState import NestState

class Execution:
    def __init__(self, keyword, arguments):
        self.keyword = keyword
        self.arguments = arguments
    def __repr__(self):
        return f"Execution(keyword: {self.keyword}, arguments: {self.arguments})"

def run(executions):
    logging.trace(f"run({executions})")
    ret = None
    for exe in executions:
        if exe is None:
            continue
        if len(global_state.nesting) > 0 and NestState.subroutine_definition in global_state.nesting:
            if exe.keyword == Keyword["if"]:
                global_state.nesting.append(NestState["ignore"])
            if exe.keyword == Keyword["end"]:
                previous_nest_state = global_state.nesting[-1]
                exe.keyword.execute([])
                if previous_nest_state == NestState.subroutine_definition:
                    continue
            global_state.subroutine_content.append(exe)
            continue
        plain_arguments = []
        for arg in exe.arguments:
            if isinstance(arg, Execution):
                plain_arguments.append(run([arg]))
            else:
                plain_arguments.append(arg)
        # this means no execution is currently supposed to take place
        # this means were in the unentered part of an if/else clause
        # we still need to explicitly skip this because the parser can't
        # know when/if it should skip certain branches
        if len(global_state.nesting) > 0 and global_state.nesting[-1] in (NestState["else"], NestState["ignore"]) and exe.keyword not in (Keyword["end"], Keyword["else"]):
            if exe.keyword == Keyword["if"]:
                # the ignore state helps keeping a valid NestState when the
                # above if-clause inevitably ends. Otherwise the above
                # skipping mechanism would wrongly execute nested ifs in
                # skipped branches
                global_state.nesting.append(NestState["ignore"])
            continue
        ret = exe.keyword.execute(plain_arguments)
    return ret
