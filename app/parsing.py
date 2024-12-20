from errors import Errors
from lexemes import STATEMENTS
from syntax import Assign, Binary, Block, Expression, Grouping, If, Literal, Logical, NodeStmt, Print, Unary, Var, Variable, While


class Parser:
    def __init__(self, tokens, lenient=False):
        self.tokens = tokens
        self.current = 0
        # lenient mode allows expressions without ending ';' to compile and returns their value
        #  ...it's the magic that allow commands 'parse' and 'evaluate' to still work
        self.lenient = lenient

    def parse(self) -> list[NodeStmt]:
        statements = []
        while True:
            try:
                statements.append(self.declaration())
            except ParserError as pex:
                Errors.report(*pex.args[0])
                break
            if self.is_at_end():
                break

        return statements

    # ## GRAMMAR ##
    """
    program        → declaration* EOF ;

    declaration    → varDecl
                    | statement ;

    varDecl        → "var" IDENTIFIER ( "=" expression )? ";" ;

    statement      → exprStmt
                    | ifStmt
                    | printStmt
                    | whileStmt
                    | block ;

    whileStmt      → "while" "(" expression ")" statement ;

    ifStmt         → "if" "(" expression ")" statement
                    ( "else" statement )? ;

    block          → "{" declaration* "}" ;

    exprStmt       → expression ";" ;
    printStmt      → "print" expression ";" ;

    expression     → assignment ;
    assignment     → IDENTIFIER "=" assignment
                    | logic_or ;
    logic_or       → logic_and ( "or" logic_and )* ;
    logic_and      → equality ( "and" equality )* ;
    equality       → comparison ( ( "!=" | "==" ) comparison )* ;
    comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
    term           → factor ( ( "-" | "+" ) factor )* ;
    factor         → unary ( ( "/" | "*" ) unary )* ;
    unary          → ( "!" | "-" ) unary
                    | primary ;
    primary        → "true" | "false" | "nil"
                    | NUMBER | STRING
                    | "(" expression ")"
                    | IDENTIFIER ;
    """

    def declaration(self):
        """ declaration    → varDecl | statement ; """
        try:
            if self.match("VAR"):
                return self.var_declaration_statement()
        except ParserError as pex:
            Errors.report(*pex.args[0])
            self.synchronize_post_error()
            return
        
        return self.statement()

    def statement(self):
        """ statement      → exprStmt | ifStmt | printStmt | whileStmt | block ; """
        if self.match("IF"):
            return self.if_statement()
        if self.match("PRINT"):
            return self.print_statement()
        if self.match("WHILE"):
            return self.while_statement()
        if self.match("LEFT_BRACE"):
            return Block(self.block())
        
        # If it's not a statement, it MUST be an expression
        return self.expression_statement()
        
    # Statement parsing

    def if_statement(self):
        currtok = self.previous_token()  # IF token
        if not self.match("LEFT_PAREN"):
            raise self.error(currtok, "Expected '(' after 'if'.")
        condition = self.expression()
        if not self.match("RIGHT_PAREN"):
            raise self.error(currtok, "Expected ')' after if condition.")
        
        then_stmt = self.statement()
        else_stmt = None
        if self.match("ELSE"):
            else_stmt = self.statement()
        
        return If(condition, then_stmt, else_stmt)

    def print_statement(self):
        """ printStmt      → "print" expression ";" ; """
        currtok = self.previous_token()  # PRINT token
        value = self.expression()
        if not (self.match("SEMICOLON") or self.lenient):
            raise self.error(currtok, "Expected ';' after value.")
        return Print(value)
    
    def while_statement(self):
        """ whileStmt      → "while" "(" expression ")" statement ; """
        currtok = self.previous_token()  # WHILE token
        if not self.match("LEFT_PAREN"):
            raise self.error(currtok, "Expected '(' after 'while'.")
        condition = self.expression()
        if not self.match("RIGHT_PAREN"):
            raise self.error(currtok, "Expected ')' after condition.")
        body = self.statement()
        return While(condition, body)

    def expression_statement(self):
        """ exprStmt       → expression ";" ; """
        # Expressions with side effect
        currtok = self.peek()
        value = self.expression()
        if not (self.match("SEMICOLON") or self.lenient):
            raise self.error(currtok, "Expected ';' after expression.")
        return Expression(value)
    
    def var_declaration_statement(self):
        """ varDecl        → "var" IDENTIFIER ( "=" expression )? ";" ; """
        currtok = self.peek()  # 'var'
        if not self.match("IDENTIFIER"):
            raise self.error(currtok, "Expected variable name.")
        name = self.previous_token()

        initializer = None
        if self.match("EQUAL"):
            initializer = self.expression()

        if not (self.match("SEMICOLON") or self.lenient):
            raise self.error(currtok, "Expected ';' after variable declaration.")
        return Var(name, expr=initializer)
    
    def block(self):
        currtok = self.previous_token()  # '{'
        statements = []

        while not self.is_at_end() and self.peek().toktype != "RIGHT_BRACE":
            statements.append(self.declaration())

        if not self.match("RIGHT_BRACE"):
            raise self.error(currtok, "Expected '}' after block.")
        
        return statements
        
    # Expression parsing

    def expression(self):
        """ expression     → assignment ; """
        return self.assignment()
    
    def assignment(self):
        """ assignment     → IDENTIFIER "=" assignment | logic_or ; """
        # Assignments (like "a = 3") are tricky because they start as regular expression
        #  (here "a" could mean we want the value of the variable) but the parser can only
        #  understand it is an assignment later, when it encounters the '=' token.
        # So we will parse the first tokens as an expression, and convert that to the left-hand
        #  side of an assignment, ie. a token, only if we meet an equal sign afterwards.
        # Otherwise we will return the expression... as an expression.
        expr = self.logic_or()

        if self.match("EQUAL"):  # it's an assignment, not a right-side expression
            currtok = self.previous_token()  # '=' token
            value = self.assignment()  # a = b = 1 is allowed

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)
            else:
                self.error(currtok, "Invalid assignment target.")

        # It wasn't an assignment, go on parsing it as an expression
        return expr
    

    def logic_or(self):
        """ logic_or       → logic_and ( "or" logic_and )* ; """
        expr = self.logic_and()

        while self.match("OR"):
            operator = self.previous_token()
            right = self.logic_and()
            expr = Logical(expr, operator, right)

        return expr
    

    def logic_and(self):
        """ logic_and      → equality ( "and" equality )* ; """
        expr = self.equality()

        while self.match("AND"):
            operator = self.previous_token()
            right = self.equality()
            expr = Logical(expr, operator, right)

        return expr

    
    def equality(self):
        """ equality       → comparison ( ( "!=" | "==" ) comparison )* ; """
        expr = self.comparison()

        while self.match(["EQUAL_EQUAL", "BANG_EQUAL"]):
            operator = self.previous_token() # '!=' or '=='
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr
    
    def comparison(self):
        """ comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ; """
        expr = self.term()

        while self.match(["GREATER", "GREATER_EQUAL", "LESS", "LESS_EQUAL"]):
            operator = self.previous_token()  # '>' / '>=' / '<' / '<='
            right = self.term()
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
        
        if self.match("IDENTIFIER"):
            return Variable(self.previous_token())
        
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