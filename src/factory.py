from src.exceptions import ConfigurationError
from src.interfaces import LogParser
from src.parsers.nginx import NginxParser


class ParserFactory:
    """Get parser"""

    _parsers = {
        "nginx": NginxParser,
        # will add another parsers here ( ex: syslog )
    }

    @staticmethod
    def get_parser(parser_type: str) -> LogParser:
        parser_class = ParserFactory._parsers.get(parser_type)
        if not parser_class:
            raise ConfigurationError(f"unsupported parser type: {parser_type}")
        return parser_class()
