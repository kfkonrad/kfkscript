import importlib
import re

from aenum import Enum
from pathlib import Path

# generate enum Keyword dynamically based on implemented keyword from files kfkscript/keyword_impl/<keyword>.py
Keyword = Enum(
    "Keyword",
    [
        file.name[:-3]
        for file in Path("kfkscript/keyword_impl/").iterdir()
        if re.search("[a-z]\.py", file.name)
    ],
)

# import the implementations of all keywords.
for keyword in Keyword:
    module = importlib.import_module(f'kfkscript.keyword_impl.{keyword.name}')
    exec(f"_{keyword.value} = module")

# map imported implementations to keywords as __impl property
Keyword.__impl = property(lambda self: eval(f"_{self.value}"))

Keyword.number_of_arguments = property(lambda self: self.__impl.number_of_arguments)

Keyword.execute = lambda self, arguments: self.__impl.execute(arguments)
