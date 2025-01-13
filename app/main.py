import sys

from output import stringify
from errors import Errors, LoxRuntimeError
from resolving import Resolver
from scanning import tokenize
from parsing import Parser
from evaluating import Interpreter
from syntax import Expression

AVAILABLE_COMMANDS = ['tokenize', 'parse', 'ast', 'evaluate', 'run', 'repl']


def usage(exitcode=0, msg=None):
    if msg:
        print(msg, file=sys.stderr)
    print(f"Usage: ./lox.sh [{{{'|'.join(AVAILABLE_COMMANDS)}}} [<filename>]]", file=sys.stderr)
    exit(exitcode)


def process(interpreter: Interpreter, command: str, source: str, exit_on_errors: bool = True):
    # scanning/tokenizing
    tokens, errs = tokenize(source)
    for line, message in errs:
        Errors.report(line, message)
    
    if command == "tokenize":
        for tok in tokens:
            print(tok)
        check_errors()
        exit(0)

    # parsing (only 'run' requires semicolon at the end of expressions, ie. all others are lenient)
    parser = Parser(tokens, lenient=(command != 'run'))
    statements = parser.parse()

    if command == "parse":
        for stmt in statements:
            print(stmt)
        check_errors()
        exit(0)
    if command == "ast":
        for stmt in statements:
            stmt.print_ast()
        check_errors()
        exit(0)       

    # exit if syntax errors before semantic pass
    if exit_on_errors:
        check_errors()

    # semantic analysis pass
    resolver = Resolver(interpreter)
    resolver.resolve_statements(statements)

    # exit if semantic errors before evaluating
    if exit_on_errors:
        check_errors()

    # evaluating/executing
    try:
        # feed each statement to the interpreter one by one, keeping the common state up-to-date
        for stmt in statements:

            # shortcut to quick evaluation of expressions
            if (command in ["evaluate", "repl"]) and isinstance(stmt, Expression):
                output = interpreter.evaluate(stmt.expr)
                print(stringify(output))

                if command == "evaluate":
                    exit(0)
            
            # full execution of a statement
            else:
                interpreter.execute(stmt)

    except LoxRuntimeError as e:
        token, message = e.args
        print(f"{message}\n[line {token.line}]", file=sys.stderr)
        if exit_on_errors:
            exit(70)


def main():
    # arguments
    if len(sys.argv) <= 1:
        command = "repl"
    else:
        command = sys.argv[1]

    if command in ("help", "-h"):
        usage(exitcode=0)

    if command not in AVAILABLE_COMMANDS:
        usage(exitcode=1, msg=f"Unknown command: {command}")

    if command != "repl":
        if len(sys.argv) < 3:
            usage(exitcode=1)

        filename = sys.argv[2]
        with open(filename) as file:
            file_contents = file.read()

    # scanner/parser/interpreter
    interpreter = Interpreter()

    if command == "repl":
        print("Welcome to Lox REPL")
        try:
            while line := input(">>> "):
                if line.strip().lower() in ('exit', 'quit'):
                    raise EOFError("quit")
                process(interpreter, command, line.strip(), exit_on_errors=False)
        except EOFError as eof:
            if not eof.args:
                print()
            print("Bye.")
            sys.exit(0)
    else:
        process(interpreter, command, file_contents)


def check_errors():
    if Errors.had_errors:
        sys.exit(65)


if __name__ == "__main__":
    main()
