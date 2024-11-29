from syntax import Binary, Grouping, Literal, Unary


class Parser:
    def __init__(self, tokens):
        self.rawtokens = tokens
        self.tokens = [t.toktype for t in tokens]
        self.current = 0

    # ## GRAMMAR ##
    """
    expression     → equality ;
    equality       → comparison ( ( "!=" | "==" ) comparison )* ;
    comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
    term           → factor ( ( "-" | "+" ) factor )* ;
    factor         → unary ( ( "/" | "*" ) unary )* ;
    unary          → ( "!" | "-" ) unary
                    | primary ;
    primary        → NUMBER | STRING | "true" | "false" | "nil"
                    | "(" expression ")" ;
    """

    def expression(self):
        return self.equality()
    
    def equality(self):
        return self.comparison()
    
    def comparison(self):
        return self.term()
    
    def term(self):
        return self.factor()
    
    def factor(self):
        """ factor         → unary ( ( "/" | "*" ) unary )* ; """
        expr = self.unary()

        while self.match(["STAR", "SLASH"]):
            operator = self.previous_token().lexeme  # '*' or '/' character
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr
    
    def unary(self):
        """
        unary          → ( "!" | "-" ) unary
                        | primary ;
        """
        if self.match(["BANG", "MINUS"]):
            operator = self.previous_token().lexeme  # '!' or '-' character
            right = self.unary()
            return Unary(operator, right)
        return self.primary()
    
    def primary(self):
        """
        primary        → NUMBER | STRING | "true" | "false" | "nil"
                        | "(" expression ")" ;
        """
        if self.match("FALSE"):
            return Literal(False)
        if self.match("TRUE"):
            return Literal(True)
        if self.match("NIL"):
            return Literal(None)
        
        if self.match(["NUMBER", "STRING"]):
            return Literal(self.previous_token().literal)
        
        if self.match("LEFT_PAREN"):
            currtok = self.previous_token()
            content = self.expression()  # "recursively" parse the content of the parentheses
            if not self.match("RIGHT_PAREN"):
                raise ParserError(currtok, "Expected ')' after expression.")
            return Grouping(content)

    # ## UTILITIES ##

    def peek(self):
        assert 0 <= self.current < len(self.tokens)
        return self.tokens[self.current]
    
    def previous_token(self):
        assert 1 <= self.current <= len(self.tokens)
        return self.rawtokens[self.current - 1]
    
    def advance(self):
        if not self.is_at_end():
            self.current += 1
    
    def is_at_end(self):
        return self.peek() == "EOF"

    def match(self, toktypes: str | list[str]):
        """Beware: if match() returns True, it increments self.current !"""
        if isinstance(toktypes, str):
            toktypes = [toktypes]
        if not self.is_at_end() and self.peek() in toktypes:
            self.advance()
            return True
        return False


class ParserError(Exception):
    pass