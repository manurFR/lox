def tokenize(source):
    tokens = []
    for char in source:
        match char:
            case '(':
                token = "LEFT_PAREN"
            case ')':
                token = "RIGHT_PAREN"

        tokens.append((token, char, None))

    return tokens
