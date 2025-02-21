import argparse
from unittest.mock import mock_open, patch

import pytest

from src import ZeConfig


# Test for __get_env_from_cli_or_variable
def test_get_env_from_cli_or_variable_dev():
    with patch(
        'argparse.ArgumentParser.parse_args',
        return_value=argparse.Namespace(dev=True, staging=False, prod=False),
    ):
        with patch('os.getenv', return_value='development'):
            zc = ZeConfig(
                settings_file='config.toml', project_name='TEST_PROJECT'
            )
            assert zc.env == 'development'


def test_get_env_from_cli_or_variable_staging():
    with patch(
        'argparse.ArgumentParser.parse_args',
        return_value=argparse.Namespace(dev=False, staging=True, prod=False),
    ):
        with patch('os.getenv', return_value='staging'):
            zc = ZeConfig(
                settings_file='config.toml', project_name='TEST_PROJECT'
            )
            assert zc.env == 'staging'


def test_get_env_from_cli_or_variable_prod():
    with patch(
        'argparse.ArgumentParser.parse_args',
        return_value=argparse.Namespace(dev=False, staging=False, prod=True),
    ):
        with patch('os.getenv', return_value='production'):
            zc = ZeConfig(
                settings_file='config.toml', project_name='TEST_PROJECT'
            )
            assert zc.env == 'production'


# Test for __get_file_location
def test_get_file_location_found():
    with patch('os.scandir') as mock_scandir, patch(
        'sys.argv', ['script_name']
    ):
        with patch('os.DirEntry') as mock_entry:
            mock_entry.is_dir.return_value = False
            mock_entry.is_file.return_value = True
            mock_entry.name = 'settings.toml'
            mock_entry.path = '/mock/path/settings.toml'
            mock_scandir.return_value = [mock_entry]

            zc = ZeConfig(
                settings_file='settings.toml', project_name='TEST_PROJECT'
            )
            assert zc.get_file_location() == '/mock/path/settings.toml'


def test_get_file_location_not_found():
    with patch('os.scandir', return_value=[]), patch(
        'sys.argv', ['script_name']
    ):
        zc = ZeConfig(settings_file='config.toml', project_name='TEST_PROJECT')
        with pytest.raises(FileNotFoundError):
            zc.get_file_location()


# Test for __get_file_extension
def test_get_file_extension():
    with patch.object(
        ZeConfig,
        '_ZeConfig__get_file_location',
        return_value='/mock/path/config.toml',
    ), patch('sys.argv', ['script_name']):
        zc = ZeConfig(settings_file='config.toml', project_name='TEST_PROJECT')
        assert zc.get_file_extension() == 'toml'


# Test for __file_reader
def test_file_reader_valid_toml():
    mock_toml_content = """
    [development]
    key = "value"
    """
    with patch('builtins.open', mock_open(read_data=mock_toml_content)):
        with patch(
            'tomllib.load', return_value={'development': {'key': 'value'}}
        ), patch('sys.argv', ['script_name']):
            zc = ZeConfig(
                settings_file='settings.toml', project_name='TEST_PROJECT'
            )
            assert zc.file_reader() == {'development': {'key': 'value'}}


def test_file_reader_invalid_toml():
    mock_toml_content = 'Invalid TOML Content'
    with patch('builtins.open', mock_open(read_data=mock_toml_content)), patch(
        'tomllib.load', side_effect=ValueError
    ), patch('sys.argv', ['script_name']):
        zc = ZeConfig(
            settings_file='settings.toml', project_name='TEST_PROJECT'
        )
        with pytest.raises(
            RuntimeError,
            match='An unexpected error occurred while reading the file',
        ):
            zc.file_reader()


# Test for get_env
def test_get_env_key_found():
    mock_data = {'development': {'key': 'value'}}
    with patch.object(
        ZeConfig, '_ZeConfig__file_reader', return_value=mock_data
    ):
        zc = ZeConfig(
            settings_file='config.toml',
            project_name='TEST_PROJECT',
            env='development',
        )
        assert zc.get_env('key') == 'value'


def test_get_env_key_not_found():
    mock_data = {'development': {'key': 'value'}}
    with patch.object(
        ZeConfig, '_ZeConfig__file_reader', return_value=mock_data
    ):
        zc = ZeConfig(
            settings_file='config.toml',
            project_name='TEST_PROJECT',
            env='development',
        )
        with pytest.raises(KeyError):
            zc.get_env('nonexistent_key')
