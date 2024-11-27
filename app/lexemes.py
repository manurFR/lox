import string


LEXEMES = {
    '(': "LEFT_PAREN",
    ')': "RIGHT_PAREN",
    '{': "LEFT_BRACE",
    '}': "RIGHT_BRACE",
    '*': "STAR",
    '.': "DOT",
    ',': "COMMA",
    '+': "PLUS",
    '-': "MINUS",
    ';': "SEMICOLON",
    '=': "EQUAL",
    '==': "EQUAL_EQUAL",
    '!': "BANG",
    '!=': "BANG_EQUAL",
    '<': "LESS",
    '<=': "LESS_EQUAL",
    '>': "GREATER",
    '>=': "GREATER_EQUAL",
    '/': "SLASH",
    '//': "COMMENT",
    ' ': "SPACE",
    '\t': "SPACE",
    '\n': "NEWLINE",
    '"': "STRING",
    '_': "IDENTIFIER",
}
# add '0': "DIGIT" to '9': "DIGIT"
for digit in range(0, 10):
    LEXEMES[str(digit)] = "DIGIT"
# add lowercase + uppercase letters as "IDENTIFIER" (underscore was already added above)
for letter in string.ascii_letters:
    LEXEMES[letter] = "IDENTIFIER"

MAX_LEX_LENGTH = max(len(lex) for lex in LEXEMES.keys())
# list of dicts ; the first dict is the sub-dict of lexemes whose length is the max, the second those whose length is one less, etc.
LEXEMES_DESC_LENGTH = list(
    reversed([{lex: toktype for lex, toktype in LEXEMES.items() if len(lex) == lexlength} for lexlength in range(1, MAX_LEX_LENGTH + 1)])
)