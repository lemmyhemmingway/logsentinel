import sys
from src.exceptions import LogSentinelError
from src.factory import ParserFactory


def main():
    print("Starting sentinel")

    try:
        selected_type = "nginx"
        parser = ParserFactory.get_parser(selected_type)
        print(f"Selected parser: {selected_type}")
        test_log = '192.168.1.100 - - [07/Jan/2026:14:30:00 +0300] "GET /api/v1/users HTTP/1.1" 200 4096'

        entry = parser.parse(test_log)
        if entry:
            print(entry)
        else:
            print("unknown format")

    except LogSentinelError as e:
        print(f"Error {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
