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
        if len(global_state.nesting) > 0 and global_state.nesting[-1] == NestState["subroutine_definition"]:
            if exe.keyword == Keyword["end"]:
                exe.keyword.execute([])
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
