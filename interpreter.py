import functools
import logging
import sys

from kfkscript import global_state
from kfkscript.parse import parse_line
from kfkscript.invocation import execute

logging.TRACE = 5
logging.addLevelName(logging.TRACE, "TRACE")
logging.Logger.trace = functools.partialmethod(logging.Logger.log, logging.TRACE)
logging.trace = functools.partial(logging.log, logging.TRACE)

# logging.getLogger().setLevel(logging.DEBUG)
# logging.getLogger().setLevel(logging.TRACE)


def main():
    logging.trace("main")
    filename = sys.argv[1]
    # arguments = sys.argv[:1]
    kfkscript = open(filename, "r").readlines()

    for line in kfkscript:
        global_state.line_number += 1
        logging.trace(f"line_number = {global_state.line_number}")
        for invocation in parse_line(line[:-1]):
            execute(invocation)


main()
