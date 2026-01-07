from abc import ABC, abstractmethod

from src.models import LogEntry


class LogParser(ABC):
    @abstractmethod
    def parse(self, line: str) -> LogEntry | None:
        """Return Log Entry or None if fails"""
        pass
