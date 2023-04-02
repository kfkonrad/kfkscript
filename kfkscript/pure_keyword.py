from types import SimpleNamespace
from kfkscript import global_state
from kfkscript import invocation
from kfkscript.invocation import Invocation
from kfkscript.keyword import Keyword


def generate_module(name, number_of_arguments):
    keyword_module = SimpleNamespace()
    keyword_module.number_of_arguments = number_of_arguments

    def execute(arguments):
        invocation.execute(Invocation(Keyword["scope::push"], []))
        let = Invocation(Keyword["let"], [f"args::size", len(arguments)])
        invocation.execute(let)
        for i, arg in enumerate(arguments, 1):
            let = Invocation(Keyword["let"], [f"args@{i}", arg])
            invocation.execute(let)

        for inv in global_state.pure_keywords[name]:
            result = invocation.execute(inv)

        invocation.execute(Invocation(Keyword["scope::pop"], []))
        return result

    keyword_module.execute = execute
    return keyword_module
