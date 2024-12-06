import sys


class Errors:
    had_errors = False

    @classmethod
    def report(cls, line: int, message: str, where: str = ""):
        cls.had_errors = True
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)


class LoxRuntimeError(RuntimeError):
    pass
