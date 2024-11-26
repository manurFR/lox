import sys

from app.scanning import tokenize


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    errors = None
    if file_contents:
        tokens, errors = tokenize(file_contents)
        for line, message in errors:
            print(f"[line {line}] Error: {message}", file=sys.stderr)
        for tok, char, val in tokens:
            print(f"{tok} {char} {val if val is not None else 'null'}")
    
    print("EOF  null")

    if errors:
        sys.exit(65)


if __name__ == "__main__":
    main()
