import os

from ze.src.core import get_file_data, parse_data


def test_parse_data_json_file(path, empty_config_data):
    """
    Tests parsing data from a JSON configuration file.

    Args:
        path: The path to the directory containing configuration files.
        empty_config_data: An empty dictionary for config data.
    """
    file = 'config.json'
    config_data = empty_config_data
    parse_data(config_data, path, file)

    assert config_data == {'DATABASE_URL': 'postgres://json_user:pass@localhost/db'}


def test_parse_data_toml_file(path, empty_config_data):
    """
    Tests parsing data from a TOML configuration file.

    Args:
        path: The path to the directory containing configuration files.
        empty_config_data: An empty dictionary for config data.
    """
    file = 'config.toml'
    config_data = empty_config_data
    parse_data(config_data, path, file)

    assert config_data == {'database_url': 'postgres://toml_user:pass@localhost/db'}


def test_parse_data_yaml_file(path, empty_config_data):
    """
    Tests parsing data from a YAML configuration file.

    Args:
        path: The path to the directory containing configuration files.
        empty_config_data: An empty dictionary for config data.
    """
    file = 'config.yaml'
    config_data = empty_config_data
    parse_data(config_data, path, file)

    assert config_data == {'DATABASE_URL_YAML': 'postgres://yaml_user:pass@localhost/db'}


def test_parse_data_env_file(path, empty_config_data):
    """
    Tests parsing data from a ENV configuration file.

    Args:
        path: The path to the directory containing configuration files.
        empty_config_data: An empty dictionary for config data.
    """
    file = 'config.env'
    config_data = empty_config_data
    parse_data(config_data, path, file)

    assert config_data == {'DATABASE_URL_ENV': 'postgres://env_user:pass@localhost/db'}


def test_parse_data_env_file_env(path, empty_config_data):
    """
    Tests parsing data from a ENV configuration file.

    Args:
        path: The path to the directory containing configuration files.
        empty_config_data: An empty dictionary for config data.
    """
    file = '.env'
    config_data = empty_config_data
    env_file_path = os.path.join(path, file)
    with open(env_file_path, 'w', encoding='utf-8') as f:
        f.write('DATABASE_URL_ENV_START=postgres://env_user:pass@localhost/db')

    parse_data(config_data, path, file)

    assert config_data == {'DATABASE_URL_ENV_START': 'postgres://env_user:pass@localhost/db'}


def test_get_file_data(path, empty_config_data, empty_config_files):
    """
    Tests retrieving and parsing data from all configuration files in a directory.

    Args:
        path: The path to the directory containing configuration files.
        empty_config_data: An empty dictionary for config data.
        empty_config_files: An empty list for config files.
    """
    config_data = empty_config_data
    config_files = empty_config_files

    get_file_data(config_files, config_data, path)
    assert sorted(config_files) == sorted([
        'config.json',
        'config.toml',
        'config.yaml',
        'config.yml',
        'config.env',
        '.env',
    ])
    assert config_data == {
        'DATABASE_URL': 'postgres://json_user:pass@localhost/db',
        'database_url': 'postgres://toml_user:pass@localhost/db',
        'DATABASE_URL_YAML': 'postgres://yaml_user:pass@localhost/db',
        'DATABASE_URL_YML': 'postgres://yml_user:pass@localhost/db',
        'DATABASE_URL_ENV': 'postgres://env_user:pass@localhost/db',
        'DATABASE_URL_ENV_START': 'postgres://env_user:pass@localhost/db',
    }
