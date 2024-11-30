import sys

from errors import Errors
from app.scanning import tokenize
from app.parsing import Parser

AVAILABLE_COMMANDS = ['tokenize', 'parse']


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
                
        case "parse":
            tokens = do_tokenize(file_contents)
            if Errors.had_errors:
                print("Errors found in scanning phase. Aborting.", file=sys.stderr)
            else:
                ast_root = do_parse(tokens)
                print(ast_root)

    if Errors.had_errors:
        sys.exit(65)


def do_tokenize(content):
    tokens, errs = tokenize(content)
    for line, message in errs:
        Errors.report(line, message)
    return tokens


def do_parse(tokens):
    parser = Parser(tokens)
    return parser.parse()


if __name__ == "__main__":
    main()
