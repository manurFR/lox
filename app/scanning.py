from dataclasses import dataclass
from typing import Any

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
    '//': "COMMENT"
}
MAX_LEX_LENGTH = max(len(lex) for lex in LEXEMES.keys())
# list of dicts ; the first dict is the sub-dict of lexemes whose length is the max, the second those whose length is one less, etc.
LEXEMES_DESC_LENGTH = list(
    reversed([{lex: toktype for lex, toktype in LEXEMES.items() if len(lex) == lexlength} for lexlength in range(1, MAX_LEX_LENGTH + 1)])
)

@dataclass
class Token:
    toktype: str
    lexeme: str | None
    literal: Any

    def __repr__(self) -> str:
        """The formatted output for this token"""
        return f"{self.toktype} {self.lexeme if self.lexeme else ''} {self.literal if self.literal is not None else 'null'}"
    

def tokenize(source):
    tokens, errors = [], []
    current = 0
    while current < len(source):
        for lexemes in LEXEMES_DESC_LENGTH:
            if len(lexemes) == 0:
                continue
            lexlength = len(list(lexemes.keys())[0])
            end = current + lexlength

            # skip lexemes of size N if there is not at least N characters remaining to scan
            if end > len(source):
                continue
            
            chars = source[current:end]
            if chars in lexemes:
                toktype = lexemes[chars]
                if toktype == "COMMENT":
                    # ignore the rest of the line
                    if (current := source.find("\n", end) + 1) == 0:
                        current = len(source)  # if the comment was on the last line, set current so that the 'while' loop stops
                    break
                tokens.append(Token(toktype, chars, None))
                current = end
                break
        else:  # 'for' ended by finding no matching lexeme
            errors.append((1, f"Unexpected character: {chars}"))
            current += 1
    
    tokens.append(Token("EOF", None, None))

    return tokens, errors
