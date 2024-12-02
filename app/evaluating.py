from syntax import Literal


def evaluate(node):
    match node:
        case Literal(float()):
            """Print the number 'with the minimum number of decimal places without losing precision'."""
            return str(node.value).rstrip("0").rstrip(".")

        case Literal():
            return repr(node)
        
        case _:
            return NotImplementedError(node)