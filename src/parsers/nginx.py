import re
from datetime import datetime

from src.exceptions import ParserError
from src.interfaces import LogParser
from src.models import LogEntry


class NginxParser(LogParser):
    # Ex: 127.0.0.1 - - [07/Jan/2026:13:55:36 +0300] "GET / HTTP/1.1" 200 ...
    LOG_PATTERN = re.compile(
        r'(?P<ip>\S+) \S+ \S+ \[(?P<time>.*?)\] "(?P<request>.*?)" (?P<status>\d+) (?P<bytes>\d+)'
    )
    DATE_FORMAT = "%d/%b/%Y:%H:%M:%S %z"
    SERVICE_NAME = "nginx-access"

    def parse(self, line: str) -> LogEntry | None:
        try:
            match = self.LOG_PATTERN.match(line)
            if not match:
                return None

            data = match.groupdict()
            dt_object = datetime.strptime(data["time"], self.DATE_FORMAT)

            return LogEntry(
                timestamp=dt_object,
                source_ip=data.get("ip", ""),
                message=data.get("request", ""),
                status_code=int(data.get("status", -1)),
                service_name=self.SERVICE_NAME,
                metadata={"bytes": int(data.get("bytes", 0))},
            )
        except Exception as e:
            raise ParserError(f"Nginx parse error: {str(e)}") from e
