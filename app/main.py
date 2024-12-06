import sys

from output import stringify
from errors import Errors, LoxRuntimeError
from scanning import Token, tokenize
from parsing import Parser
from evaluating import Interpreter
from syntax import Expression, NodeStmt

AVAILABLE_COMMANDS = ['tokenize', 'parse', 'evaluate', 'run']


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh {tokenize|parse} <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command not in AVAILABLE_COMMANDS:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

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
                operator, value, message = e.args
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
                operator, value, message = e.args
                print(f"{message}\n[line {operator.line}]", file=sys.stderr)
                sys.exit(70)      


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
