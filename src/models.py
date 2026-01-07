from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Dict

@dataclass
class LogEntry:
    timestamp: datetime
    source_ip: str
    message: str
    status_code: int = 0
    service_name: str = "unknown" #which service
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> Dict[str, Any]:
        """json serializer"""
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data
