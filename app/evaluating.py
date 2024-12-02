from syntax import Literal, Grouping, Unary, Binary


def evaluate(node):
    # print(f"...evaluating node {node}")
    match node:
        case Literal() as lit:
            return lit.value
        
        case Grouping() as gp:
            return evaluate(gp.expr)
        
        case Unary() as unary:
            operator = unary.operator
            operand = evaluate(unary.right)
            match operator:
                case "!":
                    return not is_truthy(operand)
                case "-":
                    return -operand
                
        case Binary() as binary:
            left = evaluate(binary.left)
            right = evaluate(binary.right)
            operator = binary.operator
            match operator:
                # arithmetic + string concatenation
                case "*":
                    return left * right
                case "/":
                    return left / right
                case "-":
                    return left - right
                case "+":
                    # '+' is already overloaded to do string concatenation in Python, so we have it for free in Lox!
                    return left + right
                # relational
                case ">":
                    return left > right
                case ">=":
                    return left >= right
                case "<":
                    return left < right
                case "<=":
                    return left <= right

        case _:
            return NotImplementedError(node)
        

def is_truthy(value):
    """Lox's simple rule: false and nil are falsey, and everything else is truthy."""
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    return True
