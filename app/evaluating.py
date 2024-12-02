from syntax import Literal


def evaluate(node):
    match node:
        case Literal():
            return repr(node)
        
        case _:
            return NotImplementedError(node)