from scanning import Token  # type: ignore

# Prepared tokens for unit tests
MULTIPLY = Token("STAR", "*", None, 1)
DIVISE = Token("SLASH", "/", None, 1)
MINUS = Token("MINUS", "-", None, 1)
PLUS = Token("PLUS", "+", None, 1)
NOT = Token("BANG", "!", None, 1)
LESS = Token("LESS", "<", None, 1)
LESS_EQUAL = Token("LESS_EQUAL", "<=", None, 1)
GREATER = Token("GREATER", ">", None, 1)
GREATER_EQUAL = Token("GREATER_EQUAL", ">=", None, 1)
EQUAL_EQUAL = Token("EQUAL_EQUAL", "==", None, 1)
NOT_EQUAL = Token("BANG_EQUAL", "!=", None, 1)
OR = Token("OR", "or", None, 1)
AND = Token("AND", "and", None, 1)
