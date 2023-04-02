import importlib
import importlib.util
import re

from pathlib import Path
from aenum import Enum

# generate enum Keyword dynamically based on implemented keyword from files
# kfkscript/keyword_impl/<keyword>.py
Keyword = Enum(
    "Keyword",
    [
        file.name[:-3]
        for file in Path("kfkscript/keyword_impl/").iterdir()
        if re.search(r"\.py$", file.name)
    ],
)

# import the implementations of all keywords.
for keyword in Keyword:
    spec = importlib.util.spec_from_file_location(
        name=f"_{keyword.value}",
        location=f"kfkscript/keyword_impl/{keyword.name}.py",
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    exec(f"_{keyword.value} = module")

# map imported implementations to keywords as __impl property
Keyword.__impl = property(lambda self: eval(f"_{self.value}"))

Keyword.number_of_arguments = property(lambda self: self.__impl.number_of_arguments)

Keyword.execute = lambda self, arguments: self.__impl.execute(arguments)
