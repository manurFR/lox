from dataclasses import dataclass
from typing import Any

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
    ';': "SEMICOLON",
}

@dataclass
class Token:
    toktype: str
    lexeme: str | None
    literal: Any

    def __repr__(self) -> str:
        """The formatted output for this token"""
        return f"{self.toktype} {self.lexeme if self.lexeme else ''} {self.literal if self.literal is not None else 'null'}"
    

def tokenize(source):
    def next_char(index):
        if index >= len(source) - 1:
            return ""
        return source[index + 1]

    tokens, errors = [], []
    current = 0
    while current < len(source):
        char = source[current]
        start, end = current, current + 1
        if char in SINGLE_CHARACTER_LEXEMES:
            toktype = SINGLE_CHARACTER_LEXEMES.get(char, "")
        else:
            match char:
                case '=':
                    if next_char(current) == '=':
                        toktype = "EQUAL_EQUAL"
                        end += 1
                    else:
                        toktype = "EQUAL"
                case _:
                    errors.append((1, f"Unexpected character: {char}"))
                    current = end
                    continue

        tokens.append(Token(toktype, source[start : end], None))
        current = end
    
    tokens.append(Token("EOF", None, None))

    return tokens, errors
