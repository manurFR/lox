from typing import Any


def stringify(value: Any) -> str:
    """Format the result of evaluated expressions, depending on their type"""
    match value:
        case float():
            # print the number 'with the minimum number of decimal places without losing precision'
            return str(value).rstrip("0").rstrip(".")
        
        case None:
            return "nil"
        
        case bool():
            return str(value).lower()
        
        case _ as other:
            return value