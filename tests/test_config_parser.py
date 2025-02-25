import pytest

from src.models import ENVParser, JSONParser, TOMLParser, YAMLParser


def test_json_parser(json_file):
    file_path, expected_conf = json_file
    assert JSONParser.parse(file_path) == expected_conf


def test_toml_parser(toml_file):
    file_path, excepted_conf = toml_file
    assert TOMLParser.parse(file_path) == excepted_conf


def test_yaml_parser(yaml_file):
    file_path, expected_conf = yaml_file
    assert YAMLParser.parse(file_path) == expected_conf


def test_env_parser(toml_file):
    file_path, excepted_conf = toml_file
    assert ENVParser.parse(file_path) == excepted_conf


def test_file_not_found():
    """Test error when trying to load a non-existent file."""
    with pytest.raises(FileNotFoundError):
        JSONParser.parse('file_non_existent.json')
