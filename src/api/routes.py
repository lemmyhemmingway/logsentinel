from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from src.api.schemas import BatchParseRequest, LogEntryResponse, ParseRequest
from src.exceptions import ConfigurationError, ParserError
from src.factory import ParserFactory

router = APIRouter()


@router.get(
    "/health",
    tags=["System"],
)
def health_check():
    """Returns system status"""
    return {"status": "active"}


@router.post(
    "/parse/{parser_type}",
    response_model=LogEntryResponse,
    tags=["Log Process"],
)
def parse_log(parser_type: str, request: ParseRequest):
    """
    Parses a single raw log line using the specified parser type.

    - **parser_type**: nginx, apache, syslog, etc. (Must be defined in Factory)
    """
    try:
        parser = ParserFactory.get_parser(parser_type)

        result = parser.parse(request.raw_log)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="log line cannot be parsed",
            )
        return result

    except ConfigurationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid parser type: {str(e)}",
        )
    except ParserError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Parsing Error {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail,
        )


@router.post(
    "/parse/{parser_type}/batch",
    response_model=list[LogEntryResponse],
    tags=["Log Processing"],
)
def parse_batch_logs(parser_type: str, request: BatchParseRequest):
    """
    Parses a list of raw log lines using the specified parser type.
    Failed lines are silently skipped to ensure bulk processing continuity.
    """
    try:
        # 1. Validate parser type once before the loop
        parser = ParserFactory.get_parser(parser_type)
    except ConfigurationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid Parser Type: {e}",
        )

    results = []

    # 2. Process logs
    for line in request.raw_logs:
        try:
            entry = parser.parse(line)
            if entry:
                results.append(entry)
        except Exception:
            # Skip malformed lines in batch mode
            continue

    return results
