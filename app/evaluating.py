from typing import Any
from environment import Environment
from errors import LoxRuntimeError
from functions import BreakException, LoxCallable, LoxUserFunction, ReturnException, register_native_functions
from output import stringify
from syntax import (Assign, Block, AbortLoop, Call, Expression, Function, If, Logical, NodeExpr, NodeStmt, 
                    Literal, Grouping, Print, Return, Unary, Binary, Var, Variable, While)


class Interpreter:
    def __init__(self) -> None:
        self.globals = Environment()  # always keep a reference to the global environment, for access to the native functions
        register_native_functions(self.globals)
        self.environment = self.globals  # the current environment in the stack
        self.in_loop = False

    def execute(self, node: NodeStmt) -> None:
        """Execute a statement
           (ie. a part of the Abstract-Syntax Tree that define a statement and thus has a side-effect at execution but don't return a value;
            this includes the root statement of the program; this also implies calling self.evaluate() when a expression is fed to the statement)"""
        match node:
            case If() as stmt:
                if self.is_truthy(self.evaluate(stmt.condition)):
                    self.execute(stmt.then_stmt)
                elif stmt.else_stmt:
                    self.execute(stmt.else_stmt)

            case Print() as stmt:
                value = self.evaluate(stmt.expr)
                print(stringify(value))

            case While() as stmt:
                self.in_loop = True
                while(self.is_truthy(self.evaluate(stmt.condition))):
                    try:
                        self.execute(stmt.body)
                    except BreakException as breaking:
                        toktype = breaking.args[0]
                        if toktype == "BREAK":
                            break
                        elif toktype == "CONTINUE":
                            pass  # let's evaluate the increment if it exists before starting the next loop
                    if stmt.increment:
                        self.evaluate(stmt.increment)
                self.in_loop = False

            case AbortLoop() as stmt:
                if not self.in_loop:
                    raise LoxRuntimeError(stmt.token, 
                                          f"Error at '{stmt.token.lexeme}': should only happen in loops (while or for).")
                raise BreakException(stmt.token.toktype)
        
            case Expression() as stmt:
                # do not display the value: discard it ; the statement's side-effect is the point
                value = self.evaluate(stmt.expr)

            case Var() as stmt:
                value = None
                if stmt.expr is not None:
                    value = self.evaluate(stmt.expr)
                self.environment.define(stmt.name.lexeme, value)

            case Block() as block:
                blockscope = Environment(enclosing=self.environment)
                self.execute_block(block.statements, environment=blockscope)

            case Function() as declaration:
                function = LoxUserFunction(declaration)
                self.environment.define(declaration.name.lexeme, function)

            case Return() as stmt:
                value = None
                if stmt.value:
                    value = self.evaluate(stmt.value)
                raise ReturnException(value)
        
            case _:
                raise NotImplementedError(node)
            

    def execute_block(self, statements, environment):
        """Execute a list of statements with a given environment/scope.
           Having a separated method for this allows to use it for regular blocks but also for function bodies etc."""
        previous_scope = self.environment
        try:
            self.environment = environment

            for stmt in statements:
                self.execute(stmt)
        finally:
            self.environment = previous_scope


    def evaluate(self, node: NodeExpr) -> Any:
        """Evaluate an expression 
           (ie. a part of the Abstract-Syntax Tree that define an expression and thus return a value at execution)"""
        # print(f"...evaluating node {node}")
        match node:
            case Literal() as lit:
                return lit.value
            
            case Grouping() as gp:
                return self.evaluate(gp.expr)
            
            case Unary() as unary:
                operand = self.evaluate(unary.right)
                match unary.operator.toktype:
                    case "BANG":
                        return not self.is_truthy(operand)
                    case "MINUS":
                        self.check_is_number(unary.operator, operand)
                        return -operand
                    
            case Binary() as binary:
                left = self.evaluate(binary.left)
                right = self.evaluate(binary.right)
                match binary.operator.toktype:
                    # arithmetic + string concatenation
                    case "STAR":
                        self.check_both_numbers(binary.operator, left, right)
                        return left * right
                    case "SLASH":
                        self.check_both_numbers(binary.operator, left, right)
                        return left / right
                    case "MINUS":
                        self.check_both_numbers(binary.operator, left, right)
                        return left - right
                    case "PLUS":
                        self.check_both_numbers_or_strings(binary.operator, left, right)
                        # '+' is already overloaded to do string concatenation in Python, so we have it for free in Lox!
                        return left + right
                    # relational
                    case "GREATER":
                        self.check_both_numbers(binary.operator, left, right)
                        return left > right
                    case "GREATER_EQUAL":
                        self.check_both_numbers(binary.operator, left, right)
                        return left >= right
                    case "LESS":
                        self.check_both_numbers(binary.operator, left, right)
                        return left < right
                    case "LESS_EQUAL":
                        self.check_both_numbers(binary.operator, left, right)
                        return left <= right
                    # equality
                    case "EQUAL_EQUAL":
                        # again equality (==) and non-equality (!=) operators are correctly overloaded for the various types 
                        # of left/right expressions in Python we may encounter, so life is beautiful
                        return left == right
                    case "BANG_EQUAL":
                        return left != right
                    
            case Logical() as logical:
                left = self.evaluate(logical.left)

                # short-circuit ?
                if logical.operator.toktype == "OR":
                    if self.is_truthy(left):
                        return left
                elif logical.operator.toktype == "AND":
                    if not self.is_truthy(left):
                        return left
                    
                return self.evaluate(logical.right)
                    
            case Variable() as variable:
                return self.environment.get(variable.name)
            
            case Assign() as assignment:
                value = self.evaluate(assignment.value)
                self.environment.assign(assignment.name, value)
                return value
            
            case Call() as call:
                # the callee part evaluates to the actual function to be called
                function = self.evaluate(call.callee)

                if not isinstance(function, LoxCallable):
                    raise LoxRuntimeError(call.paren, "Can only call functions and classes.")

                arguments = [self.evaluate(arg) for arg in call.arguments]

                if len(arguments) != function.arity():
                    raise LoxRuntimeError(call.paren, f"Expected {function.arity()} arguments but got {len(arguments)}.")

                return function.call(self, arguments)

            case _:
                raise NotImplementedError(node)
            

    def is_truthy(self, value):
        """Lox's simple rule: false and nil are falsey, and everything else is truthy."""
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        return True


    def check_is_number(self, operator, value):
        if isinstance(value, float):
            return
        raise LoxRuntimeError(operator, "Operand must be a number.")
    

    def check_both_numbers(self, operator, left, right):
        if isinstance(left, float) and isinstance(right, float):
            return
        raise LoxRuntimeError(operator, "Operands must be numbers.")
    

    def check_both_numbers_or_strings(self, operator, left, right):
        if ((isinstance(left, float) and isinstance(right, float)) or
            (isinstance(left, str) and isinstance(right, str))):
            return
        raise LoxRuntimeError(operator, "Operands must be two numbers or two strings.")
