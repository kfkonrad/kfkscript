from kfkscript import global_state
from kfkscript.nestState import NestState
from kfkscript import keyword
from kfkscript.pure_keyword import generate_module
from aenum import extend_enum
from kfkscript.invocation import Invocation
from kfkscript import invocation
from kfkscript.keyword import Keyword

number_of_arguments = 2


def execute(arguments):
    name = arguments[0]
    parameter_count = arguments[1]

    subroutine = Invocation(Keyword["subroutine"], [name])
    invocation.execute(subroutine)

    global_state.is_keyword_definition = True
    extend_enum(keyword.Keyword, global_state.subroutine_name)
    keyword_value = keyword.Keyword[global_state.subroutine_name].value
    keyword_module = generate_module(global_state.subroutine_name, parameter_count)
    exec(f"keyword._{keyword_value} = keyword_module")
