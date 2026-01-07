from abc import ABC, abstractmethod
from typing import Optional

from src.models import LogEntry


class LogParser(ABC):
    @abstractmethod
    def parse(self, line: str) -> Optional[LogEntry]:
        """Return Log Entry or None if fails"""
        pass
