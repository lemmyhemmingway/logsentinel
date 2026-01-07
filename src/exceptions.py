class LogSentinelError(Exception):
    """Base log sentinel error"""

    pass


class ParserError(LogSentinelError):
    """Errors when parsing fails"""

    pass


class ConfigurationError(LogSentinelError):
    """Errors when reading configuration"""

    pass
