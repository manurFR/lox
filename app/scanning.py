from dataclasses import dataclass
from typing import Any

from lexemes import LEXEMES_DESC_LENGTH


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
    line = 1
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
                match toktype:
                    case "COMMENT":  # set current to ignore the rest of the line
                        if (current := source.find("\n", end) + 1) == 0:
                            current = len(source)  # if the comment was on the last line, set current so that the 'while' loop stops
                        line += 1  # don't forget to increment since we passed a newline
                        break  # 'for' loop
                    case "STRING":  # capture the whole string literal until the closing quotes
                        end = source.find('"', end) + 1
                        if end == 0:
                            errors.append((line, "Unterminated string."))
                            current = len(source)
                            break  # 'for' loop
                        chars = source[current:end]
                        literal = chars.strip('"')
                        tokens.append(Token(toktype, chars, literal))
                        line += literal.count("\n")  # don't forget to increment line with multi-line strings
                    case "DIGIT":  # capture the whole number literal, including optional dot (but not at the end)
                        while True:
                            if end > len(source) - 1:
                                break  # we've reached the end of source, and thus the end of the number
                            else:
                                lookahead = source[end]
                                if lexemes.get(lookahead, "?") == "DIGIT":
                                    end += 1
                                elif lookahead == '.' and lexemes.get(source[end + 1], "?") == "DIGIT":
                                    end += 1
                                else:
                                    break  # the next character is not a digit or a dot: we've reached the end of the number
                        # we've reached the end of the number (or of the source)
                        chars = source[current:end]
                        literal = float(chars)
                        tokens.append(Token("NUMBER", chars, literal))
                    case "SPACE":  # ignore
                        pass
                    case "NEWLINE":  # ignore but note the line increment
                        line += 1
                    case _:  # regular token: record it
                        tokens.append(Token(toktype, chars, None))
                current = end
                break  # 'for' loop
        else:  # 'for' loop ended by finding no matching lexeme
            errors.append((line, f"Unexpected character: {chars}"))
            current += 1
    
    tokens.append(Token("EOF", None, None))

    return tokens, errors
