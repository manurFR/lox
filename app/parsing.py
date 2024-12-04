from errors import Errors
from lexemes import STATEMENTS
from syntax import Binary, Expression, Grouping, Literal, NodeStmt, Print, Unary


class Parser:
    def __init__(self, tokens, lenient=False):
        self.tokens = tokens
        self.current = 0
        # lenient mode allows expressions without ending ';' to compile and returns their value
        #  ...it's the magic that allow commands 'parse' and 'evaluate' to still work
        self.strict = not lenient

    def parse(self) -> list[NodeStmt]:
        statements = []
        while True:
            try:
                statements.append(self.statement())
            except ParserError as pex:
                Errors.report(*pex.args[0])
                break
            if self.is_at_end():
                break

        return statements

    # ## GRAMMAR ##
    """
    program        → statement* EOF ;

    statement      → exprStmt
                   | printStmt ;

    exprStmt       → expression ";" ;
    printStmt      → "print" expression ";" ;

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

    def statement(self):
        if self.match("PRINT"):
            return self.print_statement()
        
        # If it's not a statement, it MUST be an expression
        return self.expression_statement()
        
    # Statement parsing

    def print_statement(self):
        currtok = self.previous_token()  # PRINT token
        value = self.expression()
        if not self.match("SEMICOLON"):
            raise self.error(currtok, "Expected ';' after value.")
        return Print(value)

    def expression_statement(self):
        # Expressions with side effect
        currtok = self.peek()
        value = self.expression()
        if self.strict and not self.match("SEMICOLON"):
            raise self.error(currtok, "Expected ';' after expression.")
        return Expression(value)
        
    # Expression parsing

    def expression(self):
        return self.equality()
    
    def equality(self):
        """ equality       → comparison ( ( "!=" | "==" ) comparison )* ; """
        expr = self.comparison()

        while self.match(["EQUAL_EQUAL", "BANG_EQUAL"]):
            operator = self.previous_token() # '!=' or '=='
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr
    
    def comparison(self):
        """ comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ; """
        expr = self.term()

        while self.match(["GREATER", "GREATER_EQUAL", "LESS", "LESS_EQUAL"]):
            operator = self.previous_token()  # '>' / '>=' / '<' / '<='
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr
    
    def term(self):
        """ term           → factor ( ( "-" | "+" ) factor )* ; """
        expr = self.factor()

        while self.match(["PLUS", "MINUS"]):
            operator = self.previous_token()  # '+' or '-'
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr
    
    def factor(self):
        """ factor         → unary ( ( "/" | "*" ) unary )* ; """
        expr = self.unary()

        while self.match(["STAR", "SLASH"]):
            operator = self.previous_token()  # '*' or '/'
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr
    
    def unary(self):
        """
        unary          → ( "!" | "-" ) unary
                        | primary ;
        """
        if self.match(["BANG", "MINUS"]):
            operator = self.previous_token()  # '!' or '-'
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
            currtok = self.previous_token()  # the '(' token
            content = self.expression()  # "recursively" parse the content of the parentheses
            if not self.match("RIGHT_PAREN"):
                raise self.error(currtok, "Expected ')' after expression.")
            return Grouping(content)
        
        # Nothing matched
        raise self.error(self.peek(), "Expected expression.")

    # ## UTILITIES ##

    def peek(self):
        assert 0 <= self.current < len(self.tokens)
        return self.tokens[self.current]
    
    def previous_token(self):
        assert 1 <= self.current <= len(self.tokens)
        return self.tokens[self.current - 1]
    
    def advance(self):
        if not self.is_at_end():
            self.current += 1
    
    def is_at_end(self):
        return self.peek().toktype == "EOF"

    def match(self, toktypes: str | list[str]):
        """Beware: if match() returns True, it increments self.current !"""
        if isinstance(toktypes, str):
            toktypes = [toktypes]
        if not self.is_at_end() and self.peek().toktype in toktypes:
            self.advance()
            return True
        return False
    
    def error(self, token, message):
        if token.toktype == "EOF":
            return ParserError((token.line, message, " at end"))
        else:
            return ParserError((token.line, message, f" at '{token.lexeme}'"))
        
    def synchronize_post_error(self):
        """Discard tokens after an error was found, until it founds a statement boundary,
           ie. a semicolon ';' or a statement, then return so that the parsing starts back at this place.
           If it encounters the end of the tokens, so be it, there is nothing to meaningfully parse 
           after the error..."""
        while not self.is_at_end():
            self.advance()
            if self.peek().toktype == "SEMICOLON":
                self.advance()
                return
            elif self.peek().lexeme in STATEMENTS:
                return


class ParserError(Exception):
    pass