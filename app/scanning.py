SINGLE_CHARACTER_LEXEMES = {
    '(': "LEFT_PAREN",
    ')': "RIGHT_PAREN",
    '{': "LEFT_BRACE",
    '}': "RIGHT_BRACE",
    '*': "STAR",
    '.': "DOT",
    ',': "COMMA",
    '+': "PLUS",
    '-': "MINUS",
    ';': "SEMICOLON"
}

def tokenize(source):
    tokens = []
    for char in source:
        match char:
            case str if len(char) == 1:
                token = SINGLE_CHARACTER_LEXEMES.get(char)
            case _:
                token = "UNKNOWN"

        tokens.append((token, char, None))

    return tokens
