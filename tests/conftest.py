import json

import pytest
import yaml


@pytest.fixture
def settings_file(tmp_path):
    test_files = {
        'config.json': {'DATABASE_URL': 'postgres://json_user:pass@localhost/db'},
        'config.toml': 'database_url = "postgres://toml_user:pass@localhost/db" ',
        '.env': 'DATABASE_URL_ENV=postgres://env_user:pass@localhost/db\n',
        'config.yaml': {
            'DATABASE_URL_YAML': 'postgres://yaml_user:pass@localhost/db'
        },
        'config.yml': {'DATABASE_URL_YML': 'postgres://yml_user:pass@localhost/db'},
    }

    for filename, content in test_files.items():
        file_path = tmp_path / filename
        with open(file_path, 'w', encoding='utf-8') as file:
            if filename.endswith('.json'):
                json.dump(content, file)
            elif filename.endswith('.toml'):
                file.write(content)
            elif filename.endswith(('yml', 'yaml')):
                yaml.dump(content, file)
            else:
                file.write(content)

    return tmp_path
