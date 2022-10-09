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
        plain_arguments = []
        for arg in exe.arguments:
            if isinstance(arg, Execution):
                plain_arguments.append(run([arg]))
            else:
                plain_arguments.append(arg)
        if len(global_state.nesting) > 0 and global_state.nesting[-1] in (NestState["else"], NestState["ignore"]) and exe.keyword not in (Keyword["end"], Keyword["else"]):
            if exe.keyword == Keyword["if"]:
                global_state.nesting.append(NestState["ignore"])
            continue
        ret = exe.keyword.execute(plain_arguments)
    return ret
