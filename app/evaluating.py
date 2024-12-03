from syntax import Literal, Grouping, Unary, Binary

class Interpreter:
    def evaluate(self, node):
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
                        return left * right
                    case "SLASH":
                        return left / right
                    case "MINUS":
                        return left - right
                    case "PLUS":
                        # '+' is already overloaded to do string concatenation in Python, so we have it for free in Lox!
                        return left + right
                    # relational
                    case "GREATER":
                        return left > right
                    case "GREATER_EQUAL":
                        return left >= right
                    case "LESS":
                        return left < right
                    case "LESS_EQUAL":
                        return left <= right
                    # equality
                    case "EQUAL_EQUAL":
                        # again equality (==) and non-equality (!=) operators are correctly overloaded for the various types 
                        # of left/right expressions in Python we may encounter, so life is beautiful
                        return left == right
                    case "BANG_EQUAL":
                        return left != right

            case _:
                return NotImplementedError(node)
            

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
        raise LoxRuntimeError(operator, value, "Operand must be a number.")


class LoxRuntimeError(RuntimeError):
    pass
