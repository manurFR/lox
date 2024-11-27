import sys

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

    tokens, errors = tokenize(file_contents)

    match command:
        case "tokenize":
            print_errors(errors)
            for tok in tokens:
                print(tok)
            if errors:
                sys.exit(65)
        
        case "parse":
            if errors:
                print("Errors found in scanning phase. Aborting.")
                print_errors(errors)
                sys.exit(65)
            
            parser = Parser(tokens)
            expression = parser.expression()
            print(expression)


def print_errors(errors):
    for line, message in errors:
        print(f"[line {line}] Error: {message}", file=sys.stderr)


if __name__ == "__main__":
    main()
