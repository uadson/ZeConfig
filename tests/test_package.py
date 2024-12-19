from unittest.mock import MagicMock, mock_open, patch

import pytest

from .models import ZeconfigMock


@pytest.fixture
def zeconfig_instance():
    return ZeconfigMock(settings_file='settings.toml', project_name='zproject')


def test_get_file_location_file_found(zeconfig_instance):
    """Settings file within root path"""
    mock_file = MagicMock()
    mock_file.is_file.return_value = True
    mock_file.is_dir.return_value = False
    mock_file.name = 'settings.toml'
    mock_file.path = '/mock/path/settings.toml'

    mock_dir = MagicMock()
    mock_dir.is_dir.return_value = False

    with patch('os.scandir') as mock_scandir:
        mock_scandir.return_value = [mock_file, mock_dir]
        result = zeconfig_instance.get_file_location()
        assert result == '/mock/path/settings.toml'


def test_get_file_location_file_in_dir(zeconfig_instance):
    """Settings file within dir"""
    mock_dir = MagicMock()
    mock_dir.is_dir.return_value = True
    mock_dir.is_file.return_value = False
    mock_dir.path = '/mock/path'
    mock_file = 'settings.toml'

    with patch('os.scandir') as mock_scandir, patch(
        'os.listdir'
    ) as mock_listdir:
        mock_scandir.return_value = [mock_dir]
        mock_listdir.return_value = [mock_file]
        assert (
            zeconfig_instance.get_file_location() == '/mock/path/settings.toml'
        )


def test_get_file_location_file_not_found(zeconfig_instance):
    """When settings file is not found."""
    with patch('os.scandir') as mock_scandir:
        mock_scandir.return_value = []
        assert zeconfig_instance.get_file_location() is None


def test_get_file_location_exception_handling(zeconfig_instance):
    """When there is exception during file search"""
    with patch('os.scandir', side_effect=Exception('Error to access files')):
        result = zeconfig_instance.get_file_location()
        assert isinstance(result, Exception)
        assert str(result) == 'Error to access files'


def test_get_file_extension_valid(zeconfig_instance):
    """When the file has a valid extension"""
    with patch.object(
        zeconfig_instance, '_ZeconfigMock__get_file_location'
    ) as mock_get_file_location:
        mock_get_file_location.return_value = '/mock/path/settings.toml'
        result = zeconfig_instance.get_file_extension()
        assert result == 'toml'


def test_get_file_extension_no_extension(zeconfig_instance):
    """When file haven't extension"""
    with patch.object(
        zeconfig_instance, '_ZeconfigMock__get_file_location'
    ) as mock_get_file_location:
        mock_get_file_location.return_value = '/mock/path/settings'
        result = zeconfig_instance.get_file_extension()
        assert result == 'settings'


def test_get_file_extension_error_handling(zeconfig_instance):
    """When there is error to get file location."""
    with patch.object(
        zeconfig_instance, '_ZeconfigMock__get_file_location'
    ) as mock_get_file_location:
        mock_get_file_location.side_effect = FileNotFoundError(
            'File not found'
        )
        result = zeconfig_instance.get_file_extension()
        assert isinstance(result, FileNotFoundError), (
            f'Esperado FileNotFoundError, mas obteve {type(result)}'
        )
        assert str(result) == 'File not found'


def test_file_reader_toml_success(zeconfig_instance):
    """Read file .toml successfully"""
    mock_toml_content = b"""
    [section]
    key = "value"
    """
    mock_data = {'section': {'key': 'value'}}

    with patch('builtins.open', mock_open(read_data=mock_toml_content)), patch(
        'tomllib.load', return_value=mock_data
    ), patch.object(
        zeconfig_instance,
        '_ZeconfigMock__get_file_extension',
        return_value='toml',
    ):
        result = zeconfig_instance.file_reader()
        assert result == mock_data


def test_file_reader_unsupported_file_type(zeconfig_instance):
    """File type no support"""
    with patch.object(
        zeconfig_instance,
        '_ZeconfigMock__get_file_extension',
        return_value='json',
    ):
        with pytest.raises(
            ValueError, match='No support to the file type yet'
        ):
            zeconfig_instance.file_reader()


def test_file_reader_file_not_found(zeconfig_instance):
    """Error to open file"""
    with patch(
        'builtins.open', side_effect=FileNotFoundError('File not found')
    ), patch.object(
        zeconfig_instance,
        '_ZeconfigMock__get_file_extension',
        return_value='toml',
    ):
        with pytest.raises(FileNotFoundError, match='File not found'):
            zeconfig_instance.file_reader()
