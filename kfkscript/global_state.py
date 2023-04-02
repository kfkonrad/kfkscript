variables = {}
subroutines = {}
pure_keywords = {}

line_number = 0
nesting = []

subroutine_name = ""
subroutine_content = []

is_keyword_definition = False

ret = None

scopes = []

variadic_number = 0
