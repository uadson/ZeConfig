import json
import os

import yaml

from src.manager import ConfigManager

JSON_FILE = 'config.json'
TOML_FILE = 'config.toml'
YAML_FILE = 'config.yaml'
ENV_FILE = '.env'

JSON_CONTENT = {'DATABASE_URL': 'postgres://json_user:pass@localhost/db'}
TOML_CONTENT = "'database_url' = 'postgres://toml_user:pass@localhost/db'"
YAML_CONTENT = {'database_url': 'postgres://yaml_user:pass@localhost/db'}
ENV_CONTENT = 'DATABASE_URL=postgres://env_user:pass@localhost/db'


def setup_module(module):
    with open(JSON_FILE, 'w', encoding='utf-8') as file:
        json.dump(JSON_CONTENT, file)
    with open(TOML_FILE, 'w', encoding='utf-8') as file:
        file.write(TOML_CONTENT)
    with open(YAML_FILE, 'w', encoding='utf-8') as file:
        yaml.dump(YAML_CONTENT, file)
    with open(ENV_FILE, 'w', encoding='utf-8') as file:
        file.write(ENV_CONTENT)


def teardown_module(module):
    os.remove(JSON_FILE)
    os.remove(TOML_FILE)
    os.remove(YAML_FILE)
    os.remove(ENV_FILE)


def test_json_config_manager():
    ConfigManager._config_data.clear()
    ConfigManager._load_file(JSON_FILE)
    assert ConfigManager.get('DATABASE_URL') == JSON_CONTENT['DATABASE_URL']


# import tempfile
# from unittest.mock import patch

# from src.manager import ConfigManager


# @patch('src.manager.settings.BASE_DIR', tempfile.gettempdir())
# def test_json_config_manager(json_file):
#     file_path, expected_conf = json_file
#     ConfigManager._config_data.clear()
#     ConfigManager._load_file(file_path)
#     assert ConfigManager.get('DATABASE_URL') == expected_conf['DATABASE_URL']


# @patch('src.manager.settings.BASE_DIR', tempfile.gettempdir())
# def test_toml_config_manager(toml_file):
#     file_path, expected_conf = toml_file
#     ConfigManager._config_data.clear()
#     ConfigManager._load_file(file_path)
#     assert ConfigManager.get('database_url') == expected_conf['database_url']
