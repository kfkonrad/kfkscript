import functools
import logging
import sys

from kfkscript import global_state
from kfkscript.parse import parse_next_invocation
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
    kfkscript = open(filename, "r").read()

    while kfkscript is not None:
        invocation, kfkscript = parse_next_invocation(kfkscript)
        execute(invocation)

main()
