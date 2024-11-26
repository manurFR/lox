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
    tokens, errors = [], []
    for char in source:
        match char:
            case str if char in SINGLE_CHARACTER_LEXEMES:
                token = SINGLE_CHARACTER_LEXEMES.get(char)
            case _:
                errors.append((1, f"Unexpected character: {char}"))
                continue

        tokens.append((token, char, None))

    return tokens, errors
