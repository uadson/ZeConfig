import json
import tempfile

import pytest


@pytest.fixture
def json_file():
    """Create a temporary JSON file for tests"""

    conf = {'DATABASE_URL': 'postgres://json_user:pass@localhost/db'}

    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.json', delete=False, encoding='utf-8'
    ) as tmp_file:
        json.dump(conf, tmp_file)
        tmp_file_path = tmp_file.name

    return tmp_file_path, conf


@pytest.fixture
def toml_file():
    """Create a temporary TOML file for tests"""

    conf = "database_url = 'postgres://toml_user:pass@localhost/db'"

    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.toml', delete=False, encoding='utf-8'
    ) as tmp_file:
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

    conf = {'DATABASE_URL': 'postgres://json_user:pass@localhost/db'}

    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.yaml', delete=False, encoding='utf-8'
    ) as tmp_file:
        json.dump(conf, tmp_file)
        tmp_file_path = tmp_file.name

    return tmp_file_path, conf


@pytest.fixture
def env_file():
    """Create a temporary TOML file for tests"""

    conf = 'database_url=postgres://toml_user:pass@localhost/db\n'

    with tempfile.NamedTemporaryFile(
        mode='wb', suffix='.env', delete=False
    ) as tmp_file:
        tmp_file.write(conf.encode())
        tmp_file_path = tmp_file.name

    return tmp_file_path, 'database_url=postgres://toml_user:pass@localhost/db'


# import json
# import os

# import pytest
# import yaml

# test_files = {
#     'config.json': {'DATABASE_URL': 'postgres://json_user:pass@localhost/db'},
#     'config.toml': 'database_url = "postgres://toml_user:pass@localhost/db" ',
#     '.env': 'DATABASE_URL_ENV=postgres://env_user:pass@localhost/db\n',
#     'config.yaml': {'DATABASE_URL_YAML': 'postgres://yaml_user:pass@localhost/db'},
#     'config.yml': {'DATABASE_URL_YML': 'postgres://yml_user:pass@localhost/db'},
# }


# def create_file(path, content):
#     for file in os.listdir(path):
#         if file.endswith('.json'):
#             with open(os.path.join(path, file), 'w', encoding='utf-8') as f:
#                 json.dump(content, f)


# def load_file_path(file_path, content):
#     for dirname in os.scandir(file_path):
#         if dirname.is_dir():
#             create_file(dirname.path, content)
#         else:
#             create_file(dirname.name, content)


# @pytest.fixture
# def settings_file(tmp_path):
#     for filename, content in test_files.items():
#         file_path = tmp_path / filename
#         with open(file_path, 'w', encoding='utf-8') as file:
#             if filename.endswith('.json'):
#                 json.dump(content, file)
#             elif filename.endswith('.toml'):
#                 file.write(content)
#             elif filename.endswith(('yml', 'yaml')):
#                 yaml.dump(content, file)
#             else:
#                 file.write(content)

#     return tmp_path


# @pytest.fixture
# def location(tmp_path):
#     for filename, content in test_files.items():
#         path = os.path.join(tmp_path)
#         load_file_path(path, content)
#     return tmp_path
