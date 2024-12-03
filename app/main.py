import sys

from errors import Errors
from scanning import Token, tokenize
from parsing import Parser
from evaluating import Interpreter, LoxRuntimeError
from syntax import NodeStmt

AVAILABLE_COMMANDS = ['tokenize', 'parse', 'evaluate']


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
            statements = do_parse(tokens)
            print(statements)
            check_errors()

        case "evaluate":
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


def do_parse(tokens) -> list[NodeStmt]:
    parser = Parser(tokens)
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
