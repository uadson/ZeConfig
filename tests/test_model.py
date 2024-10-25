import pytest

from zeconfig.models import ZeConfig


@pytest.fixture
def json_config(tmp_path):
    config_data = '{"database": {"host": "localhost", "port": 5432}}'
    config_file = tmp_path / 'config.json'
    config_file.write_text(config_data)
    return config_file


@pytest.fixture
def toml_config(tmp_path):
    config_data = "[database]\nhost = 'localhost'\n'port' = 5432\n"
    config_file = tmp_path / 'config.toml'
    config_file.write_text(config_data)
    return config_file


def test_initialize_config(json_config):
    config = ZeConfig(str(json_config))
    assert config.settings_file == str(json_config)


def test_get_file_extension(json_config, toml_config):
    config_json = ZeConfig(str(json_config))
    config_toml = ZeConfig(str(toml_config))

    assert config_json.get_file_extension() == 'json'
    assert config_toml.get_file_extension() == 'toml'


def test_file_reader_json(json_config):
    config = ZeConfig(str(json_config))
    data = config.file_reader()

    expected_data = {'database': {'host': 'localhost', 'port': 5432}}

    assert data == expected_data


def test_file_reader_toml(toml_config):
    config = ZeConfig(str(toml_config))
    data = config.file_reader()

    expected_data = {'database': {'host': 'localhost', 'port': 5432}}

    assert data == expected_data


def test_unsupported_file_type(tmp_path):
    unsupported_file = tmp_path / 'config.xml'
    unsupported_file.write_text(
        '<database><host>localhost</host><port>5432</port></database>'
    )

    config = ZeConfig(str(unsupported_file))

    with pytest.raises(ValueError, match='No support to the file type yet'):
        config.config()
