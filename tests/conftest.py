import json
import os

import pytest

try:
    import tomllib
except ImportError:
    import tomli as tomllib

from pathlib import Path

import yaml

# Define the test directory where the config files will be created
TEST_DIR = Path(__file__).parent.resolve()


@pytest.fixture
def setup_test_files(request):
    """
    Creates test configuration files before each test and deletes
    them after.
    """

    # Ensure the test directory exists
    if not TEST_DIR.exists():
        TEST_DIR.mkdir(parents=True, exist_ok=True)

    # Configuration files and their contents
    test_files = {
        'config.json': {
            'DATABASE_URL': 'postgres://json_user:pass@localhost/db'
        },
        'config.toml': {
            'DATABASE_URL': 'postgres://toml_user:pass@localhost/db'
        },
        'config.yml': {
            'DATABASE_URL': 'postgres://yaml_user:pass@localhost/db'
        },
        '.env': 'DATABASE_URL=postgres://env_user:pass@localhost/db\n',
    }

    # Create test files
    for filename, content in test_files.items():
        file_path = TEST_DIR / filename
        with open(file_path, 'w', encoding='utf-8') as file:
            if filename.endswith('.json'):
                json.dump(content, file)
            elif filename.endswith('.toml'):
                tomllib.dump(content, file)
            elif filename.endswith(('.yml', '.yaml')):
                yaml.dump(content, file)
            else:
                file.write(content)

    # Ensure cleanup after each test
    def cleanup():
        for filename in test_files.keys():
            file_path = TEST_DIR / filename
            if file_path.exists():
                os.remove(file_path)

    request.addfinalizar(cleanup)
