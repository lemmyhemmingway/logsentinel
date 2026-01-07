import sys

from src.config import ConfigLoader
from src.exceptions import LogSentinelError
from src.factory import ParserFactory


def main():
    print("LogSentinel Starting...")

    try:
        # 1. Load Configuration
        config = ConfigLoader.load_config("config.yaml")
        app_name = config.get("app", {}).get("name")
        active_parser = config.get("parser", {}).get("active_type")

        print(f"Config Loaded: {app_name}")

        # 2. Request Parser from Factory
        parser = ParserFactory.get_parser(active_parser)
        print(f"Active Parser: {active_parser.upper()}")

        # 3. Simulate Log Processing
        test_log = '192.168.1.100 - - [07/Jan/2026:14:30:00 +0300] "GET /api/v1/users HTTP/1.1" 200 4096'

        entry = parser.parse(test_log)

        if entry:
            print(f"Result: {entry.to_json()}")
        else:
            print("Failed to parse log line.")

    except LogSentinelError as e:
        print(f"CRITICAL ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
