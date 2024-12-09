import pytest

from zeconfig.exc import FilenameError
from zeconfig.models import ZeConfig

# @pytest.fixture
# def json_config(tmp_path):
#     config_data = '{"database": {"host": "localhost", "port": 5432}}'
#     config_file = tmp_path / 'config.json'
#     config_file.write_text(config_data)
#     return config_file


# @pytest.fixture
# def toml_config(tmp_path):
#     config_data = "[database]\nhost = 'localhost'\n'port' = 5432\n"
#     config_file = tmp_path / 'config.toml'
#     config_file.write_text(config_data)
#     return config_file


@pytest.fixture
def json_config():
    return 'config.json'


@pytest.fixture
def toml_config():
    return 'config.toml'


@pytest.fixture
def not_filename_config():
    return ''


@pytest.fixture
def other_file_extension():
    return 'config.txt'


# def test_initialize_config(json_config):
#     config = ZeConfig(str(json_config))
#     assert config.settings_file == str(json_config)


def test_get_file_extension(json_config, toml_config):
    """
    Obtendo a extensão do arquivo
    """
    config_json = ZeConfig()
    config_toml = ZeConfig()

    assert config_json.get_file_extension(filename=json_config) == 'json'
    assert config_toml.get_file_extension(filename=toml_config) == 'toml'


def test_get_file_extension_error(not_filename_config):
    config_filename = ZeConfig()

    with pytest.raises(FilenameError):
        config_filename.get_file_extension(filename=not_filename_config)


def text_get_other_file_extension_error(other_file_extension):
    config_filename = ZeConfig()

    with pytest.raises(FilenameError):
        config_filename.get_file_extension(filename=other_file_extension)


# def test_file_reader_json(json_config):
#     config = ZeConfig(str(json_config))
#     data = config.file_reader()

#     expected_data = {'database': {'host': 'localhost', 'port': 5432}}

#     assert data == expected_data


# def test_file_reader_toml(toml_config):
#     config = ZeConfig(str(toml_config))
#     data = config.file_reader()

#     expected_data = {'database': {'host': 'localhost', 'port': 5432}}

#     assert data == expected_data


# def test_unsupported_file_type(tmp_path):
#     unsupported_file = tmp_path / 'config.xml'
#     unsupported_file.write_text(
#         '<database><host>localhost</host><port>5432</port></database>'
#     )

#     config = ZeConfig(str(unsupported_file))

#     with pytest.raises(ValueError, match='No support to the file type yet'):
#         config.config()


# def test_get_root_path_name_none(toml_config):
#     config = ZeConfig(str(toml_config))
#     root_path_name = config.get_root_path_name()

#     expected_root_name = None

#     assert root_path_name == expected_root_name


# def test_get_root_path_name_true(toml_config):
#     config = ZeConfig(str(toml_config), root_path=True)
#     root_path_name = config.get_root_path_name()

#     expected_root_name = 'ZeConfig'

#     assert root_path_name == expected_root_name
