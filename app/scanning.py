from dataclasses import dataclass
import string
from typing import Any

from lexemes import LEXEMES_DESC_LENGTH, RESERVED_WORDS


@dataclass
class Token:
    toktype: str
    lexeme: str | None
    literal: Any

    def __repr__(self) -> str:
        """The formatted output for this token"""
        return f"{self.toktype} {self.lexeme if self.lexeme else ''} {self.literal if self.literal is not None else 'null'}"


def lookahead_capture(remaining, valid_chars, valid_sep=None):
    """Capture a whole token one character at a time, until the next character is detected as not valid.
    If a valid_sep is given, such a character is valid only if the character after it is also valid
    (example: '12.3' is captured as '12.3' but '12.' is captured as '12' and the dot is excluded from the capture).
    Returns a tuple (captured string, index of the last captured character)."""
    next_char = 1
    while True:
        try:
            lookahead = remaining[next_char]
            if lookahead in valid_chars:
                next_char += 1
            elif valid_sep and lookahead == valid_sep and remaining[next_char + 1] in valid_chars:
                next_char += 1
            else:
                break  # the next character is not valid: we've reached the end of the capture
        except IndexError:
            break  # we've reached the end of source, and thus the capture stops here
    return remaining[:next_char], next_char - 1


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
                    case "COMMENT":  # ignore the rest of the line
                        if (end := source.find("\n", end) + 1) == 0:
                            end = len(source)  # if the comment was on the last line, set end so that the 'while' loop stops
                        line += 1  # don't forget to increment since we passed a newline
                    case "STRING":  # capture the whole string literal until the closing quotes
                        if (end := source.find('"', end) + 1) == 0:
                            errors.append((line, "Unterminated string."))  # no closing quotes
                            current = len(source)
                            break  # 'for' loop
                        chars = source[current:end]
                        literal = chars.strip('"')
                        tokens.append(Token(toktype, chars, literal))
                        line += literal.count("\n")  # don't forget to increment line when faced with multi-line strings
                    case "NUMBER":  # capture the whole number literal, including optional dot (but not at the end)
                        chars, offset = lookahead_capture(source[current:], valid_chars=string.digits, valid_sep='.')
                        end += offset
                        literal = float(chars)
                        tokens.append(Token(toktype, chars, literal))
                    case "IDENTIFIER":  # capture the identifier (digits are allowed inside an indentifier, after the first char)
                        chars, offset = lookahead_capture(source[current:], valid_chars=string.ascii_letters +
                                                                                        string.digits + '_')
                        end += offset
                        # Reserved words are detected and their toktype is specific (not IDENTIFIER)
                        if chars in RESERVED_WORDS:
                            tokens.append(Token(RESERVED_WORDS[chars], chars, None))
                        else:
                            tokens.append(Token(toktype, chars, None))
                    case "SPACE":  # ignore
                        pass
                    case "NEWLINE":  # ignore but count the line increment
                        line += 1
                    case _:  # regular lexeme: record it
                        tokens.append(Token(toktype, chars, None))
                current = end
                break  # 'for' loop
        else:  # 'for' loop ended by finding no matching lexeme
            errors.append((line, f"Unexpected character: {chars}"))
            current += 1
    
    tokens.append(Token("EOF", None, None))

    return tokens, errors
