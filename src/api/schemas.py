from datetime import datetime
from typing import Any, Dict, List


from pydantic import BaseModel

class ParseRequest(BaseModel):
    """Schema for a single log parsing request."""
    raw_log: str

class BatchParseRequest(BaseModel):
    """Schema for batch log parsing request (multiple lines)."""
    raw_logs: List[str]

class LogEntryResponse(BaseModel):
    """Schema for the standardized log response."""
    timestamp: datetime
    source_ip: str
    message: str
    status_code: int
    service_name: str
    metadata: Dict[str, Any]

class ErrorResponse(BaseModel):
    """Schema for error messages."""
    detail: str
