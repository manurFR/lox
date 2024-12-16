from pprint import pprint
import sys

from output import stringify
from errors import Errors, LoxRuntimeError
from scanning import Token, tokenize
from parsing import Parser
from evaluating import Interpreter
from syntax import Expression, NodeStmt

AVAILABLE_COMMANDS = ['tokenize', 'parse', 'evaluate', 'run', 'repl']


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 2:
        print("Usage: ./your_program.sh {tokenize|parse|evaluate|run|repl} [<filename>]", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    if len(sys.argv) == 3:
        filename = sys.argv[2]

    if command not in AVAILABLE_COMMANDS:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    if command != 'repl':
        with open(filename) as file:
            file_contents = file.read()

    match command:
        case "tokenize":
            tokens = do_tokenize(file_contents)
            for tok in tokens:
                print(tok)
            check_errors()
                
        case "parse":
            tokens = do_tokenize(file_contents)
            check_errors()
            expressions = do_parse(tokens, lenient=True)
            if expressions:
                print(expressions[0])
            check_errors()

        case "evaluate":
            tokens = do_tokenize(file_contents)
            check_errors()
            # 'evaluate' implies one expression only in the source file, for now
            expressions = do_parse(tokens, lenient=True)
            check_errors()
            if not isinstance(expressions[0], Expression):
                print("Command 'evaluate' expected a single expression.")
                sys.exit(70)
            expr = expressions[0].expr
            try:
                interpreter = Interpreter()
                output = interpreter.evaluate(expr)
                print(stringify(output))
            except LoxRuntimeError as e:
                operator, message = e.args
                print(f"{message}\n[line {operator.line}]", file=sys.stderr)
                sys.exit(70)

        case "run":
            tokens = do_tokenize(file_contents)
            check_errors()
            statements = do_parse(tokens)
            check_errors()
            try:
                do_evaluation(statements)
            except LoxRuntimeError as e:
                token, message = e.args
                print(f"{message}\n[line {token.line}]", file=sys.stderr)
                sys.exit(70)

        case "repl":
            interpreter = Interpreter()
            print("Welcome to Lox REPL")
            try:
                while line := input(">>> "):
                    if line.strip().lower() in ('exit', 'quit'):
                        raise EOFError
                    tokens = do_tokenize(line.strip())
                    statements = do_parse(tokens)
                    try:
                        for stmt in statements:
                            interpreter.execute(stmt)
                    except LoxRuntimeError as e:
                        token, message = e.args
                        print(f"{message}\n[line {token.line}]", file=sys.stderr)
            except EOFError:
                print()
                print("Bye.")
                sys.exit(0)

def do_tokenize(content) -> list[Token]:
    tokens, errs = tokenize(content)
    for line, message in errs:
        Errors.report(line, message)
    return tokens


def do_parse(tokens, lenient=False) -> list[NodeStmt]:
    parser = Parser(tokens, lenient)
    return parser.parse()


def do_evaluation(statements: list[NodeStmt]):
    interpreter = Interpreter()
    # feed each statement to the interpreter one by one, keeping the common state up-to-date
    for stmt in statements:
        # each statement is an Abstract-Syntax Tree
        interpreter.execute(stmt)


def check_errors():
    if Errors.had_errors:
        sys.exit(65)



if __name__ == "__main__":
    main()
