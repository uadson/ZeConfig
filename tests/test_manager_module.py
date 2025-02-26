import os

import pytest

from src.manager import ConfigManager
from src.settings import settings


def test_load_config_json_file_in_configs_dir(path):
    """
    Tests loading a JSON configuration file from the 'configs' directory.

    Args:
        path: The path to the temporary directory containing configuration files.
    """
    ConfigManager._load_config_files()
    assert 'config.json' in ConfigManager._config_files
    assert ConfigManager._config_data['DATABASE_URL'] == 'postgres://json_user:pass@localhost/db'


def test_load_config_json_file_in_base_dir(path):
    """
    Tests loading a JSON configuration file from the base directory when the 'configs' directory is unavailable.

    Args:
        path: The path to the temporary directory containing configuration files.
    """
    original_conf_dir = settings.CONF_DIR
    os.remove(os.path.join(settings.CONF_DIR, 'config.json'))
    settings.CONF_DIR = 'non_existent_dir'
    ConfigManager._load_config_files()
    settings.CONF_DIR = original_conf_dir
    assert 'config.json' in ConfigManager._config_files


def test_get_key_config_value(path):
    """
    Tests retrieving a configuration value by key.

    Args:
        path: The path to the temporary directory containing configuration files.
    """
    ConfigManager._load_config_files()
    value = ConfigManager.get('DATABASE_URL')
    assert value == 'postgres://json_user:pass@localhost/db'


def test_get_value_default(path):
    """
    Tests retrieving a default value when a configuration key is not found.

    Args:
        path: The path to the temporary directory containing configuration files.
    """
    value = ConfigManager.get('nonexistent_key', 'default_value')
    assert value == 'default_value'


def test_get_value_raises_error(path):
    """
    Tests that a ValueError is raised when a configuration key is not found and no default value is provided.

    Args:
        path: The path to the temporary directory containing configuration files.
    """
    with pytest.raises(KeyError, match="""Key: 'nonexistent_key' not found or file non exists"""):
        ConfigManager.get('nonexistent_key')
