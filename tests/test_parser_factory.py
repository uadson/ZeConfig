import pytest

from src.factory import ParserFactory
from src.models import ENVParser, JSONParser, TOMLParser, YAMLParser


def test_get_parser_valid_extension():
    assert isinstance(ParserFactory.get_parser('config.json'), JSONParser)
    assert isinstance(ParserFactory.get_parser('config.toml'), TOMLParser)
    assert isinstance(ParserFactory.get_parser('config.yml'), YAMLParser)
    assert isinstance(ParserFactory.get_parser('config.yaml'), YAMLParser)
    assert isinstance(ParserFactory.get_parser('config.env'), ENVParser)


def test_get_parser_invalid_extension():
    with pytest.raises(ValueError, match="Unsupported file extension: '.xml'."):
        ParserFactory.get_parser('config.xml')
