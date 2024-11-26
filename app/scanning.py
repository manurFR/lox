def tokenize(source):
    tokens = []
    for char in source:
        match char:
            case '(':
                token = "LEFT_PAREN"
            case ')':
                token = "RIGHT_PAREN"
            case '{':
                token = "LEFT_BRACE"
            case '}':
                token = "RIGHT_BRACE"
            case _:
                token = "UNKNOWN"

        tokens.append((token, char, None))

    return tokens
