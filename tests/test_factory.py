import pytest

from src.exceptions import ConfigurationError
from src.factory import ParserFactory
from src.parsers.nginx import NginxParser


def test_factory_creates_nginx_parser():
    """
    Scenario: Requesting 'nginx' parser type.
    Expectation: Should return an instance of NginxAccessParser.
    """
    parser = ParserFactory.get_parser("nginx")
    assert isinstance(parser, NginxParser)


def test_factory_raises_error_on_unknown_type():
    """
    Scenario: Requesting an undefined parser type (e.g., 'apache').
    Expectation: Should raise a ConfigurationError.
    """
    with pytest.raises(ConfigurationError):
        ParserFactory.get_parser("unknown_parser_type")
