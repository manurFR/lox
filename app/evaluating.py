from syntax import Grouping, Literal, Unary


def evaluate(node):
    match node:
        # case Literal(float()):
        #     """Print the number 'with the minimum number of decimal places without losing precision'."""
        #     return str(node.value).rstrip("0").rstrip(".")

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

        case _:
            return NotImplementedError(node)
        

def is_truthy(value):
    """Lox's simple rule: false and nil are falsey, and everything else is truthy."""
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    return True
