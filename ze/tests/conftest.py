import json
import os
import tempfile

import pytest

from ze.src.manager import ConfigManager
from ze.src.settings import settings


@pytest.fixture
def json_file():
    """Create a temporary JSON file for tests"""

    conf = {'DATABASE_URL': 'postgres://json_user:pass@localhost/db'}

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as tmp_file:
        json.dump(conf, tmp_file)
        tmp_file_path = tmp_file.name

    return tmp_file_path, conf


@pytest.fixture
def toml_file():
    """Create a temporary TOML file for tests"""

    conf = "database_url = 'postgres://toml_user:pass@localhost/db'"

    with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False, encoding='utf-8') as tmp_file:
        tmp_file.write(conf)
        tmp_file.flush()
        tmp_file_path = tmp_file.name
        yield (
            tmp_file_path,
            {'database_url': 'postgres://toml_user:pass@localhost/db'},
        )


@pytest.fixture
def yaml_file():
    """Create a temporary YAML file for tests"""

    conf = {'DATABASE_URL': 'postgres://yaml_user:pass@localhost/db'}

    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, encoding='utf-8') as tmp_file:
        json.dump(conf, tmp_file)
        tmp_file_path = tmp_file.name

    return tmp_file_path, conf


@pytest.fixture
def env_file():
    """Create a temporary TOML file for tests"""

    conf = 'database_url=postgres://env_user:pass@localhost/db\n'

    with tempfile.NamedTemporaryFile(mode='wb', suffix='.env', delete=False) as tmp_file:
        tmp_file.write(conf.encode())
        tmp_file_path = tmp_file.name

    return tmp_file_path, {'database_url': 'postgres://env_user:pass@localhost/db'}


def create_test_file(file_path: str, content: str):
    """
    Creates a test file with the given content.

    Args:
        file_path: The path to the file to create.
        content: The content to write to the file.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


@pytest.fixture(autouse=True)
def reset_config_manager():
    """Resets ConfigManager state before each test."""
    ConfigManager._files_checked = False
    ConfigManager._config_data = {}
    ConfigManager._config_files = []


@pytest.fixture
def path(tmp_path):
    """
    Creates a temporary directory with configuration files for testing.

    This fixture creates a temporary directory structure with configuration files
    in JSON, TOML, YAML, and YML formats. It also populates the `settings` module
    with the paths to the base directory and configuration directory.

    Yields:
        The path to the temporary base directory.
    """
    conf_dir = tmp_path / 'configs'
    conf_dir.mkdir(parents=True, exist_ok=True)

    json_content = '{"DATABASE_URL": "postgres://json_user:pass@localhost/db"}'
    toml_content = "database_url = 'postgres://toml_user:pass@localhost/db'"
    yaml_content = '{"DATABASE_URL_YAML": "postgres://yaml_user:pass@localhost/db"}'
    yml_content = '{"DATABASE_URL_YML": "postgres://yml_user:pass@localhost/db"}'
    env_content = 'DATABASE_URL_ENV=postgres://env_user:pass@localhost/db\n'
    env_content_on_start = 'DATABASE_URL_ENV_START=postgres://env_user:pass@localhost/db\n'

    settings.BASE_DIR = tmp_path
    settings.CONF_DIR = conf_dir

    create_test_file(os.path.join(tmp_path, 'config.json'), json_content)
    create_test_file(os.path.join(tmp_path, 'config.toml'), toml_content)
    create_test_file(os.path.join(tmp_path, 'config.yaml'), yaml_content)
    create_test_file(os.path.join(tmp_path, 'config.yml'), yml_content)
    create_test_file(os.path.join(tmp_path, 'config.env'), env_content)
    create_test_file(os.path.join(tmp_path, '.env'), env_content_on_start)

    create_test_file(os.path.join(conf_dir, 'config.json'), json_content)
    create_test_file(os.path.join(conf_dir, 'config.toml'), toml_content)
    create_test_file(os.path.join(conf_dir, 'config.yaml'), yaml_content)
    create_test_file(os.path.join(conf_dir, 'config.yml'), yml_content)
    create_test_file(os.path.join(conf_dir, 'config.env'), env_content)
    create_test_file(os.path.join(conf_dir, '.env'), env_content_on_start)

    yield tmp_path

    if os.path.exists(os.path.join(tmp_path, 'config.json')):
        os.remove(os.path.join(tmp_path, 'config.json'))
    if os.path.exists(os.path.join(tmp_path, 'config.toml')):
        os.remove(os.path.join(tmp_path, 'config.toml'))
    if os.path.exists(os.path.join(tmp_path, 'config.yaml')):
        os.remove(os.path.join(tmp_path, 'config.yaml'))
    if os.path.exists(os.path.join(tmp_path, 'config.yml')):
        os.remove(os.path.join(tmp_path, 'config.yml'))
    if os.path.exists(os.path.join(tmp_path, 'config.env')):
        os.remove(os.path.join(tmp_path, 'config.env'))
    if os.path.exists(os.path.join(tmp_path, '.env')):
        os.remove(os.path.join(tmp_path, '.env'))

    if os.path.exists(os.path.join(conf_dir, 'config.json')):
        os.remove(os.path.join(conf_dir, 'config.json'))
    if os.path.exists(os.path.join(conf_dir, 'config.toml')):
        os.remove(os.path.join(conf_dir, 'config.toml'))
    if os.path.exists(os.path.join(conf_dir, 'config.yaml')):
        os.remove(os.path.join(conf_dir, 'config.yaml'))
    if os.path.exists(os.path.join(conf_dir, 'config.yml')):
        os.remove(os.path.join(conf_dir, 'config.yml'))
    if os.path.exists(os.path.join(conf_dir, 'config.env')):
        os.remove(os.path.join(conf_dir, 'config.env'))
    if os.path.exists(os.path.join(conf_dir, '.env')):
        os.remove(os.path.join(conf_dir, '.env'))

    os.rmdir(settings.CONF_DIR)
    os.rmdir(settings.BASE_DIR)


@pytest.fixture
def empty_config_data() -> dict:
    """
    Provides an empty dictionary for config data.

    Returns:
        An empty dictionary.
    """
    return {}


@pytest.fixture
def empty_config_files() -> list:
    """
    Provides an empty list for config files.

    Returns:
        An empty list.
    """
    return []
