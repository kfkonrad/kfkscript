from enum import Enum

Keyword = Enum(
    "Keyword",
    """
print println
let tel
strunescape
plus
""",
)

Keyword.number_of_arguments = property(
    lambda self: {
        Keyword.print: 1,
        Keyword.println: 1,
        Keyword.let: 2,
        Keyword.tel: 1,
        Keyword.strunescape: 1,
        Keyword.plus: 2,
    }[self]
)
